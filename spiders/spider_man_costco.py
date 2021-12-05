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
from tools import *

import telegram


SCRAPE_COUNT = 600


class CostcoPS5Spider(feapder.BaseParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_operator = file_input_output.FileReadWrite()
        self.bot = telegram.Bot(token=self.file_operator.token)
        self.random_header = self.file_operator.create_random_header

    def start_callback(self):
        self.send_bot_msg('Costco Bot started!')
    
    def end_callback(self):
        self.send_bot_msg('Costco Bot Stopped...!')

    def download_midware(self, request):
        # Downloader middleware uses random header from file_input_output
        request.headers = self.random_header['costco']
        return request

    def start_requests(self):
        for i in range(1, SCRAPE_COUNT):
            time_gap = random.randrange(50, 70)
            # Only check costco in daytime
            # now = datetime.now().time()
            # if tm(8,00) <= now <= tm(18,30):
            yield feapder.Request("https://www.costco.ca/playstation-5-console-bundle.product.100696941.html")

            if SCRAPE_COUNT > 2:
                log.info(f'## Running for {i} / {SCRAPE_COUNT} runs, waiting for {time_gap}s...')
                time.sleep(time_gap)

    def parse(self, request, response):
        status_code = response.status_code
        if status_code == 200 and 'IN_STOCK' in response.text:
            log.info('Costco PS5 IN STOCK!!!')
            self.send_bot_msg(f'Costco PS5 updated: {response.status_code}. '
                f'Link: {request.url}')
        else:
            log.info(f'Costco PS5 not in stock...Status code: {status_code}')
    
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
