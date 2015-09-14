from rest_framework import serializers


class MarketSerializer(serializers.Serializer):
    name = serializers.CharField(read_only=True)
    total_market_cap = serializers.FloatField(read_only=True)
    volume = serializers.FloatField(required=False)
    turnover_rate = serializers.FloatField(required=False)
    pe = serializers.FloatField(required=False)


class MarketOverallSerializer(serializers.Serializer):
    # markets = MarketSerializer(many=True)  # A nested list of 'edit' items.
    sh = MarketSerializer()
    sz = MarketSerializer()
    cyb = MarketSerializer()
    zxb = MarketSerializer()


class MarketsSerializer(serializers.Serializer):
    markets = MarketSerializer(many=True)  # A nested list of 'edit' items.


