from bs4 import BeautifulSoup
from pyvirtualdisplay import Display
from selenium import webdriver
from pymongo import MongoClient
from bank_scrapers import add_to_database
class ScotiaBank:
    def __init__(self):
        self.url = "http://www.scotiabank.com/ca/en/0,,1118,00.html"
        self.display = Display(visible=0, size=(1500, 800))
        self.display.start()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome('/home/Money_Exchange_Scrapers/chromedriver', chrome_options=chrome_options)#('/home/nishaf/chromedriver')#
        mongo = MongoClient()
        self.db = mongo['transfer_rates']
        self.run()
        self.driver.close()
        mongo.close()

    def get_country_list(self):
        currencies = self.db.country_list.find()
        country_list = []
        for i in currencies:
            country_list.append(i['country_name'])
        return country_list
    def run(self):
        self.driver.get(self.url)
        soup = BeautifulSoup(self.driver.page_source)

        table = soup.find('table', attrs={'class': 'rates'})
        tr = table.find_all('tr')
        headers = tr[0]
        headers = headers.find_all('td')
        data = tr[1:]
        print(headers[0].text + "   " + headers[1].text + "   " + headers[2].text + "        1 CAD = ?")
        time = soup.find('li', attrs={'class': 'effective-date'}).text
        text = 'Rates are provided for information purposes only and are subject to change at any time.'
        country_list = self.get_country_list()
        for row in data:
            td = row.find_all('td')
            country = td[0].text
            if country in country_list:
                try:
                    convert = str(1.0 / float(td[2].text))
                except:
                    convert = None
                # print(td[0].text + "   " + td[1].text + "   " + td[2].text + "  =============> " + convert)
                data1 = self.db.country_list.find_one({'country_name': country})
                # print('Scotia Bank',country, data1['currency'],data1['cur_sign'],
                #    '$40.00', '3 to 4 business days', convert, time, text,
                #    'img/web_logo/scotiabank.jpg','http://www.scotiabank.com/ca/en/0,,1118,00.html')
                add_to_database(self.db.records, 'Scotia Bank', country, data1['currency'], data1['cur_sign'],
                                '$40.00', '3 to 4 business days', convert, time, text,
                                'img/web_logo/scotiabank.jpg', 'http://www.scotiabank.com/ca/en/0,,1118,00.html')

    '''
    table = soup.find('table', attrs={'class': 'rates'})
        tr = table.find_all('tr')
        headers = tr[0]
        headers = headers.find_all('td')
        data = tr[1:]
        print(headers[0].text + "   " + headers[1].text + "   " + headers[2].text + "        1 CAD = ?")
        text = soup.find('li', attrs={'class': 'effective-date'}).text
        text += '.\n' + 'Rates are provided for information purposes only and are subject to change at any time.'
        print(text)
        currencies = ['USD', 'GBP', 'INR', 'MXN', 'PKR', 'PHP']


        country_list= self.get_country_list()
        euro = data[1]
        euro = euro.find_all('td')

        for row in data:
            td = row.find_all('td')
            currency = td[1].text
            currency= currency[currency.find("(") + 1:currency.find(")")]
            if currency in currencies:
                try:
                    convert = str(1.0 / float(td[2].text))
                except:
                    convert = td[2].text
                print(td[0].text + "   " + td[1].text + "   " + td[2].text + "  =============> " + convert)

        for row in data:
            td = row.find_all('td')
            currency = td[1].text
            currency= currency[currency.find("(") + 1:currency.find(")")]
            if currency in currencies:
                try:
                    convert = str(1.0 / float(td[2].text))
                except:
                    convert = td[2].text
                print(td[0].text + "   " + td[1].text + "   " + td[2].text + "  =============> " + convert)
        '''