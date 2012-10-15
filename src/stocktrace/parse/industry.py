'''
Created on 2011-3-28

@author: simon
'''

class Industry(object):
    '''
    classdocs
    '''
    name = ''
    PE = 0
    avgPrice = 0


    def __init__(self):
        '''
        Constructor
        '''
    def __str__(self):
        return str(self.name)+'**PE:'+str('%.2f'%self.PE)+'**avgPrice:'+str(self.avgPrice)