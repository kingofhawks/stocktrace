'''
Created on 2012-10-9

@author: Simon
'''
import win32service
import win32serviceutil
import win32api
import win32con
import win32event
import win32evtlogutil
import os

class aservice(win32serviceutil.ServiceFramework):
   
   _svc_name_ = "aservice"
   _svc_display_name_ = "a service - it does nothing"
   _svc_description_ = "Tests Python service framework by receiving and echoing messages over a named pipe"
         
   def __init__(self, args):
           win32serviceutil.ServiceFramework.__init__(self, args)
           self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)           

   def SvcStop(self):
           self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
           win32event.SetEvent(self.hWaitStop)                    
         
   def SvcDoRun(self):
      import servicemanager      
      servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,servicemanager.PYS_SERVICE_STARTED,(self._svc_name_, '')) 
      
      self.timeout = 3000
      from lxml import etree
      from lxml.html import parse
      
      url = 'http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20in%20(%22'+'600327'+'%22)&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&diagnostics=true'
        
      try:
        page = parse(url).getroot()
        result = etree.tostring(page)
        print result
        servicemanager.LogInfoMsg(result)        
      except:
        servicemanager.LogInfoMsg('error parse yahoo')  
    
    
      while 1:
         # Wait for service stop signal, if I timeout, loop again
         rc = win32event.WaitForSingleObject(self.hWaitStop, self.timeout)
         # Check to see if self.hWaitStop happened
         if rc == win32event.WAIT_OBJECT_0:
            # Stop signal encountered
            servicemanager.LogInfoMsg("aservice - STOPPED")
            break
         else:
            servicemanager.LogInfoMsg("aservice - is alive and well")   
               
      
def ctrlHandler(ctrlType):
   return True
                  
if __name__ == '__main__':   
   win32api.SetConsoleCtrlHandler(ctrlHandler, True)   
   win32serviceutil.HandleCommandLine(aservice)