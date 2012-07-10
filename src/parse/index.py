'''
Created on 2012-7-5

@author: Simon
'''
from yahooparser import computeNhnlIndexWithinRangeWithStocks
from dao.stockdao import findAllExistentTickers
import sys, traceback
#index TODO: nhnl/nhnl by ratio/


#generate NHNL index
def nhnl(lastDays=40,beginDate='2012-04-01'):
    stocks = findAllExistentTickers()
    return computeNhnlIndexWithinRangeWithStocks(stocks,lastDays,1,beginDate)

#generate MPI(Market Prosperity Index)
#check PE/PB/
def mpi():
    pass
     
    
if __name__ == '__main__':
    print nhnl()