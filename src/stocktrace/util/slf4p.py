'''
Created on 2012-9-20
logging wrapper class
@author: Simon
'''
import logging,os
log_dir = os.path.join('E:\Dropbox\Workspace\stocktrace', "log")
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
    