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

#generate ratio for PB<1
def pb1():
    from dao.stockdao import getPbLessThan1
    from dao.stockdao import findAllExistentTickers
    list = getPbLessThan1();
    allQuotes = findAllExistentTickers()
    c1 = float(len(list))
    print c1
    print len(allQuotes)
    return c1/len(allQuotes)
    
#generate MPI(Market Prosperity Index)
#check PE/PB/
def mpi():
    #PE range [5,80],maybe need to adjust according to more history data
    from dao.stockdao import getAvgPe,getAvgPb,getPbLessThan1
    avgPe = getAvgPe();
    print 'avgPe '+str(avgPe)
    print translatePe(avgPe)
    
    avgPb = getAvgPb();
    print 'avgPb '+str(avgPb)
    print translatePb(avgPb)
    
    
    
    
    #PB1 ratio[0,100]
    pass

#mapping SH PE from [10,70] to [0,1]
def translatePe(pe):
    return translate(pe,10,70,0,1)

#mapping SH PB from [1,6] to [0,1]
def translatePb(pb):
    return translate(pb,1,6,0,1)

#mapping [leftMin,leftMax] to [rightMin,rightMax]
def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)
     
    
if __name__ == '__main__':
    #print nhnl(beginDate='2012-06-10')
    #print pb1()
    mpi()