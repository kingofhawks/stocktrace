#download securities list,statistics data,history price data

if __name__ == '__main__':	
	from download import download
	from stocktrace.util import settings
	download(clearAll= True,downloadLatest = True,downloadHistory = True,parse_industry = False,stockList=settings.STOCK_LIST_TOP100);

			

