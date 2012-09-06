'''
Created on 2011-3-7

@author: simon
'''
def parseMarket():
    from lxml import etree
    from lxml.html import parse
    page = parse('http://www.sse.com.cn/sseportal/ps/zhs/home.html').getroot()
    result = etree.tostring(page)
    print result
    import io
    with io.open('test.xml','wb') as f:
       f.writelines(result) 
    
    r = page.xpath('//table[@class="border_gray_right border_gray_bottom border_gray_left right_gk_bj"]');
    #print len(r)
    j = 0 ;
    from stockmarket import stockmarket
    stockmarket = stockmarket()
    for a in r:  
        tree= etree.ElementTree(a)  
        #print etree.tostring(tree) 
        datas = tree.xpath('//td[@align="right"]') 
        #print len(datas)
        for data in datas:
            dataTree = etree.ElementTree(data);
            #print etree.tostring(dataTree)
            values = dataTree.xpath('//text()')
            #print values
            #temp = str(values[0]).strip()
            temp = values[0].strip()
            #print temp
            length = len(temp)
            index = length
            for i in range(length):
                #print temp[i]
                if (temp[i].isalnum() or temp[i] =='.'):
                    pass
                else:
                    index = i
                    if (index == len(temp)):
                        break;
            #print index
            temp = temp[0:index]
            #print temp+'****'+str(j)
            if (j == 0):
                stockmarket.ssgs = int(temp);
            elif (j == 1):
                stockmarket.sszq = int(temp);  
            elif (j == 2):
                stockmarket.ssgp = int(temp);  
            elif (j == 3):
                stockmarket.totalShares = float(temp);
            elif (j == 4):
                stockmarket.totalFloatingShares = float(temp);
            elif (j == 5):
                stockmarket.totalCap = float(temp);
            elif (j == 6):
                stockmarket.totalMarketCap = float(temp);
            elif (j == 7):
                stockmarket.marketPe = float(temp);
            j+= 1;     
            
        print stockmarket

def parseCap(code):
    url = 'http://www.sse.com.cn/sseportal/webapp/datapresent/querythismyquat?productId='+code+'&prodType=1'
    from lxml import etree
    from lxml.html import parse
    page = parse(url).getroot()
    #result = etree.tostring(page)
    #print result
    r = page.xpath('//strong');
    #print len(r)
    from stock import Stock
    stock = Stock(code)
    cap = []
    for data in r:
        dataTree = etree.ElementTree(data);
        #print etree.tostring(dataTree)
        values = dataTree.xpath('//text()')
        temp = values[0].strip()
        #print temp
        cap.append(temp)
    #print cap
    stock.totalCap = float(cap[0])
    stock.floatingCap = float(cap[1])
    #print stock
    return stock
    
def parseIndustry():
    url = 'http://www.sse.com.cn/sseportal/webapp/datapresent/SSEQueryFirstSSENewAct'
    from lxml import etree
    from lxml.html import parse
    page = parse(url).getroot()
    result = etree.tostring(page)
    #print result
    #r = page.xpath('//td[@class="table3"]');
    r = page.xpath('//tr[@valign="top"]');
    #print len(r)
    from industry import Industry
    for data in r:
        dataTree = etree.ElementTree(data);
        #print etree.tostring(dataTree)
        #values = dataTree.xpath('//text()')
        row = dataTree.xpath('//td')
        length = len(row)
        #print length
        if (length ==5):
            continue
        rows = []
        for column in row:
            col = etree.ElementTree(column)
            #print etree.tostring(col)
            values = col.xpath('//text()')
            temp = values[0].strip()
            #print temp
            rows.append(temp)
            
        industry = Industry()
        name = str(rows[0])
        
        href = dataTree.xpath('//a/@href')
        print href
        try:
            pe = float(rows[4])
            avgPrice = str(rows[5])
            industry.name = name
            industry.PE = pe
            industry.avgPrice = avgPrice
        except:
            continue
        print industry
        newUrl = 'http://www.sse.com.cn'+str(href[0])
        print newUrl
        newPage = parse(newUrl).getroot()
        newResult = etree.tostring(newPage)
        print newResult
        
        #temp = values[0].strip()
        #print temp
        
    #print cap
    #print stock
#Parse shenzhen market
def parseSzMarket():
    from lxml import etree
    from lxml.html import parse
    page = parse('http://www.szse.cn/').getroot()
    result = etree.tostring(page)
    print result
    import io
    with io.open('test.xml','wb') as f:
       f.writelines(result) 
    
    r = page.xpath('//div[@class="agora"]');
    print len(r)
    j = 0 ;
    from stockmarket import stockmarket
    stockmarket = stockmarket()
    tree= etree.ElementTree(r[0])  
    print etree.tostring(tree) 
    datas = tree.xpath('//span/text()')
    print datas 
    stockmarket.totalCap = float(datas[3]);
    
            
    print stockmarket   
    
#parse quote list from shanghai exchange    
def downloadQuoteList(save=False,parseSse=False):
    quotes = []
    cursor = 0
    if parseSse: 
        #parse quote list from SH       
        while True:
            temp = parseQuoteListFromCursor(cursor*50);
            #print len(temp)
            if len(temp) ==0:
                break
            cursor += 1
            quotes.extend(temp)
    else:
        #parse from local text file from newone export
        from parse.stockparser import parseAll
        quotes = parseAll('stock_list')
    if save:
        from dao.stockdao import batchInsertTicker
        batchInsertTicker(quotes)

    return quotes

    #print stock
    
def parseQuoteListFromCursor(cursor=1):
    if (cursor == 0):
        cursor = 1
    url = 'http://www.sse.com.cn/sseportal/webapp/datapresent/SSEQueryStockInfoAct?reportName=BizCompStockInfoRpt&PRODUCTID=&PRODUCTJP=&PRODUCTNAME=&keyword=&tab_flg=1&CURSOR='+str(cursor)
    print url
    from lxml import etree
    from lxml.html import parse
    page = parse(url).getroot()
    result = etree.tostring(page)
    #print result
    temp = page.xpath('//a/text()');
    #print temp
    quotes = []
    for q in temp:
        if isinstance(q, str) and q.startswith('6'):
            #print "ordinary string"
            quotes.append(q)
        elif isinstance(q, unicode):
            #print "unicode string"  
            pass                     
        else:
            #print "not a valid string"
            pass        
    return quotes
   
    
if __name__ == '__main__':
    #parseMarket()
    #parseSzMarket()
    #print downloadQuoteList(True)
    #parseCap('600600')
    parseIndustry()
    #pass