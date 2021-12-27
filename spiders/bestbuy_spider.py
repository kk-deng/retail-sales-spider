# -*- coding: utf-8 -*-
"""
Created on 2021-02-08 16:06:12
---------
@summary:
---------
@author: Boris
"""
import random
import time
from datetime import datetime
from datetime import time as tm
from typing import Dict, List, Set

import feapder
import telegram
from feapder.db.mongodb import MongoDB
from feapder.utils.log import log
from items import *
from tools import *
from utils.helpers import escape_markdown

SCRAPE_COUNT = 800
BB_SHIPPING_CHECK = True
BB_PICKUP_CHECK = False


class BBSpider(feapder.AirSpider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_operator = file_input_output.FileReadWrite()
        self.bot = telegram.Bot(token=self.file_operator.token)
        self.random_header = self.file_operator.create_random_header
        self.list_skus = "|".join([
            '15604563',
            '15480289',
            # '15078017',
            # '15166285',
            # '15084753',
            '14936769',
            '14936767',
        ])

    def download_midware(self, request):
        # Downloader middleware uses random header from file_input_output
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
            
            yield feapder.Request(
                url = "https://www.bestbuy.ca/ecomm-api/availability/products?",
                params= {
                    "accept": "application/vnd.bestbuy.standardproduct.v1+json",
                    "accept-language": "en-CA",
                    "locations": "956|237|937|200|943|927|932|62|965|931|57|985|617|203|949|795|916|544|910|938",
                    "postalCode": "L3T7T7",
                    "skus": self.list_skus
                },
                payload={},
            )

            if SCRAPE_COUNT > 2:
                log.info(f'## Bestbuy running for {i} / {SCRAPE_COUNT} runs, waiting for {time_gap}s...')
                time.sleep(time_gap)

    def validate(self, request, response):
        if response.status_code != 200:
            raise Exception("response code not 200")
    
    def parse(self, request, response):
        response_json = response.json

        availabilities = response_json.get('availabilities')

        try:
            for availability in availabilities:
                product = BestBuyItem(availability)
                now = datetime.now()

                # Instantiate one item for mongoDB
                item = bestbuy_item.BbShippingItem()
                # item.identifier = f's-{product.sku}-{product.shipping_status}-{product.shipping_quantity}'
                item.sku = product.sku
                item.timestamp = now
                item.quantity = product.shipping_quantity
                item.status = product.shipping_status
                item.stock_type = 'shipping'
                item.seller_id = product.seller_id

                yield item
                if BB_SHIPPING_CHECK:
                    if product.shipping_status == 'InStock' and \
                        product.shipping_quantity <= 5:
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
            log.info(f'Bestbuy info error...\n {e}')
    
    def send_bot_msg(self, content_msg: str) -> bool:
        log_content = content_msg.replace("\n", "")
        log.info(f'## Sending: {log_content}')
        
        try:
            self.bot.send_message(
                text=content_msg, 
                chat_id=self.file_operator.channel_id,
                # reply_markup=reply_markup,
                # parse_mode=telegram.ParseMode.MARKDOWN
                )
            log.info('## Msg was sent successfully!')
            time.sleep(3)
            return True
        except Exception as e:
            log.info(f'## Msg failed sending with error:\n{e}')
            return False


class BestBuyItem:
    def __init__(self, availabilities):
        self.shipping = availabilities['shipping']
        self.pickup = availabilities['pickup']
        self.sku = int(availabilities['sku'])
        self.seller_id = availabilities['sellerId']
        self.shipping_quantity = self.shipping['quantityRemaining']
        self.shipping_status = self.shipping['status']
        self.pickup_status = self.pickup['status']
        # self.sku_map = self.get_skus_map
        self.pickup_locations = self.good_pickup_locations

    @property
    def get_skus_map(self):
        return {}

    @property
    def good_pickup_locations(self) -> List[dict]:
        locations = self.pickup.get('locations')
        
        if len(locations) == 0:
            return []
        else:
            return [loc for loc in locations if loc['quantityOnHand'] > 0]

    def check_shipping(self):
        if self.shipping_quantity > 0:
            product_info = self.check_product_info
            name = product_info['name']
            sale_price = product_info['salePrice']
            regular_price = product_info['regularPrice']

            msg_content = (
                f'Name: {name} \n'
                f'({self.sku}) is {self.shipping_status} with seller {self.seller_id}. '
                f'Quantity: {self.shipping_quantity}, Price: ${sale_price}(${regular_price})\n'
                f'Link: https://www.bestbuy.ca/en-ca/product/{self.sku}'
            )

            return msg_content
        else:
            return f'{self.sku} is {self.shipping_status} with Online seller {self.seller_id}.'

    def check_pickup(self):
        if self.pickup_status == 'InStock':
            product_info = self.check_product_info
            name = product_info['name']
            sale_price = product_info['salePrice']
            regular_price = product_info['regularPrice']

            locations_instock = [f'({loc["locationKey"]}) {loc["name"]}: {loc["quantityOnHand"]} left.' for loc in self.good_pickup_locations]

            locations_msg = "\n".join(locations_instock)

            msg_content = (
                f'Name: {name} \n'
                f'({self.sku}) has store PickUp {self.pickup_status}, Price: ${sale_price}(${regular_price}): {locations_msg}'
                f'Link: https://www.bestbuy.ca/en-ca/product/{self.sku}'
            )

            return msg_content
        else:
            return f'{self.sku} is {self.pickup_status} for PickUp.'
    
    @property
    def check_product_info(self):
        response_dict = feapder.Request(
            url = f"https://www.bestbuy.ca/api/v2/json/product/{self.sku}?",
            params= {
                "currentRegion": "ON",
                "lang": "en-CA",
                "include": "all"
            },
            headers = file_input_output.FileReadWrite().create_random_header['bestbuy']
        ) \
        .get_response().json

        target_keys = [
            'name',
            'regularPrice', 
            'salePrice', 
            'saleStartDate',
            'SaleEndDate',
            'upcNumber',
        ]

        return {key: response_dict.get(key) for key in target_keys}
        
        
# if __name__ == '__main__':
#     spider = RfdSpider(thread_count=10)
#     spider.start()
