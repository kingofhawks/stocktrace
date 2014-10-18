'''
Created on 2012-10-12

@author: Simon
'''
import pika
from util import settings

connection = pika.BlockingConnection(pika.ConnectionParameters(
               settings.RABBIT_SERVER))
channel = connection.channel()
channel.queue_declare(queue='hello')
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
connection.close()