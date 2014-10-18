class Trading(object):
	#init method called after new instance
    def __init__(self, code, count,volume, revenue):
        self.code = code
        self.count  = count
        self.volume  = volume
        self.revenue  = revenue
	
     #toString method
    def __str__(self):
	    return '***code:'+str(self.code)+'***volume:'+str(self.volume)+'***revenue:'+str(self.revenue)
	
    def add(self,volume,revenue):
	 self.volume += abs(volume)
	 self.revenue += revenue
	 self.count += 1

    def add2(self,trade):
	self.add(trade.volume,trade.revenue)
	
if __name__ == '__main__':
	t1 = Trading('600789',0,1000,100)
	t2 = Trading('600789',1,-1000,100)
	t1.add2(t2)
	print t1
	    
