from datetime import datetime
from spiders.samsung_spider import SamsungProduct


def test_z16_model_cls(api_samsung_product, api_samsung_product_no_promo):
    mock_response = api_samsung_product['productDatas'][0]
    ble_product = SamsungProduct(**mock_response)

    ble_product_changed = SamsungProduct(**mock_response)

    # New change to the item, like price drop
    ble_product_changed.salesStatus = 'IN_STOCK'

    no_promo_response = api_samsung_product_no_promo['productDatas'][0]

    no_promo_product = SamsungProduct(**no_promo_response)

    assert ble_product.promotionPrice == 27.5
    assert ble_product.stockLevelStatus == "outOfStock"

    assert no_promo_product.promotionPrice == None
    assert no_promo_product.stockLevelStatus == "outOfStock"
    
    diff = ble_product_changed.__dict__.items() - ble_product.__dict__.items()

    assert dict(diff) == {'salesStatus': 'IN_STOCK'}
