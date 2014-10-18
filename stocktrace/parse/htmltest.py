'''
Created on 2011-3-7

@author: simon
'''

if __name__ == '__main__':
    from lxml import etree
    from lxml.html import parse
    #http://finance.sina.com.cn/realstock/company/sh600880/nc.shtml?b=1
    #http://cn.reuters.com/investing/quotes/companyRatios?symbol=600880.SS
    page = parse('http://app.finance.ifeng.com/data/stock/cwjk.php?symbol=600062').getroot()
    result = etree.tostring(page)
    print result
    import io
    with io.open('test.html','wb') as f:
       f.writelines(result) 
    
    r = page.xpath('//div[@class="primaryContent1"]');
    t = page.xpath('//div[@class="navbtmmaquee"]');
    print 'haha*****'
    print len(t)
    #print len(r)
    for a in r:  
        tree= etree.ElementTree(a)  
        #print etree.tostring(tree) 
        datas = tree.xpath('//td[@class="data"]') 
        #print len(datas)
        for data in datas:
            dataTree = etree.ElementTree(data);
            #print etree.tostring(dataTree)
            #print dataTree.xpath('//text()')
    values = r[1];
    valuesTree= etree.ElementTree(values)  
        #print etree.tostring(tree) 
    valuesData = valuesTree.xpath('//td[@class="data"]') 
    for data in valuesData:
        dataTree = etree.ElementTree(data);
        #print etree.tostring(dataTree)
        print dataTree.xpath('//text()')
    r = page.xpath('//div[@class="primaryContent2"]');
    #print len(r)
    for a in r:  
        tree= etree.ElementTree(a)  
        #print etree.tostring(tree)
           
    #pass