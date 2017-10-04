from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup
from pyvirtualdisplay import Display
from bank_scrapers import *
from pymongo import MongoClient


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
        self.driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=chrome_options)
        self.mongo = MongoClient()
        db = self.mongo['transfer_rates']
        self.records = db['records']

    def run_scraper(self, url, soup):
        if 'royalbank' in url:
            royal_bank(soup, self.records)
        elif 'tdcommercial' in url:
            tdcommercialbanking(soup, self.records)
        elif 'bmo' in   url:
            bmo(soup, self.records)
        elif 'scotia' in url:
            scotia_bank(soup, self.records)
        elif 'hsbc' in url:
            hsbc(soup, self.records)

    def run(self):
        for i in self.urls:
            print('Scraping ====>  ' + i)
            self.driver.get(i)
            soup = BeautifulSoup(self.driver.page_source)
            self.run_scraper(i, soup)

        self.mongo.close()
        self.driver.close()


if __name__ == "__main__":
    time_break = 1
    while True:
        Main_Scraper().run()
        print("Going to Sleep for " + str(time_break * 60) + ' seconds!!')
        sleep(int(time_break) * 60)