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
from items import ikea_item
from tools import *
# from utils.helpers import escape_markdown
from utils.tg_bot import TelegramBot


SCRAPE_COUNT = 2000
NIGHT_START_TIME = (0,00)
NIGHT_END_TIME = (2,59)
MORNING_TIME = (7,00)


class IkeaSpider(feapder.AirSpider):
    store_id = '372'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_operator = file_input_output.FileReadWrite()
        self.ikea_api = self.file_operator.ikea_api
        self.ikea_header = self.file_operator.get_spider_header('ikea')
        self.newbot_token = self.file_operator.newbot_token
        self.chat_id = self.file_operator.chat_id
        self.bot = TelegramBot(token=self.newbot_token, chat_id=self.chat_id)
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
            # '99291745': 'HYLLIS shelving unit',
        }
        self.products_dict = self.initialized_products_dict
        self.log_msg = ''
    
    @property
    def initialized_products_dict(self) -> dict:
        """Generate the product list by combining ART and SPR products.

        Returns:
            dict: A dict contains product_id as key, and a dict of data as value
        """
        art_id_dict_copy = self.art_id_dict.copy()
        art_id_dict_copy.update(self.spr_id_dict)

        return {
            product_id: {'title': name}
            for product_id, name in
            art_id_dict_copy.items()
        }

    @property
    def id_url_str(self) -> str:
        """Create a long string with all desired products for URL parameters.

        Returns:
            str: For URL request, example: ART-10413528,ART-70339291,SPR-99291745
        """
        art_str = ','.join([f'ART-{pid}' for pid in self.art_id_dict.keys()])
        spr_str = ','.join([f'SPR-{pid}' for pid in self.spr_id_dict.keys()])

        return art_str + ',' + spr_str

    def start_requests(self):
        """Main method to yield requests by calling the API.
        The request frequency will be reduced at night time.

        Yields:
            feapder.Request: Request object with API URL
        """
        for i in range(1, SCRAPE_COUNT):
            
            # Search one product in different IKEA stores
            # for pid in self.id_list:
            #     url = f"https://shop.api.ingka.ikea.com/range/v3/ca/en/availability/product/ART,{pid}?storeIds=372"
            #     yield feapder.Request(url, method="GET")
            #     time.sleep(3)

            # Search multiple products in one IKEA store
            url = f"{self.ikea_api}/{self.store_id}/{self.id_url_str}"
            yield feapder.Request(url, method="GET")

            # Get wait time gap
            time_gap = self.scrape_time_gap

            if SCRAPE_COUNT > 2:
                log.info(f'## IKEA running for {i} / {SCRAPE_COUNT} runs, waiting for {time_gap}s...')
                time.sleep(time_gap)
            
            if i % 2 == 0:
                log.info(self.log_msg)

    def download_midware(self, request) -> feapder.Request:
        request.headers = self.ikea_header
        return request

    def parse(self, request, response):
        """Main parser method which process the responses.
        If the preset conditions are met, send telegram messages.
        Load data to MongoDB Atlas when the stock status/number is changed.

        Args:
            request (feapder.Request): Request object of feapder
            response (feapder.Response): Response object of feapder

        Yields:
            ikea_item.IkeaStockItem: To load data to MongoDB Atlas
        """
        ikea_products = response.json

        out_of_stock_dict = {}

        for product in ikea_products:
            ikea_product = IkeaProduct(product)

            # Create items to be uploaded
            upload_item = ikea_item.IkeaStockItem(
                ikea_product, 
                ref_dict=self.initialized_products_dict
            )

            if len(self.products_dict[ikea_product.product_id]) == 1:
                # If return None, initialize the dict
                self.overwrite_products_dict(ikea_product, None)
                # Add the first entry to database
                yield upload_item
            
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
                    msg_stock_num = ikea_product.stock_num

                msg_content = (
                    f'*Name*: _{saved_product["title"]}_ (*{ikea_product.product_id}*)\n'
                    f'*Status*: *{msg_status_code}* at *{ikea_product.sale_point}*. \n'
                    f'*Quantity*: *{msg_stock_num}*'
                )

                reply_to_msg_id = saved_product.get('previous_msg_id')

                # If msg sent successfully, return telegram msg id
                returned_msg = self.bot.send_bot_msg(msg_content, reply_to_msg_id)
                # returned_msg = self.send_bot_msg(msg_content, reply_to_msg_id)

                returned_msg_id = returned_msg['message_id']

                self.overwrite_products_dict(ikea_product, returned_msg_id)

                # Update items when stock changes
                yield upload_item
            
            # Example: {10413528: 'HIGH_IN_STOCK(14)'}
            out_of_stock_dict[ikea_product.product_id] = self.get_product_log_str(ikea_product)
        
        values = [f'{key}: {value}' for key, value in out_of_stock_dict.items()]
        self.log_msg = 'IKEA Stock: ' + ', '.join(values)

    @property
    def scrape_time_gap(self) -> int:
        """Get wait time gap provided by the current time.

        Returns:
            int: The seconds to be wait between API requests
        """
        # Now time
        now = datetime.now().time()

        # Lower the speed at night
        if tm(*NIGHT_START_TIME) <= now <= tm(*NIGHT_END_TIME):
            time_gap = random.randrange(180, 300)
        elif tm(*NIGHT_END_TIME) < now <= tm(*MORNING_TIME):
            log.info('Task paused...')
            time_gap = 4*60*60
        else:
            time_gap = random.randrange(100, 150)
        
        return time_gap

    def overwrite_products_dict(self, ikea_product: IkeaProduct, returned_msg_id: str) -> None:
        """Update the products_dict with the latest stock information.

        Args:
            ikea_product (IkeaProduct): An IkeaProduct object of each product from the API response
            returned_msg_id (str): The last Telegram Message ID used to quote the message
        """
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

    def get_product_log_str(self, ikea_product: IkeaProduct) -> str:
        """Return a string containing product name, status code and stock number/restock date.

        Args:
            ikea_product (IkeaProduct): An IkeaProduct object of each product from the API response

        Returns:
            str: A string with the latest stock status, example: HEMNES TV bench - HIGH_IN_STOCK(14)
        """
        # If product has a restock date rather than stock_num, use it instead
        if ikea_product.restock_date:
            stock_num_restock_date = ikea_product.restock_date
        else:
            stock_num_restock_date = ikea_product.stock_num
        
        # Get saved product name for log msg
        try:
            saved_product_name = self.products_dict[ikea_product.product_id]['title']
        except KeyError:
            saved_product_name = 'Unknown'

        return f'{saved_product_name} - {ikea_product.status_code}({stock_num_restock_date})'
            

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
        self.timestamp = datetime.now()
    
    def __str__(self) -> str:
        return str(self.__class__) + '\n' + \
            '\n'.join((str(item) + ' = ' + str(self.__dict__[item]) for item in sorted(self.__dict__)))

    @property
    def stock_num(self) -> int:
        """Get stock number of the product.
        In case of product that is not sold in the store, the status will return:
        # {'code': 'OTHER', 'htmlText': 'Not sold at Vaughan', 'label': 'Not sold at Vaughan', 'description': '', 'colour': '#929292', 'timestamp': ''}

        Returns:
            int: Number of the product available.
        """
        _description = self.status.get('description', '<b>0</b>')
        if self.status_code != 'OUT_OF_STOCK' and len(_description) > 1:
            stock_num = _description.split('<b>')[1].split('</b>')[0]
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
