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
def api_ikea_products_by_store():
    products_by_store = [
        {
            "productId": "30412165",
            "productType": "ART",
            "storeId": "372",
            "salePoint": "CONTACT_STAFF",
            "productLocation": "CONTACT STAFF",
            "status": {
                "code": "OUT_OF_STOCK",
                "htmlText": "Out of stock at <b>Vaughan</b>",
                "label": "Out of stock",
                "description": "There are <b>0</b> in stock at Vaughan",
                "colour": "#E00751",
                "timestamp": ""
            },
            "locations": []
        },
        {
            "productId": "60363597",
            "productType": "ART",
            "storeId": "372",
            "salePoint": "CONTACT_STAFF",
            "productLocation": "CONTACT STAFF",
            "status": {
                "code": "OUT_OF_STOCK",
                "htmlText": "Out of stock at <b>Vaughan</b>",
                "label": "Out of stock",
                "description": "There are <b>0</b> in stock at Vaughan",
                "colour": "#E00751",
                "timestamp": ""
            },
            "locations": []
        },
        {
            "productId": "90289172",
            "productType": "ART",
            "storeId": "372",
            "salePoint": "SELF_SERVICE",
            "productLocation": "SELF-SERVICE",
            "status": {
                "code": "OUT_OF_STOCK",
                "htmlText": "Out of stock at <b>Vaughan</b>",
                "label": "Out of stock",
                "description": "Estimated back in stock: <b>2022-02-13</b>",
                "colour": "#E00751",
                "timestamp": ""
            },
            "locations": []
        },
        {
            "productId": "79009502",
            "productType": "SPR",
            "storeId": "372",
            "salePoint": "SELF_SERVICE",
            "productLocation": "SELF-SERVICE",
            "status": {
                "code": "LOW_IN_STOCK",
                "htmlText": "Running low at <b>Vaughan</b>",
                "label": "Running low",
                "description": "There are <b>1</b> in stock at Vaughan",
                "colour": "#FFA524",
                "timestamp": ""
            },
            "locations": [
                {
                    "heading": "Can be found in the <b>self-serve</b> area",
                    "items": [
                        {
                            "title": "1 x MALM",
                            "description": "bed frame, high",
                            "articleNo": "702.494.84",
                            "productId": "70249484",
                            "itemLocation": "SELF-SERVICE",
                            "shelfOrRack": {
                                "aisle": "04",
                                "bin": "02"
                            }
                        },
                        {
                            "title": "1 x SKORVA",
                            "description": "center support beam",
                            "articleNo": "901.245.34",
                            "productId": "90124534",
                            "itemLocation": "SELF-SERVICE",
                            "shelfOrRack": {
                                "aisle": "04",
                                "bin": "35"
                            }
                        },
                        {
                            "title": "2 x MALM",
                            "description": "underbed storage box for high bed",
                            "articleNo": "602.527.21",
                            "productId": "60252721",
                            "itemLocation": "SELF-SERVICE",
                            "shelfOrRack": {
                                "aisle": "04",
                                "bin": "05"
                            }
                        },
                        {
                            "title": "1 x LURÖY",
                            "description": "slatted bed base",
                            "articleNo": "001.602.15",
                            "productId": "00160215",
                            "itemLocation": "SELF-SERVICE",
                            "shelfOrRack": {
                                "aisle": "04",
                                "bin": "36"
                            }
                        }
                    ]
                }
            ]
        },
        {
            "productId": "70404818",
            "productType": "ART",
            "storeId": "372",
            "salePoint": "CONTACT_STAFF",
            "productLocation": "CONTACT STAFF",
            "status": {
                "code": "OUT_OF_STOCK",
                "htmlText": "Out of stock at <b>Vaughan</b>",
                "label": "Out of stock",
                "description": "There are <b>0</b> in stock at Vaughan",
                "colour": "#E00751",
                "timestamp": ""
            },
            "locations": []
        },
        {
            "productId": "40444255",
            "productType": "ART",
            "storeId": "372",
            "salePoint": "SELF_SERVICE",
            "productLocation": "SELF-SERVICE",
            "status": {
                "code": "OUT_OF_STOCK",
                "htmlText": "Out of stock at <b>Vaughan</b>",
                "label": "Out of stock",
                "description": "There are <b>0</b> in stock at Vaughan",
                "colour": "#E00751",
                "timestamp": ""
            },
            "locations": []
        },
        {
            "productId": "50474341",
            "productType": "ART",
            "storeId": "372",
            "salePoint": "SELF_SERVICE",
            "productLocation": "SELF-SERVICE",
            "status": {
                "code": "OUT_OF_STOCK",
                "htmlText": "Out of stock at <b>Vaughan</b>",
                "label": "Out of stock",
                "description": "Estimated back in stock: <b>2022-01-24</b>",
                "colour": "#E00751",
                "timestamp": ""
            },
            "locations": []
        },
        {
            "productId": "99000483",
            "productType": "SPR",
            "storeId": "372",
            "salePoint": "SELF_SERVICE",
            "productLocation": "SELF-SERVICE",
            "status": {
                "code": "MEDIUM_IN_STOCK",
                "htmlText": "<b>In stock</b> at Vaughan",
                "label": "In stock",
                "description": "There are <b>5</b> in stock at Vaughan",
                "colour": "#FFA524",
                "timestamp": ""
            },
            "locations": [
                {
                    "heading": "Can be found in the <b>self-serve</b> area",
                    "items": [
                        {
                            "title": "1 x TÄRENDÖ",
                            "description": "tabletop",
                            "articleNo": "302.422.91",
                            "productId": "30242291",
                            "itemLocation": "SELF-SERVICE",
                            "shelfOrRack": {
                                "aisle": "29",
                                "bin": "11"
                            }
                        },
                        {
                            "title": "1 x TÄRENDÖ",
                            "description": "underframe",
                            "articleNo": "702.450.42",
                            "productId": "70245042",
                            "itemLocation": "SELF-SERVICE",
                            "shelfOrRack": {
                                "aisle": "29",
                                "bin": "12"
                            }
                        }
                    ]
                }
            ]
        },
        {
            "productId": "00196101",
            "productType": "ART",
            "storeId": "372",
            "salePoint": "OTHER",
            "productLocation": "Home Organisation",
            "status": {
                "code": "HIGH_IN_STOCK",
                "htmlText": "<b>In stock</b> at Vaughan",
                "label": "In stock",
                "description": "There are <b>229</b> in stock at Vaughan",
                "colour": "#0A8A00",
                "timestamp": ""
            },
            "locations": [
                {
                    "heading": "Can be found in <b>Home Organisation</b>",
                    "items": [
                        {
                            "title": "1 x FIXA",
                            "description": "screwdriver/drill, lithium-ion",
                            "articleNo": "001.961.01",
                            "productId": "00196101",
                            "itemLocation": "Home Organisation"
                        }
                    ]
                }
            ]
        },
        {
            "productId": "80361564",
            "productType": "ART",
            "storeId": "372",
            "salePoint": "SELF_SERVICE",
            "productLocation": "SELF-SERVICE",
            "status": {
                "code": "OUT_OF_STOCK",
                "htmlText": "Out of stock at <b>Vaughan</b>",
                "label": "Out of stock",
                "description": "There are <b>0</b> in stock at Vaughan",
                "colour": "#E00751",
                "timestamp": ""
            },
            "locations": []
        },
        {
            "productId": "20206806",
            "productType": "ART",
            "storeId": "372",
            "salePoint": "CONTACT_STAFF",
            "productLocation": "CONTACT STAFF",
            "status": {
                "code": "HIGH_IN_STOCK",
                "htmlText": "<b>In stock</b> at Vaughan",
                "label": "In stock",
                "description": "There are <b>2</b> in stock at Vaughan",
                "colour": "#0A8A00",
                "timestamp": ""
            },
            "locations": [
                {
                    "heading": "<b>Contact staff</b>",
                    "items": [
                        {
                            "title": "1 x IKEA PS 2012",
                            "description": "drop-leaf table",
                            "articleNo": "202.068.06",
                            "productId": "20206806",
                            "itemLocation": "CONTACT STAFF"
                        }
                    ]
                }
            ]
        },
        {
            "productId": "30473154",
            "productType": "ART",
            "storeId": "372",
            "salePoint": "SELF_SERVICE",
            "productLocation": "SELF-SERVICE",
            "status": {
                "code": "OUT_OF_STOCK",
                "htmlText": "Out of stock at <b>Vaughan</b>",
                "label": "Out of stock",
                "description": "There are <b>0</b> in stock at Vaughan",
                "colour": "#E00751",
                "timestamp": ""
            },
            "locations": []
        },
        {
            "productId": "44881100",
            "productType": "ART",
            "storeId": "372",
            "salePoint": "SELF_SERVICE",
            "productLocation": "SELF-SERVICE",
            "status": {
                "code": "OUT_OF_STOCK",
                "htmlText": "Out of stock at <b>Vaughan</b>",
                "label": "Out of stock",
                "description": "Estimated back in stock: <b>2022-01-22</b>",
                "colour": "#E00751",
                "timestamp": ""
            },
            "locations": []
        },
        {
            "productId": "00278578",
            "productType": "ART",
            "storeId": "372",
            "salePoint": "SELF_SERVICE",
            "productLocation": "SELF-SERVICE",
            "status": {
                "code": "HIGH_IN_STOCK",
                "htmlText": "<b>In stock</b> at Vaughan",
                "label": "In stock",
                "description": "There are <b>66</b> in stock at Vaughan",
                "colour": "#0A8A00",
                "timestamp": ""
            },
            "locations": [
                {
                    "heading": "Can be found in the <b>self-serve</b> area",
                    "items": [
                        {
                            "title": "1 x HYLLIS",
                            "description": "shelf unit",
                            "articleNo": "002.785.78",
                            "productId": "00278578",
                            "itemLocation": "SELF-SERVICE",
                            "shelfOrRack": {
                                "aisle": "37",
                                "bin": "20"
                            }
                        }
                    ]
                }
            ]
        },
        {
            "productId": "30428326",
            "productType": "ART",
            "storeId": "372",
            "salePoint": "SELF_SERVICE",
            "productLocation": "SELF-SERVICE",
            "status": {
                "code": "HIGH_IN_STOCK",
                "htmlText": "<b>In stock</b> at Vaughan",
                "label": "In stock",
                "description": "There are <b>205</b> in stock at Vaughan",
                "colour": "#0A8A00",
                "timestamp": ""
            },
            "locations": [
                {
                    "heading": "Can be found in the <b>self-serve</b> area",
                    "items": [
                        {
                            "title": "1 x HYLLIS",
                            "description": "shelf unit",
                            "articleNo": "304.283.26",
                            "productId": "30428326",
                            "itemLocation": "SELF-SERVICE",
                            "shelfOrRack": {
                                "aisle": "35",
                                "bin": "21"
                            }
                        }
                    ]
                }
            ]
        },
        {
            "productId": "99291745",
            "productType": "SPR",
            "storeId": "372",
            "salePoint": "CONTACT_STAFF",
            "productLocation": "SELF-SERVICE",
            "status": {
                "code": "OUT_OF_STOCK",
                "htmlText": "Out of stock at <b>Vaughan</b>",
                "label": "Out of stock",
                "description": "There are <b>0</b> in stock at Vaughan",
                "colour": "#E00751",
                "timestamp": ""
            },
            "locations": []
        },
        {
            "productId": "40201916",
            "productType": "ART",
            "storeId": "372",
            "salePoint": "CONTACT_STAFF",
            "productLocation": "CONTACT STAFF",
            "status": {
                "code": "OUT_OF_STOCK",
                "htmlText": "Out of stock at <b>Vaughan</b>",
                "label": "Out of stock",
                "description": "There are <b>0</b> in stock at Vaughan",
                "colour": "#E00751",
                "timestamp": ""
            },
            "locations": []
        },
        {
            "productId": "70294339",
            "productType": "ART",
            "storeId": "372",
            "salePoint": "CONTACT_STAFF",
            "productLocation": "CONTACT STAFF",
            "status": {
                "code": "OUT_OF_STOCK",
                "htmlText": "Out of stock at <b>Vaughan</b>",
                "label": "Out of stock",
                "description": "Estimated back in stock: <b>2022-01-21</b>",
                "colour": "#E00751",
                "timestamp": ""
            },
            "locations": []
        }
    ]

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