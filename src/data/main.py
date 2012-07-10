if __name__ == '__main__':
	from parse.yahooparser import downloadHistoryData,parseTickers
	from dao.stockdao import clear
	clear();
	parseTickers();
	downloadHistoryData()

			

