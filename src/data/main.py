if __name__ == '__main__':
	from parse.yahooparser import downloadHistoryData,parseTickers
	from dao.stockdao import clear
	from parse.sseparser import downloadQuoteList
	from parse.reutersparser import downloadKeyStatDatas
	clear();
	downloadQuoteList(True)
	downloadKeyStatDatas()
	downloadHistoryData()

			

