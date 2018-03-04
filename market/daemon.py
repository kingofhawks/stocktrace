import schedule
import time
import sys
# print(sys.path)
# 不加这行在命令行模式下python daimon.py就会找不到market.parse模块
sys.path.append('G:\\OneDrive\\Workspace\\stocktrace')
from market.parse import alert_high_diff


def job():
    alert_high_diff()
    print("I'm working...")


schedule.every(3).seconds.do(job)
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)