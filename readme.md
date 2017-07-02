pip install -r requirements.txt  
Revision History

2016/1/15--v0.4
1. use tushare to parse finance data

2013/02/05--v0.3

1.screen by Yahoo and support category

2012/09/18--v0.2

1.add django view /zytj/candle

2012/09/11--v0.1

1.Parse history data from Yahoo CSV API

2.Support NHNL screener

http://localhost:8000/zytj/alist


stocktrace will parse finance data from famous finance web sites and generate some useful report

* Parse stock data, both real time and history data from xueqiu/shenwan/Sina/Yahoo(csv or YDN)/ifeng/Google/reuters etc

* Market Analysis based on PB/PE/GDP/turnover/AH etc

* Screen stocks based on 52 week's high or low percentage

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





