if __name__ == '__main__':
	from parse.yahooparser import downloadHistoryData,parseTickers
	from dao.stockdao import clear
	from parse.sseparser import parseQuoteList
	#clear();
	#parseQuoteList(True)
	#parseTickers(begin=600484,end=603366);
	downloadHistoryData()

			

