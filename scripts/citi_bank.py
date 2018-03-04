from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from bs4 import  BeautifulSoup as bs
import pandas as pd
import time
import pyautogui
import os
import sys
import warnings
import datetime
import logging as log
from maks_lib import logpath,output_path,input_path
from maks_lib import log_config
from maks_lib import output_path

now = datetime.datetime.now()

warnings.simplefilter(action='ignore')


class Citi_bank:
    def __init__(self, url):
        self.url = url

    def start_driver(self):
        self.driver = webdriver.Firefox()

    def close_driver(self):
        return self.driver.close()

    def get_url(self):
        self.driver.get(self.url)

    def select_state(self):
        time.sleep(10)
        click1 = self.driver.find_element_by_class_name("ui-selectmenu-item-header")
        click1.click()
        time.sleep(2)
        click2 = self.driver.find_element_by_id("RegionalPricingLocation-snapshot-menu-option-1")
        click2.click()
        time.sleep(2)
        select_btn = self.driver.find_element_by_id("cmlink_GoBtnLocForm")
        select_btn.click()
        time.sleep(3)

    def get_current_url(self):
        return self.driver.current_url

    def save_page(self):
        # pyautogui.hotkey('ctrl', 's')
        # time.sleep(1)
        # pyautogui.typewrite("citi")
        # time.sleep(1)
        # pyautogui.hotkey('enter')
        page = self.driver.page_source
        with open("citi_tab2.html", 'a')as file:
            file.write(page)

    def unhide(self):
        pass
        # time.sleep(3)
        # unhind = self.driver.find_element_by_xpath('//*[@class = "open"]')
        # unhind.click()
        # time.sleep(2)



class ExtractInfo(Citi_bank):
    def __init__(self, page,tab):
        self.page = page
        self.tab = tab

    def findtables_tab1(self):
        soup = bs(self.page, "lxml")
        file = open('final.csv','a')
        data = []


        for tr in soup.find_all('tr', {"class": self.tab}):
            tds = tr.find_all('td')
            row = [elem.text.strip() for elem in tds]
            data.append(row)


        df = pd.DataFrame.from_records(data[1:])
        temp = df.iloc[5:12,3:5].copy(deep = True)
        df.drop(df.columns[[3, 4, 5]], axis=1, inplace=True)
        df_0 = df[1:4]
        df_0["Product Name"] = df.iloc[0, 0].replace("Footnote 1", "")
        df_0["Product Type"] = "Checking Account"
        df_1 = df.iloc[5:12]
        df_1[df_1.columns[1]] = temp[temp.columns[0]]
        df_1[df_1.columns[2]] = temp[temp.columns[1]]
        df_1["Product Name"] = df.iloc[4, 0]
        df_1["Product Type"] = "Savings Account"
        df_2 = df.iloc[13:20]
        df_2["Product Name"] = df.iloc[12, 0]
        df_2["Product Type"] = "Savings Account"
        df_3 = df.iloc[21:28]
        df_3["Product Name"] = df.iloc[20, 0]
        df_3["Product Type"] = "Savings Account"
        df = pd.concat([df_0, df_1, df_2, df_3])
        df.columns = ['Balance', 'APY', 'Interest Rate','Product Name', "Product Type"]
        df["Date"] = now.strftime("%m-%d-%Y")
        df["Bank Name"] = "Citi Bank"
        df["Tab Name"] = "CHECKING & SAVINGS"
        df = df.reindex(columns= ["Date","Bank Name","Tab Name","Product Type",'Product Name','Balance', 'Interest Rate', 'APY'])
        df.to_csv(output_path+"CITI_Data_Deposit_{}.csv".format(now.strftime("%m_%d_%Y")), index =False)

        file.close()

        # for table in soup.find_all('table'):
        #     for trs in table.find_all('tr'):
        #         tds = trs.find_all('td')
        #
        #         row = [elem.text.strip().encode('utf-8') for elem in tds]
        #         print(row)
        # //*[@id="cmlink_ProdDisp"]
    def findtables_tab2(self):
        soup = bs(self.page, "lxml")
        data = []
        for tr in soup.find_all('tr', {"class": self.tab}):
            tds = tr.find_all('td')

            row = [elem.text.strip() for elem in tds]
            data.append(row)
        df = pd.DataFrame.from_records(data)
        df.drop(df.columns[3], axis=1, inplace=True)
        df.drop(df.index[8:24], inplace=True)
        df.drop(df.index[16:48], inplace=True)
        df.drop(df.index[24:40], inplace=True)
        df.drop(df.index[32:40], inplace=True)
        df.drop(df.index[40:], inplace=True)
        df0 = df[1:8];df0["Years"] = "3 months"
        df1 = df[9:16];df1["Years"] = "6 months"
        df2 = df[17:24];df2["Years"] = "1 year"
        df3 = df[25:32];df3["Years"] = "2 year"
        df4 = df[33:40];df4["Years"] = "3 year"
        # df0 =  pd.DataFrame(df0.str.split('-', 1).tolist(), columns=['Minimum Balance', 'Maximum Balance'])
        dfn = pd.concat([df0,df1, df2, df3, df4])
        dfn.columns = ['Minimum Balance', 'Maximum Balance', 'APY', 'Interest Rate', "Years"]

        dfn["Date"] = now.strftime("%m-%d-%Y")
        dfn["Bank Name"] = "Citi Bank"
        dfn["Tab Name"] = "CERTIFICATES OF DEPOSIT"
        df_final = dfn.reindex(columns=["Date", "Bank Name", "Tab Name", "Years" ,'Minimum Balance','Maximum Balance', "APY", 'Interest Rate'])
        df_final.to_csv(output_path + "CITI_Data_Deposit_{}.csv".format(now.strftime("%m_%d_%Y")), index=False)




# os.path.abspath(os.getcwd())
# os.chdir('../data/input/citi')

if __name__ == "__main__":
    log.info("Starting scrapping")
    # obj = Citi_bank("https://online.citi.com/US/JRS/pands/detail.do?ID=CurrentRates&JFP_TOKEN=7JAPCVIC")
    # obj.start_driver()
    # obj.get_url()
    # obj.select_state()
    # obj.unhide()
    # obj.save_page()
    # obj.close_driver() #//*[@id="main-details"]/ul/li[2]
    # tab1 = ['header', 'switch', 'CPrates']
    # extract = ExtractInfo(open("citi.html",'r'),tab1)
    # extract.findtables_tab1()

    # obj = Citi_bank("https://online.citi.com/US/JRS/pands/detail.do?ID=CDRates&JFP_TOKEN=0UYWWGSQ")
    # obj.start_driver()
    # obj.select_state()
    # obj.unhide()
    # obj.save_page()
    # obj.close_driver()
    tab2 = ['header','switch']
    extract = ExtractInfo(open('citi_tab2.html','r'),tab2)
    extract.findtables_tab2()


#select = driver.find_element_by_xpath('//span[@class="ui-selectmenu-item-header"]/li[@id="RegionalPricingLocation-snapshot-menu-option-1"]')
#select.click()
# select = Select(driver.find_element_by_id('RegionalPricingLocation-snapshot'))
# for element in select.options:
#     if element.get_attribute("value") == "AA":
#         #select.select_by_visible_text("AA")
#         select.select_by_index(1)
#     print(element.get_attribute("value"))
#select.select_by_value("AA")

#select = Select(driver.find_element_by_id('RegionalPricingLocation-snapshot'))

#options = [x for x in select.find_elements_by_tag_name("option")]
#select.select_by_visible_text('AA')
#select.select_by_value('1')
#driver.close()


