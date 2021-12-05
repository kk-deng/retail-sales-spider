# -*- coding: utf-8 -*-
"""
Created on 2021-02-08 16:01:50
---------
@summary: 爬虫入口
---------
@author: Boris
"""

from feapder import Spider

from spiders import *


def spider_integration():
    """
    Spider integration for rfd and costco
    """
    spider = Spider(redis_key='test')
    
    spider.add_parser(spider_man.RfdSpider)
    spider.add_parser(spider_man_costco.CostcoPS5Spider)

    spider.start()

if __name__ == "__main__":
    spider_integration()
