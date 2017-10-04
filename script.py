from pymongo import MongoClient

mongo = MongoClient()

db = mongo['transfer_rates']

db.records.remove()

mongo.close()