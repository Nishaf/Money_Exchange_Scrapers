from bs4 import BeautifulSoup
from pyvirtualdisplay import Display
from selenium import webdriver
from pymongo import MongoClient
from bank_scrapers import add_to_database

class TorontoDominionBank:
    def __init__(self):
        self.url = "https://www.tdcommercialbanking.com/rates/index.jsp"
        self.display = Display(visible=0, size=(1500, 800))
        self.display.start()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome('/home/nishaf/chromedriver')#('/home/Money_Exchange_Scrapers/chromedriver', chrome_options=chrome_options)#
        mongo = MongoClient()
        self.db = mongo['transfer_rates']
        self.run()
        self.driver.close()
        mongo.close()

    def run(self):
        self.driver.get(self.url)
        soup = BeautifulSoup(self.driver.page_source)

        table = soup.find('table')
        tr = table.find_all('tr')
        headers = tr[0]
        headers = headers.find_all('th')
        data = tr[1:]
        time = soup.find('label', attrs={'class': 'ng-binding'}).text
        text = 'Rates may change throughout the day and may differ at the time of booking.'
        print(headers[0].text + "   " + headers[1].text + "   " + headers[2].text + "        1 CAD = ?")
        country_data = self.db.country_list.find()
        for i in country_data:
            for row in data:
                td = row.find_all('td')
                if i['currency'] == td[0].text:
                    try:
                        convert = str(1.0 / float(td[2].text))
                    except:
                        convert = None

                    # print('Toronto Dominion Bank',i['country_name'],  i['currency'],i['cur_sign'],
                    #                '$40.00', '3 to 4 business days', convert, time, text,
                    #                 'img/web_logo/td1.jpg', 'https://www.tdcommercialbanking.com/rates/index.jsp')

                    add_to_database(self.db.records, 'Toronto Dominion Bank', i['country_name'], i['currency'], i['cur_sign'],
                                    '$40.00', '3 to 4 business days', convert, time, text,
                                    'img/web_logo/td1.jpg', 'https://www.tdcommercialbanking.com/rates/index.jsp')

    '''
    table = soup.find('table')
        tr = table.find_all('tr')
        headers = tr[0]
        headers = headers.find_all('th')
        data = tr[1:]
        print(headers[0].text + "   " + headers[1].text + "   " + headers[2].text + "        1 CAD = ?")
        countries = ['USD', 'GBP', 'INR', 'MXN', 'PKR', 'PHP']


        for row in data:
            td = row.find_all('td')
            if (td[0].text).strip() in countries:
                try:
                    convert = str(1.0 / float(td[2].text))
                except:
                    convert = td[2].text
                print(td[0].text + "   " + td[1].text + "   " + td[2].text +   "  =============> " + convert )

    '''




