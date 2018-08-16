from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import time
from datetime import datetime
from datetime import timedelta

start_date_list = []
to_date_list = []
start_date = (datetime.now() + timedelta(days=15)).strftime('%m/%d/%Y')
todate = (datetime.now() + timedelta(days=17)).strftime('%m/%d/%Y')
todate1 = (datetime.now() + timedelta(days=22)).strftime('%m/%d/%Y')

carname = []
paylater =[]
paynow = []
port = []
vehical_name = []
d = {'ATL':[{'Location': 'Atlanta, Georgia', 'Airport_Name': 'Hartsfield–Jackson Atlanta International Airport'}],
     'ORD':[{'Location': 'Chicago, Illinois', 'Airport_Name': "Chicago O'Hare International Airport"}],
     'LAX':[{'Location': 'Los Angeles, California', 'Airport_Name': 'Los Angeles International Airport'}],
     'DFW':[{'Location': 'Dallas–Fort Worth Metroplex, Texas', 'Airport_Name': "Dallas/Fort Worth International Airport"}],
     'JFK':[{'Location': 'New York, New York', 'Airport_Name': 'John F. Kennedy International Airport'}],
     'DEN':[{'Location': 'Denver, Colorado', 'Airport_Name': "Denver International Airport"}],
     'SFO':[{'Location': 'San Francisco, California', 'Airport_Name': 'San Francisco International Airport'}],
     'LAS':[{'Location': 'Las Vegas, Nevada, Texas', 'Airport_Name': "McCarran International Airport"}],
     'CLT':[{'Location': 'Charlotte, North Carolina', 'Airport_Name': 'Charlotte Douglas International Airport'}],
     'MIA':[{'Location': 'Miami, Florida', 'Airport_Name': "Miami International Airport"}],
     'PHX':[{'Location': 'Phoenix, Arizona', 'Airport_Name': 'Phoenix Sky Harbor International Airport'}],
     'IAH':[{'Location': 'Houston, Texas', 'Airport_Name': "George Bush Intercontinental Airport"}],
     'SEA':[{'Location': 'SeaTac, Washington', 'Airport_Name': 'Seattle–Tacoma International Airport'}],
     'MCO':[{'Location': 'Orlando, Florida', 'Airport_Name': "Orlando, Florida"}],
     'EWR':[{'Location': 'Newark, New Jersey', 'Airport_Name': 'Newark Liberty International Airport'}],
     'MSP':[{'Location': 'Minneapolis–Saint Paul, Minnesota', 'Airport_Name': "Minneapolis–Saint Paul International Airport"}],
     'BOS': [{'Location': 'Boston, Massachusetts', 'Airport_Name': "Logan International Airport"}],
     'DTW': [{'Location': 'Romulus, Michigan', 'Airport_Name': 'Detroit Metropolitan Airport'}],
     'PHL': [{'Location': 'Philadelphia, Pennsylvania', 'Airport_Name': "Philadelphia International Airport"}],
     'LGA': [{'Location': 'New York, New York', 'Airport_Name': 'LaGuardia Airport'}],
     'FLL': [{'Location': 'Fort Lauderdale, Florida', 'Airport_Name': "Fort Lauderdale–Hollywood International Airport"}],
     'BWI': [{'Location': 'Linthicum, Maryland', 'Airport_Name': 'Baltimore–Washington International Airport'}],
     'DCA': [{'Location': 'Arlington, Virginia', 'Airport_Name': "Ronald Reagan Washington National Airport"}],
     'MDW': [{'Location': 'Chicago, Illinois', 'Airport_Name': 'Chicago Midway International Airport'}],
     'SLC': [{'Location': 'Salt Lake City, Utah', 'Airport_Name': "Salt Lake City International Airport"}],
     'IAD': [{'Location': 'Dulles, Virginia', 'Airport_Name': 'Washington Dulles International Airport'}],
     'SAN': [{'Location': 'San Diego, California', 'Airport_Name': "San Diego International Airport"}],
     'HNL': [{'Location': 'Honolulu, Hawaii', 'Airport_Name': 'Daniel K. Inouye International Airport'}],
     'TPA': [{'Location': 'Tampa, Florida', 'Airport_Name': "Tampa International Airport"}],
     'PDX': [{'Location': 'Portland, Oregon', 'Airport_Name': 'Portland International Airport'}]
     }

