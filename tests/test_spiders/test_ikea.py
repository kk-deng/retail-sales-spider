import pytest
from spiders import ikea_spider

@pytest.mark.ikeaitem
def test_ikea_item_cls(api_ikea_products):

    ikea_product = api_ikea_products

    product = ikea_spider.IkeaProduct(ikea_product)

    assert type(product.product_id) == int