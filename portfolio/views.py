from django.shortcuts import render
import os
from django.shortcuts import render, render_to_response
from dao import *
from stocktrace.stock import Stock
from portfolio import polling
from django.http import HttpResponse
import json
from django.shortcuts import redirect
from django.core.urlresolvers import reverse


def stock_list2(request):
    results = polling()
    #results = find_all_stocks()
    #logger.debug(results)
    print results
    market_value = 0
    for stock in results:
        try:
            market_value += float(stock['amount'])*float(stock['current'])
        except KeyError as e:
            pass
    print 'market_value:{}'.format(market_value)
    return render(request, 'portfolio/index.html', {'results': results, 'market_value': market_value})


def tag(request, pk):
    print pk
    results = find_stocks_by_tag(pk)
    print results

    return render(request, 'stock/tag.html', {'results': results})


def apply_tag(request, tag):
    print tag
    results = find_stocks_by_tag(tag)
    print results

    return render(request, 'stock/tag.html', {'results': results})


def detail(request):
    stock = find_stock_by_code(request.GET.get('code'))
    print stock
    # print json.loads(stock)
    # print type(stock)
    #You can not directly dumps mongodb cursor to JSON
    from bson import json_util
    return HttpResponse(json.dumps(stock, sort_keys=True, indent=4, default=json_util.default),
                        content_type='application/json')


def create_stock(request):
    code = request.GET.get('code')
    amount = request.GET.get('amount')
    tag = request.GET.get('tag')
    print 'code:{},amount:{},tag:{}'.format(code, amount, tag)
    stock = Stock(code, amount, 0)
    insert_stock(stock)
    add_tag(code, 'top100')
    return render_to_response('portfolio/index.html')


def update(request):
    code = request.GET.get('code')
    amount = request.GET.get('amount')
    up_threshold = request.GET.get('up_threshold')
    down_threshold = request.GET.get('down_threshold')
    print 'code:{0},amount:{1},up_threshold:{2},down_threshold:{3}'.format(code, amount,
                                                                           up_threshold, down_threshold)
    update_stock_amount(code, amount, up_threshold, down_threshold)
    return render_to_response('portfolio/index.html')


def delete(request, pk):
    print pk
    delete_stock(pk)

    return redirect(reverse('portfolio:home'))


def history(request):
    results = find_all_portfolio()
    print results

    # to resolve datetime type JSON serialization issue
    from bson import json_util

    #return HttpResponse(json.dumps(results, default=json_util.default), content_type='application/json')
    return render(request, 'portfolio/history.html', {'data': json.dumps(results, default=json_util.default)})

