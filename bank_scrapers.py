from pymongo import MongoClient
import re

def royal_bank(soup, records):
    table = soup.find_all('table')
    tr = table[5].find_all('tr')
    headers = tr[0]
    headers = headers.find_all('td')
    headers = [(i.text).strip() for i in headers]
    print(headers[0] + "   " + headers[1] + "   " + headers[3] + "       1CAD = ?")
    data = tr[1:]
    currencies = ['USD', 'GBP', 'INR', 'MXN', 'PKR', 'PHP']
    #########BRAND-TEXT############
    tr = table[4].find_all('tr')
    td = tr[3].find('td', attrs={'valign': 'top'})
    text = ((td.find('p')).text).strip()
    text = text.replace('\n', ' ')
    time = re.sub(' +', ' ', text)
    second_text = td.find('span', attrs={'class': 'disclaimer'})
    text = (second_text.find('p').text).strip()
    ###############################

    for row in data:
        td = row.find_all('td')
        string = ""
        currency = td[1].text
        currency = currency[currency.find("(") + 1:currency.find(")")]
        if currency in currencies:
            try:
                convert = str(1.0 / float(td[3].text))
            except:
                convert = None
            string += td[0].text + "   " + td[1].text + "   " + td[3].text + "   ===============>  " + convert
            add_to_database(records,'img/web_logo/rbc_royalbank_en.png', 'Royal Bank', currency,
                            '$40.00', '3 to 4 business days', convert, time, text,
                            'http://www.rbcroyalbank.com/rates/rates/cashrates.html')
            #print(string)

def bmo(soup, records):
    table = soup.find('table', attrs={'id': 'ratesTable'})
    tr = table.find_all('tr')
    headers = tr[0]
    headers = headers.find_all('th')
    headers = [(i.text).strip() for i in headers]
    print(headers[0] + "   " + headers[1] + "   " + headers[3] + "       1CAD = ?")
    time = soup.find('p', attrs={'class': 'first bold'})
    time.find('script').replaceWith('')
    time = time.text

    text = "Foreign exchange rates are subject to change at any time."
    data = tr[1:]
    currencies = ['USD', 'GBP', 'INR', 'MXN', 'PKR', 'PHP']
    for row in data:
        td = row.find_all('td')
        string = ""
        currency = td[1].text
        currency = currency[currency.find("(") + 1:currency.find(")")]
        if currency in currencies:
            try:
                convert = str(1.0 / float(td[3].text))
            except:
                convert = None
            string += td[0].text + "   " + td[1].text + "   " + td[3].text + "   ===============>  " + convert
            add_to_database(records,'img/web_logo/bmo1.jpg', 'Bank of Montreal',
                            currency, '$40.00', '3 to 4 business days', convert, time, text,
                            'https://www.bmo.com/home/personal/banking/rates/foreign-exchange')
            #print(string)

def scotia_bank(soup, records):
    table = soup.find('table', attrs={'class': 'rates'})
    tr = table.find_all('tr')
    headers = tr[0]
    headers = headers.find_all('td')
    data = tr[1:]
    print(headers[0].text + "   " + headers[1].text + "   " + headers[2].text + "        1 CAD = ?")
    currencies = ['USD', 'GBP', 'INR', 'MXN', 'PKR', 'PHP']
    time = soup.find('li', attrs={'class': 'effective-date'}).text
    text = 'Rates are provided for information purposes only and are subject to change at any time.'
    for row in data:
        td = row.find_all('td')
        currency = td[1].text
        currency = currency[currency.find("(") + 1:currency.find(")")]
        if currency in currencies:
            try:
                convert = str(1.0 / float(td[2].text))
            except:
                convert = None
            #print(td[0].text + "   " + td[1].text + "   " + td[2].text + "  =============> " + convert)
            add_to_database(records, 'img/web_logo/scotiabank.jpg', 'Scotia Bank',
                            currency, '$40.00', '3 to 4 business days', convert, time, text,
                            'http://www.scotiabank.com/ca/en/0,,1118,00.html')


