from datetime import datetime
from spiders.lenovo_spider import Z16Model
# import telegram
import pytest


def test_z16_model_cls(api_lenovo_items):
    mock_response = api_lenovo_items['data']['data'][4]
    item = Z16Model(**mock_response)

    assert item.productCode == '21D4000HUS'
    assert item.finalPrice == "3587.35"