Selected_Location = []
loc = []
air_port = []
sold_out =[]
driver = webdriver.Firefox()
file = ['ATL', 'ORD', 'LAX', 'DFW', 'JFK', 'DEN', 'SFO', 'LAS', 'CLT', 'MIA', 'PHX', 'SEA', 'MCO', 'EWR', 'MSP', 'BOS',
        'DTW', 'PHL', 'LGA', 'FLL', 'BWI', 'DCA', 'MDW', 'SLC', 'IAD', 'SAN', 'HNL', 'TPA', 'PDX', 'IAH']
for j in [todate, todate1]:
    for i in file:
        i = i.strip()
        driver.get('https://www.budget.com/en/home')
        driver.find_element_by_xpath('//*[@id="PicLoc_value"]').clear()
        h_val = driver.find_element_by_xpath('//*[@id="PicLoc_value"]')
        h_val.send_keys(i)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="PicLoc_dropdown"]/div[3]/div[1]/div[2]/div/div/span/span[1]')))
        # print(c)
        driver.find_element_by_xpath('//*[@id="PicLoc_dropdown"]/div[3]/div[1]/div[2]/div/div/span/span[1]').click()
        print(h_val.get_attribute('value'))
        l_se = h_val.get_attribute('value')
        driver.find_element_by_xpath('//*[@id="from"]').clear()
        driver.find_element_by_xpath('//*[@id="to"]').clear()
        date_pick_start = driver.find_element_by_xpath('//*[@id="from"]').send_keys(start_date)
        date_pick_end = driver.find_element_by_xpath('//*[@id="to"]').send_keys(j)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="to"]')))
        driver.find_element_by_xpath('//*[@id="to"]').send_keys(Keys.RETURN)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="res-home-select-car"]')))
        driver.find_element_by_xpath('//*[@id="res-home-select-car"]').click()
        try:
            time.sleep(10)
            try:
                wait = WebDriverWait(driver, 10)
                wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "ftrcartxt")))
                car_name = driver.find_element_by_css_selector('#reservation-partial > div > div > div.vehicle-availability > section:nth-child(7) > div.step2dtl > div > div.col-sm-5.ftrcardtl > div > h3')
                print(car_name.get_attribute('innerHTML'))
                p_later = driver.find_element_by_css_selector('#reservation-partial > div > div > div.vehicle-availability > section:nth-child(7) > div.step2dtl > div > div.col-sm-5.ftrcardtl > div > div:nth-child(6) > div.payatcntr.col-xs-6 > p')
                print(p_later.get_attribute('innerText'))
                all_cars_name = [link.find_element_by_tag_name('h3').get_attribute('innerHTML') for link in driver.find_elements_by_class_name('step2dtl-avilablecar-section')]
                all_cars_name.append(car_name.get_attribute('innerHTML'))
                v_name = driver.find_element_by_css_selector('#reservation-partial > div > div > div.vehicle-availability > section:nth-child(7) > div.step2dtl > div > div.col-sm-5.ftrcardtl > div > p')
                print(v_name.get_attribute('innerText'))
                v_n = [link.find_element_by_xpath(".//p[@class ='featurecartxt similar-car']").text for link in driver.find_elements_by_class_name('step2dtl-avilablecar-section')]
                v_n.append(v_name.get_attribute('innerText'))
                print(v_n)
                pay_later = [link.find_element_by_xpath(".//div[p/@class ='payamntp']").get_attribute('innerText').rstrip('\n\nPay at Counter') for link in driver.find_elements_by_class_name('step2dtl-avilablecar-section')]
                pay_later.append(p_later.get_attribute('innerText'))
                pay_now = driver.find_element_by_css_selector('#reservation-partial > div > div > div.vehicle-availability > section:nth-child(7) > div.step2dtl > div > div.col-sm-5.ftrcardtl > div > div:nth-child(6) > div.paynow.col-xs-6 > p.payamntr > price')
                print(pay_now.get_attribute('innerText'))
                p_now = []
                for link in driver.find_elements_by_class_name('step2dtl-avilablecar-section'):
                    try:
                        p_now.append(link.find_element_by_tag_name('price').get_attribute('innerText'))
                    except:
                        p_now.append('NAN')
                p_now.append(pay_now.get_attribute('innerText'))
                print(all_cars_name)
                print('Pay_Later', pay_later)
                print('pay_now', p_now)
                for cn in all_cars_name:
                    carname.append(cn)
                    sold_out.append('Available')
                    port.append(i)
                    Selected_Location.append(l_se)
                    loc.append(d[i][0]['Location'])
                    air_port.append(d[i][0]['Airport_Name'])
                    start_date_list.append(start_date)
                    to_date_list.append(j)
                for cp in pay_later:
                    paylater.append(cp)
                for pl in p_now:
                    paynow.append(pl)
                for vn in v_n:
                    vehical_name.append(vn)
            except:
                all_cars_name = [link.find_element_by_tag_name('h3').get_attribute('innerHTML') for link in driver.find_elements_by_class_name('step2dtl-avilablecar-section')]
                pay_later = [link.find_element_by_xpath(".//div[p/@class ='payamntp']").get_attribute('innerText').rstrip('\n\nPay at Counter') for link in driver.find_elements_by_class_name('step2dtl-avilablecar-section')]
                p_now = []
                for link in driver.find_elements_by_class_name('step2dtl-avilablecar-section'):
                    try:
                        p_now.append(link.find_element_by_tag_name('price').get_attribute('innerText'))
                    except:
                        p_now.append('NAN')
                wait = WebDriverWait(driver, 10)
                wait.until(EC.visibility_of_element_located((By.XPATH, ".//p[@class ='featurecartxt similar-car']")))
                v_n = [link.find_element_by_xpath(".//p[@class ='featurecartxt similar-car']").text for link in
                       driver.find_elements_by_class_name('step2dtl-avilablecar-section')]

                print('pay_now', p_now)
                for cn in all_cars_name:
                    carname.append(cn)
                    sold_out.append('Available')
                    port.append(i)
                    Selected_Location.append(l_se)
                    loc.append(d[i][0]['Location'])
                    air_port.append(d[i][0]['Airport_Name'])
                    start_date_list.append(start_date)
                    to_date_list.append(j)
                for cp in pay_later:
                    paylater.append(cp)
                for pl in p_now:
                    paynow.append(pl)
                for vn in v_n:
                    vehical_name.append(vn)
            # print(carname)
            print(paynow)
            # print(paylater)
            print(vehical_name)
            # print(port)
            # print(Selected_Location)
            # print(loc)
            # print(air_port)
            print(len(carname))
            print(len(paynow))
            print(len(paylater))
            print(len(vehical_name))
            print(len(port))
            print(len(Selected_Location))
            print(len(loc))
            print(len(air_port))
            print(len(start_date_list))
            print(len(to_date_list))
            print(len(sold_out))
        except:
            sold_out.append('sold out')
            port.append(i)
            carname.append('0')
            paynow.append('0')
            paylater.append('0')
            vehical_name.append('0')
            Selected_Location.append(l_se)
            loc.append(d[i][0]['Location'])
            air_port.append(d[i][0]['Airport_Name'])
            start_date_list.append(start_date)
            to_date_list.append(j)
            print(len(carname))
            print(len(paynow))
            print(len(paylater))
            print(len(vehical_name))
            print(len(port))
            print(len(Selected_Location))
            print(len(loc))
            print(len(air_port))
            print(len(start_date_list))
            print(len(to_date_list))
            print(len(sold_out))
    driver.delete_all_cookies()
driver.close()
df = pd.DataFrame({'Date': datetime.today().strftime('%d/%m/%Y'), 'Location Code': port,
                   'className': carname, 'Sold_Out': sold_out,
                   'Pay_Now_Amount': paynow, 'payLaterAmount': paylater, 'vehicleName': vehical_name,
                   'pickup_date': start_date_list, 'return_date': to_date_list,
                   'selected_location': Selected_Location,
                   'Location': loc, 'Airport name': air_port})
#  print(df)
# Rearranging columns according to requirement
df = df.reindex(columns =["Date", "pickup_date", "return_date", "Location", "Airport name", "selected_location",
             "Location Code", "className", "vehicleName", 'payLaterAmount',  'Pay_Now_Amount', "Sold_Out", "sitename"])
# df = df[["Site", "Day", "Month", "Year", 'City', 'Location', 'State', 'Country']]
df.to_excel('budget.xlsx', index=False)
