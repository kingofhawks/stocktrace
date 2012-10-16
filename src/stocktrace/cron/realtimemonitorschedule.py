'''
Created on 2012-8-15

@author: Simon
'''
#@Deprecated now,please use monitor.py instead
from stocktrace.util import settings
import time, os, sys, sched
schedule = sched.scheduler(time.time, time.sleep)
event = None

def periodic(scheduler, interval, action, actionargs=()):
  event = scheduler.enter(interval, 1, periodic,
                  (scheduler, interval, action, actionargs))
  action(*actionargs)
  #scheduler.run( )
  return event
  
  
def startMonitor():    
    from stocktrace.parse.sinaparser import getMyStock
    
#    schedule.enter(0, 0, getMyStock, ())   # 0==right now
#    schedule.run( )
    event = periodic(schedule, settings.POLLING_INTERVAL, getMyStock)
    schedule.run( )
    
def stopMonitor():
    if event is not None:
        schedule.cancel(event)
    
    sys.exit()   
    #pass
  
if __name__ =="__main__":    
    #startMonitor();
    stopMonitor()
  