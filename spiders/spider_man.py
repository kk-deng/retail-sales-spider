# -*- coding: utf-8 -*-
"""
Created on 2021-02-08 16:06:12
---------
@summary:
---------
@author: Boris
"""
from typing import List, Set, Dict

from datetime import datetime, time as tm
import time
import random
import feapder
from feapder.utils.log import log
from items import *
from tools import *

import telegram

from feapder.db.mongodb import MongoDB


SCRAPE_COUNT = 800
BB_SHIPPING_CHECK = True
BB_PICKUP_CHECK = False


class RfdSpider(feapder.AirSpider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = MongoDB()
        self.file_operator = file_input_output.FileReadWrite()
        self.bot = telegram.Bot(token=self.file_operator.token)
        self.random_header = self.file_operator.create_random_header
        self.tcl_skus = "|".join(['15604563'])

    def start_callback(self):
        self.send_bot_msg('Bot started!')
    
    def end_callback(self):
        self.send_bot_msg('Bot Stopped...!')

    def download_midware(self, request):
        # Downloader middleware uses random header from file_input_output
        if 'redflagdeals' in request.url:
            request.headers = self.random_header['rfd']
        elif 'costco' in request.url:
            request.headers = self.random_header['costco']
        elif 'bestbuy' in request.url:
            request.headers = self.random_header['bestbuy']

        return request

    def start_requests(self):
        for i in range(1, SCRAPE_COUNT):
            # Now time
            now = datetime.now().time()

            # Lower the speed at night
            if tm(1,00) <= now <= tm(2,59):
                time_gap = random.randrange(180, 300)
            elif tm(3,00) <= now <= tm(7,00):
                log.info('Task exiting...')
                break
            else:
                time_gap = random.randrange(50, 70)
            
            yield feapder.Request("https://forums.redflagdeals.com/hot-deals-f9/")
            # yield feapder.Request("https://www.bestbuy.ca/en-ca/product/playstation-5-console/15689336", callback=self.parse_bb_ps5)
            # yield feapder.Request(
            #     url = "https://www.bestbuy.ca/ecomm-api/availability/products?accept=application%2Fvnd.bestbuy.standardproduct.v1%2Bjson&accept-language=en-CA&locations=956%7C237%7C937%7C200%7C943%7C927%7C932%7C62%7C965%7C931%7C57%7C985%7C617%7C977%7C203%7C223%7C949%7C795%7C916%7C544%7C910%7C938%7C925%7C954%7C207%7C202%7C926%7C959%7C622%7C233%7C930%7C613%7C245&postalCode=L3T7T7&skus=15604563",
            #     payload={},
            #     callback=self.parse_bb_tcl
            # )

            yield feapder.Request(
                url = "https://www.bestbuy.ca/ecomm-api/availability/products?",
                params= {
                    "accept": "application/vnd.bestbuy.standardproduct.v1+json",
                    "accept-language": "en-CA",
                    "locations": "956|237|937|200|943|927|932|62|965|931|57|985|617|203|949|795|916|544|910|938",
                    "postalCode": "L3T7T7",
                    "skus": self.tcl_skus
                },
                payload={},
                callback=self.parse_bb_tcl
            )

            # Only check costco in daytime
            # if tm(8,00) <= now <= tm(18,30):
            #     yield feapder.Request("https://www.costco.ca/playstation-5-console-bundle.product.100696941.html?langId=-24", 
            #         callback=self.parse_costco)
            #     yield feapder.Request("https://www.costco.ca/.product.100780734.html?langId=-24", 
            #         callback=self.parse_costco)
            #     yield feapder.Request("https://www.costco.ca/.product.5203665.html?langId=-24", 
            #         callback=self.parse_costco)

            if SCRAPE_COUNT > 2:
                log.info(f'## Running for {i} / {SCRAPE_COUNT} runs, waiting for {time_gap}s...')
                time.sleep(time_gap)

    def validate(self, request, response):
        if ('redflagdeals' in request.url) and (response.status_code != 200):
            raise Exception("response code not 200")  # 重试

        # if "哈哈" not in response.text:
        #     return False # 抛弃当前请求

    def parse_costco(self, request, response):
        status_code = response.status_code
        if status_code == 200 and 'IN_STOCK' in response.text:
            log.info('Costco PS5 IN STOCK!!!')
            self.send_bot_msg(f'Costco PS5 updated: {response.status_code}. '
                f'Link: {request.url}')
        else:
            log.info(f'Costco PS5 not in stock...Status code: {status_code}')
    
    def parse_bb_ps5(self, request, response):
        add_to_cart_btn = response.xpath('//*[@id="test"]/button[not(@disabled)]')
        disabled_btn = response.xpath('//*[@id="test"]/button[@disabled]')

        if len(add_to_cart_btn) > 0:
            log.info('Bestbuy PS5 IN STOCK!!!')
            self.send_bot_msg(f'Bestbuy PS5 updated {add_to_cart_btn}.'
                f'Link: {request.url}')
        else:
            log.info(f'Bestbuy PS5 not in stock... {disabled_btn}')
    
    def parse_bb_tcl(self, request, response):
        response_json = response.json

        availabilities = response_json.get('availabilities')

        try:
            for availability in availabilities:
                product = BestBuyItem(availability)

                if BB_SHIPPING_CHECK:
                    if product.shipping_status == 'InStock':
                        msg_content = product.check_shipping()
                        log.warning(msg_content)
                        self.send_bot_msg(msg_content)
                    else:
                        msg_content = product.check_shipping()
                        log.info(msg_content)

                if BB_PICKUP_CHECK: 
                    if product.pickup_status == 'InStock':
                        msg_content = product.check_pickup()
                        log.warning(msg_content)
                        self.send_bot_msg(msg_content)
                    else:
                        msg_content = product.check_pickup()
                        log.info(msg_content)
                
        except Exception as e:
            log.info(f'Bestbuy TCL 55" info error...\n {e}')
  
        # try:
        #     availabilities = response.json['availabilities'][0]

        #     shipping = availabilities['shipping']
        #     pickup = availabilities['pickup']
        #     sku = availabilities['sku']
        #     seller_id = availabilities['sellerId']

        #     quantity_remaining = shipping['quantityRemaining']
        #     if quantity_remaining > 0:
        #         log.info(f'TCL 55\" IN STOCK!!! Status: {shipping["status"]} Quantity: {quantity_remaining}')
        #         self.send_bot_msg(f'TCL 55" in stock!! Status: {shipping["status"]}: {quantity_remaining} left.'
        #             f'Link: https://www.bestbuy.ca/en-ca/product/tcl-6-series-55-4k-uhd-hdr-qled-mini-led-smart-google-tv-55r646-ca-2021/15604563')
            
        #     elif pickup['status'] not in  ('OutOfStock', 'NotAvailable'):
        #         locations = pickup['locations']

        #         locations_instock = [f'{location["name"]}: {location["quantityOnHand"]} left.' for location in locations if location['quantityOnHand'] > 0]

        #         msg_content = "\n".join(locations_instock)

        #         log.info(f'TCL 55\" can Pick UP!! Status: {pickup["status"]}: {msg_content}')
        #         self.send_bot_msg(f'TCL 55 can Pick Up!! Status: {pickup["status"]}: {msg_content}.'
        #             f'Link: https://www.bestbuy.ca/en-ca/product/tcl-6-series-55-4k-uhd-hdr-qled-mini-led-smart-google-tv-55r646-ca-2021/15604563')
            
        #     else:
        #         log.info(f'TCL 55" NOT in stock...')

        except Exception as e:
            log.info(f'Bestbuy TCL 55" info error...\n {e}')


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
                (elapsed_mins <= 240 and upvotes >= 40)
            ]

            if any(record_conditions):
                item = spider_data_item.SpiderDataItem()  # 声明一个item

                # item.thread_id = thread_id  # 给item属性赋值
                item.thread_id = thread_id
                item.topic_title = topic_title  # 给item属性赋值
                item.upvotes = upvotes  # 给item属性赋值
                item.elapsed_mins = elapsed_mins
                item.retailer_name = topictitle_retailer
                item.first_post_time_obj = first_post_time_obj
                item.first_post_time = first_post_time_string
                item.reply_count = posts
                item.view_count = views
                item.topic_link = topic_title_link

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
        
        return self.send_bot_msg(msg_content)
    
    def send_bot_msg(self, content_msg: str) -> bool:
        log.info(f'## Sending: {content_msg}')
        try:
            self.bot.send_message(text=content_msg, chat_id=self.file_operator.chat_id)
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

