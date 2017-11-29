from pymongo import MongoClient
import re


def get_country_list(countries):
    currencies = countries.find()
    country_list = []
    for i in currencies:
        country_list.append(i['country_name'])
    return country_list


def get_list(countries):
    currencies = countries.find()
    return currencies


def royal_bank(soup, records, countries_list):
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


def bmo(soup, records, countries_list):
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
    country_list = get_country_list(countries_list)
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

            data1 = countries_list.find_one({'country_name': country})
            string += td[0].text + "   " + td[1].text + "   " + td[3].text + "   ===============>  " + convert
            #print('Bank of Montreal',country,data1['currency'],data1['cur_sign'],
            #                '$40.00', '3 to 4 business days', convert, time, text,
            #                'img/web_logo/bmo1.jpg', 'https://www.bmo.com/home/personal/banking/rates/foreign-exchange')
            add_to_database(records,'Bank of Montreal',country, data1['currency'],data1['cur_sign'],
                            '$40.00', '3 to 4 business days', convert, time, text,
                            'img/web_logo/bmo1.jpg', 'https://www.bmo.com/home/personal/banking/rates/foreign-exchange')
            #print(string)


def scotia_bank(soup, records, countries_list):
    table = soup.find('table', attrs={'class': 'rates'})
    tr = table.find_all('tr')
    headers = tr[0]
    headers = headers.find_all('td')
    data = tr[1:]
    print(headers[0].text + "   " + headers[1].text + "   " + headers[2].text + "        1 CAD = ?")
    time = soup.find('li', attrs={'class': 'effective-date'}).text
    text = 'Rates are provided for information purposes only and are subject to change at any time.'
    country_list = get_country_list(countries_list)
    for row in data:
        td = row.find_all('td')
        country = td[0].text
        if country in country_list:
            try:
                convert = str(1.0 / float(td[2].text))
            except:
                convert = None
            #print(td[0].text + "   " + td[1].text + "   " + td[2].text + "  =============> " + convert)
            data1 = countries_list.find_one({'country_name': country})
            #print('Scotia Bank',country, data1['currency'],data1['cur_sign'],
            #    '$40.00', '3 to 4 business days', convert, time, text,
            #    'img/web_logo/scotiabank.jpg','http://www.scotiabank.com/ca/en/0,,1118,00.html')
            add_to_database(records, 'Scotia Bank',country, data1['currency'],data1['cur_sign'],
                            '$40.00', '3 to 4 business days', convert, time, text,
                            'img/web_logo/scotiabank.jpg', 'http://www.scotiabank.com/ca/en/0,,1118,00.html')



def tdcommercialbanking(soup, records, countries_list):
    table = soup.find('table')
    tr = table.find_all('tr')
    headers = tr[0]
    headers = headers.find_all('th')
    data = tr[1:]
    time = soup.find('label', attrs={'class': 'ng-binding'}).text
    text = 'Rates may change throughout the day and may differ at the time of booking.'
    print(headers[0].text + "   " + headers[1].text + "   " + headers[2].text + "        1 CAD = ?")
    country_data = get_list(countries_list)
    for i in country_data:
        for row in data:
            td = row.find_all('td')
            if i['currency'] == td[0].text:
                try:
                    convert = str(1.0 / float(td[2].text))
                except:
                    convert = None

                #print('Toronto Dominion Bank',i['country_name'],  i['currency'],i['cur_sign'],
                #                '$40.00', '3 to 4 business days', convert, time, text,
                #                 'img/web_logo/td1.jpg', 'https://www.tdcommercialbanking.com/rates/index.jsp')

                add_to_database(records,'Toronto Dominion Bank',i['country_name'],  i['currency'],i['cur_sign'],
                                '$40.00', '3 to 4 business days', convert, time, text,
                                 'img/web_logo/td1.jpg', 'https://www.tdcommercialbanking.com/rates/index.jsp')



def hsbc(soup, records, countries_list):
    table = soup.find('table', attrs={'class': 'hsbcTableStyleViewRates'})
    tr = table.find_all('tr')
    headers = tr[0]
    headers = headers.find_all('th')
    data = tr[1:]
    print(headers[0].text + "   " + headers[1].text + "   " + headers[2].text + "        1 CAD = ?")
    time= soup.find('div', attrs={'class': 'hsbcTextStyle15'}).text
    text = 'Rates are subject to change without notice.'
    country_data = get_list(countries_list)
    print(len(data))
    for i in country_data:
        for row in data:
            td = row.find_all('td')
            if i['currency'] == td[1].text:
                try:
                    convert = str(1.0 / float(td[2].text))
                except:
                    convert = None

                #print(td[0].text + "   " + td[1].text + "   " + td[2].text + "  =============> " + convert)
                #print('HSBC Bank',i['country_name'],  i['currency'],i['cur_sign'],
                #                '$40.00', '3 to 4 business days', convert, time, text,
                #                'img/web_logo/hsbc-logo.gif')

                add_to_database(records, 'HSBC Bank',i['country_name'],  i['currency'],i['cur_sign'],
                                '$40.00', '3 to 4 business days', convert, time, text,
                                'img/web_logo/hsbc-logo.gif',
                                'http://www.hsbc.ca/1/2/personal/banking/accounts/foreign-currency-accounts/foreign-currency-exchange')



