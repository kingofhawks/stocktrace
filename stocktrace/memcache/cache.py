'''
Created on 2012-10-16

@author: Simon
'''
import memcache
#mc = memcache.Client(['172.25.21.16:11211'], debug=0)
#print mc
#
#mc.set("some_key", "Some value")
#value = mc.get("some_key")
#print value
#print mc.get('key1')
#
#mc.set("another_key", 3)
#mc.delete("another_key")
#
#mc.set("key", "1")   # note that the key used for incr/decr must be a string.
#mc.incr("key")
#mc.decr("key")

class Cache(object):
    def __init__(self):
        self.mc = memcache.Client(['172.25.21.16:11211'], debug=0)
        
    def get(self,key):
        return self.mc.get(key)
    
    def set(self,key,value):
        self.mc.set(key,value)
        
    def delete(self,key):
        self.mc.delete(key)
        
    def getmc(self):
        return self.mc
        
if __name__ =="__main__":    
    cache = Cache()
    #cache.set('key1','hello simon')
    key = '600327_10_2012-10-18'
    print cache.get(key)
    cache.delete(key)