class BestBuyItem:
    def __init__(self, availabilities):
        self.shipping = availabilities['shipping']
        self.pickup = availabilities['pickup']
        self.sku = availabilities['sku']
        self.seller_id = availabilities['sellerId']
        self.shipping_quantity = self.shipping['quantityRemaining']
        self.shipping_status = self.shipping['status']
        self.pickup_status = self.pickup['status']
        self.sku_map = self.get_skus_map
    
    @property
    def get_skus_map(self):
        return {}

    def check_shipping(self):
        if self.shipping_quantity > 0:
            msg_content = (
                f'{self.sku} is {self.shipping_status} with seller {self.seller_id}. '
                f'Quantity: {self.shipping_quantity}\n'
                f'Link: https://www.bestbuy.ca/en-ca/product/{self.sku}'
            )

            return msg_content
        else:
            return f'{self.sku} is {self.shipping_status} with Online seller {self.seller_id}.'

    def check_pickup(self):
        if self.pickup_status == 'InStock':
            locations = self.pickup['locations']

            locations_instock = [f'({loc["locationKey"]}) {loc["name"]}: {loc["quantityOnHand"]} left.' for loc in locations if loc['quantityOnHand'] > 0]

            locations_msg = "\n".join(locations_instock)

            msg_content = (
                f'{self.sku} has store PickUp {self.pickup_status}: {locations_msg}'
                f'Link: https://www.bestbuy.ca/en-ca/product/{self.sku}'
            )

            return msg_content
        else:
            return f'{self.sku} is {self.pickup_status} for PickUp.'


# if __name__ == '__main__':
#     spider = RfdSpider(thread_count=10)
#     spider.start()
