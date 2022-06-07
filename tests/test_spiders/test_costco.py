from datetime import datetime
from spiders.costco_spider import CostcoSpider, CostcoItem
# import telegram
import pytest

def test_costco_item(api_costco_item):
    item = CostcoItem(**api_costco_item)

    assert type(item.itemNumber) is str
    assert type(item.availableForSale) is bool
