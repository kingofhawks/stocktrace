from django.shortcuts import render

# Create your views here.

def sw(request):
    return render(request, 'sw.html')

def history(request):
    return render(request, 'stock_history.html')
