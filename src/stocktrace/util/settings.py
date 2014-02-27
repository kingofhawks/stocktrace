'''
Created on 2012-9-19

@author: Simon
'''
YAHOO = "yahoo"
CSV_ENGINE = "csv"
STOCK_LIST_ALL='stock_list_all'
STOCK_LIST_HOLD='stock_list_hold'
STOCK_LIST_TOP100='stock_list_top100'
STOCK_LIST_SELF_SELECTION='stock_list_self_selection'
ALL_LIST = [STOCK_LIST_ALL,STOCK_LIST_HOLD,STOCK_LIST_SELF_SELECTION,STOCK_LIST_TOP100]
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
PAGING_TOTAL = 10000

#redis
REDIS_SERVER = '192.168.192.128'
INDUSTRY_SET = 'industry'

APP_ROOT = 'G:\Dropbox\Workspace\stocktrace'
