# -*- coding: utf-8 -*-
"""
Created on 2021-11-29 16:06:12
---------
@summary:
---------
@author: Kelvin
"""
import random
import time
from datetime import datetime, timezone, time as tm
from functools import wraps
from typing import Dict, List, Set

import feapder
import telegram
from feapder.db.mongodb import MongoDB
from feapder.utils.log import log
from items import *
from tools import *
from utils.helpers import escape_markdown

SCRAPE_COUNT = 1000
BB_SHIPPING_CHECK = True
BB_PICKUP_CHECK = False


class RfdSpider(feapder.AirSpider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = MongoDB()
        self.file_operator = file_input_output.FileReadWrite()
        self.rfd_api = self.file_operator.rfd_api
        self.rfd_api_params = self.file_operator.rfd_api_params
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
            yield feapder.Request(self.rfd_api, params=self.rfd_api_params, method="GET")

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
        # Read watchlist for keywords watching
        watch_list = self.file_operator.watchlist_csv

        topic_list = response.json['topics']

        for thread in topic_list:
            topic = RfdTopic(thread)

            record_conditions = [
                (topic.elapsed_mins <= 180), 
                (topic.elapsed_mins <= 300 and topic.upvotes >= 30)
            ]

            if any(record_conditions):

                try:
                    # Find the same thread_id in MongoDB
                    db_documents = self.db.find(coll_name='rfd_topic', condition={'topic_id': topic.topic_id}, limit=1)
                    msg_sent_counter = db_documents[0]['msg_sent_cnt']
                except:
                    self.log_new_topic(topic)
                    msg_sent_counter = 0
            
                # Parse retailer name and deal title, compared with watch_list and return list of boolean
                boolean_watchlist = self.match_watchlist(topic.dealer_name, topic.topic_title, watch_list)
                matched_keywords = self.matched_keywords(boolean_watchlist, watch_list)

                # Collect the msg sending conditions, any of them is True
                sendmsg_conditions_1 = [
                    (topic.upvotes >= 8), 
                    (any(boolean_watchlist)),
                    (topic.upvotes/topic.elapsed_mins >= 0.4)
                ]
                sendmsg_conditions_2 = [(topic.upvotes >= 20),]

                # 1st condition for less popular deal, 2nd condition for popular deal
                if (any(sendmsg_conditions_1) and msg_sent_counter == 0) or \
                    (any(sendmsg_conditions_2) and msg_sent_counter < 2):
                    returned_msg = self.send_text_msg(topic, watchlist=f'{matched_keywords}*NEW*')
                    if returned_msg:
                        # If a deal has high upvotes, pin the msg in the channel
                        if any(sendmsg_conditions_2):
                            pin_message_id = returned_msg['message_id']

                            self.bot.pin_chat_message(
                                chat_id=self.file_operator.channel_id,
                                message_id=pin_message_id
                            )

                        msg_sent_counter += 1  # Record the sending count
                
                item = rfd_item.RfdTopicItem(topic)
                item.msg_sent_cnt = msg_sent_counter
                yield item
    
    def send_text_msg(self, topic, **kwargs):
        watchlist_str = kwargs.get('watchlist', '*Hot*')

        # Get strings from item_dict
        elapsed_mins = topic.elapsed_mins
        upvotes = topic.upvotes
        upvotes_per_min = upvotes/elapsed_mins
        topic_title = topic.topic_title
        topic_link = topic.topic_title_link
        dealer_name = topic.dealer_name
        offer_url = topic.offer_url

        msg_content = (
            f'*🔥Deal*: {watchlist_str} @*{"{:.2f}".format(elapsed_mins)}* mins ago\n'
            f'*👍Votes*: *{upvotes}* votes (↑{topic.total_up} | ↓{topic.total_down}) ({"{:.2f}".format(upvotes_per_min)}/min)\n'
            f'*📕Title*: _({dealer_name.strip("[]")})_ {(topic_title)} \n'
            f'*🔗Link*: {topic_link}'
        )
        
        return self.send_bot_msg(msg_content, offer_url)
    
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
    def send_bot_msg(self, content_msg: str, offer_url: str = None) -> bool:
        log_content = content_msg.replace("\n", "")
        log.warning(f'## Sending: {log_content}')

        if offer_url:
            keyboard = [
                [
                    telegram.InlineKeyboardButton("Open Direct Link", url=offer_url),
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
    def log_new_topic(topic):
        offer_price_str = f'${topic.offer_price}' if topic.offer_price else ''
        offer_savings_str = f', saving: {topic.offer_savings}' if topic.offer_savings else ''
        
        log.warning(
            f'New Added: {topic.topic_id} ({topic.upvotes} Votes) '
            f'{"{:.2f}".format(topic.elapsed_mins)}mins ago (@{topic.post_time_str}), '
            f'Dealer: {topic.dealer_name}, Title: {topic.topic_title} '
            f'{offer_price_str + offer_savings_str}'
        )

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


class RfdTopic:
    def __init__(self, topic):
        self.topic_id = topic['topic_id']
        self.topic_title = topic['title']
        self.votes = topic['votes'] or {}
        self.total_up = self.votes.get('total_up', 0)
        self.total_down = self.votes.get('total_down', 0)
        self.upvotes = self.total_up - self.total_down
        self.total_replies = topic['total_replies']
        self.total_views = topic['total_views']
        self.summary = topic['summary'] or {}
        self.summary_body = self.summary.get('body')
        self.topic_title_link = 'https://forums.redflagdeals.com' + topic['web_path']
        self.post_time = self.utc_to_local(topic['post_time'])
        self.post_time_str = self.convert_dt_to_str(self.post_time)
        self.last_post_time = self.utc_to_local(topic['last_post_time'])
        self.elapsed_mins = self.compare_with_now(self.post_time)
        self.offer = topic['offer']
        self.dealer_name = self.offer['dealer_name'] or ""
        self.offer_price = self.offer['price']
        self.offer_url = self.offer['url']
        self.offer_savings = self.offer['savings']
        self.offer_expires_at = self.offer['expires_at']
    
    @staticmethod
    def utc_to_local(utc_dt: str) -> datetime:
        utc_dt_iso = datetime.fromisoformat(utc_dt)
        return utc_dt_iso.replace(tzinfo=timezone.utc).astimezone(tz=None).replace(tzinfo=None)
    
    @staticmethod
    def convert_dt_to_str(post_time_obj: datetime) -> str:
        return datetime.strftime(post_time_obj, '%m-%d %H:%M:%S')

    @staticmethod
    def compare_with_now(post_time_obj: datetime) -> float:
        now = datetime.now()
        return (now - post_time_obj).total_seconds() / 60


if __name__ == '__main__':
    spider = RfdSpider(thread_count=2)
    spider.start()
