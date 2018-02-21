import json
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.serializers import *
from market.models import Index, Sw, Cix, AhIndex
from market.parse import *
import pymongo

DB_NAME = 'stocktrace'
DB_HOST = 'localhost'
db = getattr(pymongo.MongoClient(host=DB_HOST), DB_NAME)


class IndexView(APIView):

    def get(self, request, *args, **kw):
        # Process any get params that you may need
        # If you don't need to process get params,
        # you can skip this part
        print('*'*15)
        name = request.GET.get('name')
        items = Index.objects(name=name).order_by('date')
        index_col = db.index.find({'name': name})
        df = pd.DataFrame(list(index_col))
        serializer = IndexListSerializer({'items': items})
        # print serializer.is_valid()
        # print serializer.errors
        content = JSONRenderer().render(serializer.data)
        print('**********content:{}'.format(content))
        json_output = json.loads(content)
        print('****json:{}'.format(json_output))
        pb_list = []
        pe_list = []
        for item in json_output.get('items'):
            date = arrow.get(item.get('date'), 'YYYY-MM-DD HH:mm:ss').timestamp
            pb_list.append([date, item.get('pb')])
            pe_list.append([date, item.get('pe')])
        result = {'PB': pb_list, 'PE': pe_list, 'PB_avg': df['pb'].mean(), 'PE_avg': df['pe'].mean()}
        response = Response(result, status=status.HTTP_200_OK)

        return response


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
        content = JSONRenderer().render(serializer.data)
        # print('**********content:{}'.format(content))
        json_output = json.loads(content)
        # print('****json:{}'.format(json_output))
        pb_list = []
        pe_list = []
        for item in json_output.get('items'):
            # date = int(item.get('date'))
            # date = datetime.strptime(item.get('date'), '%Y-%m-%d %H:%M:%S').date()
            date = arrow.get(item.get('date'), 'YYYY-MM-DD HH:mm:ss').timestamp
            pb_list.append([date, item.get('pb')])
            pe_list.append([date, item.get('pe')])
        result = {'PB': pb_list, 'PE': pe_list, 'PB_avg': df['pb'].mean(), 'PE_avg': df['pe'].mean()}
        response = Response(result, status=status.HTTP_200_OK)

        return response


class EquityView(APIView):

    def get(self, request, *args, **kw):
        # Process any get params that you may need
        # If you don't need to process get params,
        # you can skip this part
        print('*'*15)
        name = request.GET.get('name')
        items = Equity.objects(name=name).order_by('date')
        equity_col = db.equity.find({'name': name})
        df = pd.DataFrame(list(equity_col))
        df = pd.DataFrame(list(items))
        serializer = EquityListSerializer({'items': items})
        content = JSONRenderer().render(serializer.data)
        print('**********content:{}'.format(content))
        json_output = json.loads(content)
        print('****json:{}'.format(json_output))
        pb_list = []
        pe_list = []
        for item in json_output.get('items'):
            date = arrow.get(item.get('date'), 'YYYY-MM-DD HH:mm:ss').timestamp
            pb_list.append([date, item.get('pb')])
            pe_list.append([date, item.get('pe')])
        result = {'PB': pb_list, 'PE': pe_list, 'PB_avg': df['pb'].mean(), 'PE_avg': df['pe'].mean()}
        response = Response(result, status=status.HTTP_200_OK)

        return response


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

        return response


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
        content = JSONRenderer().render(serializer.data)
        # print '**********content:{}'.format(content)
        json_output = json.loads(content)
        # print '****json:{}'.format(json_output)
        pb_list = []
        pe_list = []
        for item in json_output.get('items'):
            date = int(item.get('BargainDate'))
            pb_list.append([date, item.get('PB')])
            pe_list.append([date, item.get('PE')])
        result = {'PB': pb_list, 'PE': pe_list, 'PB_avg': df['PB'].mean(), 'PE_avg': df['PE'].mean()}
        response = Response(result, status=status.HTTP_200_OK)

        return response


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
            history_list = xueqiu_history(code)
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

        return response


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
    result = {'pe_list': pe_list, 'PE_avg': pe_avg}
    response = Response(result, status=status.HTTP_200_OK)
    return response


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