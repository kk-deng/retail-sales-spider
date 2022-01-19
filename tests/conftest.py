import pytest
from spiders.spider_man import RfdTopic
from spiders.bestbuy_spider import BestBuyItem
import random

@pytest.fixture(autouse=True)
def api_topic():
    info = {
        'topic_id': 2512445, 
        'forum_id': 9, 
        'title': 'Fido Internet 150Mps service for 42.50  (first 12 months)', 
        'slug': 'fido-fido-internet-150mps-service-42-50-first-12-months', 
        'author_id': 21329, 
        'is_subscribed': False, 
        'can_subscribe': False, 
        'can_report': False, 
        'can_reply': False, 
        'is_poll': False, 
        'status': 0, 
        'type': 0, 
        'post_time': '2021-12-16T22:05:26+00:00', 
        'last_post_time': '2022-01-03T20:53:40+00:00', 
        'first_post_id': 35448857, 
        'last_post_id': 35533982, 
        'total_replies': 213, 
        'has_new_post': False, 
        'total_views': 32290, 
        'visibility': 1, 
        'has_replied': False, 
        'attachments': [], 
        'shadow_type': 0, 
        'votes': {
            'total_up': 50, 
            'total_down': 2, 
            'current_vote': 0, 
            'can_vote_up': False, 
            'can_vote_down': False
            }, 
        'prefix': None, 
        'summary': {
            'can_edit': False, 
            'body': ''
        }, 
        'trader_type': None, 
        'web_path': '/fido-fido-internet-150mps-service-42-50-first-12-months-2512445/', 
        'offer': {
            'category_id': 5125, 
            'dealer_id': 158, 
            'dealer_name': 'Fido', 
            'url': 'https://www.fido.ca/internet/packages', 
            'price': '42.50', 
            'savings': '50% off', 
            'expires_at': None, 
            'holiday': 0
        }
    }

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
    availabilities = {
        "availabilities": [
            {
                "pickup": {
                    "status": "OutOfStock",
                    "purchasable": False,
                    "locations": [
                        {
                            "name": "Richmond Hill",
                            "locationKey": "956",
                            "quantityOnHand": 0,
                            "fulfillmentKey": "506",
                            "isReservable": False,
                            "hasInventory": False,
                            "supportsFulfillment": False,
                            "id": None,
                            "fulfillmentPartnerId": None
                        },
                        {
                            "name": "Best Buy Mobile Centrepoint Mall",
                            "locationKey": "237",
                            "quantityOnHand": 0,
                            "fulfillmentKey": "506",
                            "isReservable": False,
                            "hasInventory": False,
                            "supportsFulfillment": False,
                            "id": None,
                            "fulfillmentPartnerId": None
                        },
                        {
                            "name": "Markham",
                            "locationKey": "937",
                            "quantityOnHand": 0,
                            "fulfillmentKey": "506",
                            "isReservable": False,
                            "hasInventory": False,
                            "supportsFulfillment": False,
                            "id": None,
                            "fulfillmentPartnerId": None
                        }
                    ]
                },
                "shipping": {
                    "status": "InStock",
                    "quantityRemaining": 83,
                    "purchasable": True,
                    "levelsOfServices": [
                        {
                            "carrierId": "FEDX",
                            "carrierName": "",
                            "deliveryDate": "2022-01-10T23:59:00Z",
                            "deliveryDateExpiresOn": "2022-01-08T15:00:00Z",
                            "deliveryDatePrecision": "1.00:00:00",
                            "id": "SOP_506-84_0_0_FEDX-GROUND_IR-SC",
                            "name": "",
                            "price": 0
                        }
                    ],
                    "orderLimit": None,
                    "restrictedZoneRegions": [],
                    "hasActiveCountdown": True,
                    "countdownIsZone": False,
                    "preorderInfo": None,
                    "isFreeShippingEligible": True,
                    "isBackorderable": False
                },
                "sku": "14671247",
                "sellerId": "bbyca",
                "saleChannelExclusivity": "InStoreAndOnline",
                "scheduledDelivery": False,
                "isGiftCard": False,
                "isService": False
            }
        ]
    }

    availability = availabilities['availabilities'][0]

    return BestBuyItem(availability)


