## crazy index
from numpy import interp
from parse import *
from .models import Cix


# return value [0,100]
def cix(day='2016-08-06'):
    value = 0
    weight_range = [0, 10]

    #1 SH PE from 2010 year
    pe_df = avg_sh_pe('2009-12-31')
    max_pe = pe_df['PE'].max()
    min_pe = pe_df['PE'].min()
    # get latest PE DF by tail()
    latest_pe_df = pe_df.tail(1)
    latest_pe = latest_pe_df.iloc[0][1]
    print 'latest PE:{}'.format(latest_pe)
    pe = interp(latest_pe, [min_pe, max_pe], weight_range)
    print pe
    value += pe

    #2 low PB
    pb_ratio = low_pb_ratio()
    low_pb = pb_ratio[0]
    print low_pb
    min_low_pb = 0
    max_low_pb = 0.1
    pb = interp(-low_pb, [-max_low_pb, min_low_pb], weight_range)
    print pb
    value += pb

    #3 AH premium index
    ah_now = xueqiu('HKHSAHP')
    ah_current = ah_now.current
    ah = interp(ah_current, [100, 150], weight_range)
    print ah
    value += ah

    #4 high price
    high_price = high_price_ratio()
    print high_price
    high = interp(high_price, [0, 0.036], weight_range)
    print high
    value += high

    #5 SW index sample

    date = arrow.get(day)
    time_stamp = date.timestamp*1000
    return Cix(value,time_stamp)

if __name__ == '__main__':
    print cix(None)
