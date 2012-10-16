'''
Created on 2012-10-12

@author: Simon
'''
import pika
import sys
from util import settings

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=settings.RABBIT_SERVER))
channel = connection.channel()

channel.exchange_declare(exchange='topic_logs',
                         type='topic')

routing_key = sys.argv[1] if len(sys.argv) > 1 else 'anonymous.info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'
channel.basic_publish(exchange='topic_logs',
                      routing_key=routing_key,
                      body=message)
print " [x] Sent %r:%r" % (routing_key, message)
connection.close()