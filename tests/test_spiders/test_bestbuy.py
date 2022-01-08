from items.bestbuy_item import BbShippingItem

def test_bestbuy_item_cls(api_bestbuy_product):
    item = BbShippingItem(api_bestbuy_product)

    assert item.sku == api_bestbuy_product.sku
    assert item.quantity == api_bestbuy_product.shipping_quantity
    assert item.status == api_bestbuy_product.shipping_status
    assert item.seller_id == api_bestbuy_product.seller_id