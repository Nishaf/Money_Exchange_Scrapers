from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup
from pyvirtualdisplay import Display
from bank_scrapers import *
from pymongo import MongoClient
from datetime import datetime
class Main_Scraper:
    def __init__(self):
        self.urls = [
            'http://www.rbcroyalbank.com/rates/rates/cashrates.html',
            'https://www.tdcommercialbanking.com/rates/index.jsp',
            'https://www.bmo.com/home/personal/banking/rates/foreign-exchange',
            'http://www.scotiabank.com/ca/en/0,,1118,00.html',
            'http://www.hsbc.ca/1/2/personal/banking/accounts/foreign-currency-accounts/foreign-currency-exchange',
        ]
        self.display = Display(visible=0, size=(1500, 800))
        self.display.start()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome('/home/Money_Exchange_Scrapers/chromedriver', chrome_options=chrome_options)#('/home/nishaf/chromedriver')#
        self.mongo = MongoClient()
        db = self.mongo['transfer_rates']
        self.records = db['records']
        self.country_list = db['country_list']

    def run_scraper(self, url, soup):
        if 'royalbank' in url:
            royal_bank(soup, self.records,self.country_list)
        elif 'tdcommercial' in url:
            tdcommercialbanking(soup, self.records, self.country_list)
        elif 'bmo' in   url:
            bmo(soup, self.records, self.country_list)
        elif 'scotia' in url:
            scotia_bank(soup, self.records, self.country_list)
        elif 'hsbc' in url:
            hsbc(soup, self.records, self.country_list)

    def run(self):
        for i in self.urls:
            print('Scraping ====>  ' + i)
            self.driver.get(i)
            soup = BeautifulSoup(self.driver.page_source)
            self.run_scraper(i, soup)

        self.mongo.close()
        self.driver.close()



if __name__ == '__main__':
    time_break = 720
    while True:
        print("Starting Time: " + str(datetime.now()))
        Main_Scraper().run()
        print("Going to Sleep for " + str(time_break * 60) + ' seconds!!')
        print("Ending Time: " + str(datetime.now()))
        print("Going to Sleep")
        sleep(int(time_break) * 60)




'''
try:
    mongo = MongoClient('mongodb://45.56.221.44:27017')
except:
    print("connection refused")
try:
    db = mongo['transfer_rates']
    item = db['records']

    print(item.count())
except:
    print('db not available')
'''

