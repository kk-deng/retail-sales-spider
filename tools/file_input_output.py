import json
import csv
# from fake_useragent import UserAgent
import random
import re


class FileReadWrite:
    def __init__(self):
        self.settings_path = 'resources\settings.json'
        self.deal_csv_path = 'resources\deal.csv'
        self.watchlist_csv_path = 'resources\watchlist.csv'
        self.token = self.__import_keys['token']
        self.chat_id = self.__import_keys['chat_id']
        self.channel_id = self.__import_keys['channel_id']
        self.MONGO_IP = self.__import_keys["MONGO_IP"]
        self.MONGO_DB = self.__import_keys["MONGO_DB"]
        self.MONGO_USER_NAME = self.__import_keys["MONGO_USER_NAME"]
        self.MONGO_USER_PASS = self.__import_keys["MONGO_USER_PASS"]
        self.mongodb_url = self.__import_keys['mongodb_url']
        self.bby_cookies = self.__import_keys['bby_cookies']
        # self.ua = UserAgent(verify_ssl=False)
    
    @property
    def __import_keys(self):
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

    # @staticmethod
    # def grp(pat, txt):
    #     r = re.search(pat, txt)
    #     return r.group(0) if r else '&'

    @property
    def create_random_header(self):
        # browsers = {
        #     'chrome': r'Chrome/[^ ]+',
        #     'safari': r'AppleWebKit/[^ ]+',
        #     'opera': r'Opera\s.+$',
        #     'firefox': r'Firefox/.+$',
        #     'internetexplorer': r'Trident/[^;]+',
        # }
        # browser = random.choice(self.ua.data_randomize)
        # user_agent = sorted(self.ua.data_browsers[browser], key=lambda a: self.grp(browsers[browser], a))[-1]
        # # user_agent = self.ua.random
        with open('resources/user_agent.json') as s:
            ua_list = json.load(s)
            # Get a random index within the json list length
            random_ua = random.choice(ua_list)['useragent']
            ua_list = {"rfd": {"user-agent": random_ua},
                        "costco": {
                            "accept": "pplication/json, text/javascript, */*; q=0.01",
                            "accept-encoding": 'gzip, deflate, br',
                            "accept-language": 'zh-CN,zh;q=0.9,en-CA;q=0.8,en;q=0.7',
                            "user-agent": random_ua,
                            'referer': 'https://www.costco.ca/'},
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
                        }
            }
        return ua_list
        # 'https://www.costco.ca/.product.5203665.html'
        # headers={
        #     'authority': 'www.costco.ca',
        #     'path': '/.product.5203665.html',
        #     'headers': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        #     'referer': 'https://www.costco.ca/playstation-5-console-bundle.product.100696941.html'}
