# -*- coding: utf-8 -*-
"""
Created on 2021-02-08 16:06:12
---------
@summary:
---------
@author: Boris
"""

from datetime import datetime
import feapder
from items import *


class TestSpider(feapder.AirSpider):
    __custom_setting__ = dict(
        ITEM_PIPELINES=["feapder.pipelines.mongo_pipeline.MongoPipeline"],
        MONGO_IP="localhost",
        MONGO_PORT=27017,
        MONGO_DB="feapder",
        MONGO_USER_NAME="",
        MONGO_USER_PASS="",
        SPIDER_MAX_RETRY_TIMES=2,
    )

    def start_requests(self):
        yield feapder.Request("https://forums.redflagdeals.com/hot-deals-f9/")

    def validate(self, request, response):
        if response.status_code != 200:
            raise Exception("response code not 200")  # 重试

        # if "哈哈" not in response.text:
        #     return False # 抛弃当前请求

    def parse(self, request, response):
        topic_list = response.bs4().find_all('li', class_='row topic')

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

            if elapsed_mins <= 120:

                item = spider_data_item.SpiderDataItem()  # 声明一个item

                item._id = thread_id  # 给item属性赋值
                item.topic_title = topic_title  # 给item属性赋值
                item.upvotes = upvotes  # 给item属性赋值
                item.elapsed_mins = elapsed_mins
                item.retailer_name = retailer_name
                item.first_post_time_obj = first_post_time_obj
                item.first_post_time = first_post_time_string
                item.reply_count = posts
                item.view_count = views
                item.msg_sent_cnt = 0
                item.topic_link = topic_title_link

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
            'st': '',
            'nd': '',
            'rd': '',
            'th': ''
        }
        for i, j in date_suffix_dict.items():
            date_text = first_post_time_raw.replace(i, j)
        
        return datetime.strptime(date_text, '%b %d, %Y %I:%M %p')
    
    @staticmethod
    def topictitle_retailer(topic):
        try:
            topictitle_retailer = topic.find('a', class_='topictitle_retailer').text.strip()
        except:
            topictitle_retailer = topic.find('h3', class_='topictitle').text.split('\n')[1].strip()
        return topictitle_retailer


if __name__ == '__main__':
    spider = TestSpider(redis_key="feapder3:test_spider", thread_count=10)
    spider.start()