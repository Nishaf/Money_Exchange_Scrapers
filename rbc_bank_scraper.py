import requests
from bs4 import BeautifulSoup
from pyvirtualdisplay import Display
from selenium import webdriver
import re
from pymongo import MongoClient
from time import sleep
from bank_scrapers import add_to_database

class RoyalBank:
    def __init__(self):
        self.url = "https://online.royalbank.com/cgi-bin/tools/foreign-exchange-calculator/start.cgi"
        self.display = Display(visible=0, size=(1500, 800))
        self.display.start()
        self.currency_li = list()
        self.rate_li = list()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        self.driver = webdriver.Firefox(executable_path='/home/Money_Exchange_Scrapers/geckodriver')#('/home/Money_Exchange_Scrapers/chromedriver', chrome_options=chrome_options)#
        mongo = MongoClient()
        self.db = mongo['transfer_rates']
        self.run()
        self.driver.close()
        mongo.close()

    def get_currency(self):
        cur = []
        for i in self.db.country_list.find():
            cur.append(i['currency'])

        return cur

    def insert_in_db(self):
        textt = self.driver.find_elements_by_xpath(
            "//div[@class='currency-select ui fluid selection dropdown']/div[@class='text']")[1].text
        textt = textt[textt.index("(") + 1:textt.rindex(")")]
        print(textt)
        rate = self.driver.find_element_by_xpath("//span[@id='noncash-currencyWantRate']").text
        #print(textt + " =====> " + rate + " ========> " + str(1.0 / float(rate)))
        self.currency_li.append(textt)
        self.rate_li.append(str(1.0 / float(rate)))
        sleep(2)


    def get_rates_from_webpage(self):
        self.driver.execute_script("return window.scrollBy(0,300);")
        time_text = self.driver.find_element_by_xpath("//p[@class='pad-t-qtr text-center text-grey minor']").text
        statement = self.driver.find_element_by_xpath("//p[@class='pad-b-0 mob-pad-b-hlf text-center text-grey minor']").text
        sleep(2)
        self.cur_list = self.get_currency()
        self.insert_in_db()
        self.driver.find_elements_by_xpath("//div[@class='currency-select ui fluid selection dropdown']")[1].click()
        element = self.driver.find_elements_by_xpath("//div[@class='input-wpr w-100']")
        print(len(element))
        count = 10
        elem = element[1].find_elements_by_xpath("//div[@class='item']")
        for i in range(15, 43):
            sleep(4)
            try:
                elem[i].click()
            except:
                try:
                    print("2nd try")
                    sleep(2)
                    elem[i].click()
                except:
                    elem = element[1].find_elements_by_xpath("//div[@class='item']")
                    print(elem[i].text)
                    sleep(4)
                    elem[i].click()

            sleep(3)
            self.insert_in_db()
            self.driver.find_elements_by_xpath("//div[@class='currency-select ui fluid selection dropdown']")[1].click()
            sleep(2)
            element = self.driver.find_elements_by_xpath("//div[@class='input-wpr w-100']")
            element1 = self.driver.find_element_by_xpath("//div[@class='menu transition visible']")
            self.driver.execute_script("return arguments[0].scrollBy(0,"+str(count)+");", element1)
            elem = element[1].find_elements_by_xpath("//div[@class='item']")
            sleep(2)
            count += 10

        return time_text, statement

    def run(self):
        self.driver.get(self.url)
        time, textt = self.get_rates_from_webpage()

        country_list = self.db.country_list.find()
        for entity in country_list:
            if entity['currency'] in self.currency_li:
                index = self.currency_li.index(entity['currency'])
                rate = self.rate_li[index]
                print(self.currency_li[index] + " =====> " + rate)

                add_to_database(self.db.records, 'Royal Bank', entity['country_name'], entity['currency'],
                                entity['cur_sign'], '$40.00', '3 to 4 business days', rate, time, textt,
                                'img/web_logo/rbc_royalbank_en.png',
                                'http://www.rbcroyalbank.com/rates/rates/cashrates.html')



