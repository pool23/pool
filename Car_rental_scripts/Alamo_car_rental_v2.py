# -*- coding:utf-8 -*-
from datetime import datetime
from datetime import timedelta
import pandas as pd
import time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from bs4 import BeautifulSoup
from tabulate import tabulate
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


import warnings
warnings.simplefilter(action='ignore')





car_data_headers = ['Date', 'pickup_date', 'return_date','Location', 'Airport name','selected_location', 'Location Code',
                    'className', 'vehicleName', 'payNowAmount', 'payNowAmountUnit',
                'payNowTotalAmount','payNowTotalUnit','payLaterAmount','payLaterAmountUnit','payLaterTotalAmount','payLaterTotalUnit','sitename']
car_data = []

startTime = time.time()

airport = [["Hartsfield–Jackson Atlanta International Airport","Atlanta, Georgia","ATL"],["Chicago O'Hare International Airport","Chicago, Illinois","ORD"],["Los Angeles International Airport","Los Angeles, California","LAX"],["Dallas/Fort Worth International Airport","Dallas–Fort Worth Metroplex, Texas","DFW"],["John F. Kennedy International Airport","New York, New York","JFK"],["Denver International Airport","Denver, Colorado","DEN"],["San Francisco International Airport","San Francisco, California","SFO"],["McCarran International Airport","Las Vegas, Nevada","LAS"],["Charlotte Douglas International Airport","Charlotte, North Carolina","CLT"],["Miami International Airport","Miami, Florida","MIA"],["Phoenix Sky Harbor International Airport","Phoenix, Arizona","PHX"],["George Bush Intercontinental Airport","Houston, Texas","IAH"],["Seattle–Tacoma International Airport","SeaTac, Washington","SEA"],["Orlando International Airport","Orlando, Florida","MCO"],["Newark Liberty International Airport","Newark, New Jersey","EWR"],["Minneapolis–Saint Paul International Airport","Minneapolis–Saint Paul, Minnesota","MSP"],["Logan International Airport","Boston, Massachusetts","BOS"],["Detroit Metropolitan Airport","Romulus, Michigan","DTW"],["Philadelphia International Airport","Philadelphia, Pennsylvania","PHL"],["LaGuardia Airport","New York, New York","LGA"],["Fort Lauderdale–Hollywood International Airport","Fort Lauderdale, Florida","FLL"],["Baltimore–Washington International Airport","Linthicum, Maryland","BWI"],["Ronald Reagan Washington National Airport","Arlington, Virginia","DCA"],["Chicago Midway International Airport","Chicago, Illinois","MDW"],["Salt Lake City International Airport","Salt Lake City, Utah","SLC"],["Washington Dulles International Airport","Dulles, Virginia","IAD"],["San Diego International Airport","San Diego, California","SAN"],["Daniel K. Inouye International Airport","Honolulu, Hawaii","HNL"],["Tampa International Airport","Tampa, Florida","TPA"],["Portland International Airport","Portland, Oregon","PDX"]]
for i in airport:
    # time.sleep(10)
    kk = [[15, 17], [15, 22]]
    for k in kk:
        print(i[2])
        try:

            start_date = (datetime.now() + timedelta(days=k[0])).strftime('%m/%d/%Y')
            end_date = (datetime.now() + timedelta(days=k[1])).strftime('%m/%d/%Y')
            print(start_date,end_date)

            browser = webdriver.Firefox()

            browser.maximize_window()
            browser.get('https://www.alamo.com/en_US/car-rental/home.html') #https://www.alamo.com/en_US/car-rental/reservation/aboutYourTrip.html
            time.sleep(5)

            try:
                browser.find_element_by_xpath('/html/body/div[3]/div/p/a[1]/img').click()
            except :
                pass

            #LOCATION
            browser.find_element_by_xpath('//*[@id="_content_alamo_en_US_car_rental_home_jcr_content_reservationStart_pickUpLocation_searchCriteria"]').clear()
            browser.find_element_by_xpath('//*[@id="_content_alamo_en_US_car_rental_home_jcr_content_reservationStart_pickUpLocation_searchCriteria"]').send_keys(i[2])

            #POPUP
            try:
                browser.find_element_by_xpath('/html/body/div[3]/div/p/a[1]/img').click()
            except:
                pass

            time.sleep(3)

            #LOCATION
            browser.find_element_by_xpath('//*[@id="_content_alamo_en_US_car_rental_home_jcr_content_reservationStart_pickUpLocation_searchCriteria"]').send_keys(Keys.ARROW_DOWN)
            browser.find_element_by_xpath('//*[@id="_content_alamo_en_US_car_rental_home_jcr_content_reservationStart_pickUpLocation_searchCriteria"]').send_keys(Keys.RETURN)
            time.sleep(2)
            browser.find_element_by_css_selector('#_content_alamo_en_US_car_rental_home_jcr_content_reservationStart_countryOfResidenceResident').click()
            time.sleep(3)

            #POPUP
            try:
                browser.find_element_by_xpath('/html/body/div[3]/div/p/a[1]/img').click()
            except:
                pass

            #PICKUP_DATE
            browser.find_element_by_xpath('//*[@id="_content_alamo_en_US_car_rental_home_jcr_content_reservationStart_pickUpDateTime_date"]').send_keys(start_date)

            #RETURN_DATE
            browser.find_element_by_xpath('//*[@id="_content_alamo_en_US_car_rental_home_jcr_content_reservationStart_dropOffDateTime_date"]').send_keys(end_date)
            browser.find_element_by_xpath('//*[@id="_content_alamo_en_US_car_rental_home_jcr_content_reservationStart_dropOffDateTime_date"]').send_keys(Keys.RETURN)
            time.sleep(5)

            #SCROLL_DOWN
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

            #POPUP
            try:
                browser.find_element_by_xpath('/html/body/div[3]/div/p/a[1]/img').click()
            except:
                pass

            time.sleep(3)

            #SUBMIT_BUTTON
            try:
                browser.find_element_by_css_selector('button.a-btn:nth-child(2)').click()
                time.sleep(5)
            except:
                pass
            #SOLD_OUT POPUP
            try:

                if 'sold out'.lower() in browser.page_source.lower():
                    print('sold_out')
                    browser.close()
                    continue

            except:
                pass

            #POPUP
            try:
                browser.find_element_by_xpath('/html/body/div[3]/div/p/a[1]/img').click()
            except :
                pass

            print(browser.current_url)

            time.sleep(5)
            #PAGE_SOURCE
            jsoup = BeautifulSoup(browser.page_source)
            lis = jsoup.find('section',attrs={'class':'blockPrimary'}).find('ul', attrs={'class': 'carList'}).find_all('li',attrs={'class':re.compile('\w*')})

            for li in lis:
                # print(li)
                car_class = li.find('div', attrs={'class':'carDetails'}).find('h2')
                print(car_class.text)
                car_name = li.find('div', attrs={'class':'vehiclesSimilar'}).find('span')
                print(car_name.text)

                #UNCOMMENT_OR_COMMENT_ACCORDING_CLASS_NAME
                # pay_later_price = li.find('div',attrs = {'class':'priceInfoDetails'})
                # pay_later_price = pay_later_price.find('div',attrs={'class':'price qcca pkgRate'}).find('p') if pay_later_price is not None else None
                # pay_later_price_unit = re.search('[ A-Za-z]+',pay_later_price.text) if pay_later_price is not None else None
                # pay_later_price_unit = pay_later_price_unit.group(0) if pay_later_price_unit is not None else None
                # print(pay_later_price_unit)
                # pay_later_price = re.search('\$[0-9\.]+', pay_later_price.text) if pay_later_price is not None else None
                # pay_later_price = pay_later_price.group(0) if pay_later_price is not None else None
                # print(pay_later_price)






                per_day_now = li.find('div',attrs = {'class':'priceInfoDetails'})
                per_day_now = per_day_now.find('div', attrs={'class':'largePayment'})if per_day_now is not None else None

                per_day_now = per_day_now.find_all('p')[0] if per_day_now is not None else None
                # print(per_day_now.text)

                per_day_now = re.search('\$[0-9\.]+', per_day_now.text) if per_day_now is not None else None
                per_day_now = per_day_now.group(0) if per_day_now is not None else None
                print(per_day_now)


                per_day_now_unit = li.find('div',attrs = {'class':'priceInfoDetails'})
                per_day_now_unit = per_day_now_unit.find_all('p')[0] if per_day_now_unit is not None else None
                per_day_now_unit = per_day_now_unit.find_all('span')[1] if per_day_now_unit is not None else None
                per_day_now_unit = re.search('[ A-Za-z]+', per_day_now_unit.text) if per_day_now is not None else None
                per_day_now_unit = per_day_now_unit.group(0) if per_day_now_unit is not None else None
                print(per_day_now_unit)




                pay_now_total = li.find('div', attrs={'class': 'priceInfoDetails'})
                # print('++++++++++++++++++++++++++++++++')
                pay_now_total = pay_now_total.find('div', attrs={'class': 'largePayment'}) if pay_now_total is not None else None
                # print('-------------------------------')
                pay_now_total = pay_now_total.find_all('p')[1] if pay_now_total is not None else None
                pay_now_total_unit = re.search('[A-Za-z]+', pay_now_total.text) if pay_now_total is not None else None
                pay_now_total_unit = pay_now_total_unit.group(0) if pay_now_total_unit is not None else None
                print(pay_now_total_unit)
                pay_now_total = re.search('\$[0-9\.]+', pay_now_total.text) if pay_now_total is not None else None
                pay_now_total = pay_now_total.group(0) if pay_now_total is not None else None
                print(pay_now_total)



                print('-----------------------------------------------------------------------------------------------')
                per_day_later = li.find('div', attrs={'class': 'priceInfoDetails'})
                per_day_later = per_day_later.find('div', attrs={'class':re.compile('smallPayment|smallPaymentOnly')}) if per_day_later is not None else None
                per_day_later = per_day_later.find_all('p')[0] if per_day_later is not None else None
                # per_day_later_unit = re.search('[ A-Za-z]+',per_day_later.text) if per_day_later is not None else None
                # per_day_later_unit = per_day_later_unit.group(1) if per_day_later_unit is not None else None
                # print(per_day_later_unit)
                # per_day_later_unit = per_day_later_unit if per_day_later_unit is not None else None
                per_day_later = re.search('\$[0-9\.]+',per_day_later.text) if per_day_later is not None else None
                per_day_later = per_day_later.group(0) if per_day_later is not None else None
                print(per_day_later)

                per_day_later_unit = li.find('div', attrs={'class': 'priceInfoDetails'})
                per_day_later_unit = per_day_later_unit.find('div', attrs={'class': re.compile('smallPayment|smallPaymentOnly')}) if per_day_later_unit is not None else None
                per_day_later_unit = per_day_later_unit.find_all('p')[0] if per_day_later_unit is not None else None
                per_day_later_unit = per_day_later_unit.find_all('span')[1] if per_day_later_unit is not None else None
                per_day_later_unit = re.search('[ A-Za-z]+',per_day_later_unit.text) if per_day_later_unit is not None else None
                per_day_later_unit = per_day_later_unit.group(0) if per_day_later_unit is not None else None
                print(per_day_later_unit)


                pay_later_total = li.find('div',attrs = {'class':'priceInfoDetails'})
                pay_later_total = pay_later_total.find('div', attrs={'class':re.compile('smallPayment|smallPaymentOnly')}) if pay_later_total is not None else None
                pay_later_total = pay_later_total.find_all('p')[1] if pay_later_total is not None else None
                pay_later_total_unit = re.search('[A-Za-z]+', pay_later_total.text) if pay_later_total is not None else None
                pay_later_total_unit = pay_later_total_unit.group(0) if pay_later_total_unit is not None else None
                print(pay_later_total_unit)
                pay_later_total = re.search('\$[0-9\.]+', pay_later_total.text) if pay_later_total is not None else None
                pay_later_total = pay_later_total.group(0) if pay_later_total is not None else None
                print(pay_later_total)
                print('-'.center(100,'-'))

                data = [datetime.now().strftime('%m/%d/%Y'), start_date,end_date, i[1], i[0], i[0], i[2], car_class.text, car_name.text,per_day_now,per_day_now_unit,pay_now_total,pay_now_total_unit,per_day_later,per_day_later_unit, pay_later_total,pay_later_total_unit,'Alamo']
                car_data.append(data)

            browser.close()


        except Exception as e:
            print(e)


print(tabulate(car_data))
df = pd.DataFrame(car_data,columns=car_data_headers)
print(df)
df.to_excel('Alamo.xlsx', index=False)
print('Time = ', (time.time()-startTime)/60)
