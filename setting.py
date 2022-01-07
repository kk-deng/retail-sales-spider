# -*- coding: utf-8 -*-

import os
# import sys
from tools import *
file_operator = file_input_output.FileReadWrite()
#
# # MYSQL
# MYSQL_IP = "localhost"
# MYSQL_PORT = 3306
# MYSQL_DB = ""
# MYSQL_USER_NAME = ""
# MYSQL_USER_PASS = ""
#
# # MONGODB
# MONGO_IP = "localhost"
# MONGO_PORT = 27017
# MONGO_DB = "feapder"
# MONGO_USER_NAME = ""
# MONGO_USER_PASS = ""
MONGO_IP = file_operator.MONGO_IP  #"localhost"
MONGO_PORT = 27017
MONGO_DB = "feapder"
MONGO_USER_NAME = file_operator.MONGO_USER_NAME
MONGO_USER_PASS = file_operator.MONGO_USER_PASS

ITEM_PIPELINES = [
    "feapder.pipelines.mongo_pipeline.MongoPipeline",
]

# # COLLECTOR
# COLLECTOR_SLEEP_TIME = 1  
# COLLECTOR_TASK_COUNT = 10 

# # SPIDER
SPIDER_THREAD_COUNT = 2  
# SPIDER_SLEEP_TIME = [50, 60]  
# SPIDER_TASK_COUNT = 1 
SPIDER_MAX_RETRY_TIMES = 3  
KEEP_ALIVE = True  

# RETRY_FAILED_REQUESTS = False
# SAVE_FAILED_REQUEST = True
# REQUEST_LOST_TIMEOUT = 600

REQUEST_TIMEOUT = 30

# RESPONSE_CACHED_ENABLE = False
# RESPONSE_CACHED_EXPIRE_TIME = 3600
# RESPONSE_CACHED_USED = False

RANDOM_HEADERS = False

# USER_AGENT_TYPE = "chrome"
DEFAULT_USERAGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"

# USE_SESSION = False

# EMAIL_SENDER = "" 
# EMAIL_PASSWORD = "" 
# EMAIL_RECEIVER = "" 
# EMAIL_SMTPSERVER = "smtp.163.com" 

# WARNING_INTERVAL = 3600 
# WARNING_LEVEL = "DEBUG" 
# WARNING_FAILED_COUNT = 1000
#
LOG_NAME = os.path.basename(os.getcwd())
LOG_PATH = "log/%s.log" % LOG_NAME 
LOG_LEVEL = "INFO"
# LOG_COLOR = True 
# LOG_IS_WRITE_TO_CONSOLE = True 
LOG_IS_WRITE_TO_FILE = True
# LOG_MODE = "w"
# LOG_MAX_BYTES = 10 * 1024 * 1024 
# LOG_BACKUP_COUNT = 20 
# LOG_ENCODING = "utf8" 
# OTHERS_LOG_LEVAL = "ERROR" 

# project_path = os.path.abspath(os.path.dirname(__file__))
# os.chdir(project_path)
# sys.path.insert(0, project_path)
# print(os.getcwd())
