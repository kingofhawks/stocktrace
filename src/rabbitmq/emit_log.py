'''
Created on 2012-10-12

@author: Simon
'''
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='172.25.21.160'))
channel = connection.channel()

channel.exchange_declare(exchange='logs',
                         type='fanout')

message = ' '.join(sys.argv[1:]) or "info: Hello World!"
channel.basic_publish(exchange='logs',
                      routing_key='',
                      body=message)
print " [x] Sent %r" % (message,)
connection.close()