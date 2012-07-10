'''
Created on 2012-7-5

@author: Simon
'''
from yahooparser import triggerNhNl
from dao.stockdao import findAllExistentTickers
import sys, traceback


#find quotes triggered nhnl index during the last days
def findByNhnl(lastDays=40,nearDays=7):
    stocks = findAllExistentTickers()
    nhnlList = {'nhList':[],'nlList':[]}
    nh = 0
    nl = 0
   
    for code in stocks:       
                try:
                    triggered = triggerNhNl(code,lastDays,nearDays) 
                    print triggered
                    if triggered == 0:
                        continue
                    elif triggered.get('value') == 1:
                        nhnlList['nhList'].append({'date':triggered['date'],'code':code})
                        nh += 1;
                    elif triggered.get('value') == -1:
                        nhnlList['nlList'].append({'date':triggered['date'],'code':code})
                        nl += 1;
                                                                                            
                except:
                    traceback.print_exc(file=sys.stdout)
                    continue 
    nhnlList['nh'] = nh
    nhnlList['nl'] = nl
    nhnlList['nhnl'] = nh - nl
    return nhnlList  

#find quotes by MA index
def findByMa(lastDays=40,nearDays=7):
    stocks = findAllExistentTickers()
    nhnlList = {'nhList':[],'nlList':[]}
    for code in stocks:       
                try:
                    triggered = triggerNhNl(code,lastDays,nearDays) 
                    print triggered
                    if triggered == 0:
                        continue
                    elif triggered.get('value') == 1:
                        nhnlList['nhList'].append({'date':triggered['date'],'code':code})
                    elif triggered.get('value') == -1:
                        nhnlList['nlList'].append({'date':triggered['date'],'code':code})
                                                                                            
                except:
                    traceback.print_exc(file=sys.stdout)
                    continue 
    return nhnlList         
    
if __name__ == '__main__':
    print findByNhnl(40,1)