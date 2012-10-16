'''
Created on 2012-10-16

@author: Simon
'''
from stocktrace.util import settings
from stocktrace.parse.sinaparser import getMyStock   
import time, os, sys, sched

#real time polling stock price periodically
class Monitor(object):
    def __init__(self):
        self.schedule = sched.scheduler(time.time, time.sleep)
        self.interval = settings.POLLING_INTERVAL
        self._running = False

    def periodic(self, action, actionargs=()):
        if self._running:
            self.event = self.schedule.enter(self.interval, 1, self.periodic,
              (action, actionargs)
            )
            action(*actionargs)

    def start(self):
        self._running = True
        self.periodic(getMyStock)
        self.schedule.run( )

    def stop(self):
        self._running = False
        if self.schedule and self.event:
            self.schedule.cancel(self.event)
            
if __name__ =="__main__":    
    #startMonitor();
    monitor = Monitor()
    monitor.start()