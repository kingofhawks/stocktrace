from rest_framework import serializers


class MarketSerializer(serializers.Serializer):
    total_market_cap = serializers.FloatField(read_only=True)
    volume = serializers.FloatField(required=False)
    turnover_rate = serializers.FloatField(required=False)
    pe = serializers.FloatField(required=False)

