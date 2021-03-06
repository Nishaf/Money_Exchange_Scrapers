import requests
from selenium import webdriver
from pyvirtualdisplay import Display
from bs4 import BeautifulSoup
from pymongo import MongoClient
from bank_scrapers import add_to_database
import datetime

class BMO:
    def __init__(self):
        self.url = "https://www.bmo.com/home/personal/banking/rates/foreign-exchange"
        self.display = Display(visible=0, size=(1500, 800))
        self.display.start()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome('/home/Money_Exchange_Scrapers/chromedriver', chrome_options=chrome_options)#('/home/nishaf/chromedriver')#
        mongo = MongoClient("mongodb://harmitkamboe:harmitkamboe!!fxratehunter!!.com@127.0.0.1/admin")
        self.db = mongo['transfer_rates']
        self.run()
        self.driver.quit()
        mongo.close()

    def get_country_list(self):
        currencies = self.db.country_list.find()
        country_list = []
        for i in currencies:
            country_list.append(i['country_name'])
        return country_list

    def check_date(self, time):
        mongo = MongoClient("mongodb://harmitkamboe:harmitkamboe!!fxratehunter!!.com@127.0.0.1/admin")
        db = mongo['transfer_rates']
        items = db['records']

        item = items.find({'time': time}).count()
        mongo.close()
        if item > 0:
            self.up_to_date = True
            return True
        else:
            self.up_to_date = False
            return False

    def get_date(self):
        date = datetime.datetime.now()
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

    def run(self):
        try:
            self.driver.get(self.url)
            soup = BeautifulSoup(self.driver.page_source)
            table = soup.find('table', attrs={'id': 'ratesTable'})
            tr = table.find_all('tr')
            headers = tr[0]
            headers = headers.find_all('th')
            headers = [(i.text).strip() for i in headers]
            print(headers[0] + "   " + headers[1] + "   " + headers[3] + "       1CAD = ?")
            time = soup.find('p', attrs={'class': 'first bold'})
            time.find('script').replaceWith('')
            time = (time.text).strip()

            if self.check_date(time):
                return
            text = ["Foreign exchange rates are subject to change at any time."]
            data = tr[1:]
            country_list = self.get_country_list()
            for row in data:
                td = row.find_all('td')
                string = ""
                country = td[0].text
                if country == 'United Kingdom':
                    country = 'Great Britain'
                if country in country_list:
                    try:
                        convert = str(1.0 / float(td[3].text))
                    except:
                        convert = None

                    data1 = self.db.country_list.find_one({'country_name': country})
                    string += td[0].text + "   " + td[1].text + "   " + td[3].text + "   ===============>  " + convert
                    # print('Bank of Montreal',country,data1['currency'],data1['cur_sign'],
                    #                '$40.00', '3 to 4 business days', convert, time, text,
                    #                'img/web_logo/bmo1.jpg', 'https://www.bmo.com/home/personal/banking/rates/foreign-exchange')
                    add_to_database(self.db.records, 'Bank of Montreal', country, data1['currency'], data1['cur_sign'],
                                    '$40.00', self.get_date(), convert, time, text,
                                    'img/web_logo/bmo1.jpg',
                                    'https://www.bmo.com/home/personal/banking/rates/foreign-exchange')
                    # print(string)

        except Exception as e:
            print(e)
            self.driver.quit()
        '''
        table = soup.find('table', attrs={'id': 'ratesTable'})
        tr = table.find_all('tr')
        headers = tr[0]
        headers = headers.find_all('th')
        headers = [(i.text).strip() for i in headers]
        print(headers[0] + "   " + headers[1] + "   " + headers[3] + "       1CAD = ?")

        data = tr[1:]
        currencies = ['USD', 'GBP', 'INR', 'MXN', 'PKR', 'PHP']
        for row in data:
            td = row.find_all('td')
            string = ""
            currency = td[1].text
            currency= currency[currency.find("(") + 1:currency.find(")")]
            if currency in currencies:
                try:
                    convert = str(1.0 / float(td[3].text))
                except:
                    convert = td[2].text
                string += td[0].text + "   " + td[1].text + "   " + td[3].text + "   ===============>  " + convert

                print(string)
        '''


