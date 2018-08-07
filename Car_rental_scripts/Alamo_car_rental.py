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

import warnings
warnings.simplefilter(action='ignore')





car_data_headers = ['Date', 'pickup_date', 'return_date','Location', 'Airport name','selected_location', 'Location Code',
                    'className', 'vehicleName', 'payNowAmount', 'payNowAmountUnit',
                'payNowTotalAmount','payNowTotalUnit','payLaterAmount','payLaterTotalAmount','payLaterAmountUnit','payLaterTotalUnit']
car_data = []

startTime = time.time()

airport = [["Hartsfield–Jackson Atlanta International Airport","Atlanta, Georgia","ATL"],["Chicago O'Hare International Airport","Chicago, Illinois","ORD"],["Los Angeles International Airport","Los Angeles, California","LAX"],["Dallas/Fort Worth International Airport","Dallas–Fort Worth Metroplex, Texas","DFW"],["John F. Kennedy International Airport","New York, New York","JFK"],["Denver International Airport","Denver, Colorado","DEN"],["San Francisco International Airport","San Francisco, California","SFO"],["McCarran International Airport","Las Vegas, Nevada","LAS"],["Charlotte Douglas International Airport","Charlotte, North Carolina","CLT"],["Miami International Airport","Miami, Florida","MIA"],["Phoenix Sky Harbor International Airport","Phoenix, Arizona","PHX"],["George Bush Intercontinental Airport","Houston, Texas","IAH"],["Seattle–Tacoma International Airport","SeaTac, Washington","SEA"],["Orlando International Airport","Orlando, Florida","MCO"],["Newark Liberty International Airport","Newark, New Jersey","EWR"],["Minneapolis–Saint Paul International Airport","Minneapolis–Saint Paul, Minnesota","MSP"],["Logan International Airport","Boston, Massachusetts","BOS"],["Detroit Metropolitan Airport","Romulus, Michigan","DTW"],["Philadelphia International Airport","Philadelphia, Pennsylvania","PHL"],["LaGuardia Airport","New York, New York","LGA"],["Fort Lauderdale–Hollywood International Airport","Fort Lauderdale, Florida","FLL"],["Baltimore–Washington International Airport","Linthicum, Maryland","BWI"],["Ronald Reagan Washington National Airport","Arlington, Virginia","DCA"],["Chicago Midway International Airport","Chicago, Illinois","MDW"],["Salt Lake City International Airport","Salt Lake City, Utah","SLC"],["Washington Dulles International Airport","Dulles, Virginia","IAD"],["San Diego International Airport","San Diego, California","SAN"],["Daniel K. Inouye International Airport","Honolulu, Hawaii","HNL"],["Tampa International Airport","Tampa, Florida","TPA"],["Portland International Airport","Portland, Oregon","PDX"]]
for i in airport:
    # time.sleep(10)
    browser = webdriver.Firefox()

    browser.maximize_window()
    browser.get('https://www.alamo.com/en_US/car-rental/reservation/selectCar.html')
    kk = [[15, 17], [15, 22]]
    for k in kk:
        print(i[2])

        try:
            start_date = (datetime.now() + timedelta(days=k[0])).strftime('%m/%d/%Y')
            end_date = (datetime.now() + timedelta(days=k[1])).strftime('%m/%d/%Y')
            print(start_date,end_date)



            main_url = 'https://www.alamo.com/en_US/car-rental/reservation/selectCar.html'
            sub_url = 'https://www.alamo.com/en_US/car-rental/reservation/selectCar.html'

            time.sleep(5)
            try:
                browser.find_element_by_xpath('/html/body/div[8]/div/div[1]/a').click()
            except :
                pass
            browser.find_element_by_xpath('//*[@id="_content_alamo_en_US_car_rental_reservation_startReservation_jcr_content_cq_colctrl_lt30_c1_start_pickUpLocation_searchCriteria"]').clear()
            browser.find_element_by_xpath('//*[@id="_content_alamo_en_US_car_rental_reservation_startReservation_jcr_content_cq_colctrl_lt30_c1_start_pickUpLocation_searchCriteria"]').send_keys(i[2])

            time.sleep(3)
            browser.find_element_by_xpath('//*[@id="_content_alamo_en_US_car_rental_reservation_startReservation_jcr_content_cq_colctrl_lt30_c1_start_pickUpLocation_searchCriteria"]').send_keys(Keys.ARROW_DOWN)
            browser.find_element_by_xpath('//*[@id="_content_alamo_en_US_car_rental_reservation_startReservation_jcr_content_cq_colctrl_lt30_c1_start_pickUpLocation_searchCriteria"]').send_keys(Keys.RETURN)

            try:
                browser.find_element_by_xpath('/html/body/div[3]/div/p/a[1]').click()
            except:
                pass
            browser.find_element_by_xpath('//*[@id="_content_alamo_en_US_car_rental_reservation_startReservation_jcr_content_cq_colctrl_lt30_c1_start_pickUpDateTime_date"]').clear()
            browser.find_element_by_xpath('//*[@id="_content_alamo_en_US_car_rental_reservation_startReservation_jcr_content_cq_colctrl_lt30_c1_start_pickUpDateTime_date"]').send_keys(start_date)
            browser.find_element_by_xpath('//*[@id="_content_alamo_en_US_car_rental_reservation_startReservation_jcr_content_cq_colctrl_lt30_c1_start_dropOffDateTime_date"]').clear()
            browser.find_element_by_xpath('//*[@id="_content_alamo_en_US_car_rental_reservation_startReservation_jcr_content_cq_colctrl_lt30_c1_start_dropOffDateTime_date"]').send_keys(end_date)
            # time.sleep(5)
            browser.find_element_by_xpath('//*[@id="_content_alamo_en_US_car_rental_reservation_startReservation_jcr_content_cq_colctrl_lt30_c1_start_submit"]').click()
            time.sleep(5)

            if main_url == browser.current_url and 'sold out'.lower() in browser.page_source:
                # print('========================================')
                # browser.close()

                continue
            time.sleep(5)
            # print('------------------------------')
            for m in range(10):
                jsoup = BeautifulSoup(browser.page_source)

                if sub_url == browser.current_url and jsoup.find('ul', attrs={'class': 'carList'}) is not None:
                    # print('11111111111111111111111111111111111111111111')
                    break
                elif sub_url == browser.current_url:
                    browser.refresh()
                    time.sleep(8)
                    # browser.close()



            # print('++++++++++++++++++++++++++++++')
            kk.append(k)
            # browser.close()


            for li in jsoup.find('ul', attrs={'class':'carList'}):
                try:
                    car_class = li.find('div', attrs={'class':'carDetails'}).find('h2')
                    print(car_class.text)
                    car_name = li.find('div', attrs={'class':'vehiclesSimilar'}).find('span')
                    print(car_name.text)
                    per_day_now = li.find('div',attrs = {'class':'priceInfoDetails'})
                    per_day_now = per_day_now.find('div', attrs={'class':'largePayment'})if per_day_now is not None else None

                    per_day_now = per_day_now.find_all('p')[0] if per_day_now is not None else None

                    per_day_now = re.search('\$[0-9\.]+', per_day_now.text) if per_day_now is not None else None

                    per_day_now = per_day_now.group(0) if per_day_now is not None else None

                    print(per_day_now)
                    pay_now_total = li.find('div', attrs={'class': 'priceInfoDetails'})
                    # print('++++++++++++++++++++++++++++++++')
                    pay_now_total = pay_now_total.find('div', attrs={'class': 'largePayment'}) if pay_now_total is not None else None
                    # print('-------------------------------')
                    pay_now_total = pay_now_total.find_all('p')[1] if pay_now_total is not None else None
                    pay_now_total = re.search('\$[0-9\.]+', pay_now_total.text) if pay_now_total is not None else None
                    pay_now_total = pay_now_total.group(0) if pay_now_total is not None else None
                    print(pay_now_total)


                    per_day_later = li.find('div',attrs = {'class':'priceInfoDetails'})
                    # print('-----------------------------------------------------------------------------------------------')
                    per_day_later = per_day_later.find('div', attrs={'class':re.compile('smallPayment|smallPaymentOnly')}) if per_day_later is not None else None
                    per_day_later = per_day_later.find_all('p')[0] if per_day_later is not None else None
                    per_day_later = re.search('\$[0-9\.]+',per_day_later.text) if per_day_later is not None else None
                    per_day_later = per_day_later.group(0) if per_day_later is not None else None
                    print(per_day_later)
                    pay_later_total = li.find('div',attrs = {'class':'priceInfoDetails'})
                    pay_later_total = pay_later_total.find('div', attrs={'class':re.compile('smallPayment|smallPaymentOnly')}) if pay_later_total is not None else None
                    pay_later_total = pay_later_total.find_all('p')[1] if pay_later_total is not None else None

                    pay_later_total = re.search('\$[0-9\.]+', pay_later_total.text) if pay_later_total is not None else None
                    pay_later_total = pay_later_total.group(0) if pay_later_total is not None else None
                    print(pay_later_total)
                    print('-'.center(100,'-'))
                    # break
                    data = [datetime.now().strftime('%m/%d/%Y'), start_date,end_date, i[1], i[0], i[0], i[2], car_class.text, car_name.text,per_day_now,'per  day',pay_now_total,' Est. Total', per_day_later,'per  day', pay_later_total,' Est. Total']
                    car_data.append(data)
                except Exception as e:
                    print(e)

        except:
            pass
    browser.close()

print(tabulate(car_data))
df = pd.DataFrame(car_data,columns=car_data_headers)
print(df)
df.to_excel('alamo.xlsx', index=False)
print('Time = ', (time.time()-startTime)/60)















