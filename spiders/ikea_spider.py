# -*- coding: utf-8 -*-
"""
Created on 2022-01-16 17:06:12
---------
@summary: A IKEA spider which can scraped sales quantity of specific SKUs.
---------
@author: Kelvin
"""
# import random
# import time
# from datetime import datetime, time as tm
# from typing import Dict, List, Set

import feapder
import telegram
# from feapder.db.mongodb import MongoDB
# from feapder.utils.log import log
# from items import *
from tools import *
# from utils.helpers import escape_markdown

# SCRAPE_COUNT = 1000
# BB_SHIPPING_CHECK = True
# BB_PICKUP_CHECK = False


class IkeaSpider(feapder.AirSpider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_operator = file_input_output.FileReadWrite()
        self.bot = telegram.Bot(token=self.file_operator.newbot_token)
        self.products_dict = {}
        self.skus_list = [
            10413528,
            90301621,
        ]
        self.skus_str = "|".join([str(sku) for sku in self.skus_list])

    def start_requests(self):
        
        url = f"https://shop.api.ingka.ikea.com/range/v3/ca/en/availability/product/ART,90301621?storeIds=372"
        yield feapder.Request(url, method="GET")

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
            stock_des = self.status.get('description', '')
            stock_num = stock_des.split('<b>')[1].split('</b>')[0]
            return int(stock_num)
        else:
            return 0

if __name__ == "__main__":
    IkeaSpider(thread_count=1).start()
