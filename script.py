from pymongo import MongoClient

mongo = MongoClient("mongodb://45.56.221.43:27017")
db = mongo['transfer_rates']
items = db['flags']
print(items.count())

mongo.close()