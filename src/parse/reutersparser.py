'''
Created on 2011-3-7

@author: simon
'''
import sys, traceback
from datetime import date
from datetime import datetime
from datetime import timedelta
from stock import Stock
from lxml import etree
from lxml.html import parse
from dao.stockdao import *
from lxml import etree
from lxml.html import parse
import io    
from urllib2 import urlopen
    
#parse stock statistics data from reuters finance
def parseKeyStatData(code):        
    url ='http://cn.reuters.com/investing/quotes/quote?symbol='+str(code)+".SS"  
    page = parse(url).getroot()
    result = etree.tostring(page)
#    print result
    r = page.xpath('//div[@class="primaryContent2"]');
    #print 'div length'+str(len(r))
    statisticsDiv= etree.ElementTree(r[1])  
    #print etree.tostring(statisticsDiv)
    valuations = statisticsDiv.xpath('//td[@class="data"]/text()');
    #print 'td length'+str(len(valuations))
    #print valuations
    ttmPe = valuations[0]
    ps = valuations[1]
    mrqPb = valuations[2]
    
    content1 = page.xpath('//div[@class="primaryContent1"]');
    financialDiv = etree.ElementTree(content1[2])
    financialDatas = financialDiv.xpath('//td[@class="data"]/text()');
    #print financialDatas
    epsTtm = financialDatas[0].encode('utf-8').decode("ascii", "ignore")
    bookingValue = financialDatas[2].encode('utf-8').decode("ascii", "ignore")
    #print epsTtm+bookingValue
   
    updateTickerWithKeyStats(str(code),float(epsTtm),float(bookingValue))

                    
if __name__ == '__main__':
#    stocks = ['600327','600739','600573','600583','600718','600827','601111','601866','600880']
    parseKeyStatData('600327')
#    stocks = findAllExistentTickers()
#    for stock in stocks:
#       parseKeyStatData(stock)
#    for stock in stocks:
#        getHistorialData(stock)
#    getHistorialData('600383',True,'2011-01-01')