# -*- coding: utf-8 -*-
"""
Created on 2022-01-16 17:06:12
---------
@summary: An IKEA spider which can scraped sales quantity of specific SKUs.
---------
@author: Kelvin
"""
from __future__ import annotations
import random
import time
from datetime import datetime, time as tm
from functools import wraps
from typing import Dict, List, Set

import feapder
import telegram
# from feapder.db.mongodb import MongoDB
from feapder.utils.log import log
# from items import *
from tools import *
# from utils.helpers import escape_markdown

SCRAPE_COUNT = 2000


class IkeaSpider(feapder.AirSpider):
    store_id = '372'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_operator = file_input_output.FileReadWrite()
        self.ikea_api = self.file_operator.ikea_api
        self.ikea_header = self.file_operator.get_spider_header('ikea')
        self.bot = telegram.Bot(token=self.file_operator.newbot_token)
        self.art_id_dict = {
            '10413528': 'HEMNES TV bench',
            '70339291': 'FJÄLLBO Shelf unit',
            '70342199': 'FJÄLLBO Shelf unit (S)',
            '60427293': 'KNOPPÄNG Frame W',
            '30387118': 'KNOPPÄNG Frame B',
            '20436713': 'BAGGEBO Bookcase',
            '10287049': 'STRELITZIA Potted plant',
        }
        self.spr_id_dict = {
            '99291745': 'HYLLIS shelving unit',
        }
        self.products_dict = self.initialized_products_dict
        self.log_msg = ''
    
    @property
    def initialized_products_dict(self) -> dict:
        art_id_dict_copy = self.art_id_dict.copy()
        art_id_dict_copy.update(self.spr_id_dict)

        return {
            product_id: {'title': name}
            for product_id, name in
            art_id_dict_copy.items()
        }

    @property
    def id_url_str(self) -> str:
        art_str = ','.join([f'ART-{pid}' for pid in self.art_id_dict.keys()])
        spr_str = ','.join([f'SPR-{pid}' for pid in self.spr_id_dict.keys()])

        return art_str + ',' + spr_str

    def start_requests(self):

        for i in range(1, SCRAPE_COUNT):
            
            # Search one product in different IKEA stores
            # for pid in self.id_list:
            #     url = f"https://shop.api.ingka.ikea.com/range/v3/ca/en/availability/product/ART,{pid}?storeIds=372"
            #     yield feapder.Request(url, method="GET")
            #     time.sleep(3)

            # Search multiple products in one IKEA store
            url = f"{self.ikea_api}/{self.store_id}/{self.id_url_str}"
            yield feapder.Request(url, method="GET")

            # Now time
            now = datetime.now().time()

            # Lower the speed at night
            if tm(0,00) <= now <= tm(2,59):
                time_gap = random.randrange(180, 300)
            elif tm(3,00) <= now <= tm(7,00):
                log.info('Task paused...')
                time_gap = 4*60*60
            else:
                time_gap = random.randrange(100, 150)

            if SCRAPE_COUNT > 2:
                log.info(f'## IKEA running for {i} / {SCRAPE_COUNT} runs, waiting for {time_gap}s...')
                time.sleep(time_gap)
            
            if i % 2 == 0:
                log.info(self.log_msg)

    def download_midware(self, request) -> feapder.Request:
        request.headers = self.ikea_header
        return request

    def parse(self, request, response):
        ikea_products = response.json

        out_of_stock_dict = {}

        for product in ikea_products:
            ikea_product = IkeaProduct(product)

            if len(self.products_dict[ikea_product.product_id]) == 1:
                # If return None, initialize the dict
                self.overwrite_products_dict(ikea_product, None)
            
            saved_product = self.products_dict[ikea_product.product_id]

            yield_conditions = [
                (saved_product.get('status_code') != ikea_product.status_code),
                (saved_product.get('stock_num') != ikea_product.stock_num),
            ]

            # Only update the product_dict and MongoDB when there is change
            if any(yield_conditions):
                # If status_code changed, return a change string
                if yield_conditions[0]:
                    msg_status_code = f'{saved_product.get("status_code", "Unknown")} -> {ikea_product.status_code}'
                else:
                    msg_status_code = ikea_product.status_code
                
                # If stock_num changed, return a change string
                if yield_conditions[1]:
                    msg_stock_num = f'{saved_product.get("stock_num", 0)} -> {ikea_product.stock_num}'
                else:
                    msg_stock_num = self.resolve_stock_num(ikea_product)

                msg_content = (
                    f'*Name*: _{saved_product["title"]}_ (*{ikea_product.product_id}*)\n'
                    f'*Status*: *{msg_status_code}* at *{ikea_product.sale_point}*. \n'
                    f'*Quantity*: *{msg_stock_num}*'
                )

                reply_to_msg_id = saved_product.get('previous_msg_id')

                # If msg sent successfully, return telegram msg id
                returned_msg = self.send_bot_msg(msg_content, reply_to_msg_id)

                returned_msg_id = returned_msg['message_id']

                self.overwrite_products_dict(ikea_product, returned_msg_id)
            
            log_stock_num = self.resolve_stock_num(ikea_product)

            # Example: {10413528: 'HIGH_IN_STOCK(14)'}
            out_of_stock_dict[ikea_product.product_id] =  f'{saved_product["title"]} - {ikea_product.status_code}({log_stock_num})'
        
        values = [f'{key}: {value}' for key, value in out_of_stock_dict.items()]
        self.log_msg = 'IKEA Stock: ' + ', '.join(values)

    def overwrite_products_dict(self, ikea_product: IkeaProduct, returned_msg_id: str) -> None:
        staged_product = self.products_dict[ikea_product.product_id]
        staged_product['store_id'] = ikea_product.store_id
        staged_product['sale_point'] = ikea_product.sale_point
        staged_product['status_code'] = ikea_product.status_code
        staged_product['stock_num'] = ikea_product.stock_num
        staged_product['store_name'] = ikea_product.store_name
        
        if ikea_product.restock_date:
            staged_product['restock_date'] = ikea_product.restock_date
        
        # If the sent msg id is not None, record it into the product dict
        if returned_msg_id:
            staged_product['previous_msg_id'] = returned_msg_id
    
    def resolve_stock_num(self, ikea_product: IkeaProduct) -> str:
        if ikea_product.restock_date:
            return ikea_product.restock_date
        else:
            return ikea_product.stock_num

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
    def send_bot_msg(self, content_msg: str, reply_to_msg_id: str) -> str or bool:
        log_content = content_msg.replace("\n", "")
        log.warning(f'## Sending: {log_content}')
        
        try:
            returned_msg = self.bot.send_message(
                text=content_msg, 
                chat_id=self.file_operator.chat_id,
                reply_to_message_id=reply_to_msg_id,
                # reply_markup=reply_markup,
                parse_mode=telegram.ParseMode.MARKDOWN
                )
            log.info('## Msg was sent successfully!')
            time.sleep(3)
            return returned_msg
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
        self.product_id = ikea_product.get('productId')
        self.product_type = ikea_product.get('productType')
        self.store_id = ikea_product.get('storeId')
        self.sale_point = ikea_product.get('salePoint')
        self.status = ikea_product.get('status')
        self.status_code = self.status.get('code')
        self.store_name = self.store_list.get(self.store_id, "Other")
        self.locations = ikea_product.get('locations')
    
    def __str__(self) -> str:
        return str(self.__class__) + '\n' + \
            '\n'.join((str(item) + ' = ' + str(self.__dict__[item]) for item in sorted(self.__dict__)))

    @property
    def stock_num(self) -> int:
        if self.status_code != 'OUT_OF_STOCK':
            stock_des = self.status.get('description', '<b>0</b>')
            stock_num = stock_des.split('<b>')[1].split('</b>')[0]
            return int(stock_num)
        else:
            return 0

    @property
    def items(self) -> List[Dict]: 
        try:
            return self.locations[0]['items']
        except:
            return []
    
    @property
    def title(self) -> str:
        try:
            return self.items[0]['title']
        except:
            return 'Unknown'
    
    @property
    def restock_date(self) -> str or None:
        description = self.status.get('description')
        if 'Estimated' in description:
            # Extract date from "Estimated back in stock: <b>2022-01-21</b>"
            return description.split('<b>')[1].split('</b>')[0]
        else:
            return None


if __name__ == "__main__":
    IkeaSpider(thread_count=1).start()
