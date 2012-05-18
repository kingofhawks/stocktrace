if __name__ == '__main__':
	from stockutil import getStock
	getStock('sh600327')
	from lxml import etree
	from easyExcel import EasyExcel	
	from excelutil import getStockDataBySheet
	import os,sys
	root = os.path.abspath(os.path.dirname(sys.argv[0]))
	print '*******root path*****',root
	path = root +'\\2010-trade.xls'	
	try:
		excelProxy = EasyExcel(path)
		for sheets in excelProxy.getAllSheets():
			#print sheets.name
			try:
				directory = getStockDataBySheet(excelProxy,sheets.name)
				for trade in directory.values():
					print trade
			except:
				continue
			finally:
				print "=============================================="
		#print directory
	finally:
		excelProxy.close()
			

