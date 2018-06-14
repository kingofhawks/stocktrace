# crazy index
from numpy import interp
from market.parse import *
from market.utils import get_date
from market.xueqiu import low_pb_ratio, high_price_ratio
from .models import Cix


# return value [0,100]
def cix(day='2016-08-06'):
    value = 0
    weight_range = [0, 10]

    # 1 SH PE from 2000 year
    pe_df = avg_sh_pe('2000-1-31')
    max_pe = pe_df['PE'].max()
    min_pe = pe_df['PE'].min()
    # get latest PE DF by tail()
    latest_pe_df = pe_df.tail(1)
    latest_pe = latest_pe_df.iloc[0][1]
    # print 'latest PE:{}'.format(latest_pe)
    pe = interp(latest_pe, [min_pe, max_pe], weight_range)
    print('min_pe:{} max_pe:{} latest_pe:{} pe:{}'.format(min_pe, max_pe, latest_pe, pe))
    value += pe

    # 2 破净率
    pb_ratio = low_pb_ratio()
    broken_net_ratio = pb_ratio[0]
    # print low_pb
    min_low_pb = 0
    max_low_pb = 0.1
    pb = interp(-broken_net_ratio, [-max_low_pb, min_low_pb], weight_range)
    # print pb
    value += pb

    # 3 AH premium index
    ah_now = xueqiu('HKHSAHP')
    ah_current = ah_now.current
    ah = interp(ah_current, [100, 150], weight_range)
    # print ah
    value += ah

    # 4 GDP rate
    rate = gdp_rate()
    gdp = interp(rate, [0.4, 1], weight_range)
    value += gdp

    # 5 high price [0,3.6%]
    high_price = high_price_ratio()
    high = interp(high_price, [0, 0.036], weight_range)
    value += high

    # 6 换手率 [1%,3%]
    sh = read_index_market('SH000001')
    turnover_rate = sh['turnover_rate']
    turnover = interp(turnover_rate, [1, 3], weight_range)
    value += turnover

    Cix.objects(date=get_date(day)).update_one(pe=latest_pe, broken_net_ratio=broken_net_ratio, ah=ah_current,
                                               gdp=rate, high_price_ratio=high_price, turnover=turnover_rate,
                                               value=value,
                                               upsert=True)