from django.shortcuts import render
import os
from django.shortcuts import render, render_to_response
from portfolio.dao import *
from stocktrace.stock import Stock
from portfolio.portfolio import  snapshot, market_value
from django.http import HttpResponse
import json
from django.shortcuts import redirect
from django.urls import reverse
# to resolve datetime type JSON serialization issue
from bson import json_util


def stock_list(request):
    portfolio = snapshot(False)
    results = portfolio.stocks
    # print 'result:{}'.format(results)

    context = {'results': results, 'market_value': portfolio.market_value, 'total': portfolio.total,
               'net_asset': portfolio.net_asset,
               'position_ratio': portfolio.position_ratio, 'financing': portfolio.financing,
               'lever': portfolio.lever, 'profit_ratio': portfolio.profit_ratio}
    return render(request, 'portfolio/index.html', context)


def portfolio_detail(request, pk):
    portfolio = find_portfolio(pk)
    # print 'portfolio:{}'.format(portfolio)
    results = portfolio.get('stocks')
    # print results
    real_time_market = market_value(results)
    # print 'real time market:{}'.format(real_time_market)
    context = {'results': results, 'name':portfolio.get('name'),
               'market_value': portfolio.get('market_value'), 'real_time_market': real_time_market,
               'total': portfolio.get('total'),
               'position_ratio': portfolio.get('position_ratio')}
    return render(request, 'portfolio/index.html', context)


def tag(request, pk):
    # print pk
    results = find_stocks_by_tag(pk)
    # print results

    return render(request, 'stock/tag.html', {'results': results})


def apply_tag(request, tag):
    # print tag
    results = find_stocks_by_tag(tag)
    # print results

    return render(request, 'stock/tag.html', {'results': results})


def detail(request):
    # print '*'*10
    stock = find_stock_by_code(request.GET.get('code'))
    # print stock
    # print json.loads(stock)
    # print type(stock)
    #You can not directly dumps mongodb cursor to JSON
    from bson import json_util
    return HttpResponse(json.dumps(stock, sort_keys=True, indent=4, default=json_util.default),
                        content_type='application/json')


def create_stock(request):
    code = request.GET.get('code')
    amount = request.GET.get('amount')
    stock_tag = request.GET.get('tag')
    # print 'code:{},amount:{},tag:{}'.format(code, amount, stock_tag)
    stock = Stock(code, amount=amount)
    stock.save()
    # insert_stock(stock)
    add_tag(code, 'top100')
    return render_to_response('portfolio/index.html')


def update(request):
    code = request.GET.get('code')
    amount = request.GET.get('amount')
    up_threshold = request.GET.get('up_threshold')
    down_threshold = request.GET.get('down_threshold')
    # print 'code:{0},amount:{1},up_threshold:{2},down_threshold:{3}'.format(code, amount,
    #                                                                        up_threshold, down_threshold)
    update_stock_amount(code, amount, up_threshold, down_threshold)
    return render_to_response('portfolio/index.html')


def delete(request, pk):
    # print pk
    delete_stock(pk)

    return redirect(reverse('portfolio:home'))


def snapshot_view(request):
    portfolio = snapshot(True)
    # print 'snapshot:{}'.format(portfolio)
    data = json.dumps(portfolio, default=json_util.default)
    # print 'data:{}'.format(data)
    return HttpResponse(data, content_type='application/json')


def history(request):
    #generate history for today
    # delete_portfolio_today()
    # snapshot()

    results = find_all_portfolio()

    #return HttpResponse(json.dumps(results, default=json_util.default), content_type='application/json')
    data = json.dumps(results, default=json_util.default)
    # print 'data:{}'.format(data)
    return render(request, 'portfolio/history.html', {'data': data})


def delete_portfolio(request, pk):
    # print 'delete portfolio:{pk}'.format(pk=pk)
    delete_portfolio_by_id(pk)
    return HttpResponse(json.dumps('OK'), content_type='application/json')

