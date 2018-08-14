import time
from datetime import datetime
from datetime import timedelta
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate
import re
import warnings
warnings.simplefilter(action='ignore')


car_data_headers = ['Date', 'pickup_date', 'return_date','Location', 'Airport name','selected_location', 'Location Code',
                    'className', 'vehicleName', 'payNowAmount', 'payNowAmountUnit',
                'payNowTotalAmount','payNowTotalUnit','payLaterAmount','payLaterAmountUnit','payLaterTotalAmount','payLaterTotalUnit','sitename']
car_data = []
startTime = time.time()
browser = webdriver.Firefox()
browser.maximize_window()
airport = [["Hartsfield–Jackson Atlanta International Airport","Atlanta, Georgia","ATL"],["Chicago O'Hare International Airport","Chicago, Illinois","ORD"],["Los Angeles International Airport","Los Angeles, California","LAX"],["Dallas/Fort Worth International Airport","Dallas–Fort Worth Metroplex, Texas","DFW"],["John F. Kennedy International Airport","New York, New York","JFK"],["Denver International Airport","Denver, Colorado","DEN"],["San Francisco International Airport","San Francisco, California","SFO"],["McCarran International Airport","Las Vegas, Nevada","LAS"],["Charlotte Douglas International Airport","Charlotte, North Carolina","CLT"],["Miami International Airport","Miami, Florida","MIA"],["Phoenix Sky Harbor International Airport","Phoenix, Arizona","PHX"],["George Bush Intercontinental Airport","Houston, Texas","IAH"],["Seattle–Tacoma International Airport","SeaTac, Washington","SEA"],["Orlando International Airport","Orlando, Florida","MCO"],["Newark Liberty International Airport","Newark, New Jersey","EWR"],["Minneapolis–Saint Paul International Airport","Minneapolis–Saint Paul, Minnesota","MSP"],["Logan International Airport","Boston, Massachusetts","BOS"],["Detroit Metropolitan Airport","Romulus, Michigan","DTW"],["Philadelphia International Airport","Philadelphia, Pennsylvania","PHL"],["LaGuardia Airport","New York, New York","LGA"],["Fort Lauderdale–Hollywood International Airport","Fort Lauderdale, Florida","FLL"],["Baltimore–Washington International Airport","Linthicum, Maryland","BWI"],["Ronald Reagan Washington National Airport","Arlington, Virginia","DCA"],["Chicago Midway International Airport","Chicago, Illinois","MDW"],["Salt Lake City International Airport","Salt Lake City, Utah","SLC"],["Washington Dulles International Airport","Dulles, Virginia","IAD"],["San Diego International Airport","San Diego, California","SAN"],["Daniel K. Inouye International Airport","Honolulu, Hawaii","HNL"],["Tampa International Airport","Tampa, Florida","TPA"],["Portland International Airport","Portland, Oregon","PDX"]]
for i in airport:
    for k in [[15, 17], [15, 22]]:
        print(i[2])
        try:

            start_date = (datetime.now() + timedelta(days=k[0])).strftime('%B %d')
            start_day = str(int(start_date.split()[-1]))
            start_month = str(start_date.split()[0])
            end_date = (datetime.now() + timedelta(days=k[1])).strftime('%B %d')
            end_day = str(int(end_date.split()[-1]))
            end_month = str(end_date.split()[0])


            print(start_date, end_date)
            pickup_date = (datetime.now() + timedelta(days=k[0])).strftime('%m/%d/%Y')
            return_date = (datetime.now() + timedelta(days=k[1])).strftime('%m/%d/%Y')
            print('https://www.nationalcar.com/en_US/car-rental/reservation/startReservation.html')
            #LOAD_URL
            browser.get('https://beta.nationalcar.com/en/car-rental.html?icid=ab-_-gotoBeta-_-startReservation&mboxSession=0eaa7efb533c477c867d509501fcf163&adobe_mc_ref=&adobe_mc_sdid=SDID%3D6272ABCE4665E897-5DDDAFA7C8B6B6A5%7CMCORGID%3D30545A0C536B768C0A490D44%2540AdobeOrg%7CTS%3D1533887357')
            time.sleep(5)

            #LOCATION
            browser.find_element_by_xpath('//*[@id="search-autocomplete__input-PICKUP"]').clear()
            browser.find_element_by_xpath('//*[@id="search-autocomplete__input-PICKUP"]').send_keys(i[2])
            time.sleep(5)
            browser.find_element_by_xpath('/html/body/div[2]/main/div[2]/section/div/div/div/h1').click()

            #PICKUP_DATE
            browser.find_element_by_xpath('//*[@id="date-time__pickup-toggle"]').click()
            browser.find_element_by_xpath("//*[@id='dateContainerId']//button[contains(@class, 'date-selector') and contains(@aria-label, '"+start_month+" "+start_day+"')]").click()
            time.sleep(5)

            #RETURN_DATE
            browser.find_element_by_xpath('//*[@id="date-time__return-toggle"]').click()
            browser.find_element_by_xpath("//*[@id='dateContainerId']//button[contains(@class, 'date-selector') and contains(@aria-label, '"+end_month+" "+end_day+"')]").click()

            #SUBMIT
            browser.find_element_by_css_selector('#booking-widget-inputs > div.booking-widget__right-column > div > button').click()
            # time.sleep(5)
            #POPUP
            try:

                browser.find_element_by_css_selector('body > div:nth-child(27) > div > div > div > div.modal__body > div > div.login-or-guest-modal__info-container > div > button').click()
            except:
                pass
            time.sleep(10)

            #PAGE_SOURCE
            jsoup = BeautifulSoup(browser.page_source)
            car_details = jsoup.find('div',attrs={'class':'vehicle-list'})
            for cars in car_details:
                car_class = cars.find('div',attrs={'class':'vehicle__content'}).find('h2', attrs={'class':'vehicle__type-name'})
                print(car_class.text)
                car_name = cars.find('p', attrs={'class':'vehicle__type-desc'})
                print(car_name.text)
                per_day_later = cars.find('p', attrs={'class': 'vehicle__price-day'})

                per_day_later = re.search('(\$[0-9\., ]+)(/[a-zA-Z ]+)', per_day_later.text) if per_day_later is not None else None
                per_day_later, per_day_later_unit = (per_day_later.group(1),per_day_later.group(2).replace('/','')) if per_day_later is not None else (None, None)
                print(per_day_later)
                print(per_day_later_unit)


                pay_later_total = cars.find('p', attrs={'class': 'vehicle__price-total'})

                pay_later_total = re.search('(\$[0-9\., ]+)([a-zA-Z ]+)', pay_later_total.text) if pay_later_total is not None else None
                pay_later_total,pay_later_total_unit = (pay_later_total.group(1),pay_later_total.group(2)) if pay_later_total is not None else (None,None)
                print(pay_later_total)
                print(pay_later_total_unit)
                data = [datetime.now().strftime('%m/%d/%Y'), pickup_date, return_date, i[1], i[0], i[0], i[2],car_class.text,
                        car_name.text, None, None, None, None, per_day_later,per_day_later_unit,pay_later_total, pay_later_total_unit,'National']
                car_data.append(data)
        except Exception as e:
            print(e)



browser.close()

print(tabulate(car_data))
df = pd.DataFrame(car_data,columns=car_data_headers)
print(df)
df.to_excel('National_car.xlsx', index=False)
print('Time = ', (time.time()-startTime)/60)
