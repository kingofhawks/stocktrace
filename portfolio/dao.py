'''
Created on 2011-3-7

@author: simon
'''
from datetime import date
from datetime import timedelta
from datetime import datetime
from stocktrace.stock import Stock
from django.conf import settings
    
#connection = Connection()

#uri = "mongodb://admin:A9Z711brQp__@127.10.39.2:27017/django"
#MongoHQ URL
#uri = "mongodb://kingofhawks:lazio_2000@dharma.mongohq.com:10089/stocktrace"

#MongoLab URL
#uri = "mongodb://kingofhawks:lazio_2000@ds061288.mongolab.com:61288/stocktrace"
#client = MongoClient(uri)

#client = MongoClient('localhost', 27017)
##cache = Cache()
#db = client.stocktrace
#print db
db = settings.DB


def update_stock_price(code,current):
    stocks = db.stock
    return stocks.update({"code":code},
    {"$set":{"current":float(current)}}, upsert=True,safe=True)


def update_stock_amount(code,amount,up_threshold,down_threshold):
    stocks = db.stock
    return stocks.update({"code":code},
    {"$set":{"amount":int(amount),"up_threshold":float(up_threshold),"down_threshold":float(down_threshold)}}, upsert=True,safe=True)


def insert_stock(stock):
    #connection = Connection()
    #db = db.stock
    data = {"code": stock.code,
            "high": stock.high,
            "low": stock.low,
            "open": stock.openPrice,
            "close": stock.close,
            "volume": stock.volume,
            "date": stock.date,
            "amount": stock.amount,
            "current": stock.current}
    stocks = db.stock
    stocks.insert(data)
    #connection.end_request()


#use mongodb array type for tags
def add_tag(code,tag):
    data = {"code": code, "tags": [tag]}
    stocks = db.stock
    return stocks.update({"code":code},
    {"$set":{"tags":[tag]}}, upsert=True,safe=True)


def delete_stock(code):
    stocks = db.stock
    stocks.remove({"code": code})


def find_all_stocks():
    #connection = Connection()
    # #db = connection.stock
    # stocks = db.stock
    # result = []
    # for s in stocks.find():
    #     #print stock
    #     result.append(s)
    # #return stocks.find()
    # return result

    #list() method will convert pymongo cursor to python list
    return list(db.stock.find())

#TODO
def find_stocks_by_tag(tag):
    stocks = db.stock
    return stocks.find({"tags":tag});


def find_stock_by_code(code):
    stocks = db.stock
    return stocks.find_one({"code":code});


#clear all data in system
def clear():
    db.tickers.remove()
    db.non_existent_tickers.remove()
    db.stock_history.remove()


def find_all_portfolio():
    return list(db.portfolio.find({}))


def delete_portfolio_today():
    from datetime import time
    today_min = datetime.combine(date.today(), time.min)
    today_max = datetime.combine(date.today(), time.max)
    db.portfolio.remove({'date': {'$gte': today_min, '$lt': today_max}})
