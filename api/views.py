import json
from django.shortcuts import render

# Create your views here.
from rest_framework.renderers import JSONRenderer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from serializers import MarketSerializer, MarketOverallSerializer, MarketsSerializer
from market.models import Market
from market.parse import *


class MarketView(APIView):

    def get(self, request, *args, **kw):
        # Process any get params that you may need
        # If you don't need to process get params,
        # you can skip this part
        print '*'*15
        # market = Market(1000, 100, 1.2, 20)
        # serializer = MarketSerializer(market)
        market = market_overall()
        # print json.dumps(market)
        # serializer = MarketOverallSerializer(market)
        serializer = MarketsSerializer({'markets': market})
        # print serializer.is_valid()
        # print serializer.errors
        content = JSONRenderer().render(serializer.data)
        print '**********content:{}'.format(content)
        json_output = json.loads(content)
        print '****json:{}'.format(json_output)
        # response = Response(json_output.get('markets'), status=status.HTTP_200_OK)
        response = Response(json_output, status=status.HTTP_200_OK)

        return response
