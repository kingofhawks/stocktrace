#download securities list,statistics data,history price data

if __name__ == '__main__':	
	from download import download
	from util import settings
	download(True,stockList=settings.STOCK_LIST);

			

