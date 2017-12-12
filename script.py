
'''
from pymongo import MongoClient

mongo = MongoClient("mongodb://45.56.221.43:27017")
db = mongo['transfer_rates']
items = db['flags']
print(items.count())

mongo.close()
'''

import datetime


def get_date():
    date = datetime.datetime.now() + datetime.timedelta(2)
    print(date)
    if date.weekday() in [0, 1]:
        date += datetime.timedelta(3)
    elif date.weekday() in [2,3,4,5]:
        print(3)
        date += datetime.timedelta(5)
    elif date.weekday() == 6:
        print(6)
        date += datetime.timedelta(4)

    print("Print Date:" + str(date.strftime("%Y-%m-%d")))
    return date.strftime("%Y-%m-%d")




