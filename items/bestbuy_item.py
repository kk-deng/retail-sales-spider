# -*- coding: utf-8 -*-
"""
Created on 2021-12-26 17:28:36
---------
@summary:
---------
@author: Kelvin
"""

from feapder import Item, UpdateItem


class BbShippingItem(UpdateItem):
    """
    This class was generated by feapder.
    command: feapder create -i spider_data.
    """

    def __init__(self, product, *args, **kwargs):
        self.sku = product.sku
        self.timestamp = None
        self.quantity = product.shipping_quantity
        self.status = product.shipping_status
        self.stock_type = None
        self.seller_id = product.seller_id
        # self.pickup_status = None
        # self.rmd_hill_quantity = None
        # self.pickup_locations = None
