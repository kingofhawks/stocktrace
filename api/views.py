import json
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.serializers import *
from market.models import Index, Sw, Cix, AhIndex, Market
from market.parse import *
import pymongo

from portfolio.portfolio import snapshot
from stocktrace.stock import StockHistory

DB_NAME = 'stocktrace'
DB_HOST = 'localhost'
db = getattr(pymongo.MongoClient(host=DB_HOST), DB_NAME)


def get_result(serializer, df):
    content = JSONRenderer().render(serializer.data)
    print('**********content:{}'.format(content))
    json_output = json.loads(content)
    print('****json:{}'.format(json_output))
    pb_list = []
    pe_list = []
    pe_ttm_list = []
    dyr_list = []
    turnover_list = []
    for item in json_output.get('items'):
        if item.get('date'):
            timestamp = arrow.get(item.get('date'), 'YYYY-MM-DD HH:mm:ss').timestamp * 1000
        else:
            # SW index
            timestamp = int(item.get('BargainDate'))
        pb_list.append([timestamp, item.get('pb') or item.get('PB')])
        pe_list.append([timestamp, item.get('pe') or item.get('PE')])
        pe_ttm_list.append([timestamp, item.get('pe_ttm')])
        dyr_list.append([timestamp, item.get('dividend_yield_ratio')])
        turnover = item.get('TurnoverRate')
        if turnover:
            turnover_list.append([timestamp, float(turnover)])
        else:
            turnover_list.append([timestamp, 0])
    # https://stackoverflow.com/questions/455612/limiting-floats-to-two-decimal-points
    if 'pb' in df:
        pb_avg = df['pb'].mean()
    else:
        pb_avg = 0
    if 'pe' in df:
        pe_avg = df['pe'].mean()
    else:
        pe_avg = 0
    if 'pe_ttm' in df:
        pe_ttm_avg = df['pe_ttm'].mean()
    else:
        pe_ttm_avg = 0
    # if 'TurnoverRate' in df:
    #     turnover_avg = df['TurnoverRate'].mean()
    # else:
    #     turnover_avg = 0

    result = {'PB': pb_list, 'PE': pe_list, 'PE_TTM': pe_ttm_list, 'DYR': dyr_list, 'turnover': turnover_list,
              'PB_avg': float("{0:.2f}".format(pb_avg)),
              'PE_avg': float("{0:.2f}".format(pe_avg)), 'PE_ttm_avg': float("{0:.2f}".format(pe_ttm_avg)),
              # 'turnover_avg': float("{0:.2f}".format(turnover_avg)),
              }
    return result


def get_response_cors(response):
    # TODO
    response['Access-Control-Allow-Origin'] = '*'
    return response


class IndexView(APIView):

    def get(self, request, *args, **kw):
        # Process any get params that you may need
        # If you don't need to process get params,
        # you can skip this part
        name = request.GET.get('code')
        items = Index.objects(name=name).order_by('date')
        index_col = db.index.find({'name': name})
        df = pd.DataFrame(list(index_col))
        serializer = IndexListSerializer({'items': items})

        # HSCEI index has no pb data
        if name == 'HSCEI':
            df['pb'] = 0

        result = get_result(serializer, df)
        response = Response(result, status=status.HTTP_200_OK)

        return get_response_cors(response)


class IndustryView(APIView):

    def get(self, request, *args, **kw):
        # Process any get params that you may need
        # If you don't need to process get params,
        # you can skip this part
        print('*'*15)
        code = request.GET.get('code')
        items = Industry.objects(code=code).order_by('date')
        industry_col = db.industry.find({'code': code})
        df = pd.DataFrame(list(industry_col))
        print(df)
        serializer = IndustryListSerializer({'items': items})

        result = get_result(serializer, df)
        response = Response(result, status=status.HTTP_200_OK)

        return get_response_cors(response)


class EquityView(APIView):

    def get(self, request, *args, **kw):
        # Process any get params that you may need
        # If you don't need to process get params,
        # you can skip this part
        code = request.GET.get('code')
        items = Equity.objects(code=code).order_by('date')
        equity_col = db.equity.find({'code': code})
        df = pd.DataFrame(list(equity_col))
        serializer = EquityListSerializer({'items': items})
        result = get_result(serializer, df)

        response = Response(result, status=status.HTTP_200_OK)
        return get_response_cors(response)


