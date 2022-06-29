# -*- coding: utf-8 -*-
"""
Created on 2022-06-22 16:06:12
---------
@summary:
---------
@author: Kelvin
"""
from __future__ import annotations

import random
import time
from datetime import datetime
from datetime import time as tm

import feapder
from feapder.utils.log import log
from pydantic import BaseModel
from tools import file_input_output
from utils.tg_bot import TelegramBot

SCRAPE_COUNT = 3000


class LenovoSpider(feapder.AirSpider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_operator = file_input_output.FileReadWrite()
        self.chat_id = self.file_operator.chat_id
        self.tg_token = self.file_operator.newbot_token
        self.bot = TelegramBot(token=self.tg_token, chat_id=self.chat_id, parse_mode=False)
        self.request_header = self.file_operator.get_spider_header('lenovo_header')
        self.url = self.file_operator.lenovo_api
        self.params = {
            "pageFilterId": "49c9f88b-069a-41c9-9785-643e6aab7e96",
            "subseriesCode": "LEN101T0037",
            # "couponCode": "THINKBIGDEALS",
            "params": r"%7B%22classificationGroupIds%22%3A%22800001%22%2C%22pageFilterId%22%3A%2249c9f88b-069a-41c9-9785-643e6aab7e96%22%2C%22facets%22%3A%5B%5D%2C%22page%22%3A%221%22%2C%22pageSize%22%3A%2220%22%2C%22boostsProductCodes%22%3A%22%22%2C%22init%22%3Atrue%2C%22sorts%22%3A%5B%22shippingDate%22%5D%2C%22subseriesCode%22%3A%22LEN101T0037%22%7D"
        }
        self.previous_models = Z16Model()
        self.previous_model = {
            '21D4000FUS': Z16Model(),
            '21D4000GUS': Z16Model(),
            '21D4000JUS': Z16Model(),
            '21D4000KUS': Z16Model(),
            '21D4000HUS': Z16Model(),
        }

    def start_requests(self):
        for i in range(1, SCRAPE_COUNT):
            time_gap = self.get_random_time_gap()
        
            yield feapder.Request(self.url, params=self.params, method="GET")
            
            if SCRAPE_COUNT > 2:
                log.info(f'## Lenovo.ca running for {i} / {SCRAPE_COUNT} runs, waiting for {time_gap}s...')
                time.sleep(time_gap)
    
    def validate(self, request, response):
        if response.status_code != 200:
            content_msg = f'Error: HTTP {response.status_code}, pausing...'
            self.bot.send_bot_msg(content_msg)
            # raise Exception("response code not 200")

    def download_midware(self, request):
        request.headers = self.request_header
        return request

    def parse(self, request, response):
        api_json = response.json

        # Only check the highest spec HUS model
        product_list = api_json['data']['data']

        for product in product_list:
            # Create an object from dataclass
            z16_model = Z16Model(**product)

            # Get the difference between two record (new - old), converted to dict (asymmetric)
            info_diff = self.compare_model_diff(z16_model)
            
            if info_diff:
                content_msg = self.compose_diff_msg(z16_model, info_diff)
                self.bot.send_bot_msg(content_msg)

                # Save model if new changes are found
                self.save_new_model(z16_model)
            else:
                log.info(f'{z16_model.productCode} Model, price: ${z16_model.finalPrice}/-{z16_model.savePercent}% and {z16_model.leadTimeMessage} ({z16_model.leadTime} days) w/ {z16_model.couponCode} (Save {z16_model.couponSavePercentage}%)')

                # log.info(f'ModifyTime: {z16_model.modifyTime}; OnlineTime: {z16_model.onlineDate}; ')

    def get_random_time_gap(self) -> int:
        # Now time
        now = datetime.now().time()

        # Lower the speed at night
        if tm(1,00) <= now <= tm(2,59):
            time_gap = random.randrange(380, 500)
        elif tm(3,00) <= now <= tm(7,00):
            log.info('Task paused...')
            time_gap = 4*60*60
        else:
            time_gap = random.randrange(250, 270)
        
        return time_gap

    def compare_model_diff(self, new_model: Z16Model) -> dict:
        """Compare the new record of model with the saved model"""
        product_code = new_model.productCode
        saved_product = self.previous_model[product_code]

        return dict(new_model.__dict__.items() - saved_product.__dict__.items())

    def save_new_model(self, new_model: Z16Model) -> None:
        """Save the new model to self.previous_model"""
        product_code = new_model.productCode
        self.previous_model[product_code] = new_model

    @staticmethod
    def compose_diff_msg(z16_model: Z16Model, dct: dict) -> str:
        msg_content = f'Z16 {z16_model.productCode} price ${z16_model.finalPrice}/-{z16_model.savePercent}%:\n'

        for k, v in dct.items():
            msg_content += f'📄 {k}: {str(v)} \n'
        
        return msg_content


class Z16Model(BaseModel):
    productName: str="NB TP Z16 G1 R7_PRO 32G 2T 11P"
    productType: str="0"
    productCode: str="21D4000HUS"
    productStatus: str=""
    webPrice: str="5519.00"
    finalPrice: str="0000.00"
    couponPrice: str="9999.99"
    couponSaveAmount: str="1931.65"
    couponSavePercentage: str="35"
    saveAmount: str="1931.65"
    savePercent: str="35"
    couponCode: str="THINKJUNE"
    isMedion: bool=False
    ratingStar: str="0.0"
    commentCount: int=0
    marketingStatus: str="Available"
    modelsCount: int=0
    leadTime: int=85
    leadTimeMessage: str="Ships in 3+ months"
    inventoryStatus: int=1
    currencySymbol: str="$"
    currencyCode: str="CAD"
    modifyTime: datetime=1655700587736
    onlineDate: datetime=1655390050000
    machineType: str="22TPZ16Z6A121D4"
    summary: str="ThinkPad Z16 AMD (16″)"
    url: str="/p/laptops/thinkpad/thinkpadz/thinkpad-z16-16-amd/21D4000HUS"
    flCode: str="laptops"
    flName: str="Laptops"
    hasClaimIndicator: bool=False
    maxBuy: int=2
    maxBuyMessage: str="eCoupon limited to  2 units"
    couponCount: int=-1
    couponConsumed: bool=False
    couponProgress: int=-1
    couponRuleDiscount: int=35
    couponDiscountType: int=2
    isDCGSubseries: bool=False

    @classmethod
    @property
    def product_url(cls):
        return f'https://www.lenovo.com/ca/en{cls.url}'


if __name__ == "__main__":
    LenovoSpider(thread_count=1).start()

