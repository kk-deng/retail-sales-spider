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
    store_id = '372'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_operator = file_input_output.FileReadWrite()
        self.bot = telegram.Bot(token=self.file_operator.newbot_token)
        self.art_id_list = [
            '10413528',
            '90301621',
            '70339291',
            '60427293',
            '30387118',
            '20436713',
            '10287049',
        ]
        self.spr_id_list = [
            '79009502',
            '99000483',
            '99291745',
        ]
        self.products_dict = {product_id: {} for product_id in self.art_id_list + self.spr_id_list}
        self.log_msg = ''
    
    @property
    def id_url_str(self):
        art_str = ','.join([f'ART-{pid}' for pid in self.art_id_list])
        spr_str = ','.join([f'SPR-{pid}' for pid in self.spr_id_list])

        return art_str + ',' + spr_str

    def start_requests(self):

        for i in range(1, SCRAPE_COUNT):

            # for pid in self.id_list:
            #     url = f"https://shop.api.ingka.ikea.com/range/v3/ca/en/availability/product/ART,{pid}?storeIds=372"
            #     yield feapder.Request(url, method="GET")
            #     time.sleep(3)

            url = f"https://shop.api.ingka.ikea.com/range/v3/ca/en/availability/store/{self.store_id}/{self.id_url_str}"
            yield feapder.Request(url, method="GET")

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
            
            if i % 2 == 0:
                log.info(self.log_msg)

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

        out_of_stock_dict = {}

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
                    f'*Name*: _{ikea_product.title}_ (*{ikea_product.product_id}*)\n'
                    f'*Status*: *{msg_status_code}* at *{ikea_product.sale_point}*. \n'
                    f'*Quantity*: *{msg_stock_num}*'
                )

                self.send_bot_msg(msg_content)

                self.overwrite_products_dict(ikea_product)
            
            # Example: {10413528: 'HIGH_IN_STOCK(14)'}
            out_of_stock_dict[ikea_product.product_id] =  f'{ikea_product.title}-{ikea_product.status_code}({str(ikea_product.stock_num)})'
        
        values = [f'{key}: {value}' for key, value in out_of_stock_dict.items()]
        self.log_msg = 'IKEA Stock: ' + ', '.join(values)
        
        # print(response.json)
            
    def overwrite_products_dict(self, ikea_product):
        saved_product = self.products_dict[ikea_product.product_id]
        saved_product['store_id'] = ikea_product.store_id
        saved_product['sale_point'] = ikea_product.sale_point
        saved_product['status_code'] = ikea_product.status_code
        saved_product['stock_num'] = ikea_product.stock_num
        saved_product['store_name'] = ikea_product.store_name
        if saved_product['title'] == 'Unknown':
            saved_product['title'] = ikea_product.title
            
        if ikea_product.restock_date:
            saved_product['restock_date'] = ikea_product.restock_date
    
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
        self.product_id = ikea_product.get('productId')
        self.product_type = ikea_product.get('productType')
        self.store_id = ikea_product.get('storeId')
        self.sale_point = ikea_product.get('salePoint')
        self.status = ikea_product.get('status')
        self.status_code = self.status.get('code')
        self.store_name = self.store_list.get(self.store_id, "Other")
        self.locations = ikea_product.get('locations')
        
    @property
    def stock_num(self):
        if self.status_code in ['HIGH_IN_STOCK', 'LOW_IN_STOCK']:
            stock_des = self.status.get('description', '<b>0</b>')
            stock_num = stock_des.split('<b>')[1].split('</b>')[0]
            return int(stock_num)
        else:
            return 0

    @property
    def items(self): 
        try:
            return self.locations[0]['items']
        except:
            return []
    
    @property
    def title(self):
        try:
            return self.items[0]['title']
        except:
            return 'Unknown'
    
    @property
    def restock_date(self):
        description = self.status.get('description')
        if 'Estimated' in description:
            # Extract date from "Estimated back in stock: <b>2022-01-21</b>"
            return description.split('<b>')[1].split('</b>')[0]
        else:
            return None


if __name__ == "__main__":
    IkeaSpider(thread_count=1).start()