class AhView(APIView):

    def get(self, request, *args, **kw):
        # Process any get params that you may need
        # If you don't need to process get params,
        # you can skip this part
        ah_data = AhIndex.objects()
        print(ah_data)
        df = DataFrame(list(ah_data))
        # print df
        max_ah = df['value'].max()
        min_ah = df['value'].min()
        avg_ah = df['value'].mean()
        print('PE max:{} min:{} average:{} median:{}'.format(max_ah, min_ah, avg_ah))
        serializer = AhIndexSerializer({'items': ah_data})
        content = JSONRenderer().render(serializer.data)
        # print '**********content:{}'.format(content)
        json_output = json.loads(content)
        # print '****json:{}'.format(json_output)
        response = Response(json_output, status=status.HTTP_200_OK)
        return get_response_cors(response)


class SwView(APIView):

    def get(self, request, *args, **kw):
        # Process any get params that you may need
        # If you don't need to process get params,
        # you can skip this part
        code = request.GET.get('code')
        print('code {}'.format(code))

        # limit to 1000 points
        # sw_data = Sw.objects[:1000].order_by('BargainDate')
        sw_data = Sw.objects(SwIndexCode=code).order_by('BargainDate')
        # print len(sw_data)

        sw_col = db.sw.find({'SwIndexCode': code})
        # print sw_col
        df = pd.DataFrame(list(sw_col))
        df['pb'] = df['PB']
        df['pe'] = df['PE']
        # print len(df)
        # df = DataFrame(list(sw_data))
        print(df)
        # df = df.sort_index(by='BargainDate', ascending=False)
        # print 'PE min:{}'.format(df['PE'].min())
        # print 'PE mean:{}'.format(df['PE'].mean())
        # print 'PE median:{}'.format(df['PE'].median())
        # print 'PE max:{}'.format(df['PE'].max())
        # print 'PB min:{}'.format(df['PB'].min())
        # print 'PB mean:{}'.format(df['PB'].mean())
        # print 'PB median:{}'.format(df['PB'].median())
        # print 'PB max:{}'.format(df['PB'].max())
        # print sw_data
        serializer = SwIndexSerializer({'items': sw_data})

        result = get_result(serializer, df)
        response = Response(result, status=status.HTTP_200_OK)
        return get_response_cors(response)


class StockView(APIView):

    def get(self, request, *args, **kw):
        # Process any get params that you may need
        # If you don't need to process get params,
        # you can skip this part
        code = request.GET.get('code')
        # print 'code {}'.format(code)

        sw_data = StockHistory.objects(code=code).order_by('time')
        # print sw_data

        sw_col = db.stock_history.find({'code': code})
        # print sw_col
        history_list = list(sw_col)
        if len(history_list) == 0:
            history_list = read_history(code)
            for history in history_list:
                history.save()
            sw_col = db.stock_history.find({'code': code})
            history_list = list(sw_col)

        df = pd.DataFrame(history_list)
        # print len(df)
        # df = DataFrame(list(sw_data))
        # print df
        # df = df.sort_index(by='BargainDate', ascending=False)
        # print 'PE min:{}'.format(df['PE'].min())
        # print 'PE mean:{}'.format(df['PE'].mean())
        # if 'turn_rate' in df.index:
        #     print 'turnover median:{}'.format(df['turn_rate'].median())
        # print 'PE max:{}'.format(df['PE'].max())
        # print 'PB min:{}'.format(df['PB'].min())
        # print 'PB mean:{}'.format(df['PB'].mean())
        # print 'PB median:{}'.format(df['PB'].median())
        # print 'PB max:{}'.format(df['PB'].max())
        serializer = StockListSerializer({'items': sw_data})
        content = JSONRenderer().render(serializer.data)
        # print '**********content:{}'.format(content)
        json_output = json.loads(content)
        # print '****json:{}'.format(json_output)
        close_list = []
        volume_list = []
        turn_over_list = []
        for item in json_output.get('items'):
            # print 'item *** {}'.format(item)
            date = int(item.get('timestamp'))
            close_list.append([date, item.get('close')])
            volume_list.append([date, item.get('volume')])
            turn_over_list.append([date, item.get('turn_rate')])
        result = {'close': close_list, 'volume': volume_list, 'turnover': turn_over_list}
        if 'volume_avg' in df.index:
            result.update({'volume_avg': df['volume'].mean()})
        if 'turnover_avg' in df.index:
            result.update({'turnover_avg': df['turn_rate'].mean()})
        response = Response(result, status=status.HTTP_200_OK)
        return get_response_cors(response)


@api_view(['GET'])
def equity_list(request):
    equity_group = db.equity.aggregate([{"$group": {"_id": "$code"}}], cursor={})
    equities = list(equity_group)
    print(len(equities))
    # filter wrong data
    filtered_equities = list(filter(lambda x: len(x.get('_id')) == 6, equities))
    print(len(filtered_equities))
    response = Response(filtered_equities, status=status.HTTP_200_OK)

    return get_response_cors(response)


