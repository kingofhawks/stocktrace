from django.shortcuts import render

# Create your views here.
from rest_framework.renderers import JSONRenderer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from serializers import MarketSerializer
from market.models import Market


class MarketView(APIView):

    def get(self, request, *args, **kw):
        # Process any get params that you may need
        # If you don't need to process get params,
        # you can skip this part
        print '*'*15
        market = Market(1000, 100, 1.2, 20)
        serializer = MarketSerializer(market)
        content = JSONRenderer().render(serializer.data)
        response = Response(content, status=status.HTTP_200_OK)
        return response
