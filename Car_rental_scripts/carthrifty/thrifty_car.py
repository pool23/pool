"""
Purpose     : Extract data from comparefirst
        #####################     Change log   ###############################
        ##------------------------------------------------------------------##
        ##  Author              ##Date                ##Current Version     ##
        ##------------------------------------------------------------------##
        ## Moody's Analytics    ##11th July, 2018     ##V1.0                ##
        ##------------------------------------------------------------------##
        ######################################################################
        Date              Version     Author      Description
        11th July, 2018   v 1.0       Sairam      Data Extraction
"""
from selenium_browser import maks_browser
from datetime import datetime
from datetime import timedelta
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import re

def get_carthrifty_data(row, car_data):
    driver = maks_browser()
    carData = []
    count = 0
    check_count = 0
    check_days = [[15, 17],[15, 22]]
    for k in check_days:
        print(row['Code'], k)
        try:
            start_date = (datetime.now() + timedelta(days=k[0])).strftime('%b %d,%Y')
            end_date = (datetime.now() + timedelta(days=k[1])).strftime('%b %d,%Y')
            driver.getDriver().delete_all_cookies()
            driver.loadBrowser('https://www.thrifty.com/Reservations/index.aspx?SavedState=True&ControlTarget=TransitionLocationTime')
            driver.oneClick('//*[@id="reservations_controls_locationtime_ascx1_FeedbackCtrlLightBox_buttonLightBoxClose"]')
            selected_airport = driver.getDriver().find_element_by_xpath('//*[@id="reservations_controls_locationtime_ascx1_PickupLocationTextBox"]').get_attribute('value')
            if 'enter' in str(selected_airport).lower():
                driver.getDriver().find_element_by_xpath('//*[@id="reservations_controls_locationtime_ascx1_PickupLocationTextBox"]').clear()
            driver.sendKeys('reservations_controls_locationtime_ascx1_PickupLocationTextBox', row['Code'])
            driver.dropDown(row['Short Name'], '//*[@id="reservations_controls_locationtime_ascx1_PickupLocationTextBox"]', '//*[@id="reservations_controls_locationtime_ascx1_PickupLocationTextBox_LocationSearch_list"]')
            selected_airport = driver.getDriver().find_element_by_xpath('//*[@id="reservations_controls_locationtime_ascx1_PickupLocationTextBox"]').get_attribute('value')
            time.sleep(3)

            # Book Date
            driver.sendKeys('reservations_controls_locationtime_ascx1_PickupDateCalendar_CalendarTextBox', start_date)
            time.sleep(3)
            driver.oneClick('//*[@id="reservations_controls_locationtime_ascx1_PickupDateCalendar_AJAXCalendar"]')

            driver.sendKeys("reservations_controls_locationtime_ascx1_ReturnDateCalendar_CalendarTextBox", end_date)
            time.sleep(3)
            driver.oneClick('//*[@id="reservations_controls_locationtime_ascx1_ReturnDateCalendar_AJAXCalendar"]')

            driver.oneClick('//*[@id="reservations_controls_locationtime_ascx1_PickupDateCalendar_TimeDropDownList"]/option[24]')
            driver.oneClick('//*[@id="reservations_controls_locationtime_ascx1_ReturnDateCalendar_TimeDropDownList"]/option[24]')
            # Get Rates
            driver.oneClick('//*[@id="reservations_controls_locationtime_ascx1_SubmitButton"]')
            time.sleep(5)

            WebDriverWait(driver.getDriver(), 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'BodyPlaceHolder'))
            )

            driver.oneClick('//*[@id="mm-seeMoreCarsToggle"]')

            WebDriverWait(driver.getDriver(), 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'BodyPlaceHolder'))
            )

            page_source = driver.getDriver().page_source
            jsoup = BeautifulSoup(page_source)
            pickupLocation = jsoup.find('span', attrs={'id': re.compile('pickupLocation')})
            pickupLocation = pickupLocation.text.strip() if pickupLocation is not None else selected_airport
            vehicles = jsoup.find_all('div', attrs={'id': re.compile('vehicleOption')})
            duplicates = set()
            for vehicle in vehicles:

                className = vehicle.find('span', attrs={'class':re.compile('className')})
                className = className.text.strip() if className is not None else className
                vehicleName = vehicle.find('span', attrs={'class': re.compile('vehicleName')})
                vehicleName = vehicleName.text.strip() if vehicleName is not None else vehicleName

                payNowColumn = vehicle.find('div', attrs={'class': re.compile('payNowColumn')})
                payNowAmount = None
                payNowAmountUnit = None
                payNowTotalAmount = None
                payNowTotalUnit = None
                if payNowColumn is not None:
                    payNowPrice = payNowColumn.find('span', attrs={'class': re.compile('payNowPrice')})
                    if payNowPrice is not None:
                        payNowAmount = re.search('(\$[0-9\.,]+)( .*)', payNowPrice.text.strip())
                        payNowAmount, payNowAmountUnit = (payNowAmount.group(1), payNowAmount.group(2)) if payNowAmount is not None else (None, None)

                    payNowTotal = payNowColumn.find('span', attrs={'class': re.compile('payNowTotal')})
                    if payNowTotal is not None:
                        payNowTotalAmount = re.search('(\$[0-9\.,]+)( .*)', payNowTotal.text.strip())
                        payNowTotalAmount,payNowTotalUnit = (payNowTotalAmount.group(1),payNowTotalAmount.group(2).strip()) if payNowTotalAmount is not None else (None, None)

                payLaterColumn = vehicle.find('div', attrs={'class': re.compile('payLaterColumn')})
                payLaterAmount = None
                payLaterTotalAmount = None
                payLaterAmountUnit = None
                payLaterTotalUnit = None
                if payLaterColumn is not None:
                    payLaterPrice = payLaterColumn.find('span', attrs={'class': re.compile('payLaterPrice')})
                    if payLaterPrice is not None:
                        payLaterAmount = re.search('(\$[0-9\.,]+)( .*)', payLaterPrice.text.strip())
                        payLaterAmount, payLaterAmountUnit = (payLaterAmount.group(1), payLaterAmount.group(2).strip()) if payLaterAmount is not None else (None, None)

                    payLaterTotal = payLaterColumn.find('span', attrs={'class': re.compile('payLaterTotal')})
                    if payLaterTotal is not None:
                        payLaterTotalAmount = re.search('(\$[0-9\.,]+)( .*)', payLaterTotal.text.strip())
                        payLaterTotalAmount, payLaterTotalUnit = (payLaterTotalAmount.group(1), payLaterTotalAmount.group(2)) if payLaterTotalAmount is not None else (None, None)

                data = [datetime.now(), start_date, end_date, row['Location'], row['Airport name'], pickupLocation,row['Code'], className, vehicleName, payNowAmount, payNowAmountUnit,payNowTotalAmount,payNowTotalUnit,payLaterAmount,payLaterTotalUnit,payLaterTotalAmount,payLaterAmountUnit]
                if className not in duplicates:
                    duplicates.add(className)
                    carData.append(data)
            count+=1
        except Exception as e:

            driver.getDriver().save_screenshot(row['Code']+".png")
            if check_count == 2:
                break
            check_count+= 1
            check_days.append(k)
            print(e, row)

    driver.closeBrowser()
    if len(carData) != 0:
        car_data[row['Code']] = carData
        return car_data