@api_view(['GET'])
def index_list(request):
    index_group = db.index.aggregate([{"$group": {"_id": "$name"}}], cursor={})
    indexes = list(index_group)
    response = Response(indexes, status=status.HTTP_200_OK)

    return get_response_cors(response)


@api_view(['GET'])
def industry_list(request):
    industry_col = db.industry.aggregate([{"$group": {"_id": {"code": "$code", "name": "$name"}}}], cursor={})
    result = list(map(lambda x: x.get('_id'), list(industry_col)))
    # filter those name is empty
    result = list(filter(lambda x: x.get('name') is not None, result))
    response = Response(result, status=status.HTTP_200_OK)
    return get_response_cors(response)


@api_view(['GET'])
def portfolio(request):
    p = snapshot(True)
    results = sorted(p.stocks, key=lambda s: s.ratio, reverse=True)
    print(results)
    serializer = PortfolioListSerializer({'list': results, 'market_value': p.market_value,
                                          'cost_zs': p.cost_zs, 'cost_ht1': p.cost_ht1, 'cost_ht2': p.cost_ht2,
                                          'cost': p.cost,
                                          'total': p.total, 'net_asset': p.net_asset, 'lever': p.lever,
                                          'position_ratio': p.position_ratio, 'financing': p.financing,
                                          'profit': p.profit, 'profit_ratio': p.profit_ratio,
                                          'profit_today': p.profit_today, 'profit_ratio_today': p.profit_ratio_today})
    content = JSONRenderer().render(serializer.data)
    print('**********content:{}'.format(content))
    json_output = json.loads(content)
    response = Response(json_output, status=status.HTTP_200_OK)
    return get_response_cors(response)


@api_view(['GET'])
def fake(request):
    response = Response([], status=status.HTTP_200_OK)
    return get_response_cors(response)


@api_view(['GET'])
def sw_list(request):
    result = list()
    result.append({'value': '801010', 'name': '农林牧渔'})
    result.append({'value': '801020', 'name': '采掘'})
    result.append({'value': '801030', 'name': '化工'})
    result.append({'value': '801040', 'name': '钢铁'})
    result.append({'value': '801050', 'name': '有色金属'})
    result.append({'value': '801080', 'name': '电子'})

    result.append({'value': '801110', 'name': '家用电器'})
    result.append({'value': '801120', 'name': '食品饮料'})
    result.append({'value': '801130', 'name': '纺织服装'})
    result.append({'value': '801140', 'name': '轻工制造'})
    result.append({'value': '801150', 'name': '医药生物'})
    result.append({'value': '801160', 'name': '公用事业'})
    result.append({'value': '801170', 'name': '交通运输'})
    result.append({'value': '801180', 'name': '房地产'})

    result.append({'value': '801200', 'name': '商业贸易'})
    result.append({'value': '801210', 'name': '休闲服务'})
    result.append({'value': '801230', 'name': '综合'})

    result.append({'value': '801710', 'name': '建筑材料'})
    result.append({'value': '801720', 'name': '建筑装饰'})
    result.append({'value': '801730', 'name': '电气设备'})
    result.append({'value': '801740', 'name': '国防军工'})
    result.append({'value': '801750', 'name': '计算机'})
    result.append({'value': '801760', 'name': '传媒'})
    result.append({'value': '801770', 'name': '通信'})
    result.append({'value': '801780', 'name': '银行'})
    result.append({'value': '801790', 'name': '非银金融'})
    result.append({'value': '801880', 'name': '汽车'})
    result.append({'value': '801890', 'name': '机械设备'})

    response = Response(result, status=status.HTTP_200_OK)
    return get_response_cors(response)


@api_view(['GET'])
def diff(request):
    result = {}
    code = request.GET.get('code')
    codes = code.split(',')
    # print codes
    # print 'code {}'.format(code)
    for code in codes:
        sw_data = StockHistory.objects(code=code).order_by('time')
        serializer = StockListSerializer({'items': sw_data})
        content = JSONRenderer().render(serializer.data)
        # print '**********content:{}'.format(content)
        json_output = json.loads(content)
        # print '****json:{}'.format(json_output)
        close_list = []
        for item in json_output.get('items'):
            date = int(item.get('timestamp'))
            close_list.append([date, item.get('close')])
        # result = {'close': close_list}
        result.update({code: close_list})
    response = Response(result, status=status.HTTP_200_OK)

    return response


@api_view(['GET'])
def sh(request):
    df = avg_sh_pe()
    # print df
    pe_avg = df['PE'].mean()
    data = df.to_json(orient="records")
    # print 'sh***{}'.format(data)
    # print 'pe_avg***{}'.format(pe_avg)
    items = json.loads(data)
    pe_list = []
    for item in items:
        # print 'item:{}'.format(item)
        date = int(item.get('Date'))
        pe_list.append([date, item.get('PE')])
    result = {'PE': pe_list, 'PE_avg': float("{0:.2f}".format(pe_avg))}
    response = Response(result, status=status.HTTP_200_OK)
    return get_response_cors(response)


