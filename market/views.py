import pymongo
from django.shortcuts import render
DB_NAME = 'stocktrace'
DB_HOST = 'localhost'
db = getattr(pymongo.MongoClient(host=DB_HOST), DB_NAME)


# Create your views here.
def sw(request):
    return render(request, 'sw.html')


def cs_index(request):
    name = request.GET.get('name') or '上海A股'
    index_group = db.index.aggregate([{"$group": {"_id": "$name"}}], cursor={})
    index_list = list(index_group)
    for index in index_list:
        index['name'] = index.get('_id')
    print(index_list)
    return render(request, 'cs_index.html', {'name': name, 'indexes': index_list})


def industry(request):
    code = request.GET.get('code') or '00'
    industry_col = db.industry.aggregate([{"$group": {"_id": {"code": "$code", "name": "$name"}}}], cursor={})
    industry_list = list(industry_col)
    # print(industry_list)
    industry_list = list(map(lambda x: x.get('_id'), industry_list))
    print(industry_list)
    return render(request, 'industry.html', {'code': code, 'industry_list': industry_list})


def equity(request):
    code = request.GET.get('code') or '00'

    return render(request, 'equity.html', {'code': code})


def history(request):
    code = request.GET.get('code') or 'SH600420'
    return render(request, 'stock_history.html', {'code': code})


def diff(request):
    code = request.GET.get('code') or 'SH600029,SH601111'
    return render(request, 'stock_diff.html', {'code': code})


def sh(request):
    return render(request, 'sh.html')


