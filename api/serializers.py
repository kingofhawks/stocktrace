from rest_framework import serializers

from portfolio.models import Dividend


class IndexSerializer(serializers.Serializer):
    name = serializers.CharField(read_only=True)
    pe = serializers.FloatField(required=False)
    pe_ttm = serializers.FloatField(required=False)
    pb = serializers.FloatField(required=False)
    total_market_cap = serializers.FloatField(read_only=True)
    volume = serializers.FloatField(required=False)
    turnover = serializers.FloatField(required=False)
    date = serializers.CharField(required=False)


class IndexListSerializer(serializers.Serializer):
    items = IndexSerializer(many=True)  # A nested list of 'edit' items.


class IndustrySerializer(serializers.Serializer):
    name = serializers.CharField(read_only=True)
    code = serializers.CharField(read_only=True)
    pe = serializers.FloatField(required=False)
    pe_ttm = serializers.FloatField(required=False)
    pb = serializers.FloatField(required=False)
    date = serializers.CharField(required=False)


class IndustryListSerializer(serializers.Serializer):
    items = IndexSerializer(many=True)  # A nested list of 'edit' items.


class EquitySerializer(serializers.Serializer):
    name = serializers.CharField(read_only=True)
    code = serializers.CharField(read_only=True)
    pe = serializers.FloatField(required=False)
    pe_order = serializers.IntegerField(required=False)
    pe_ttm = serializers.FloatField(required=False)
    pb = serializers.FloatField(required=False)
    pb_order = serializers.IntegerField(required=False)
    magic_order = serializers.IntegerField(required=False)
    dividend_yield_ratio = serializers.FloatField(required=False)
    roe = serializers.FloatField(required=False)
    roe_order = serializers.IntegerField(required=False)
    date = serializers.CharField(required=False)


class EquityListSerializer(serializers.Serializer):
    items = EquitySerializer(many=True)  # A nested list of 'edit' items.


class EquityListSerializer2(serializers.Serializer):
    list = EquitySerializer(many=True)  # A nested list of 'edit' items.


@DeprecationWarning
class MarketOverallSerializer(serializers.Serializer):
    # markets = MarketSerializer(many=True)  # A nested list of 'edit' items.
    sh = IndexSerializer()
    sz = IndexSerializer()
    cyb = IndexSerializer()
    zxb = IndexSerializer()


class MarketSerializer(serializers.Serializer):
    date = serializers.CharField(required=False)
    stock_count = serializers.IntegerField(read_only=True)
    nh = serializers.IntegerField(read_only=True)
    nh_ratio = serializers.FloatField(read_only=True)
    nl = serializers.IntegerField(read_only=True)
    nl_ratio = serializers.FloatField(read_only=True)
    nhnl = serializers.IntegerField(read_only=True)
    broken_net = serializers.IntegerField(read_only=True)
    broken_net_ratio = serializers.FloatField(read_only=True)
    zt = serializers.FloatField(read_only=True)
    zt_ratio = serializers.FloatField(read_only=True)
    dt = serializers.FloatField(read_only=True)
    dt_ratio = serializers.FloatField(read_only=True)
    zdr = serializers.FloatField(read_only=True)
    cix = serializers.FloatField(read_only=True)
    turnover = serializers.FloatField(read_only=True)
    cost = serializers.FloatField(read_only=True)


class MarketListSerializer(serializers.Serializer):
    items = MarketSerializer(many=True)  # A nested list of 'edit' items.


class AhSerializer(serializers.Serializer):
    value = serializers.FloatField(read_only=True)
    date = serializers.CharField(required=False)


class AhIndexSerializer(serializers.Serializer):
    items = AhSerializer(many=True)  # A nested list of 'edit' items.


class SwSerializer(serializers.Serializer):
    BargainDate = serializers.IntegerField(required=False)
    PB = serializers.FloatField(read_only=True)
    PE = serializers.FloatField(read_only=True)
    TurnoverRate = serializers.CharField(read_only=True)


class SwIndexSerializer(serializers.Serializer):
    items = SwSerializer(many=True)  # A nested list of 'edit' items.


class StockSerializer(serializers.Serializer):
    code = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    current = serializers.FloatField(read_only=True)
    amount = serializers.IntegerField(read_only=True)
    percentage = serializers.FloatField(read_only=True)
    change = serializers.FloatField(read_only=True)
    market = serializers.FloatField(read_only=True)
    ratio = serializers.FloatField(read_only=True)
    close = serializers.FloatField(read_only=True)
    volume = serializers.FloatField(read_only=True)
    timestamp = serializers.IntegerField(read_only=True)
    turn_rate = serializers.FloatField(read_only=True)


class StockListSerializer(serializers.Serializer):
    items = StockSerializer(many=True)  # A nested list of 'edit' items.


class PortfolioSerializer(serializers.Serializer):
    date = serializers.CharField(required=False)
    list = StockSerializer(many=True)  # A nested list of 'edit' items.
    market_value = serializers.FloatField(read_only=True)
    cash = serializers.FloatField(read_only=True)
    total = serializers.FloatField(read_only=True)
    net_asset = serializers.FloatField(read_only=True)
    cost = serializers.FloatField(read_only=True)
    cost_zs = serializers.FloatField(read_only=True)
    cost_ht1 = serializers.FloatField(read_only=True)
    cost_ht2 = serializers.FloatField(read_only=True)
    position_ratio = serializers.FloatField(read_only=True)
    financing = serializers.FloatField(read_only=True)
    lever = serializers.FloatField(read_only=True)
    profit = serializers.FloatField(read_only=True)
    profit_ratio = serializers.FloatField(read_only=True)
    profit_today = serializers.FloatField(read_only=True)
    profit_ratio_today = serializers.FloatField(read_only=True)


class PortfolioListSerializer(serializers.Serializer):
    items = PortfolioSerializer(many=True)  # A nested list of 'edit' items.


class DividendSerializer(serializers.Serializer):
    id = serializers.CharField(required=False)
    date = serializers.CharField(required=True)
    money = serializers.FloatField(required=True)
    description = serializers.CharField(required=False)

    def create(self, validated_data):
        """ Create and return a new `Text` instance, given the validated data. """
        return Dividend.objects.create(**validated_data)


class DividendListSerializer(serializers.Serializer):
    list = DividendSerializer(many=True)