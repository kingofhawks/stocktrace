#download securities list,statistics data,history price data
import logging

if __name__ == '__main__':
	from parse.yahooparser import downloadHistoryData,parseTickers
	from dao.stockdao import clear,findAllExistentTickers
	from parse.sseparser import downloadQuoteList
	from parse.reutersparser import downloadKeyStatDatas
	from parse.sinaparser import downloadLatestData
	
	logging.basicConfig(filename='stocktrace.log', level=logging.INFO)
	logging.info('***Start download finance data****')
    
	clear();
	#download securities list from sse
	downloadQuoteList(True,stockList='stock_list')
	#download statistics from reuters
	downloadKeyStatDatas()
	quotes = findAllExistentTickers()
	#download history data from yahoo
	downloadHistoryData(quotes)
	#update latest price from sina
	downloadLatestData(quotes,'yahoo')
	
	logging.info('***Finish download finance data****')

			

