import pymongo
import os
import ssl
import certifi
from urllib.request import urlopen

# from dotenv import load_dotenv
# load_dotenv()

class db_driver(object):
   connection = None
   def __init__(self):
      if db_driver.connection is None:
         try:
            mongo_url=os.environ['MONGO_URL']
            db_driver.connection = pymongo.MongoClient(mongo_url,tlsCAFile=certifi.where())
         except Exception as error:
            print("Error: Connection not established {}".format(error))
         else:
            print("Connection established")