def get_market_result(serializer):
    content = JSONRenderer().render(serializer.data)
    print('**********content:{}'.format(content))
    json_output = json.loads(content)
    print('****json:{}'.format(json_output))
    nh_list = []
    nl_list = []
    nhnl_list = []
    nh_ratio_list = []
    nl_ratio_list = []
    broken_net_list = []
    broken_net_ratio_list = []
    zt_list = []
    zt__ratio_list = []
    dt_list = []
    dt__ratio_list = []
    zdr_list = []
    for item in json_output.get('items'):
        if item.get('date'):
            timestamp = arrow.get(item.get('date'), 'YYYY-MM-DD HH:mm:ss').timestamp * 1000
        nh_list.append([timestamp, item.get('nh')])
        nl_list.append([timestamp, item.get('nl')])
        nhnl_list.append([timestamp, item.get('nh')-item.get('nl')])
        nh_ratio = item.get('nh_ratio')*100
        nh_ratio_list.append([timestamp, float("{0:.2f}".format(nh_ratio))])
        nl_ratio = item.get('nl_ratio')*100
        nl_ratio_list.append([timestamp, float("{0:.2f}".format(nl_ratio))])
        broken_net = item.get('broken_net')
        broken_net_list.append([timestamp, float("{0:.2f}".format(broken_net))])
        broken_net_ratio = item.get('broken_net_ratio') * 100
        broken_net_ratio_list.append([timestamp, float("{0:.2f}".format(broken_net_ratio))])
        zt = item.get('zt')
        if zt:
            zt_list.append([timestamp, float("{0:.2f}".format(zt))])
        zt_ratio = item.get('zt_ratio')
        if zt_ratio:
            zt__ratio_list.append([timestamp, float("{0:.2f}".format(zt_ratio*100))])
        dt = item.get('dt')
        if dt:
            dt_list.append([timestamp, float("{0:.2f}".format(dt))])
        dt_ratio = item.get('dt_ratio')
        if dt_ratio:
            dt__ratio_list.append([timestamp, float("{0:.2f}".format(dt_ratio*100))])
        zdr = item.get('zdr')
        if zdr:
            zdr_list.append([timestamp, float("{0:.2f}".format(zdr*100))])
    result = {'nh': nh_list, 'nl': nl_list, 'nhnl': nhnl_list,
              'nh_ratio': nh_ratio_list, 'nl_ratio': nl_ratio_list,
              'broken_net': broken_net_list, 'broken_net_ratio': broken_net_ratio_list,
              'zt': zt_list, 'dt': dt_list, 'zt_ratio': zt__ratio_list, 'dt_ratio': dt__ratio_list,
              'zdr': zdr_list,
              }
    return result


class MarketView(APIView):

    def get(self, request, *args, **kw):
        # Process any get params that you may need
        # If you don't need to process get params,
        # you can skip this part
        data = Market.objects().order_by('date')
        print(data)
        # df = DataFrame(list(data))
        # print df
        # max_ah = df['value'].max()
        # min_ah = df['value'].min()
        # avg_ah = df['value'].mean()
        # print('PE max:{} min:{} average:{} median:{}'.format(max_ah, min_ah, avg_ah))
        serializer = MarketListSerializer({'items': data})
        # content = JSONRenderer().render(serializer.data)
        # print '**********content:{}'.format(content)
        # json_output = json.loads(content)
        # print '****json:{}'.format(json_output)
        result = get_market_result(serializer)
        response = Response(result, status=status.HTTP_200_OK)
        return get_response_cors(response)


class CixView(APIView):

    def get(self, request, *args, **kw):
        # Process any get params that you may need
        # If you don't need to process get params,
        # you can skip this part
        cix_data = Cix.objects()
        # print cix_data
        df = DataFrame(list(cix_data))        
        # print df
        # max_ah = df['value'].max()
        # min_ah = df['value'].min()
        # avg_ah = df['value'].mean()
        # print 'PE max:{} min:{} average:{} median:{}'.format(max_ah, min_ah, avg_ah)
        serializer = CixListSerializer({'items': cix_data})
        content = JSONRenderer().render(serializer.data)
        # print '**********content:{}'.format(content)
        json_output = json.loads(content)
        # print '****json:{}'.format(json_output)
        cix_list = []
        for item in json_output.get('items'):
            cix_list.append([item.get('timestamp'), item.get('value')])
        response = Response({'items': cix_list}, status=status.HTTP_200_OK)

        return response