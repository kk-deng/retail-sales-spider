import pytest
from spiders.spider_man import RfdTopic
from spiders.bestbuy_spider import BestBuyItem

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
    