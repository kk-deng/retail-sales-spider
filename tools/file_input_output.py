import json
import csv
from fake_useragent import UserAgent


class FileReadWrite:
    def __init__(self, settings_path, deal_csv_path, watchlist_csv_path):
        self.settings_path = settings_path
        self.deal_csv_path = deal_csv_path
        self.watchlist_csv_path = watchlist_csv_path
        self.token = self.__import_keys['token']
        self.chat_id = self.__import_keys['chat_id']
        self.ua = UserAgent()
    
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

    @property
    def create_random_header(self):
        user_agent = self.ua.random
        return {"user-agent": str(user_agent),
            'referer': 'https://forums.redflagdeals.com/hot-deals-f9/?sk=tt&rfd_sk=tt&sd=d'}

