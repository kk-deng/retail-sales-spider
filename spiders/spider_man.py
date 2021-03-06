# -*- coding: utf-8 -*-
"""
Created on 2021-11-29 16:06:12
---------
@summary:
---------
@author: Kelvin
"""
from __future__ import annotations

import random
import time
from datetime import datetime, timezone, time as tm
from functools import wraps
from typing import Dict, List

import feapder
import telegram
from feapder.db.mongodb import MongoDB
from feapder.utils.log import log
from items import rfd_item
from tools import file_input_output
from utils.helpers import escape_markdown
from utils.tg_bot import TelegramBot

SCRAPE_COUNT = 3000
NIGHT_START_TIME = (1,00)
NIGHT_END_TIME = (2,59)
MORNING_TIME = (7,59)


class RfdSpider(feapder.AirSpider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = MongoDB()
        self.file_operator = file_input_output.FileReadWrite()
        self.rfd_api = self.file_operator.rfd_api
        self.rfd_api_params = self.file_operator.rfd_api_params
        self.tg_token = self.file_operator.token
        self.chat_id = self.file_operator.channel_id
        self.bot = TelegramBot(token=self.tg_token, chat_id=self.chat_id)
        self.rfd_header = self.file_operator.get_spider_header('rfd')

    def start_callback(self):
        welcome_str = 'π*New*: (ps5) @*43.24* mins agoπ*Votes*: *4* votes (β4 | β0) (0.09/min)*πReply|Views*: 5 | 825 (19.08/min)π*Title*: _(Western Digital)_ WD\\_BLACK SN850 for PS5 2TB - \$216.99 or \$184.44 w/ student or senior discount, no PST π*Link*: https://forums.redflagdeals.com/western-digital-wd_black-sn850-ps5-2tb-216-99-184-44-w-student-senior-discount-no-pst-2552689/'
        self.bot.send_bot_msg(escape_markdown(welcome_str))
    
    def end_callback(self):
        self.bot.send_bot_msg('Bot Stopped...')

    def download_midware(self, request):
        # Downloader middleware uses random header from file_input_output
        request.headers = self.rfd_header
        return request

    def start_requests(self):
        """Main method to yield API requests every min.

        Yields:
            feapder.Request: A feapder.Request object of API call and params
        """
        for i in range(1, SCRAPE_COUNT):
            yield feapder.Request(self.rfd_api, params=self.rfd_api_params, method="GET")

            time_gap = self.scrape_time_gap
            
            if SCRAPE_COUNT > 2:
                log.info(f'## Running for {i} / {SCRAPE_COUNT} runs, waiting for {time_gap}s...')
                time.sleep(time_gap)

    def validate(self, request, response):
        if response.status_code != 200:
            raise Exception("Response code not 200")
    
    def parse(self, request, response):
        """Main function to parse response, trigger alert and yield to update database items.

        Args:
            request: API request sent by start_requests
            response: Json file returned by the API request

        Yields:
            feapder.UpdateItem: Buffered items to be sent to database
        """
        # Read watchlist for keywords watching
        watch_list = self.file_operator.watchlist_csv

        topic_list = response.json['topics']

        # For each topic from the API response
        for thread in topic_list:
            topic = RfdTopic(topic=thread, watch_list=watch_list)

            # Only topics with the record_conditions will be checked, e.g. recent or high votes topics
            record_conditions = [
                (topic.elapsed_mins <= 180), 
                (topic.elapsed_mins <= 300 and topic.upvotes >= 20)
            ]

            record_conditions_minimum = (topic.upvotes >= 0)

            if any(record_conditions) and record_conditions_minimum:

                db_topic_dict = self.find_db_topic_by_id(topic.topic_id)

                if db_topic_dict:
                    topic.msg_sent_counter = db_topic_dict.get('msg_sent_cnt')
                    topic.telegram_msg_id = db_topic_dict.get('telegram_msg_id')
                else:
                    self.log_new_topic(topic)

                # Collect the msg sending conditions, any of them is True
                # TODO: 1st condition (will send only 1 time) is for final upvotes, 2nd is for up only
                sendmsg_conditions_1 = [
                    (topic.upvotes >= 4), 
                    topic.matched_keywords,
                    (topic.total_up_per_min >= 0.4)
                ]
                # 2nd condition (will send only 2 times) is upvote count > 15, or total_views > 200 w/ upvote > 1
                sendmsg_conditions_2 = [
                    (topic.upvotes >= 15),
                    (topic.total_views >= 400 and topic.upvotes > 1 and topic.elapsed_mins <= 30),
                ]

                # 3rd condition (will send only 4 times) is views/min > 50 w/ recent topic
                sendmsg_conditions_3 = [
                    (topic.views_per_min >= 50 and topic.elapsed_mins <= 60),
                ]

                # 1st condition for less popular deal, 2nd condition for popular deal
                if (any(sendmsg_conditions_1) and topic.msg_sent_counter == 0) or \
                    (any(sendmsg_conditions_2) and topic.msg_sent_counter < 2) or \
                    (any(sendmsg_conditions_3) and topic.msg_sent_counter < 3) :
                    
                    returned_msg = self.send_text_msg(topic)

                    if returned_msg:

                        telegram_msg_id = returned_msg['message_id']
                        # If a deal has high upvotes, pin the msg in the channel
                        if all(sendmsg_conditions_2):

                            self.bot.pin_message(pin_message_id=telegram_msg_id)

                        topic.msg_sent_counter += 1  # Record the sending count
                        topic.telegram_msg_id = returned_msg['message_id']
                
                elif topic.elapsed_mins <= 60 and topic.telegram_msg_id:
                    # Edit to update the latest change
                    returned_msg = self.update_sent_msg(topic)
                    log.warning(f'Updated! {returned_msg["message_id"]}') 

                item = rfd_item.RfdTopicItem(topic)

                yield item
    
    @property
    def scrape_time_gap(self) -> int:
        """Get wait time gap provided by the current time.

        Returns:
            int: The seconds to be wait between API requests
        """
        # Now time
        now = datetime.now().time()

        # Lower the speed at night
        if tm(*NIGHT_START_TIME) <= now <= tm(*MORNING_TIME):
            time_gap = random.randrange(180, 300)
        else:
            time_gap = random.randrange(50, 70)
        
        return time_gap

    def send_text_msg(self, topic: RfdTopic, **kwargs) -> telegram.Message or False:
        """Compose telegram messages from topic and return the msg_id from sent messages.

        Args:
            topic (RfdTopic): An object of each topic 

        Returns:
            telegram.Message: A Message object returned from send_bot_msg
        """
        msg_content = str(topic)

        return self.bot.send_bot_msg(content_msg=msg_content, markup_url=topic.offer_url)
    
    def update_sent_msg(self, topic: RfdTopic, **kwargs) -> telegram.Message or False:
        """Edit telegram messages from topic and return the msg_id from sent messages.

        Args:
            topic (RfdTopic): An object of each topic 

        Returns:
            telegram.Message: A Message object returned from send_bot_msg
        """
        update_timestamp = datetime.now().strftime('%H:%M:%S')
        msg_content = f"β²οΈ@{update_timestamp}\n{str(topic)}"

        return self.bot.edit_message(content_msg=msg_content, edit_msg_id=topic.telegram_msg_id ,markup_url=topic.offer_url)

    @staticmethod
    def log_new_topic(topic: RfdTopic) -> None:
        offer_price_str = f'| Price: ${topic.offer_price}' if topic.offer_price else ''
        offer_savings_str = f'| Saving: {topic.offer_savings}' if topic.offer_savings else ''
        
        log.warning(
            f'New Added: {topic.topic_id} ({topic.upvotes} Votes) '
            f'{topic.elapsed_mins:.2f}mins ago (@{topic.post_time_str}), '
            f'Dealer: {topic.dealer_name}, Title: {topic.topic_title} '
            f'{offer_price_str + offer_savings_str}'
        )

    def find_db_topic_by_id(self, topic_id) -> dict:
        # Slow down the get DB operation
        # time.sleep(2)
        try:
            return self.db.find(
                coll_name='rfd_topic', 
                condition={'topic_id': topic_id}, 
                limit=1
            )[0]
        except Exception as e:
            return {}


class RfdTopic:
    def __init__(self, topic, telegram_msg_id: str=None, watch_list: List[str]=[]):
        self.topic_id = topic['topic_id']
        self.topic_title = topic['title'].replace('_', '\\_')
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
        self.dealer_name = (self.offer['dealer_name'] or "").strip("[]")
        self.offer_price = self.offer['price']
        self.offer_url = self.offer['url']
        self.offer_savings = self.offer['savings']
        self.offer_expires_at = self.offer['expires_at']
        self.watch_list = watch_list
        self.total_up_per_min = self.total_up / self. elapsed_mins
        self.upvotes_per_min = self.upvotes / self.elapsed_mins
        self.views_per_min = self.total_views / self.elapsed_mins
        self.msg_sent_counter = 0
        self.telegram_msg_id = telegram_msg_id
    
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
    
    @property
    def watchlist_bool(self) -> List[bool]:
        dealer_and_title = f'{self.dealer_name} {self.topic_title}'
        return [keyword in dealer_and_title.lower() for keyword in self.watch_list]
    
    @property
    def matched_keywords(self) -> str|None:
        if any(self.watchlist_bool):
            keyword_list = [i for (i, v) in zip(self.watch_list, self.watchlist_bool) if v]
            return f'{"&".join(keyword_list)}'
        else:
            return None
    
    @property
    def tg_msg_header(self) -> str:
        """Return a msg header decided by the total_up and upvote/view rate."""
        if self.total_up >= 8:
            # If total upvotes are greater than 8, assign hot emoji
            hot_emoji = 'π₯' * round(self.total_up / 8)
            return f"{hot_emoji}*Hot*:"
        # If total upvotes between 2 and 8
        elif self.upvotes_per_min >= 0.4 and self.total_up >= 2:
            # upvote rate is > 0.4/min, assign rocket emoji
            return "π*Trending*:"
        elif self.views_per_min >= 20.0 and self.total_up >= 2:
            # view rate is > 20/min, assign breaking emoji
            return "β¨*Breaking*:"
        else:
            # Anything else, assign New emoji
            return "π*New*:"

    def __str__(self):
        # Other string components
        replies_n_views_str = f'*πReply|Views*: {self.total_replies} | {self.total_views} ({self.views_per_min:.2f}/min)\n'

        keywords_str = f'({self.matched_keywords}) ' if self.matched_keywords else ''

        msg_content = (
            f'{self.tg_msg_header} {keywords_str}@*{self.elapsed_mins:.2f}* mins ago\n'
            f'π*Votes*: *{self.upvotes}* votes (β{self.total_up} | β{self.total_down}) ({self.upvotes_per_min:.2f}/min)\n'
            f'{replies_n_views_str}'
            f'π*Title*: _({escape_markdown(self.dealer_name)})_ {(escape_markdown(self.topic_title))} \n'
            f'π*Link*: {self.topic_title_link}'
        )

        return msg_content

if __name__ == '__main__':
    spider = RfdSpider(thread_count=2)
    spider.start()
