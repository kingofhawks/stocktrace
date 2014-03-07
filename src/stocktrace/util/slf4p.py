'''
Created on 2012-9-20
logging wrapper class
@author: Simon
'''
import logging,os,settings
from stocktrace.settings import PROJECT_DIR

#print PROJECT_DIR
parent = os.path.abspath(os.path.join(PROJECT_DIR, os.pardir))
#print parent
#print os.path.join(parent, "zytj","template")
#print '**************'
#PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))
#log_dir = os.path.join(settings.APP_ROOT, "log")
log_dir = os.path.join(parent, "log")
log_name = os.path.join(log_dir, "stocktrace.log")

logging.basicConfig(filename=log_name, level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',)
#console handler
ch = logging.StreamHandler()
#ch.setLevel(logging.DEBUG)


#get a Logger from any module
def getLogger(name):
    logger = logging.getLogger(name)
    logger.addHandler(ch)
    return logger
    