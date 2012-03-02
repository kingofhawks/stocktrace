'''
Created on 2011-3-7

@author: simon
'''
def parseMarket():
    from lxml import etree
    from lxml.html import parse
    page = parse('http://www.sse.com.cn/sseportal/ps/zhs/home.html').getroot()
    result = etree.tostring(page)
    #print result
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
        try:
            pe = float(rows[4])
            avgPrice = str(rows[5])
            industry.name = name
            industry.PE = pe
            industry.avgPrice = avgPrice
        except:
            continue
        print industry
        
        #temp = values[0].strip()
        #print temp
        
    #print cap
    #print stock
    
    
if __name__ == '__main__':
    parseMarket()
    #parseCap('600600')
    #parseIndustry()
    #pass