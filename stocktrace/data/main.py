#download securities list,statistics data,history price data
from download import download
from stocktrace.util import settings

if __name__ == '__main__':
	download(clearAll=True, downloadLatest=True, downloadHistory=True,
        parse_industry=False, stockList=settings.STOCK_LIST_TOP100);

			

