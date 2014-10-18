'''
Created on 2011-3-25

@author: simon
'''
def parseCap(code):
    url = 'http://www.sse.com.cn/sseportal/ps/zhs/hqjt/hqjy.shtml'
    from lxml import etree
    from lxml.html import parse
    page = parse(url).getroot()
    result = etree.tostring(page)
    print result
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

if __name__ == '__main__':
    parseCap('');
    pass