from datetime import datetime
from spiders.spider_man import RfdSpider
import telegram
import pytest

def test_votes(api_topic):
    assert type(api_topic.upvotes) is int

def test_views(api_topic):
    assert api_topic.total_views == 32290
    assert api_topic.total_replies == 213

def test_topic_link(api_topic):
    topic_title_link = api_topic.topic_title_link
    print(topic_title_link)
    assert type(topic_title_link) is str

def test_topic_post_time(api_topic):
    assert type(api_topic.post_time) is datetime
    assert api_topic.post_time_str == "12-16 17:05:26"
    assert api_topic.last_post_time == datetime(2022,1,3,15,53,40)

def test_offer(api_topic):
    assert type(api_topic.dealer_name) is str
    assert api_topic.offer_price == '42.50'
    assert "https://" in api_topic.offer_url
    assert api_topic.offer_expires_at == None

def test_matched_keywords(api_topic):
    assert any(api_topic.watchlist_bool) == True
    assert api_topic.matched_keywords == 'fido'

@pytest.mark.rfd
def test_rfd_spider_send_text_msg(api_topic):
    spider = RfdSpider()

    assert type(spider.send_text_msg(api_topic)) is telegram.Message

def test_rfd_topic_cls_str(api_topic):
    msg_content = str(api_topic)
    assert '*Hot*' in msg_content
    assert 'Reply|Views' in msg_content
