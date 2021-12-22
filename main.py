# -*- coding: utf-8 -*-
"""
Created on 2021-02-08 16:01:50
---------
@summary: 爬虫入口
---------
@author: Boris
"""

from spiders import spider_man, bestbuy_spider

if __name__ == "__main__":
    spider = spider_man.RfdSpider()
    bb_spider = bestbuy_spider.BBSpider()
    spider.start()
    bb_spider.start()