'''

def get_country_list(self):
    currencies = self.db.country_list.find()
    country_list = []
    for i in currencies:
        country_list.append(i['country_name'])
    return country_list

def run(self):
    self.driver.get(self.url)
    soup = BeautifulSoup(self.driver.page_source)
    table = soup.find_all('table')
    tr = table[5].find_all('tr')
    headers = tr[0]
    headers = headers.find_all('td')
    headers = [(i.text).strip() for i in headers]
    print(headers[0] + "   " + headers[1] + "   " + headers[3] + "       1CAD = ?")

    data = tr[1:]
    tr = table[4].find_all('tr')
    td = tr[3].find('td', attrs={'valign': 'top'})
    text = ((td.find('p')).text).strip()
    text = text.replace('\n', ' ')
    text = re.sub(' +', ' ', text)
    text += "\n"
    second_text = td.find('span', attrs={'class': 'disclaimer'})
    text += (second_text.find('p').text).strip()
    print(text)
    country_list= self.get_country_list()
    euro = data[1]
    euro = euro.find_all('td')
    for row in data:
        td = row.find_all('td')
        string = ""
        country = td[0].text
        if country in country_list:
            if (td[3].text).strip() == 'Refer to Euro':
                value = euro[3].text
                convert = str(1.0/float(euro[3].text))
            elif td[3].text != 'N/A':
                value = td[3].text
                convert = str(1.0 / float(td[3].text))
            data1 = self.db.country_list.find_one({'country_name': country})
            string += td[0].text + "   " + td[1].text + "   " + data1['cur_sign'] + "   " + value + "   ===============>  " + convert
            #print(euro[3].text)
            #print(country + "       " + data['cur_sign'] + value)
            print(string)

'''
doc = {
    # id = countryname,
    # currency = PKR or GBP etc.
    # rate = rate bank will sell to you
    # transfer fee
    # amount-receivable
}




'''
table = soup.find_all('table')
    tr = table[5].find_all('tr')
    headers = tr[0]
    headers = headers.find_all('td')
    headers = [(i.text).strip() for i in headers]
    print(headers[0] + "   " + headers[1] + "   " + headers[3] + "       1CAD = ?")
    data = tr[1:]
    #########BRAND-TEXT############
    tr = table[4].find_all('tr')
    td = tr[3].find('td', attrs={'valign': 'top'})
    text = ((td.find('p')).text).strip()
    text = text.replace('\n', ' ')
    time = re.sub(' +', ' ', text)
    second_text = td.find('span', attrs={'class': 'disclaimer'})
    text = (second_text.find('p').text).strip()
    ###############################

    country_list = get_country_list(countries_list)
    euro = data[1]
    euro = euro.find_all('td')
    value, convert ="",""
    for row in data:
        td = row.find_all('td')
        string = ""
        country = td[0].text
        if country in country_list:
            if (td[3].text).strip() == 'Refer to Euro':
                value = euro[3].text
                convert = str(1.0 / float(euro[3].text))
            elif td[3].text != 'N/A':
                value = td[3].text
                convert = str(1.0 / float(td[3].text))
            data1 = countries_list.find_one({'country_name': country})
            string += td[0].text + "   " + td[1].text + "   " + data1[
                'cur_sign'] + "   " + value + "   ===============>  " + convert

            #print('Royal Bank', country, data1['currency'],
            #                data1['cur_sign'],'$40.00', '3 to 4 business days', convert, time, text,
            #                    'img/web_logo/rbc_royalbank_en.png','http://www.rbcroyalbank.com/rates/rates/cashrates.html')
            add_to_database(records, 'Royal Bank', country, data1['currency'],
                            data1['cur_sign'],'$40.00', '3 to 4 business days', convert, time, text,
                                'img/web_logo/rbc_royalbank_en.png','http://www.rbcroyalbank.com/rates/rates/cashrates.html')
            #print(string)
'''