def tdcommercialbanking(soup, records):
    table = soup.find('table')
    tr = table.find_all('tr')
    headers = tr[0]
    headers = headers.find_all('th')
    data = tr[1:]
    time = soup.find('label', attrs={'class': 'ng-binding'}).text
    text = 'Rates may change throughout the day and may differ at the time of booking.'
    print(headers[0].text + "   " + headers[1].text + "   " + headers[2].text + "        1 CAD = ?")
    countries = ['USD', 'GBP', 'INR', 'MXN', 'PKR', 'PHP']
    for row in data:
        td = row.find_all('td')
        if (td[0].text).strip() in countries:
            try:
                convert = str(1.0 / float(td[2].text))
            except:
                convert = None
            #print(td[0].text + "   " + td[1].text + "   " + td[2].text + "  =============> " + convert)
            add_to_database(records, 'img/web_logo/td1.jpg', 'Toronto Dominion Bank', td[0].text,
                            '$40.00','3 to 4 business days', convert, time, text,
                            'https://www.tdcommercialbanking.com/rates/index.jsp')


def hsbc(soup, records):
    table = soup.find('table', attrs={'class': 'hsbcTableStyleViewRates'})
    tr = table.find_all('tr')
    headers = tr[0]
    headers = headers.find_all('th')
    data = tr[1:]
    print(headers[0].text + "   " + headers[1].text + "   " + headers[2].text + "        1 CAD = ?")
    currencies = ['USD', 'GBP', 'INR', 'MXN', 'PKR', 'PHP']
    time= soup.find('div', attrs={'class': 'hsbcTextStyle15'}).text
    text = 'Rates are subject to change without notice.'
    for row in data:
        td = row.find_all('td')
        currency = td[1].text
        if currency in currencies:
            try:
                convert = str(1.0 / float(td[2].text))
            except:
                convert = None
            #print(td[0].text + "   " + td[1].text + "   " + td[2].text + "  =============> " + convert)
            add_to_database(records,'img/web_logo/hsbc-logo.gif', 'HSBC Bank', currency,
                            '$40.00', '3 to 4 business days', convert, time, text,
                            'http://www.hsbc.ca/1/2/personal/banking/accounts/foreign-currency-accounts/foreign-currency-exchange')




def add_to_database(records_col, bank_logo, bank_name, currency, transfer_fee, transfer_time, rate, time, text, web_link):
    if records_col.find({'bank_name': bank_name, 'currency':currency}).count() == 0:
        print("Inserting")
        records_col.insert(
            {
                'bank_logo': bank_logo,
                'bank_name': bank_name,
                'currency': currency,
                'transfer_fee': transfer_fee,
                'transfer_time': transfer_time,
                'rate': rate,
                'time': time,
                'bank_note': text,
                'web_link':web_link,
            }
        )
    else:
        print("Updating Database")
        records_col.update(
            {'bank_name': bank_name, 'currency': currency},
            {
                'bank_logo': bank_logo,
                'bank_name': bank_name,
                'currency': currency,
                'transfer_fee': transfer_fee,
                'transfer_time': transfer_time,
                'rate': rate,
                'time': time,
                'bank_note': text,
                'web_link':web_link,
            }
        )




def insert_all():
    mongo = MongoClient()
    db=mongo['transfer_rates']
    items = db['flags']
    items.insert({'country':'canada','flag':'/img/icon/canada.jpg'})
    items.insert({'country':'india','flag':'/img/icon/india.jpg'})
    items.insert({'country':'mexico','flag':'/img/icon/mexico.jpg'})
    items.insert({'country':'pakistan','flag':'/img/icon/pakistan.jpg'})
    items.insert({'country':'uk','flag':'/img/icon/uk.jpg'})
    items.insert({'country':'usa','flag':'/img/icon/usa.jpg'})

    mongo.close()