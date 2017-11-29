
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
    if date.weekday() in [0, 1, 2]:
        print(date.weekday())
        date += datetime.timedelta(2)
    elif date.weekday() == 3:
        print(3)
        date += datetime.timedelta(4)
    elif date.weekday() == 4:
        print(4)
        date += datetime.timedelta(4)
    elif date.weekday() == 5:
        print(5)
        date += datetime.timedelta(4)
    elif date.weekday() == 6:
        print(6)
        date += datetime.timedelta(3)

    print("Print Date:" + str(date.strftime("%Y-%m-%d")))
    return date.strftime("%Y-%m-%d")



get_date()