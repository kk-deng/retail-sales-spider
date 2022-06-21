import json
import random

import pytest
from spiders.bestbuy_spider import BestBuyItem
from spiders.spider_man import RfdTopic


def load_json(file_path) -> dict:
    with open(file_path) as json_file:
        return json.load(json_file)


@pytest.fixture(autouse=True)
def api_topic():
    info = load_json('tests/jsons/rfd_topic.json')

    watch_list = [
        'PS5',
        'PlayStation 5',
        '1000XM4',
        'Bambino',
        'Breville',
        'Fido',
    ]

    watch_list = [item.lower() for item in watch_list]

    return RfdTopic(info, watch_list)


@pytest.fixture(autouse=True)
def api_bestbuy_product():
    availabilities = load_json('tests/jsons/bestbuy.json')

    availability = availabilities['availabilities'][0]

    return BestBuyItem(availability)


@pytest.fixture
def api_ikea_products():
    ikea_products = load_json('tests/jsons/ikea.json')

    ikea_product = random.choice(ikea_products)

    return ikea_product

@pytest.fixture
def api_ikea_products_by_store():
    products_by_store = load_json('tests/jsons/ikea_by_store.json')

    return random.choice(products_by_store)

@pytest.fixture
def api_ikea_product_storeid():
    ikea_product_contact_staff = [
        {
            "productId": "10413528",
            "productType": "ART",
            "storeId": "149",
            "salePoint": "CONTACT_STAFF",
            "productLocation": "CONTACT STAFF",
            "status": {
                "code": "HIGH_IN_STOCK",
                "htmlText": "<b>In stock</b> at North York",
                "label": "In stock",
                "description": "There are <b>14</b> in stock at North York",
                "colour": "#0A8A00",
                "timestamp": ""
            },
            "locations": [
                {
                    "heading": "<b>Contact staff</b>",
                    "items": [
                        {
                            "title": "1 x HEMNES",
                            "description": "TV bench",
                            "articleNo": "104.135.28",
                            "productId": "10413528",
                            "itemLocation": "CONTACT STAFF"
                        }
                    ]
                }
            ]
        }
    ]

    ikea_product_instock = [
        {
            "productId": "10413528",
            "productType": "ART",
            "storeId": "372",
            "salePoint": "SELF_SERVICE",
            "productLocation": "SELF-SERVICE",
            "status": {
                "code": "HIGH_IN_STOCK",
                "htmlText": "<b>In stock</b> at Vaughan",
                "label": "In stock",
                "description": "There are <b>8</b> in stock at Vaughan",
                "colour": "#0A8A00",
                "timestamp": ""
            },
            "locations": [
                {
                    "heading": "Can be found in the <b>self-serve</b> area",
                    "items": [
                        {
                            "title": "1 x HEMNES",
                            "description": "TV bench",
                            "articleNo": "104.135.28",
                            "productId": "10413528",
                            "itemLocation": "SELF-SERVICE",
                            "shelfOrRack": {
                                "aisle": "19",
                                "bin": "11"
                            }
                        }
                    ]
                }
            ]
        }
    ]

    ikea_product = random.choice([ikea_product_contact_staff[0], ikea_product_instock[0]])

    return ikea_product


@pytest.fixture
def api_costco_item():
    return load_json('tests/jsons/costco.json')


@pytest.fixture
def api_lenovo_items():
    data = load_json('tests/jsons/lenovo.json')
        
    return data
