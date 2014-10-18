__author__ = 'Simon'

MONGOHQ_URL= 'mongodb://kingofhawks:lazio_2000@dharma.mongohq.com:10089/stocktrace'
import os
import datetime
import pymongo
from pymongo import MongoClient

# Grab our connection information from the MONGOHQ_URL environment variable
# (mongodb://linus.mongohq.com:10045 -u username -pmy_password)
MONGO_URL = os.environ.get('MONGOHQ_URL')
#connection = Connection(MONGO_URL)
client = MongoClient('mongodb://dharma.mongohq.com:10089 -u kingofhawks -plazio_2000')
print client
# Specify the database
db = client.mytestdatabase
# Print a list of collections
print db.collection_names()

# Specify the collection, in this case 'monsters'
collection = db.monsters

# Get a count of the documents in this collection
count = collection.count()
print "The number of documents you have in this collection is:", count

# Create a document for a monster
monster = {"name": "Dracula",
           "occupation": "Blood Sucker",
           "tags": ["vampire", "teeth", "bat"],
           "date": datetime.datetime.utcnow()
           }

# Insert the monster document into the monsters collection
monster_id = collection.insert(monster)

# Print out our monster documents
for monster in collection.find():
    print monster

# Query for a particular monster
print collection.find_one({"name": "Dracula"})
