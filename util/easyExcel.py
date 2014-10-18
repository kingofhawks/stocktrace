#!/usr/bin/env python
from win32com.client import constants, Dispatch

class EasyExcel:

     def __init__(self, filename=None):
        self.xlApp = Dispatch('Excel.Application')
        if filename:
            self.filename = filename
            self.xlBook = self.xlApp.Workbooks.Open(filename)
        else:
           print "please input the filename"

     def close(self):
        self.xlBook.Close(SaveChanges=0)
        del self.xlApp
     
     
     def getCell(self, sheet, row, col):
        "Get value of one cell"
        sht = self.xlBook.Worksheets(sheet)
        return sht.Cells(row, col).Value
   
     def getRange(self, sheet, row1, col1, row2, col2):
        "return a 2d array (i.e. tuple of tuples)"
        sht = self.xlApp.Worksheets(sheet)
        return sht.Range(sht.Cells(row1, col1), sht.Cells(row2, col2)).Value
	
		
     def getAllSheets(self):
	return self.xlApp.Worksheets

     def getSheetByName(self,sheet):
	     if type(sheet) is int:
		return self.xlApp.Worksheets[sheet]
	     else:
		return self.xlApp.Worksheets(sheet)
		
     def getSheetValues(self,sheet):
	     #content = excelProxy.getRange(sheet,2,1,line-1,5)   
	     directory = dict()
	     return 0
	     
     def getSheetLines(self,sheet):
	     return 0     
     

	
if __name__ == '__main__':
	import os,sys
	root = os.path.abspath(os.path.dirname(sys.argv[0]))
	print '*******root path*****'+root
	path = root+'\\test.xls'	
	excelProxy = EasyExcel(path)
	for sheets in excelProxy.getAllSheets():
		print sheets.name
	print excelProxy.getSheetByName('2')
	print excelProxy.getSheetByName(0).Rows.count
    
	
