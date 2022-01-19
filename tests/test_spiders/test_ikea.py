import pytest
from spiders import ikea_spider


def test_ikea_item_cls(api_ikea_products):

    ikea_product = api_ikea_products[0]

    product = ikea_spider.IkeaProduct(ikea_product)
