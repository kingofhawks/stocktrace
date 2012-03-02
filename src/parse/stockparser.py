'''
Created on 2011-3-14

@author: simon
'''
from stock import Stock

def parse(code,parseCap = True):
    from ifengparser import parseFinanceData
    deli = '*************************************'
    print deli
    s = parseFinanceData(code)
    
    from stockutil import getStock
    s1 = getStock('sh'+code)
    s.current = s1.current
    s.percent = s1.percent
    
    if parseCap:
        from sseparser import parseCap
        s2 = parseCap(code)
        s.totalCap = s2.totalCap
        s.floatingCap = s2.floatingCap
    
    s.compute()
    print s
    return s

def parseAll(file,parseCap = False):
    import io
    with io.open(file,'rb') as f:
        list = [];
        for i in range(1000):
            line = f.readline()
            if (len(line) == 0):
                break;
            else :
                l = line.strip();
                if (len(l)==7):
                    code = l[1:]                    
                    #print len(l)  
                    #print l  
                elif (len(l) == 6):
                    code = l;                   
                else :
                    print l; 
                    continue
                
               #parse code
                try:
                    list.append(parse(code,parseCap))
                except:
                    continue       
                
        #write to log        
        import logging
        LOG_FILENAME = 'stockparser_result.log'
        logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG) 
        #sort by rank
        result = sorted(list, key=lambda stock: stock.rank)
        for stock in result:
            if stock.rank >=200:
                logging.warn(stock);
            else:
                logging.info(stock)
        pass

if __name__ == '__main__':
    #parse('600600')
    parseAll('stock_list')
    
    pass