# -*- coding: utf-8 -*-
"""
Created on 2021-11-29 16:01:50
---------
@summary: Main Function for all spiders
---------
@author: Kelvin
"""

from spiders import spider_man, bestbuy_spider, ikea_spider

if __name__ == "__main__":
    spider = spider_man.RfdSpider()
    bb_spider = bestbuy_spider.BBSpider()
    ik_spider = ikea_spider.IkeaSpider()
    spider.start()
    # bb_spider.start()
    ik_spider.start()
