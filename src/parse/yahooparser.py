'''
Created on 2011-3-7

@author: simon
'''
def parseFinanceData(code):
    from lxml import etree
    from lxml.html import parse
    url = 'http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20in%20(%22600327.SS%22)&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys'
    print url
    page = parse(url).getroot()
    result = etree.tostring(page)
    print result
    import io
    with io.open('test.xml','wb') as f:
       #f.writelines(result)
       pass 
    
    r = page.xpath('//div[@class="tab01"]');
    #print len(r)    
    from stock import Stock
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
    
def getHistorialData(code):
    from lxml import etree
    from lxml.html import parse
    code2 = code +".SS"
    url = 'http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.historicaldata%20where%20symbol%20%3D%20%22'+code2+'%22%20and%20startDate%20%3D%20%222012-01-01%22%20and%20endDate%20%3D%20%222012-03-31%22&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys'
    print url
    page = parse(url).getroot()
    result = etree.tostring(page)
    print result
    
    r = page.xpath('//quote');
    from stock import Stock
    historyDatas = []
    for a in r:  
        tree= etree.ElementTree(a)  
        #print etree.tostring(tree) 

        stock = Stock(code)           
        stock.date = tree.xpath('//date')[0].text
        stock.high = float(tree.xpath('//high')[0].text)
        stock.low = float(tree.xpath('//low')[0].text)  
        stock.openPrice = float(tree.xpath('//open')[0].text)
        stock.close = float(tree.xpath('//close')[0].text)
        stock.volume = float(tree.xpath('//volume')[0].text)
        #print stock    
        historyDatas.append(stock) 
    historyDatas.sort(key=lambda item:item.date,reverse=True) 
#    for stock in historyDatas:
#        print stock 
#    pass 
    
    for i in  range(len(historyDatas)):
        if i == len(historyDatas)-1:
            continue
        else:
            last = historyDatas[i]
            prev = historyDatas[i+1]
            if (last.openPrice!= prev.close and
                (last.low >prev.high or last.high<prev.low)):
                print "gap***"+last.__str__()            
                    
if __name__ == '__main__':
    stocks = ['600327','600739','600573','600583','600718','600827','601111','601866']
    for stock in stocks:
        getHistorialData(stock)
    getHistorialData('600890')
    import logging
    LOG_FILENAME = 'example.log'
    logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

    logging.error('This message should go to the log file')
