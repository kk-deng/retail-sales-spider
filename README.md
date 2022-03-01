# Bestbuy & RFD Deals Spider

A web-scraping based on `feapder` web spider framework (A `scrapy`-like framework) which can collect sales data from **Bestbuy** and **IKEA.ca** website and send telegram messages when stocks of products change. It includes the following features:

* All scraped data will be loaded in real-time to an online cloud database _MongoDB Atlas_ or a local Database with _MongoDB Compass_ for future sales analysis.

  *Note: Walmart.ca removed the stock number of products in Dec 2021, so it is not considered for the future support.*

* It can also web scrape trending deals from **Redflagdeals** forum and alert users through telegram bot channels with multiple conditions, including trending index (e.g. upvotes per minute), keywords list (csv file input), and overall upvotes, etc.

* Scraping behaviours can be customized by setting random time gaps, dynamic scraping frequency, and targeted products.

## Featured Modules
Each spider class scrapes data for one website/app.
They can be triggered and run asynchronously in the main.py.
Module logics can be found in the `def parse(self, request, response)` method in each class.

* [Bestbuy Spider Class][https://github.com/kk-deng/retail-sales-spider/blob/main/spiders/bestbuy_spider.py]
* [IKEA.ca Spider Class][https://github.com/kk-deng/retail-sales-spider/blob/main/spiders/ikea_spider.py]
* [Redflagdeals Spider Class][https://github.com/kk-deng/retail-sales-spider/blob/main/spiders/spider_man.py]

## Unit Test Codes - PyTest

* [PyTest Fixtures][https://github.com/kk-deng/retail-sales-spider/blob/main/tests/conftest.py]
  * [Bestbuy Unit Test][https://github.com/kk-deng/retail-sales-spider/blob/main/tests/test_spiders/test_bestbuy.py]
  * [IKEA.ca Unit Test][https://github.com/kk-deng/retail-sales-spider/blob/main/tests/test_spiders/test_ikea.py]
  * [Redflagdeals Unit Test][https://github.com/kk-deng/retail-sales-spider/blob/main/tests/test_spiders/test_rfdtopic.py]

## Usage

Create a `settings.json` file under `/resources` folder with the following information:

*Note: The rfd_api was hidden because it is reverse engineered. To protect it from being potentially abused, it is not shown here.*

```json
{
    "rfd_api":  <hidden>,
    "rfd_api_params":   {
        "forum_id": "9",
        "page": "1",
        "per_page": "30",
        "sort_field": "last_post_date",
        "sort_direction": "desc",
        "topic_type": "both",
        "return_attachments": "false"
    },
    "token": <telegram_bot_token_for_rfd>,
    "newbot_token": <telegram_bot_token_2_for_bestbuy>,
    "chat_id": <your_telegram_account_chat_id>,
    "channel_id": <your_telegram_channel_id>, 
    "MONGO_IP": <your_mongoDB_uri|mongoDB_Atlas_link>,
    "MONGO_DB": <mongoDB_database_name>,
    "MONGO_USER_NAME": <mongoDB_username>,
    "MONGO_USER_PASS": <mongoDB_password>
}
```
