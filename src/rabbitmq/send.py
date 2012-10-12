'''
Created on 2012-10-12

@author: Simon
'''
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
               '172.25.21.160'))
channel = connection.channel()
channel.queue_declare(queue='hello')
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
connection.close()