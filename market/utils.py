import pandas as pd
from lxml import etree
from lxml.html import parse
import arrow


# HK and USD to RMB exchange rate from boc.cn
def rmb_exchange_rate():
    page = parse('http://www.boc.cn/sourcedb/whpj/').getroot()
    # result = etree.tostring(page)
    # print result
    tables = page.xpath("//table")

    # import lxml.html as H
    # doc = H.document_fromstring(result)
    # tables=doc.xpath("//table")

    # print len(tables)

    # use the first row as DF columns
    dfs = pd.read_html(etree.tostring(tables[1]), header=0, flavor='lxml')
    # print len(dfs)
    df = dfs[0]
    # print df
    # print df.index
    # print df.columns
    name = '货币名称'
    usd = '美元'
    hk = '港币'
    zh = '中行折算价'
    # usd_to_rmb = df.loc[df[name] == usd][zh]
    # print 'usd_to_rmb:{}'.format(usd_to_rmb)
    # hk_to_rmb = df.loc[df[name] == hk][zh]
    # print 'hk_to_rmb:{}'.format(hk_to_rmb)
    # print type(hk_to_rmb)
    usd_df = df.loc[df[name] == usd]
    usd_to_rmb = usd_df.iloc[0][5]

    hk_df = df.loc[df[name] == hk]
    hk_to_rmb = hk_df.iloc[0][5]

    result = hk_to_rmb, usd_to_rmb
    # print result

    # select with iloccheck column 0 name
    # hk_to_rmb = df.iloc[8][5]
    # usd_to_rmb = df.iloc[22][5]
    # print 'hk_to_rmb:{}'.format(hk_to_rmb)
    # print 'usd_to_rmb:{}'.format(usd_to_rmb)
    return result


def get_date(day):
    date_format = 'YYYY-MM-DD'
    date = arrow.get(day, date_format).date()
    return date
