'''
Created on 2011-3-16

@author: JCB-SJR-102
'''

class stockmarket(object):
    '''
    classdocs
    '''
    ssgs = 0
    sszq = 0
    ssgp = 0
    totalShares = 0
    totalFloatingShares = 0
    totalCap = 0
    totalMarketCap = 0
    marketPe = 0
    avgPrice = 0;
    

    def __init__(self):
        '''
        Constructor
        '''
    def __str__(self):
        #self.pe = self.current/self.mgsy
        if self.totalFloatingShares !=0:
            self.avgPrice = self.totalMarketCap/self.totalFloatingShares
        return 'PE:'+str(self.marketPe)+'**avgPrice:'+str('%.2f'%self.avgPrice)+'**totalCap:'+str(self.totalCap)+'**marketCap:'+str(self.totalMarketCap)+'**totalShares:'+str(self.totalShares)+'**totalFloatingShares:'+str(self.totalFloatingShares)+'**ssgs:'+str(self.ssgs)+'**sszq:'+str(self.sszq)+'**ssgp:'+str(self.ssgp)
        