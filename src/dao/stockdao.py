'''
Created on 2011-3-7

@author: simon
'''
def insertStock():
    import pymongo
    from pymongo import Connection
    connection = Connection()
    db = connection.test_database
    collection = db.test_collection
    import datetime
    post = {"author": "Mike",
            "text": "My first blog post!",
            "tags": ["mongodb", "python", "pymongo"],
            "date": datetime.datetime.utcnow()}
    posts = db.posts
    posts.insert(post)
    posts.find_one()
    posts.find_one({"author": "Mike"})
    for post in posts.find():
        print post
        
def saveStock(stock):
    from pymongo import Connection
    connection = Connection()
    db = connection.stock
    data = {"code": stock.code,
            "high": stock.high,
            "low": stock.low,
            "open": stock.openPrice,
            "close": stock.close,
            "volume": stock.volume,
            "date": stock.date}
    historyDatas = db.stock_history
    historyDatas.insert(data)
        
def findAllStocks():
    from pymongo import Connection
    connection = Connection()
    db = connection.stock
    historyDatas = db.stock_history
    for stock in historyDatas.find():
        print stock   
        
def findLastUpdate(code):
    print "To find latest update****"+code
    from pymongo import Connection
    connection = Connection()
    db = connection.stock
    historyDatas = db.stock_history
    return historyDatas.find_one({"code": code}).sort({"date":1});
    
def findStockByDate(code,date):
    from pymongo import Connection
    connection = Connection()
    db = connection.stock
    historyDatas = db.stock_history
    return historyDatas.find({"code":code,"date" : {"$gt":date}});
    
    
if __name__ == '__main__':
    from stock import Stock
    stock = Stock('600880')
#    saveStock(stock)
#    print findLastUpdate('600890')
    stocks = findStockByDate('600890','2012-03-01')
    for stock in stocks:
        print stock
