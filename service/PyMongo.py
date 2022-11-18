import pymongo
import os

class db_driver(object):
   connection = None
   def __init__(self):
      if db_driver.connection is None:
         try:
            mongo_url=os.getenv('MONGO_URL')
            db_driver.connection = pymongo.MongoClient(mongo_url)
         except Exception as error:
            print("Error: Connection not established {}".format(error))
         else:
            print("Connection established")
