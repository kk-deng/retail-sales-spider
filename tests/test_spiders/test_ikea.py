import pytest
from spiders import ikea_spider

@pytest.mark.ikeaitem
def test_ikea_item_cls(api_ikea_products_by_store):

    product = ikea_spider.IkeaProduct(api_ikea_products_by_store)

    assert type(product.product_id) == str
    assert len(product.product_id) == 8
    assert len(product.store_id) == 3
    assert type(product.sale_point) == str
    assert product.status_code in ['HIGH_IN_STOCK', 'OUT_OF_STOCK', 'LOW_IN_STOCK', 'MEDIUM_IN_STOCK']

    # Only out_of_stock will get 0 inventory
    if product.status_code == 'OUT_OF_STOCK':
        assert product.stock_num == 0
    else:
        assert product.stock_num > 0

    # Assert the "Estimated back in stock: <b>2022-01-21</b>"
    if product.restock_date:
        assert product.restock_date.split('-')[0] == '2022'

    # When in stock, check if items show location information
    if product.status_code != 'OUT_OF_STOCK':
        assert type(product.items) == list
        assert len(product.items) > 0
        assert product.title != 'Unknown'
    
    print(product)
    assert type(product.__str__()) == str

    # if product.restock_date:
    assert product.restock_date.split('-')[0] == '2022'


@pytest.mark.ikeaitem
def test_ikea_item_spider():
    spider = ikea_spider.IkeaSpider()
    # assert '10413528' in spider.products_dict
    assert type(spider.id_url_str) == str
    assert type(spider.id_url_str) == str
