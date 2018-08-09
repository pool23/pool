from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd
import datetime


now = datetime.datetime.today().day
# d1 = now + int(2)
cd1 = now + int(15)
todate = cd1 + int(2)
todate1 = cd1 + int(7)

# to_date2 = datetime.datetime.today().replace(day = d2)
# print(to_date2.strftime('%m/%d/%Y'))
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
start_date_list = []
to_date_list = []
driver = webdriver.Firefox()
file = ['ATL', 'ORD', 'LAX', 'DFW', 'JFK', 'DEN', 'SFO', 'LAS', 'CLT', 'MIA', 'PHX', 'SEA', 'MCO', 'EWR', 'MSP', 'BOS',
        'DTW', 'PHL', 'LGA', 'FLL', 'BWI', 'DCA', 'MDW', 'SLC', 'IAD', 'SAN', 'HNL', 'TPA', 'PDX']
for j in [todate, todate1]:
    for i in file:
            # st_date = datetime.datetime.today().replace(day = cd1)
            start_date = datetime.datetime.today().replace(day=cd1).strftime('%m/%d/%Y')
            # to_date = datetime.datetime.today().replace(day = cd1)
            to_date = datetime.datetime.today().replace(day=j).strftime('%m/%d/%Y')
            i = i.strip()
            driver.get('https://www.avis.com/en/home')
            time.sleep(10)
            driver.find_element_by_xpath('//*[@id="PicLoc_value"]').clear()
            h_val = driver.find_element_by_xpath('//*[@id="PicLoc_value"]')
            h_val.send_keys(i)
            time.sleep(15)
            wait = WebDriverWait(driver, 20)
            wait.until(EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="PicLoc_dropdown"]/div[3]/div[1]/div[2]/div/div/span/span[1]')))
            # print(c)
            driver.find_element_by_xpath('//*[@id="PicLoc_dropdown"]/div[3]/div[1]/div[2]/div/div/span/span[1]').click()
            print(h_val.get_attribute('value'))
            l_se = h_val.get_attribute('value')
            driver.find_element_by_xpath('//*[@id="from"]').clear()
            driver.find_element_by_xpath('//*[@id="to"]').clear()
            date_pick_start = driver.find_element_by_xpath('//*[@id="from"]').send_keys(start_date)
            date_pick_end = driver.find_element_by_xpath('//*[@id="to"]').send_keys(to_date)
            try:
                wait = WebDriverWait(driver, 25)
                wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="calendarclose"]')))
                driver.find_element_by_xpath('//*[@id="calendarclose"]').click()
                wait = WebDriverWait(driver, 20)
                wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="res-home-select-car"]')))
                driver.find_element_by_xpath('//*[@id="res-home-select-car"]').click()
            except:
                wait = WebDriverWait(driver, 25)
                wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="calendarclose"]')))
                driver.find_element_by_xpath('//*[@id="calendarclose"]').click()
                wait = WebDriverWait(driver, 20)
                wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="res-home-select-car"]')))
                driver.find_element_by_xpath('//*[@id="res-home-select-car"]').click()
            try:
                time.sleep(20)
                try:
                    wait = WebDriverWait(driver, 20)
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
                        to_date_list.append(to_date)
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
                    wait = WebDriverWait(driver, 20)
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
                        to_date_list.append(to_date)
                    for cp in pay_later:
                        paylater.append(cp)
                    for pl in p_now:
                        paynow.append(pl)
                    for vn in v_n:
                        vehical_name.append(vn)
                print(paynow)
                print(vehical_name)
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
                to_date_list.append(to_date)
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
driver.close()
with open('Avis.csv', 'a') as f:
    df = pd.DataFrame({'Scrape_Date': datetime.datetime.today().strftime('%d/%m/%Y'), 'Location_Code': port,
                       'Class_Name': carname, 'Sold_Out': sold_out,
                       'Pay_Now_Amount': paynow, 'Pay_Later_Amount': paylater, 'Vehicle_Name': vehical_name,
                       'Pickup_Date': start_date_list, 'Return_Date': to_date_list,
                       'Selected_Location': Selected_Location,
                       'Location': loc, 'Airport_Name': air_port})
    #  print(df)
    # Rearranging columns according to requirement
    df = df[["Scrape_Date", "Pickup_Date", "Return_Date", "Location", "Airport_Name", "Selected_Location",
                 "Location_Code","Sold_Out", "Class_Name", "Vehicle_Name", 'Pay_Now_Amount', 'Pay_Later_Amount']]
    # df = df[["Site", "Day", "Month", "Year", 'City', 'Location', 'State', 'Country']]
    df.to_csv(f, header= False, index=False)
h=["Scrape_Date", "Pickup_Date", "Return_Date", "Location", "Airport_Name", "Selected_Location",
                 "Location_Code","Sold_Out", "Class_Name", "Vehicle_Name", 'Pay_Now_Amount', 'Pay_Later_Amount']
df1 = pd.DataFrame(df.values, columns=h)
df1.to_excel('Avis.xlsx', index=False)


