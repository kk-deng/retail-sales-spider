# -*- coding: utf-8 -*-
"""
Created on 2021-02-08 16:06:12
---------
@summary:
---------
@author: Boris
"""
from typing import List, Set, Dict

from datetime import datetime
import time
import random
import feapder
from feapder.utils.log import log
from items import *
from tools import *

import telegram

from feapder.db.mongodb import MongoDB

db = MongoDB()
file_operator = file_input_output.FileReadWrite()
bot = telegram.Bot(token=file_operator.token)

SCRAPE_COUNT = 600


class TestSpider(feapder.AirSpider):

    def start_requests(self):
        for i in range(1, SCRAPE_COUNT):
            time_gap = random.randrange(50, 70)
            yield feapder.Request("https://forums.redflagdeals.com/hot-deals-f9/")

            if SCRAPE_COUNT > 2:
                log.info(f'## Running for {i} / {SCRAPE_COUNT} runs, waiting for {time_gap}s...')
                time.sleep(time_gap)

    def validate(self, request, response):
        if response.status_code != 200:
            raise Exception("response code not 200")  # 重试

        # if "哈哈" not in response.text:
        #     return False # 抛弃当前请求

    def parse(self, request, response):
        topic_list = response.bs4().find_all('li', class_='row topic')

        # Read watchlist for keywords watching
        watch_list = file_operator.watchlist_csv

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
            retailer_name = self.topictitle_retailer(topic)

            record_conditions = [
                (elapsed_mins <= 120), 
                (elapsed_mins <= 240 and upvotes >= 40)
            ]

            if any(record_conditions):
                item = spider_data_item.SpiderDataItem()  # 声明一个item

                # item.thread_id = thread_id  # 给item属性赋值
                item.thread_id = thread_id
                item.topic_title = topic_title  # 给item属性赋值
                item.upvotes = upvotes  # 给item属性赋值
                item.elapsed_mins = elapsed_mins
                item.retailer_name = retailer_name
                item.first_post_time_obj = first_post_time_obj
                item.first_post_time = first_post_time_string
                item.reply_count = posts
                item.view_count = views
                item.topic_link = topic_title_link

                # Find the same thread_id in MongoDB
                db_documents = db.find(coll_name='spider_data', condition={'thread_id': thread_id}, limit=1)
                
                # Parse retailer name and deal title, compared with watch_list and return list of boolean
                boolean_watchlist = self.match_watchlist(retailer_name, topic_title, watch_list)
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
                    (upvotes >= 9), 
                    (any(boolean_watchlist))
                ]
                sendmsg_conditions_2 = [(upvotes >= 30),]

                # 1st condition for less popular deal, 2nd condition for popular deal
                if (any(sendmsg_conditions_1) and msg_sent_counter == 0) or \
                    (any(sendmsg_conditions_2) and msg_sent_counter < 2):
                    sent = self.send_text_msg(item.to_dict, watchlist=f'{matched_keywords}NEW!')
                    if sent:
                        msg_sent_counter += 1  # Record the sending count

                item.msg_sent_cnt = msg_sent_counter
                yield item  # 返回item， item会自动批量入库
    
    @staticmethod
    def upvotes(topic):
        upvotes_soup = topic.find('dl', {'class':'post_voting'})
        upvotes = int(upvotes_soup.text.strip('+')) if upvotes_soup else 0
        return upvotes
    
    @classmethod
    def first_post_time_obj(cls, topic):
        first_post_time_raw = topic.find('span', class_='first-post-time').text.strip()
        
        return cls.resolve_times_from_topic(first_post_time_raw)

    @staticmethod
    def first_post_time_string(first_post_time_obj):
        return datetime.strftime(first_post_time_obj, '%m-%d %H:%M')

    @staticmethod
    def elapsed_mins(first_post_time_obj):
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
    def topictitle_retailer(topic):
        try:
            topictitle_retailer = topic.find('a', class_='topictitle_retailer').text.strip()
        except:
            topictitle_retailer = topic.find('h3', class_='topictitle').text.split('\n')[1].strip()
        return topictitle_retailer
    
    @classmethod
    def send_text_msg(cls, item_dict, **kwargs):
        watchlist_str = kwargs.get('watchlist', 'Hot')

        # Get strings from item_dict
        elapsed_mins = item_dict["elapsed_mins"]
        upvotes = item_dict["upvotes"]
        upvotes_per_min = upvotes/elapsed_mins
        topic_title = item_dict["topic_title"]
        topic_link = item_dict["topic_link"]
        msg_content = f'{watchlist_str} @{"{:.2f}".format(elapsed_mins)}mins ago ' \
            f'[{upvotes} Votes] ({"{:.2f}".format(upvotes_per_min)}/min): ' \
            f'{topic_title}. Link: {topic_link}'
        
        return cls.send_bot_msg(msg_content)
    
    @staticmethod
    def send_bot_msg(content_msg):
        log.info(f'## Sending: {content_msg}')
        try:
            bot.send_message(text=content_msg, chat_id=file_operator.chat_id)
            log.info('## Msg was sent successfully!')
            time.sleep(3)
            return True
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
            return f'[{"&".join(matches_list)}] '
        else:
            return ''

# if __name__ == '__main__':
#     spider = TestSpider(thread_count=10)
#     spider.start()
