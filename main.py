# -*- coding: utf-8 -*-
"""
Created on 2021-02-08 16:01:50
---------
@summary: 爬虫入口
---------
@author: Boris
"""

from spiders import *

if __name__ == "__main__":
    spider = spider_man.TestSpider()
    spider.send_bot_msg('Bot started!')
    spider.start()
