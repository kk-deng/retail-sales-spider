from datetime import datetime
from spiders.costco_spider import CostcoSpider, CostcoItem
# import telegram
import pytest

def test_costco_item_cls(api_costco_item):
    item = CostcoItem(**api_costco_item)

    assert type(item.item_number) is str
    assert type(item.availableForSale) is bool
