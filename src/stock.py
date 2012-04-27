#from datetime import date
class Stock:
	mgsy = 0
	mgjzc = 0
	pe = 0;#dynamic PE
	lastYearPe = 0#last year PE
	pb = 0;
	rank = 0;
	lastUpdate = '';
	totalCap = 0;
	floatingCap = 0;
	date = '';
	close = 0 ;
	openPrice = 0;
	volume = 0;
	hasGap = False;
	def __init__(self,code,current=0,percent=0,low=0,high=0):
		self.code = code
		self.current = current
		self.percent = percent
		self.low = low
		self.high = high
		
	def __str__(self):
		#self.pe = self.current/self.mgsy
		return self.code+'**date:'+str(self.date)+'**now:'+str(self.current)+'**change:'+str('%.2f'%self.percent+'%')+'**high:'+str('%.2f'%self.high)+'**low:'+str('%.2f'%self.low)+'**open:'+str('%.2f'%self.openPrice)+'**close:'+str('%.2f'%self.close)+'**volume:'+str(self.volume)+'**PE:'+str('%.2f'%self.pe)+'**PB:'+str('%.2f'%self.pb)+'**rank:'+str('%.2f'%self.rank)+'**EPS:'+str(self.mgsy)+'**mgjzc:'+str(self.mgjzc)+'**last:'+str(self.lastUpdate)+'**totalCap:'+str('%.2f'%(self.totalCap/10000))+'**marketCap:'+str('%.2f'%(self.floatingCap/10000))
	
	def compute(self):
		if (self.lastUpdate.find('03-31')!= -1):
			self.pe = self.current/(float(self.mgsy)*4)
			#print '03-31'			
		elif (self.lastUpdate.find('06-30')!= -1):
			self.pe = self.current/(float(self.mgsy)*4/2)
			#print '06-30'			
		elif (self.lastUpdate.find('09-30')!= -1):
			self.pe = self.current/(float(self.mgsy)*4/3)	
			#print '09-30'		
		elif (self.lastUpdate.find('12-31')!= -1):
			self.pe = self.current/float(self.mgsy)	
			#print '12-31'
		if (self.mgjzc!= 0):
			self.pb = self.current/float(self.mgjzc)
		self.rank = self.pe * self.pb
		pass 

if __name__ == "__main__":
	stock = Stock('601766')
	print stock
	