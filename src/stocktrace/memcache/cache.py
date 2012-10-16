'''
Created on 2012-10-16

@author: Simon
'''
import memcache
mc = memcache.Client(['172.25.21.16:11211'], debug=0)
print mc

mc.set("some_key", "Some value")
value = mc.get("some_key")
print value
print mc.get('key1')

mc.set("another_key", 3)
mc.delete("another_key")

mc.set("key", "1")   # note that the key used for incr/decr must be a string.
mc.incr("key")
mc.decr("key")