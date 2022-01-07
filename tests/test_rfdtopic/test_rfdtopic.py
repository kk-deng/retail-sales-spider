from datetime import datetime


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