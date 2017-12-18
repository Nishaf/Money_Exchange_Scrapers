from bs4 import BeautifulSoup
from pyvirtualdisplay import Display
from selenium import webdriver
from pymongo import MongoClient
from bank_scrapers import add_to_database
import datetime


class HSBCBank:
    def __init__(self):
        self.url = "http://www.hsbc.ca/1/2/personal/banking/accounts/foreign-currency-accounts/foreign-currency-exchange"
        self.display = Display(visible=0, size=(1500, 800))
        self.display.start()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome('/home/Money_Exchange_Scrapers/chromedriver', chrome_options=chrome_options)#('/home/nishaf/chromedriver')#
        mongo = MongoClient("mongodb://hkamboe:hkamboefxratehunter8080!!@127.0.0.1/transfer_rates")
        self.db = mongo['transfer_rates']
        self.run()
        self.driver.quit()
        mongo.close()

    def check_date(self, time):
        mongo = MongoClient("mongodb://hkamboe:harmitkamboe!!fxratehunter!!.com@127.0.0.1/transfer_rates")
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
        if date.weekday() in [0, 1]:
            date += datetime.timedelta(3)
        elif date.weekday() in [2, 3, 4, 5]:
            print(3)
            date += datetime.timedelta(5)
        elif date.weekday() == 6:
            print(6)
            date += datetime.timedelta(4)

        print("Print Date:" + str(date.strftime("%Y-%m-%d")))
        return date.strftime("%Y-%m-%d")

    def run(self):
        try:
            self.driver.get(self.url)
            soup = BeautifulSoup(self.driver.page_source)

            table = soup.find('table', attrs={'class': 'hsbcTableStyleViewRates'})
            tr = table.find_all('tr')
            headers = tr[0]
            headers = headers.find_all('th')
            data = tr[1:]
            print(headers[0].text + "   " + headers[1].text + "   " + headers[2].text + "        1 CAD = ?")
            time = (soup.find('div', attrs={'class': 'hsbcTextStyle15'}).text).strip()

            if self.check_date(time):
                return

            text = ['Rates are subject to change without notice.']
            country_data = self.db.country_list.find()
            print(len(data))
            for i in country_data:
                for row in data:
                    td = row.find_all('td')
                    if i['currency'] == td[1].text:
                        try:
                            convert = str(1.0 / float(td[2].text))
                        except:
                            convert = None

                        # print(td[0].text + "   " + td[1].text + "   " + td[2].text + "  =============> " + convert)
                        # print('HSBC Bank',i['country_name'],  i['currency'],i['cur_sign'],
                        #                '$40.00', '3 to 4 business days', convert, time, text,
                        #                'img/web_logo/hsbc-logo.gif')

                        add_to_database(self.db.records, 'HSBC Bank', i['country_name'], i['currency'], i['cur_sign'],
                                        '$40.00', self.get_date(), convert, time, text,
                                        'img/web_logo/hsbc-logo.png',
                                        'http://www.hsbc.ca/1/2/personal/banking/accounts/foreign-currency-accounts/foreign-currency-exchange')
        except Exception as e:
            print(e)
            self.driver.quit()
    '''
    table = soup.find('table', attrs={'class': 'hsbcTableStyleViewRates'})
        tr = table.find_all('tr')
        headers = tr[0]
        headers = headers.find_all('th')
        data = tr[1:]
        print(headers[0].text + "   " + headers[1].text + "   " + headers[2].text + "        1 CAD = ?")
        currencies = ['USD', 'GBP', 'INR', 'MXN', 'PKR', 'PHP']
        text = soup.find('div', attrs={'class': 'hsbcTextStyle15'}).text
        text += '\n' + 'Rates are subject to change without notice.'
        print(text)
        for row in data:
            td = row.find_all('td')
            currency = td[1].text
            if currency in currencies:
                try:
                    convert = str(1.0 / float(td[2].text))
                except:
                    convert = td[2].text
                print(td[0].text + "   " + td[1].text + "   " + td[2].text + "  =============> " + convert)
        '''
