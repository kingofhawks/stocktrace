'''
Created on 2011-3-14

@author: simon
'''
from stock import Stock
import sys, traceback

def parse(code,parseIfeng= True,parseCap = True,parseSina = True):
    from ifengparser import parseFinanceData
    deli = '*************************************'
    print deli
    if (parseIfeng):
        s = parseFinanceData(code)
    else:
        s = Stock(code)
        
    if parseSina is False:
        pass
    else:
        from sinaparser import getStock
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

def parseAll(file,parseSina = False, parseIfeng= False,parseCap = False):
    import io
    list = [];
    
    import os
    fn = os.path.join(os.path.dirname(__file__),'..', '..','resources',file)
    print fn
    print os.path.abspath(fn)
    
    
    with io.open(fn,'rb') as f:        
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
                        s = parse(code,parseIfeng,parseCap,parseSina)
                        if (s.percent == -100.00):
                            print "not in trading now"
                        elif (s.percent >=2 or s.percent <=-2):
                            from util.mailutil import sendMail
                            sendMail()  
                        list.append(s)                  
                except:
                    traceback.print_exc(file=sys.stdout)
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
                
        return list
        


if __name__ == '__main__':
    #parse('600600')
    print parseAll('stock_list',parseSina=False)
    
    pass