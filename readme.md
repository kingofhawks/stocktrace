pip install -r requirements.txt  
mongodb 3.6  
mongodb backup:  
mongodump  --db stocktrace  
mongodb restore:  
mongorestore --collection industry --db stocktrace dump/stocktrace/industry.bson  

http://localhost:8000

stocktrace will parse finance data from famous finance web sites and generate some useful report

* Parse stock data, both real time and history data from xueqiu/shenwan/Sina/Yahoo(csv or YDN)/ifeng etc
* Market Analysis based on PB/PE/GDP/turnover/AH from csindex/SW index/AH index etc  
* Screen stocks based on 52 week's high or low percentage
* NHNL index  
* Generate OHLC chart

How to run tests

1. run module

> python manage.py test market.tests.ParseTestCase.test_sw_history

2. run test method

> python manage.py test test.yahoo_test.TestSequenceFunctions.test_print_stock


xueqiu.com API token:

> Login xueqiu.com check HTTP request Cookie "xq_a_token"


Upgrade from python2 to 3  
$2to3 -w analysis.py  
https://docs.python.org/3/howto/pyporting.html  
https://docs.python.org/3/library/2to3.html  
http://python-future.org/  

### Reference

[xueqiu](www.xueqiu.com)

[robinhood](https://www.robinhood.com/)

[tradehero](http://www.tradehero.mobi/)

[pandas to parse Excel](http://pbpython.com/excel-pandas-comp.html)





