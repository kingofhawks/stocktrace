import pymongo
from django.shortcuts import render
from market.cix import cix as cix2
DB_NAME = 'stocktrace'
DB_HOST = 'localhost'
db = getattr(pymongo.MongoClient(host=DB_HOST), DB_NAME)


# Create your views here.
def sw(request):
    return render(request, 'sw.html')


def cs_index(request):
    name = request.GET.get('name') or '上海A股'
    return render(request, 'cs_index.html', {'name': name})


def industry(request):
    code = request.GET.get('code') or '00'
    industry_col = db.industry.find()
    print(industry_col)
    industry_list = list(industry_col)
    print(industry_list)
    # for industry in industry_list:

    return render(request, 'industry.html', {'code': code, 'industry_list': industry_list})


def history(request):
    code = request.GET.get('code') or 'SH600029'
    return render(request, 'stock_history.html', {'code': code})


def diff(request):
    code = request.GET.get('code') or 'SH600029,SH601111'
    return render(request, 'stock_diff.html', {'code': code})


def sh(request):
    return render(request, 'sh.html')


def cix(request):
    cix_index = cix2()
    # print cix_index
    return render(request, 'cix.html', {'cix': cix_index})
