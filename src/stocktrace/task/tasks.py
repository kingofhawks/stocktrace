#usage:
#under current directory: celery -A tasks worker --loglevel=info
#python run_tasks.py
#you could use flower to monitor Celery:
#celery flower --broker=redis://guest:guest@localhost:6379/0

from __future__ import absolute_import

from celery import Celery

broker = 'redis://192.168.72.128:6379/0'
app = Celery('tasks', broker=broker,backend=broker)


@app.task()
def add(x, y):
    return x + y

if __name__ == '__main__':
    app.start()
