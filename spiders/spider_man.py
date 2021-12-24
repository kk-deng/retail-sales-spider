# -*- coding: utf-8 -*-
"""
Created on 2021-11-29 16:06:12
---------
@summary:
---------
@author: Kelvin
"""
from typing import List, Set, Dict
from functools import wraps
from datetime import datetime, time as tm
import time
import random
import feapder
from feapder.utils.log import log
from items import *
from tools import *
from utils.helpers import escape_markdown
import telegram

from feapder.db.mongodb import MongoDB


SCRAPE_COUNT = 1000
BB_SHIPPING_CHECK = True
BB_PICKUP_CHECK = False


class RfdSpider(feapder.AirSpider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = MongoDB()
        self.file_operator = file_input_output.FileReadWrite()
        self.bot = telegram.Bot(token=self.file_operator.token)
        self.random_header = self.file_operator.create_random_header

    def start_callback(self):
        self.send_bot_msg('Bot started...')
    
    def end_callback(self):
        self.send_bot_msg('Bot Stopped...')

    def download_midware(self, request):
        # Downloader middleware uses random header from file_input_output
        request.headers = self.random_header['rfd']
        return request

    def start_requests(self):
        for i in range(1, SCRAPE_COUNT):
            yield feapder.Request("https://forums.redflagdeals.com/hot-deals-f9/")

            # Lower the speed at night by checking the now time
            if tm(1,00) <= datetime.now().time() <= tm(7,59):
                time_gap = random.randrange(180, 300)
            else:
                time_gap = random.randrange(50, 70)
            
            if SCRAPE_COUNT > 2:
                log.info(f'## Running for {i} / {SCRAPE_COUNT} runs, waiting for {time_gap}s...')
                time.sleep(time_gap)

    def validate(self, request, response):
        if response.status_code != 200:
            raise Exception("Response code not 200")
    
    def parse(self, request, response):
        topic_list = response.bs4().find_all('li', class_='row topic')

        # Read watchlist for keywords watching
        watch_list = self.file_operator.watchlist_csv

        for topic in topic_list:

            thread_id = int(topic['data-thread-id'])
            topic_title = topic.find('a', {'class': 'topic_title_link'}).text.strip()
            upvotes = self.upvotes(topic)
            posts = int(topic.find('div', {'class': 'posts'}).text.replace(',', ''))
            views = int(topic.find('div', {'class': 'views'}).text.replace(',', ''))
            topic_title_link = topic.find('a', {'class': 'topic_title_link'})['href']
            first_post_time_obj = self.first_post_time_obj(topic)
            first_post_time_string = self.first_post_time_string(first_post_time_obj)
            elapsed_mins = self.elapsed_mins(first_post_time_obj)
            topictitle_retailer = self.topictitle_retailer(topic)

            record_conditions = [
                (elapsed_mins <= 120), 
                (elapsed_mins <= 240 and upvotes >= 30)
            ]

            if any(record_conditions):
                item = spider_data_item.SpiderDataItem()  # Define an item to save to the database

                item.thread_id = thread_id
                item.topic_title = topic_title
                item.upvotes = upvotes
                item.elapsed_mins = elapsed_mins
                item.retailer_name = topictitle_retailer
                item.first_post_time_obj = first_post_time_obj
                item.first_post_time = first_post_time_string
                item.reply_count = posts
                item.view_count = views
                item.topic_link = topic_title_link
                upvotes_per_min = upvotes/elapsed_mins

                # Find the same thread_id in MongoDB
                db_documents = self.db.find(coll_name='spider_data', condition={'thread_id': thread_id}, limit=1)
                
                # Parse retailer name and deal title, compared with watch_list and return list of boolean
                boolean_watchlist = self.match_watchlist(topictitle_retailer, topic_title, watch_list)
                matched_keywords = self.matched_keywords(boolean_watchlist, watch_list)

                try:
                    msg_sent_counter = db_documents[0]['msg_sent_cnt']
                except:
                    log.info(f'New Added: {thread_id} [{upvotes} Votes] '
                        f'@{"{:.2f}".format(elapsed_mins)}mins ago, '
                        f'Brand: {topictitle_retailer}, Title: {topic_title}')
                    msg_sent_counter = 0

                # Collect the msg sending conditions, any of them is True
                sendmsg_conditions_1 = [
                    (upvotes >= 8), 
                    (any(boolean_watchlist)),
                    (upvotes/elapsed_mins >= 0.4)
                ]
                sendmsg_conditions_2 = [(upvotes >= 20),]

                # 1st condition for less popular deal, 2nd condition for popular deal
                if (any(sendmsg_conditions_1) and msg_sent_counter == 0) or \
                    (any(sendmsg_conditions_2) and msg_sent_counter < 2):
                    returned_msg = self.send_text_msg(item.to_dict, watchlist=f'{matched_keywords}*NEW*')
                    if returned_msg:
                        # If a deal has high upvotes, pin the msg in the channel
                        if any(sendmsg_conditions_2):
                            pin_message_id = returned_msg['message_id']

                            self.bot.pin_chat_message(
                                chat_id=self.file_operator.channel_id,
                                message_id=pin_message_id
                            )

                        msg_sent_counter += 1  # Record the sending count

                item.msg_sent_cnt = msg_sent_counter
                yield item  # 返回item， item会自动批量入库
    
    @staticmethod
    def upvotes(topic) -> int:
        upvotes_soup = topic.find('dl', {'class':'post_voting'})
        upvotes = int(upvotes_soup.text.strip('+')) if upvotes_soup else 0
        return upvotes
    
    @classmethod
    def first_post_time_obj(cls, topic):
        first_post_time_raw = topic.find('span', class_='first-post-time').text.strip()
        
        return cls.resolve_times_from_topic(first_post_time_raw)

    @staticmethod
    def first_post_time_string(first_post_time_obj) -> str:
        return datetime.strftime(first_post_time_obj, '%m-%d %H:%M')

    @staticmethod
    def elapsed_mins(first_post_time_obj) -> float:
        now = datetime.now()
        post_time = first_post_time_obj
        return (now - post_time).total_seconds() / 60

    @staticmethod
    def resolve_times_from_topic(first_post_time_raw):
        date_suffix_dict = {
            "st": '',
            "nd": '',
            "rd": '',
            "th": ''
        }
        for i, j in date_suffix_dict.items():
            first_post_time_raw = first_post_time_raw.replace(i, j)
        
        return datetime.strptime(first_post_time_raw, '%b %d, %Y %I:%M %p')
    
    @staticmethod
    def topictitle_retailer(topic) -> str:
        try:
            topictitle_retailer = topic.find('a', class_='topictitle_retailer').text.strip()
        except:
            topictitle_retailer = topic.find('h3', class_='topictitle').text.split('\n')[1].strip()
        return topictitle_retailer
    
    def send_text_msg(self, item_dict, **kwargs):
        watchlist_str = kwargs.get('watchlist', '*Hot*')

        # Get strings from item_dict
        elapsed_mins = item_dict["elapsed_mins"]
        upvotes = item_dict["upvotes"]
        upvotes_per_min = upvotes/elapsed_mins
        topic_title = item_dict["topic_title"]
        topic_link = item_dict["topic_link"]
        retailer_name = item_dict["retailer_name"]

        msg_content = (
            f'*Deal*: {watchlist_str} @*{"{:.2f}".format(elapsed_mins)}* mins ago\n'
            f'*Votes*: *{upvotes}* votes ({"{:.2f}".format(upvotes_per_min)}/min)\n'
            f'*Title*: _({retailer_name.strip("()")})_ `{(topic_title)}` \n'
            f'[Click to open Deal link]({topic_link})'
        )
        
        return self.send_bot_msg(msg_content, topic_link)
    
    def send_action(action):
        """Sends `action` while processing func command."""

        def decorator(func):
            @wraps(func)
            def command_func(self, *args, **kwargs):
                self.bot.send_chat_action(chat_id=self.file_operator.chat_id, action=action)
                return func(self,  *args, **kwargs)
            return command_func
        
        return decorator

    @send_action(telegram.ChatAction.TYPING)
    def send_bot_msg(self, content_msg: str, topic_link: str = None) -> bool:
        log_content = content_msg.replace("\n", "")
        log.info(f'## Sending: {log_content}')

        if topic_link:
            keyboard = [
                [
                    telegram.InlineKeyboardButton("Open Link", url=topic_link),
                ],
            ]
            reply_markup = telegram.InlineKeyboardMarkup(keyboard)
        else:
            reply_markup = None
        
        try:
            returned_msg = self.bot.send_message(
                text=content_msg, 
                chat_id=self.file_operator.channel_id,
                reply_markup=reply_markup,
                parse_mode=telegram.ParseMode.MARKDOWN
                )
            log.info('## Msg was sent successfully!')
            time.sleep(3)
            return returned_msg
        except Exception as e:
            log.info(f'## Msg failed sending with error:\n{e}')
            return False

    @staticmethod
    def match_watchlist(topictitle_retailer: str, topic_title: str, watch_list: List[str]) -> List[bool]:
        retailer_and_title = topictitle_retailer + ' ' + topic_title
        true_watchlist = [keyword in retailer_and_title.lower() for keyword in watch_list]
        return true_watchlist
    
    @staticmethod
    def matched_keywords(boolean_watchlist: List[bool], watch_list: List[str]) -> str:
        if any(boolean_watchlist):
            matches_list = [i for (i, v) in zip(watch_list, boolean_watchlist) if v]
            return f'({"&".join(matches_list)}) '
        else:
            return ''

# if __name__ == '__main__':
#     spider = RfdSpider(thread_count=10)
#     spider.start()
