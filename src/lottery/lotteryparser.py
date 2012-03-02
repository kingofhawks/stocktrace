'''
Created on 2011-3-7

@author: simon
'''
def parseMarket():
    from lxml import etree
    from lxml.html import parse
    page = parse('http://www.js-lottery.com/dlt/dltlssj/index.html').getroot()
    result = etree.tostring(page)
    print result
    import io
    with io.open('test.xml','wb') as f:
       f.writelines(result) 
    
    r = page.xpath('//table[@width="600"]');
    print len(r)
    j = 0 ;
    
    
    
if __name__ == '__main__':
    parseMarket()
    #parseCap('600600')
    #parseIndustry()
    #pass