def add_to_database(records_col, bank_name,country, currency, cur_sign,transfer_fee, transfer_time, rate, time, text,bank_logo, web_link):
    if records_col.find({'bank_name': bank_name, 'country':country}).count() == 0:
        print("Inserting")
        records_col.insert(
            {
                'bank_logo': bank_logo,
                'country': country,
                'cur_sign': cur_sign,
                'bank_name': bank_name,
                'currency': currency,
                'transfer_fee': transfer_fee,
                'transfer_time': str(transfer_time),
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
                'country': country,
                'cur_sign': cur_sign,
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
    mongo = MongoClient("mongodb://hkamboe:hkamboefxratehunter8080!!@127.0.0.1/transfer_rates")
    db=mongo['transfer_rates']
    items = db['flags']
    items.insert({'country':'canada','flag':'/img/icon/canada.jpg'})
    items.insert({'country':'india','flag':'/img/icon/india.jpg'})
    items.insert({'country':'mexico','flag':'/img/icon/mexico.jpg'})
    items.insert({'country':'pakistan','flag':'/img/icon/pakistan.jpg'})
    items.insert({'country':'uk','flag':'/img/icon/uk.jpg'})
    items.insert({'country':'usa','flag':'/img/icon/usa.jpg'})

    mongo.close()





def sitemap_generator():
    string = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="https://fxratehunter.com">\n'
    url = "https://fxratehunter.com/send-money-from-canada-to-"
    mongo = MongoClient("mongodb://hkamboe:hkamboefxratehunter8080!!@127.0.0.1/transfer_rates")
    db = mongo['transfer_rates']
    for item in db.country_list.find():
        country_name = '-'.join(item['country_name'].split(' ')) if ' ' in item['country_name'] else item['country_name']
        string += "<url>\n<loc>"+url+(country_name).lower()+"</loc>\n<lastmod>2017-11-06</lastmod>\n<changefreq>hourly</changefreq>\n</url>\n"

    string += "</urlset>"

    print(string)
    mongo.close()



from pymongo import MongoClient
import xlwt
def get():
    wb = xlwt.Workbook()
    sheet1 = wb.add_sheet('Countries')
    sheet1.write(0,0,'Country_Names')
    sheet1.write(0,1,'Country_URLS')
    mongo = MongoClient("mongodb://hkamboe:hkamboefxratehunter8080!!@127.0.0.1/transfer_rates")
    db = mongo['transfer_rates']
    count = 1
    for i in db.country_list.find():
        country_name = '-'.join(i['country_name'].split(' ')) if ' ' in i['country_name'] else i['country_name']
        link = 'https://fxratehunter.com/send-money-from-canada-to-'+ country_name.lower()
        sheet1.write(count,0,i['country_name'])
        sheet1.write(count,1, link)
        count += 1
    wb.save('workbook.xls')


#get()


import datetime

import ebaysdk
from ebaysdk.finding import Connection as finding

api = finding(siteid='EBAY-US', appid='NishafNa-Nishaf-PRD-2090fc79c-557dac4b',config_file=None)

'''
api.execute('findItemsAdvanced', {
    'keywords': 'laptop',
    'categoryId': ['177', '111422'],
    'itemFilter': [
        {'name': 'Condition', 'value': 'Used'},
        {'name': 'MinPrice', 'value': '200', 'paramName': 'Currency', 'paramValue': 'USD'},
        {'name': 'MaxPrice', 'value': '2000', 'paramName': 'Currency', 'paramValue': 'USD'}
    ],
    'paginationInput': {
        'entriesPerPage': '500',
        'pageNumber': '5'
    },
    'sortOrder': 'CurrentPriceHighest'
})
'''

'''

api.execute('findItemsAdvanced', {'keywords': 'laptop', 'PageNumber': 1})

dictstr = api.response.dict()

for item in dictstr['searchResult']['item']:
    print(item)

'''

import xlwt
def ebay_api():
    count = 1
    wb = xlwt.Workbook()
    sheet = wb.add_sheet('Ebay-Laptop-Results')
    sheet.write(0,0,'ItemID')
    sheet.write(0,1,'Title')
    sheet.write(0,2,'CategoryID')
    sheet.write(0,3,'CategoryName')
    sheet.write(0,4,'SellingPrice')
    sheet.write(0,5,'GalleryURL')
    item_count = 1
    while True:
        try:
            api.execute('findItemsByProduct', {'productId': '182550465931'})

            dictstr = api.response.dict()
            print(dictstr)
                #for item in dictstr['searchResult']['item']:
                #    print(item)
                #print("ItemID: %s" % item['itemId'])
                #print("Title: %s" % item['title'])
                #print("CategoryID: %s" % item['primaryCategory']['categoryId'])
                #print("CategoryID: %s" % item['primaryCategory']['categoryName'])
                #print("Selling Price: %s" % item['sellingStatus']['currentPrice']['value'])
                #print("GalleryUrl: %s" % item['galleryURL'])
                #sheet.write(item_count,0, item['itemId'])
                #sheet.write(item_count,1, item['title'])
                #sheet.write(item_count,2, item['primaryCategory']['categoryId'])
                #sheet.write(item_count,3, item['primaryCategory']['categoryName'])
                #sheet.write(item_count,4, item['sellingStatus']['currentPrice']['value'])
                #sheet.write(item_count,5, item['galleryURL'])
                #item_count += 1
            #count += 1

            #wb.save('Ebay-Laptop-Results.xls')

        except Exception as e:
            print(e)
            wb.save('Ebay-Laptop-Results.xls')
