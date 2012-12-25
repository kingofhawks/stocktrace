'''
Created on 2011-3-7

@author: simon
'''

import redis
from stocktrace.util import slf4p
from stocktrace.util import settings

logger = slf4p.getLogger(__name__)
redclient = redis.StrictRedis(host=settings.REDIS_SERVER, port=6379, db=0)
industries = redclient.zrange(settings.INDUSTRY_SET,0,-1)
for industry in industries:
    print industry
    stocks = redclient.lrange(industry,0,-1)
    for stock in stocks:
        print stock

def parseFinanceData(code):
    from lxml import etree
    from lxml.html import parse
    url = 'http://app.finance.ifeng.com/data/stock/cwjk.php?symbol='+code
    print url
    page = parse(url).getroot()
    result = etree.tostring(page)
    #print result
    import io
    with io.open('test.xml','wb') as f:
       #f.writelines(result)
       pass 
    
    r = page.xpath('//div[@class="tab01"]');
    #print len(r)    
    from stocktrace.stock import Stock
    stock = Stock(code)
    for a in r:  
        tree= etree.ElementTree(a)  
        #print etree.tostring(tree) 
        datas = tree.xpath('//td') 
        #print len(datas)
        index =0
        for data in datas:
            dataTree = etree.ElementTree(data);
            #print etree.tostring(dataTree)
            values = dataTree.xpath('//text()')
            index +=1
            #print index
            if (len(values)==1 ):
                #print values
                #print len(values[0])
                #print str(values[0])
                if (index == 32):
                    mgsy = values[0]
                    #print mgsy+'***************'
                    stock.mgsy = mgsy
                elif (index == 52):
                    mgjzc = values[0]
                    #print mgjzc+'***************'
                    stock.mgjzc = mgjzc
                elif (index == 2):
                    last_update = values[0]
                    #print last_update
                    stock.lastUpdate = last_update                    
         
        return stock   
    
def parseIndustry():
    industrySet = redclient.zrange(settings.INDUSTRY_SET,0,-1)
    if (len(industrySet)!= 0):
        return
    from lxml import etree
    from lxml.html import parse
    url = 'http://app.finance.ifeng.com/list/all_stock_cate.php?s=1'
    print url
    page = parse(url).getroot()
    #result = etree.tostring(page)
    #print result 
    
    from lxml.cssselect import CSSSelector
    for links in CSSSelector('a[href]')(page):
        href = links.attrib['href']
        #print href
        index =  href.find('stock_cate.php')
        if (index !=-1):
            print href
            industry = links.text
            redclient.zadd(settings.INDUSTRY_SET,1.1,industry)
            print industry
            page = parse(href).getroot()
            #result = etree.tostring(page)
            #print result 
#            import io
#            with io.open('test.html','wb') as f:
#               f.writelines(result)
#               pass
            r = page.xpath('//a/text()'); 
            #print len(r)
            #print r
            size = 0;
            for text in r:
                if len(text) == 6 and isinstance(text, str):
                    print text 
                    redclient.rpush(industry,text)  
                    size = size+1
            #print redclient.lrange(industry,0,size-1)
            #print redclient.keys(industry)                     
            #break;
    #print redclient.zrange(industrySet,0,-1)
    #print redclient.keys()
        
        
#    r = page.xpath('//div[@class="main"]');
#    print len(r)     
#    for a in r:  
#        tree= etree.ElementTree(a)  
#        print etree.tostring(tree) 
#        datas = tree.xpath('//tr') 
#        #print len(datas)
#        index =0
#        for data in datas:
#            dataTree = etree.ElementTree(data);
#            values = dataTree.xpath('//text()')     
#            #print str(unicode(values))  
#            print  values[1]
#            #print etree.tostring(dataTree)
            
      

        
if __name__ == '__main__':
    print 'ok'
    #print parseFinanceData('600327')
    #parseFinanceData('600327')
    #parseIndustry('')
#    import logging
#    LOG_FILENAME = 'example.log'
#    logging.basicConfig(level=logging.DEBUG)
#
#    logging.error('This message should go to the log file')
