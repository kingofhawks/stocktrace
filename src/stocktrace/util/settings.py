'''
Created on 2012-9-19

@author: Simon
'''
YAHOO = "yahoo"
CSV_ENGINE = "csv"
STOCK_LIST_ALL='stock_list_all'
STOCK_LIST='stock_list'
STOCK_LIST_TOP100='stock_list_top100'
STOCK_LIST_SELF_SELECTION='stock_list_self_selection'
DOWNLOAD_KEY_STAT = False
DOWNLOAD_LATEST_PRICE = True
HIGHER = 1
LOWER = 2


#rabbitmq settings
STOCK_ALARMS_TOPIC ='stock_alarms'
RABBIT_SERVER = '172.25.21.16'

#monitoring settings
POLLING_INTERVAL = 180
STATUS_UP = 'UP'
STATUS_WARNING = 'WARNING'
STATUS_CRITICAL = 'CRITICAL'

#paging
PAGING_ITEM = 20
PAGING_TOTAL = 500

#redis
REDIS_SERVER = '172.25.21.85'
INDUSTRY_SET = 'industry'
