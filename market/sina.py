# sina real time API
import requests

from stocktrace.stock import Stock


def get_real_time(code='600276'):
    if code.startswith('60') or code.startswith('51'):
        code = 'sh'+code
    elif len(code) == 5:
        code = 'hk'+code
    else:
        code = 'sz'+code
    url = "http://hq.sinajs.cn/list="+code
    print('url:{}'.format(url))
    r = requests.get(url)
    print(r.content)
    string = str(r.content, encoding="gbk")
    test = string.split(',')
    # print test
    if code.startswith('hk'):
        current = float(test[6])
    else:
        current = float(test[3])

    yesterday = float(test[2])
    high = float(test[4])
    low = float(test[5])
    volume = float(test[8])
    if yesterday != 0:
        percent = (current-yesterday)/yesterday*100
    else:
        percent = 0
    name = test[0].split('"')[1]
    enc = "gbk"
    # u_content = name.decode(enc)  # decodes from enc to unicode
    # utf8_name = u_content.encode("utf8")
    stock = Stock(code, 0, current, percent, low, high, volume)
    print(stock)
    return stock


def get_real_time_list(codes):
    result = []
    for code in codes:
        stock = get_real_time(code)
        result.append(stock)
    return result
