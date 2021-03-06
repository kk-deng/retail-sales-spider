# -*- coding: utf-8 -*-
"""
Created on 2022-03-11 1:23:36
---------
@summary: Ikea item for database loading
---------
@author: Kelvin
"""

from feapder import UpdateItem


class IkeaStockItem(UpdateItem):
    """Ikea stock information for database storage, e.g. MongoDB"""

    def __init__(self, ikea_product, *args, **kwargs):
        # art_id_dict = kwargs.get('ref_dict')[0]
        # spr_id_dict = kwargs.get('ref_dict')[1]
        # art_id_dict.update(spr_id_dict)

        product_id_dict = kwargs.get('ref_dict')

        self.product_id = ikea_product.product_id
        self.name = product_id_dict.get(self.product_id)['title']
        self.status_code = ikea_product.status_code
        self.stock_num = ikea_product.stock_num
        self.timestamp = ikea_product.timestamp
        self.store_id = ikea_product.store_id
        self.restock_date = ikea_product.restock_date
        self.product_type = ikea_product.product_type
        self.sale_point = ikea_product.sale_point
        self.status = ikea_product.status
        self.store_name = ikea_product.store_name
        self.locations = ikea_product.locations
