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
import pandas as pd
import time
from bs4 import BeautifulSoup
from tabulate import tabulate
from datetime import datetime
from datetime import timedelta

import re
def load_car_data():
    pass
DF = pd.read_excel('dollar_car_locations.xlsx')
print(DF.to_dict(orient='records'))
mainRows = total_records = DF.to_dict(orient='records')
print(mainRows)
car_data_headers = ['Date','Location', 'Airport name','selected_location', 'Location Code', 'className', 'vehicleName', 'payNowAmount', 'payNowAmountUnit',
                'payNowTotalAmount','payNowTotalUnit','payLaterAmount','payLaterTotalAmount','payLaterAmountUnit','payLaterTotalUnit', 'pickup_date', 'return_date']
car_data = []
driver = maks_browser()
start_time = time.time()
for row in mainRows:
    for k in [[15, 17], [15, 22]]:
        try:
            start_date = (datetime.now() + timedelta(days=k[0])).strftime('%b %d,%Y')
            end_date = (datetime.now() + timedelta(days=k[1])).strftime('%b %d,%Y')
            print(row)
            driver.getDriver().delete_all_cookies()
            driver.loadBrowser('https://www.dollar.com/Reservations/TimePlace.aspx?MessageType=Modify')
            # driver.oneClick('//*[@id="contentplaceholder_0_column1placeholder_0_ResStartColumnLayout_LocationTime_FeedbackCtrlLightBox_buttonLightBoxClose"]')

            # Book Date
            # driver.sendKeys('contentplaceholder_0_column2placeholder_0_TimePlaceColumnLayout_LocationTime_PickupLocationTextBox', row['Code'])
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

            vehicles = BeautifulSoup(driver.getDriver().page_source).find_all('div', attrs={'id':re.compile('VehicleRatesRepeater_Detail')})

            print('vehicles = ', vehicles)
            if len(vehicles)==0:
                continue
            duplicates = set()
            for vehicle in vehicles:
                try:
                    VehicleGroupLevel = vehicle.find('span', attrs={'id': re.compile('VehicleGroupLevel')})
                    VehicleGroupLevel = VehicleGroupLevel.text if VehicleGroupLevel is not None else None
                    # print('VehicleGroupLevel = ', VehicleGroupLevel)
                    DescriptionLabel = vehicle.find('span', attrs={'id': re.compile('DescriptionLabel')})
                    DescriptionLabel = DescriptionLabel.text if DescriptionLabel is not None else None
                    # print('DescriptionLabel = ', DescriptionLabel)

                    #  Rapid Rental PrePay Rate
                    BaseRateHyperlinkPP = vehicle.find('a', attrs={'id': re.compile('BaseRateHyperlinkPP')})
                    payNowAmountUnits = None
                    if BaseRateHyperlinkPP is not None:
                        payNowAmountUnits = BaseRateHyperlinkPP.findNext('span')
                        payNowAmountUnits = payNowAmountUnits.text if payNowAmountUnits is not None else None
                    pay_now_BaseRate_hyperlinkPP = BaseRateHyperlinkPP.text if BaseRateHyperlinkPP is not None else None
                    BaseRateHyperlinkPP.decompose() if BaseRateHyperlinkPP is not None else None
                    # print('BaseRateHyperlinkPP = ', BaseRateHyperlinkPP)

                    RateTotalAmountLabelPP = vehicle.find('span', attrs={'id': re.compile('RateTotalAmountLabelPP')})
                    payNowTotalAmountUnits = None
                    if RateTotalAmountLabelPP is not None:
                        payNowTotalAmountUnits = RateTotalAmountLabelPP.findNext('span')
                        payNowTotalAmountUnits = payNowTotalAmountUnits.text if payNowTotalAmountUnits is not None else None

                    pay_now_Rate_Total_AmountLabelPP = RateTotalAmountLabelPP.text if RateTotalAmountLabelPP is not None else None
                    RateTotalAmountLabelPP.decompose() if RateTotalAmountLabelPP is not None else None
                    # print('Rate_Total_AmountLabelPP = ', pay_now_Rate_Total_AmountLabelPP)

                    # Approx Total
                    BaseRateHyperlink = vehicle.find('a', attrs={'id': re.compile(('RateHyperlink'))})
                    paylateramountunits = None
                    if BaseRateHyperlink is not None:
                        paylateramountunits = BaseRateHyperlink.findNext('span')
                        paylateramountunits = paylateramountunits.text if paylateramountunits is not None else None
                        # day_form = day_form.text.replace('/', '').strip() if day_form is not None else None
                    Pay_Later_BaseRateHyperlink = BaseRateHyperlink.text if BaseRateHyperlink is not None else None

                    # print('BaseRateHyperlink = ', Pay_Later_BaseRateHyperlink)

                    RateTotal = vehicle.find('span', attrs={'id': re.compile('RateTotalAmountLabel|RateTotalDescLabel'), 'class':re.compile('FontSmallEmphasisLegal|RateLink')})
                    paylatertotalamountunits = None

                    if RateTotal is not None:
                        paylatertotalamountunits = RateTotal.findNext('span')
                        paylatertotalamountunits = paylatertotalamountunits.text if paylatertotalamountunits is not None else None

                    # print('RateTotal = ', RateTotal)
                    RateTotal = re.search('\$[0-9\.,]+',RateTotal.text) if RateTotal is not None else None
                    RateTotal = RateTotal.group(0) if RateTotal is not None else None
                    # print('After RateTotal = ', RateTotal)
                    # print('RateTotalAmountLabel = ', RateTotal)

                    if VehicleGroupLevel not in duplicates:
                        duplicates.add(VehicleGroupLevel)
                        data = [datetime.now(), row['Location'], row['Airport name'],selected_airport,row['Code'], VehicleGroupLevel, DescriptionLabel, pay_now_BaseRate_hyperlinkPP,payNowAmountUnits, pay_now_Rate_Total_AmountLabelPP,payNowTotalAmountUnits, Pay_Later_BaseRateHyperlink,paylateramountunits, RateTotal, paylatertotalamountunits, start_date, end_date]
                        print(data)
                        car_data.append(data)
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)
            print('Missed row', row)
print(tabulate(car_data))
df = pd.DataFrame(car_data,columns=car_data_headers)
df.to_excel('sample.xlsx', index=False)
driver.closeBrowser()
print('Total Execution time = ', (time.time()-start_time)/60, 'Min')




