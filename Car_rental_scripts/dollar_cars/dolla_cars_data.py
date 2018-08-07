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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta
import re


def get_dollar_car_data(row, car_data):
    driver = maks_browser()
    carData = []
    count = 0
    check_count = 0
    check_days = [[15, 17], [15, 22]]
    for k in check_days:
        print(row['Code'], k)
        try:
            start_date = (datetime.now() + timedelta(days=k[0])).strftime('%b %d,%Y')
            end_date = (datetime.now() + timedelta(days=k[1])).strftime('%b %d,%Y')
            driver.getDriver().delete_all_cookies()
            driver.loadBrowser('https://www.dollar.com/Reservations/TimePlace.aspx?MessageType=Modify')

            # Select Location
            driver.sendKeys('contentplaceholder_0_column2placeholder_0_TimePlaceColumnLayout_LocationTime_PickupLocationTextBox', row['Code'])
            driver.dropDown(row['Short Name'], '//*[@id="contentplaceholder_0_column2placeholder_0_TimePlaceColumnLayout_LocationTime_PickupLocationTextBox"]','//*[@id="contentplaceholder_0_column2placeholder_0_TimePlaceColumnLayout_LocationTime_PickupLocationTextBox_LocationSearch_list"]')
            time.sleep(5)
            selected_airport = driver.getDriver().find_element_by_xpath('//*[@id="contentplaceholder_0_column2placeholder_0_TimePlaceColumnLayout_LocationTime_PickupLocationTextBox"]').get_attribute('value')
            # print('selected_location = ', selected_airport)


            time.sleep(2)
            driver.getDriver().find_element_by_tag_name('body').click()
            time.sleep(3)

            # Return Date
            driver.sendKeys('contentplaceholder_0_column2placeholder_0_TimePlaceColumnLayout_LocationTime_PickupDateCalendar_CalendarTextBox', start_date)
            time.sleep(3)
            driver.closePopUp('contentplaceholder_0_column2placeholder_0_TimePlaceColumnLayout_LocationTime_SectionLabelDiv3')


            driver.sendKeys("contentplaceholder_0_column2placeholder_0_TimePlaceColumnLayout_LocationTime_ReturnDateCalendar_CalendarTextBox", end_date)
            time.sleep(3)
            driver.oneClick('//*[@id="contentplaceholder_0_column2placeholder_0_TimePlaceColumnLayout_LocationTime_ReturnDateCalendar_AJAXCalendarLink"]')
            # driver.oneClick('contentplaceholder_0_column2placeholder_0_TimePlaceColumnLayout_LocationTime_ReturnDateCalendar_AJAXCalendarLink')

            time.sleep(3)

            # Get Rates
            driver.oneClick('//*[@id="contentplaceholder_0_column2placeholder_0_TimePlaceColumnLayout_LocationTime_GetRatesButton"]')
            time.sleep(5)

            WebDriverWait(driver.getDriver(), 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'PageMainContainer'))
            )
            jsoup = BeautifulSoup(driver.getDriver().page_source)
            selected_name = jsoup.find('span', attrs={'id':'contentplaceholder_0_column1placeholder_0_ReservationStatusColumnLayout_PickupAirportLabel'})
            selected_airport = selected_name.text.strip() if selected_name is not None else selected_airport
            vehicles = jsoup.find_all('div', attrs={'id':re.compile('VehicleRatesRepeater_Detail')})

            if len(vehicles)==0:
                continue
            duplicates = set()
            for vehicle in vehicles:
                VehicleGroupLevel = vehicle.find('span', attrs={'id': re.compile('VehicleGroupLevel')})
                VehicleGroupLevel = VehicleGroupLevel.text if VehicleGroupLevel is not None else None

                DescriptionLabel = vehicle.find('span', attrs={'id': re.compile('DescriptionLabel')})
                DescriptionLabel = DescriptionLabel.text if DescriptionLabel is not None else None


                #  Rapid Rental PrePay Rate
                BaseRateHyperlinkPP = vehicle.find('a', attrs={'id': re.compile('BaseRateHyperlinkPP')})
                payNowAmountUnits = None
                if BaseRateHyperlinkPP is not None:
                    payNowAmountUnits = BaseRateHyperlinkPP.findNext('span')
                    payNowAmountUnits = payNowAmountUnits.text if payNowAmountUnits is not None else None
                pay_now_BaseRate_hyperlinkPP = BaseRateHyperlinkPP.text if BaseRateHyperlinkPP is not None else None
                BaseRateHyperlinkPP.decompose() if BaseRateHyperlinkPP is not None else None


                RateTotalAmountLabelPP = vehicle.find('span', attrs={'id': re.compile('RateTotalAmountLabelPP')})
                payNowTotalAmountUnits = None
                if RateTotalAmountLabelPP is not None:
                    payNowTotalAmountUnits = RateTotalAmountLabelPP.findNext('span')
                    payNowTotalAmountUnits = payNowTotalAmountUnits.text if payNowTotalAmountUnits is not None else None

                pay_now_Rate_Total_AmountLabelPP = RateTotalAmountLabelPP.text if RateTotalAmountLabelPP is not None else None
                RateTotalAmountLabelPP.decompose() if RateTotalAmountLabelPP is not None else None

                # Approx Total
                BaseRateHyperlink = vehicle.find('a', attrs={'id': re.compile(('RateHyperlink'))})
                paylateramountunits = None
                if BaseRateHyperlink is not None:
                    paylateramountunits = BaseRateHyperlink.findNext('span')
                    paylateramountunits = paylateramountunits.text if paylateramountunits is not None else None

                Pay_Later_BaseRateHyperlink = BaseRateHyperlink.text if BaseRateHyperlink is not None else None


                RateTotal = vehicle.find('span', attrs={'id': re.compile('RateTotalAmountLabel|RateTotalDescLabel'), 'class':re.compile('FontSmallEmphasisLegal|RateLink')})
                paylatertotalamountunits = None

                if RateTotal is not None:
                    paylatertotalamountunits = RateTotal.findNext('span')
                    paylatertotalamountunits = paylatertotalamountunits.text if paylatertotalamountunits is not None else None

                RateTotal = re.search('\$[0-9\.,]+',RateTotal.text) if RateTotal is not None else None
                RateTotal = RateTotal.group(0) if RateTotal is not None else None

                if VehicleGroupLevel not in duplicates:
                    duplicates.add(VehicleGroupLevel)
                    data = [datetime.now(),  start_date, end_date, row['Location'], row['Airport name'],selected_airport,row['Code'], VehicleGroupLevel, DescriptionLabel, pay_now_BaseRate_hyperlinkPP,payNowAmountUnits, pay_now_Rate_Total_AmountLabelPP,payNowTotalAmountUnits, Pay_Later_BaseRateHyperlink,paylateramountunits, RateTotal, paylatertotalamountunits]
                    carData.append(data)

            count += 1

        except Exception as e:
            driver.getDriver().save_screenshot(row['Code'] + ".png")
            if check_count == 2:
                break
            check_count += 1
            check_days.append(k)
            print(e, row)
    driver.closeBrowser()
    if len(carData) != 0:
        car_data[row['Code']] = carData
        return car_data





