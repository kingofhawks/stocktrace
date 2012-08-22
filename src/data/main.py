#download securities list,statistics data,history price data
if __name__ == '__main__':
	from parse.yahooparser import downloadHistoryData,parseTickers
	from dao.stockdao import clear
	from parse.sseparser import downloadQuoteList
	from parse.reutersparser import downloadKeyStatDatas
	from parse.sinaparser import downloadLatestData
	clear();
	#download securities list from sse
	downloadQuoteList(True)
	#download statistics from reuters
	downloadKeyStatDatas()
	#download history data from yahoo
	downloadHistoryData()
	#update latest price from sina
	downloadLatestData()

			

