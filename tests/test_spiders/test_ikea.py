import pytest
from spiders import ikea_spider

@pytest.mark.ikeaitem
def test_ikea_item_cls(api_ikea_products):

    ikea_product = api_ikea_products

    product = ikea_spider.IkeaProduct(ikea_product)

    assert type(product.product_id) == int
    assert len(product.store_id) == 3
    assert type(product.sale_point) == str
    assert product.status_code in ['HIGH_IN_STOCK', 'OUT_OF_STOCK', 'LOW_IN_STOCK']
    if product.status_code == 'OUT_OF_STOCK':
        assert product.stock_num == 0
    else:
        assert product.stock_num > 0
        