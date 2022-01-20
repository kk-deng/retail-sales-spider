# -*- coding: utf-8 -*-
"""
Created on 2022-01-16 17:06:12
---------
@summary: A IKEA spider which can scraped sales quantity of specific SKUs.
---------
@author: Kelvin
"""
import random
import time
from datetime import datetime, time as tm
# from typing import Dict, List, Set

import feapder
import telegram
# from feapder.db.mongodb import MongoDB
from feapder.utils.log import log
# from items import *
from tools import *
# from utils.helpers import escape_markdown

SCRAPE_COUNT = 1000
# BB_SHIPPING_CHECK = True
# BB_PICKUP_CHECK = False


class IkeaSpider(feapder.AirSpider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_operator = file_input_output.FileReadWrite()
        self.bot = telegram.Bot(token=self.file_operator.newbot_token)
        self.id_list = [
            10413528,
            90301621,
            70339291,
            60427293,
            30387118,
            20436713,
        ]
        self.products_dict = {product_id: {} for product_id in self.id_list}

    def start_requests(self):

        for i in range(1, SCRAPE_COUNT):

            for pid in self.id_list:
                url = f"https://shop.api.ingka.ikea.com/range/v3/ca/en/availability/product/ART,{pid}?storeIds=372"
                yield feapder.Request(url, method="GET")
                time.sleep(3)
            
            # Now time
            now = datetime.now().time()

            # Lower the speed at night
            if tm(1,00) <= now <= tm(2,59):
                time_gap = random.randrange(180, 300)
            elif tm(3,00) <= now <= tm(7,00):
                log.info('Task paused...')
                time_gap = 4*60*60
            else:
                time_gap = random.randrange(50, 70)

            if SCRAPE_COUNT > 2:
                log.info(f'## IKEA running for {i} / {SCRAPE_COUNT} runs, waiting for {time_gap}s...')
                time.sleep(time_gap)

    def download_midware(self, request):
        request.headers = {
            "Host": "shop.api.ingka.ikea.com",
            "Content-Type": "application/json",
            "Connection": "keep-alive",
            "IOS-Build-Nr": "4660",
            "Contract": "40663",
            "Accept": "application/json",
            "User-Agent": "IKEA App/3.8.2-4660 (iOS)",
            "Consumer": "IKEAAPPI",
            "Accept-Language": "en-ca",
            "Accept-Encoding": "gzip, deflate, br"
        }
        return request

    def parse(self, request, response):
        ikea_products = response.json

        for product in ikea_products:
            ikea_product = IkeaProduct(product)

            saved_product = self.products_dict[ikea_product.product_id]

            if not saved_product.get('stock_num'):
                # If return None, initialize the dict
                self.overwrite_products_dict(ikea_product)
            
            yield_conditions = [
                (saved_product.get('status_code') != ikea_product.status_code),
                (saved_product.get('stock_num') != ikea_product.stock_num),
            ]

            # Only update the product_dict and MongoDB when there is change
            if any(yield_conditions):
                # yield item

                msg_content = (
                    f'*ID*: _{ikea_product.product_id}_ \n'
                    f'(*{ikea_product.product_id}*) is *{ikea_product.status_code}* with sale *{ikea_product.sale_point}*. \n'
                    f'*Quantity*: *{saved_product.get("stock_num", 0)}->{ikea_product.stock_num}*'
                )

                self.send_bot_msg(msg_content)

                self.overwrite_products_dict(ikea_product)
        
        # print(response.json)
            
    def overwrite_products_dict(self, product):
        saved_product = self.products_dict[product.product_id]
        saved_product['store_id'] = product.store_id
        saved_product['sale_point'] = product.sale_point
        saved_product['status_code'] = product.status_code
        saved_product['stock_num'] = product.stock_num
        saved_product['store_name'] = product.store_name
    
    def send_bot_msg(self, content_msg: str) -> bool:
        log_content = content_msg.replace("\n", "")
        log.info(f'## Sending: {log_content}')
        
        try:
            self.bot.send_message(
                text=content_msg, 
                chat_id=self.file_operator.chat_id,
                # reply_markup=reply_markup,
                parse_mode=telegram.ParseMode.MARKDOWN
                )
            log.info('## Msg was sent successfully!')
            time.sleep(3)
            return True
        except Exception as e:
            log.info(f'## Msg failed sending with error:\n{e}')
            return False
            

class IkeaProduct:

    store_list = {
        "372": "Vaughan",
        "149": "North York",
        "256": "Etobicoke",
    }

    def __init__(self, ikea_product):
        self.product_id = int(ikea_product.get('productId'))
        self.store_id = ikea_product.get('storeId')
        self.sale_point = ikea_product.get('salePoint')
        self.status = ikea_product.get('status')
        self.status_code = self.status.get('code')
        self.store_name = self.store_list.get(self.store_id, "Other")
        
    @property
    def stock_num(self):
        if self.status_code in ['HIGH_IN_STOCK', 'LOW_IN_STOCK']:
            stock_des = self.status.get('description', '<b>0</b>')
            stock_num = stock_des.split('<b>')[1].split('</b>')[0]
            return int(stock_num)
        else:
            return 0

if __name__ == "__main__":
    IkeaSpider(thread_count=1).start()
