# Bestbuy & RFD Deals Spider

A web-scraping based on `feapder` web spider framework (A `scrapy`-like framework) which can collect sales data from Bestbuy website and send telegram messages when stocks of products change.

For all new scraped items/products, this spider will store in a cloud database service, e.g. MongoDB Atlas.

## Usage

Create a `settings.json` file under `/resources` folder with the following information:
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
