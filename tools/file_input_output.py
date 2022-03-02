import json
import csv
# from fake_useragent import UserAgent
import random
import re


class FileReadWrite:
    def __init__(self):
        self.settings_path = r'resources\settings.json'
        self.deal_csv_path = r'resources\deal.csv'
        self.watchlist_csv_path = r'resources\watchlist.csv'
        self.rfd_api = self._import_keys.get('rfd_api')
        self.rfd_api_params = self._import_keys.get('rfd_api_params')
        self.ikea_api = self._import_keys.get('ikea_api')
        self.token = self._import_keys.get('token')
        self.newbot_token = self._import_keys.get('newbot_token')
        self.chat_id = self._import_keys.get('chat_id')
        self.channel_id = self._import_keys.get('channel_id')
        self.MONGO_IP = self._import_keys.get("MONGO_IP")
        self.MONGO_DB = self._import_keys.get("MONGO_DB")
        self.MONGO_USER_NAME = self._import_keys.get("MONGO_USER_NAME")
        self.MONGO_USER_PASS = self._import_keys.get("MONGO_USER_PASS")
        self.mongodb_url = self._import_keys.get('mongodb_url')
        self.bby_cookies = self._import_keys.get('bby_cookies')
        # self.ua = UserAgent(verify_ssl=False)
    
    @property
    def _import_keys(self):
        with open(self.settings_path) as s:
            return json.load(s)

    def write_to_csv(self, deal_dict):
        with open(self.deal_csv_path, mode='w', newline='', encoding='utf-8') as csv_file:
            fieldnames = ['thread_id', 
                        'upvotes', 
                        'upvotes_per_min', 
                        'elapsed_mins', 
                        'retailer_name', 
                        'topic_title', 
                        'first_post_time_obj', 
                        'first_post_time', 
                        'reply_count', 
                        'view_count', 
                        'msg_sent_cnt',
                        'topic_link']
                        
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            for key, value_dict in deal_dict.items():
                collector = {'thread_id': key}
                collector.update(value_dict)
                writer.writerow(collector)
    
    @property
    def thread_csv(self):
        try:
            with open(self.deal_csv_path, mode='r', encoding='utf-8') as infile:
                reader = csv.reader(infile)
                next(reader)
                mydict = {rows[0]: {'upvotes':          rows[1],
                                    'upvotes_per_min':  rows[2], 
                                    'elapsed_mins':     rows[3], 
                                    'retailer_name':    rows[4],
                                    'topic_title':      rows[5], 
                                    'first_post_time_obj':  rows[6], 
                                    'first_post_time':  rows[7], 
                                    'reply_count':      rows[8],
                                    'view_count':       rows[9],
                                    'msg_sent_cnt':     int(rows[10]),
                                    'topic_link':       rows[11]} for rows in reader}
                return mydict
        except:
            return {}
    
    @property
    def watchlist_csv(self):
        try:
            with open(self.watchlist_csv_path, mode='r') as infile:
                reader = csv.reader(infile)
                watchlist = [row[0].lower() for row in reader]
                return watchlist
        except:
            return []

    def get_spider_header(self, website: str) -> dict:
        with open('resources/user_agent.json') as s:
            ua_loaded_file = json.load(s)
            # Get a random index within the json list length
            random_ua = random.choice(ua_loaded_file)['useragent']
            ua_list = {
                "rfd": {
                    "Host": "forums.redflagdeals.com",
                    "API-Key-Version": "1",
                    "API-Version": "1.0",
                    "Accept": "*/*",
                    "User-Agent": "RedFlagDeals/6063 CFNetwork/1209 Darwin/20.2.0",
                    "Accept-Language": "en-ca",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Connection": "keep-alive"
                },
                "costco": {
                    "accept": "pplication/json, text/javascript, */*; q=0.01",
                    "accept-encoding": 'gzip, deflate, br',
                    "accept-language": 'zh-CN,zh;q=0.9,en-CA;q=0.8,en;q=0.7',
                    "user-agent": random_ua,
                    'referer': 'https://www.costco.ca/'
                },
                "bestbuy": {
                    "user-agent": random_ua,
                    "referer": 'https://www.bestbuy.ca/en-ca/product/playstation-5-console/15689336',
                    "dnt": '1',
                    "accept-language": 'zh-CN,zh;q=0.9,en-CA;q=0.8,en;q=0.7',
                    'authority': 'www.bestbuy.ca',
                    'pragma': 'no-cache',
                    'cache-control': 'no-cache',
                    'accept': '*/*',
                    'sec-fetch-site': 'same-origin',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-dest': 'empty',
                    "Cookie": self.bby_cookies,
                },
                "ikea": {
                    "Host": "shop.api.ingka.ikea.com",
                    "Content-Type": "application/json",
                    "Connection": "keep-alive",
                    "IOS-Build-Nr": "4660",
                    "Contract": "40663",
                    "Accept": "application/json",
                    "User-Agent": "IKEA App/3.8.2-4660 (iOS)",
                    "Consumer": "IKEAAPPI",
                    "Accept-Language": "en-ca",
                    "Accept-Encoding": "gzip, deflate, br"
                }
            }
            
        return ua_list[website]
