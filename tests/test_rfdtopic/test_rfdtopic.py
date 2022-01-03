from datetime import datetime


def test_topic_link(api_topic):
    topic_title_link = api_topic.topic_title_link
    print(topic_title_link)
    assert type(topic_title_link) is str

def test_topic_post_time(api_topic):
    assert type(api_topic.post_time) is datetime
    assert api_topic.post_time_str == "12-16 17:05:26"
