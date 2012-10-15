'''
Created on 2012-8-15

@author: Simon
'''
from stocktrace.util import settings

def periodic(scheduler, interval, action, actionargs=()):
  scheduler.enter(interval, 1, periodic,
                  (scheduler, interval, action, actionargs))
  action(*actionargs)
  #scheduler.run( )
  
  
def startMonitor():
    import time, os, sys, sched
    from stocktrace.parse.sinaparser import getMyStock
    schedule = sched.scheduler(time.time, time.sleep)
#    schedule.enter(0, 0, getMyStock, ())   # 0==right now
#    schedule.run( )
    periodic(schedule, settings.POLLING_INTERVAL, getMyStock)
    schedule.run( )
  
  
if __name__ =="__main__":    
    startMonitor();
  