@pytest.fixture
def api_ikea_products():
    ikea_products = [
        {
            "productId": "10413528",
            "productType": "ART",
            "storeId": "414",
            "salePoint": "SELF_SERVICE",
            "productLocation": "SELF-SERVICE",
            "status": {
                "code": "HIGH_IN_STOCK",
                "htmlText": "<b>In stock</b> at Boucherville",
                "label": "In stock",
                "description": "There are <b>6</b> in stock at Boucherville",
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
                                "aisle": "20",
                                "bin": "28"
                            }
                        }
                    ]
                }
            ]
        },
        {
            "productId": "10413528",
            "productType": "ART",
            "storeId": "040",
            "salePoint": "SELF_SERVICE",
            "productLocation": "SELF-SERVICE",
            "status": {
                "code": "HIGH_IN_STOCK",
                "htmlText": "<b>In stock</b> at Burlington",
                "label": "In stock",
                "description": "There are <b>6</b> in stock at Burlington",
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
                                "aisle": "14",
                                "bin": "19"
                            }
                        }
                    ]
                }
            ]
        },
        {
            "productId": "10413528",
            "productType": "ART",
            "storeId": "216",
            "salePoint": "SELF_SERVICE",
            "productLocation": "SELF-SERVICE",
            "status": {
                "code": "OUT_OF_STOCK",
                "htmlText": "Out of stock at <b>Calgary</b>",
                "label": "Out of stock",
                "description": "Estimated back in stock: <b>2022-03-20</b>",
                "colour": "#E00751",
                "timestamp": ""
            },
            "locations": []
        },
        {
            "productId": "10413528",
            "productType": "ART",
            "storeId": "313",
            "salePoint": "SELF_SERVICE",
            "productLocation": "SELF-SERVICE",
            "status": {
                "code": "LOW_IN_STOCK",
                "htmlText": "Running low at <b>Coquitlam</b>",
                "label": "Running low",
                "description": "There are <b>1</b> in stock at Coquitlam",
                "colour": "#FFA524",
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
                                "aisle": "20",
                                "bin": "43"
                            }
                        }
                    ]
                }
            ]
        },
        {
            "productId": "10413528",
            "productType": "ART",
            "storeId": "349",
            "salePoint": "SELF_SERVICE",
            "productLocation": "SELF-SERVICE",
            "status": {
                "code": "OUT_OF_STOCK",
                "htmlText": "Out of stock at <b>Edmonton</b>",
                "label": "Out of stock",
                "description": "Estimated back in stock: <b>2022-03-21</b>",
                "colour": "#E00751",
                "timestamp": ""
            },
            "locations": []
        },
        {
            "productId": "10413528",
            "productType": "ART",
            "storeId": "256",
            "salePoint": "CONTACT_STAFF",
            "productLocation": "CONTACT STAFF",
            "status": {
                "code": "HIGH_IN_STOCK",
                "htmlText": "<b>In stock</b> at Etobicoke",
                "label": "In stock",
                "description": "There are <b>40</b> in stock at Etobicoke",
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
        },
        {
            "productId": "10413528",
            "productType": "ART",
            "storeId": "529",
            "salePoint": "SELF_SERVICE",
            "productLocation": "SELF-SERVICE",
            "status": {
                "code": "HIGH_IN_STOCK",
                "htmlText": "<b>In stock</b> at Halifax",
                "label": "In stock",
                "description": "There are <b>6</b> in stock at Halifax",
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
                                "aisle": "17",
                                "bin": "18"
                            }
                        }
                    ]
                }
            ]
        },
        {
            "productId": "10413528",
            "productType": "ART",
            "storeId": "039",
            "salePoint": "SELF_SERVICE",
            "productLocation": "SELF-SERVICE",
            "status": {
                "code": "HIGH_IN_STOCK",
                "htmlText": "<b>In stock</b> at Montreal",
                "label": "In stock",
                "description": "There are <b>6</b> in stock at Montreal",
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
                                "aisle": "13",
                                "bin": "15"
                            }
                        }
                    ]
                }
            ]
        },
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
        },
        {
            "productId": "10413528",
            "productType": "ART",
            "storeId": "004",
            "salePoint": "SELF_SERVICE",
            "productLocation": "SELF-SERVICE",
            "status": {
                "code": "HIGH_IN_STOCK",
                "htmlText": "<b>In stock</b> at Ottawa",
                "label": "In stock",
                "description": "There are <b>10</b> in stock at Ottawa",
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
                                "aisle": "09",
                                "bin": "15"
                            }
                        }
                    ]
                }
            ]
        },
        {
            "productId": "10413528",
            "productType": "ART",
            "storeId": "559",
            "salePoint": "SELF_SERVICE",
            "productLocation": "SELF-SERVICE",
            "status": {
                "code": "HIGH_IN_STOCK",
                "htmlText": "<b>In stock</b> at Quebec City",
                "label": "In stock",
                "description": "There are <b>39</b> in stock at Quebec City",
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
                                "aisle": "15",
                                "bin": "14"
                            }
                        }
                    ]
                }
            ]
        },
        {
            "productId": "10413528",
            "productType": "ART",
            "storeId": "003",
            "salePoint": "SELF_SERVICE",
            "productLocation": "SELF-SERVICE",
            "status": {
                "code": "OUT_OF_STOCK",
                "htmlText": "Out of stock at <b>Richmond</b>",
                "label": "Out of stock",
                "description": "Estimated back in stock: <b>2022-03-22</b>",
                "colour": "#E00751",
                "timestamp": ""
            },
            "locations": []
        },
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
        },
        {
            "productId": "10413528",
            "productType": "ART",
            "storeId": "249",
            "salePoint": "SELF_SERVICE",
            "productLocation": "SELF-SERVICE",
            "status": {
                "code": "HIGH_IN_STOCK",
                "htmlText": "<b>In stock</b> at Winnipeg",
                "label": "In stock",
                "description": "There are <b>2</b> in stock at Winnipeg",
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
                                "aisle": "15",
                                "bin": "01"
                            }
                        }
                    ]
                }
            ]
        }
    ]

    ikea_product = random.choice(ikea_products)

    return ikea_product


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