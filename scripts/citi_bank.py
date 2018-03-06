from selenium import webdriver
from bs4 import  BeautifulSoup as bs
import pandas as pd
import time
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
    def __init__(self, url, tab):
        self.url = url
        self.tab = tab

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
        return "AA"

    def get_current_url(self):
        return self.driver.current_url

    def save_page(self):
        # pyautogui.hotkey('ctrl', 's')
        # time.sleep(1)
        # pyautogui.typewrite("citi")
        # time.sleep(1)
        # pyautogui.hotkey('enter')
        page = self.driver.page_source
        with open("citi_"+self.tab+".html", 'w')as file:
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
        dff = df.reindex(columns= ["Date","Bank Name","Tab Name","Product Type",'Product Name','Balance', 'Interest Rate', 'APY'])
        #dff.to_csv(output_path+"CITI_Data_Deposit_{}.csv".format(now.strftime("%m_%d_%Y")), index =False)

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
        df_fin = dfn.reindex(columns=["Date", "Bank Name", "Tab Name", "Years" ,'Minimum Balance','Maximum Balance', "APY", 'Interest Rate'])
        df_final = pd.concat([findtables_tab1.dff, df_fin])
        df_final.to_csv(output_path + "CITI_Data_Deposit_{}.csv".format(now.strftime("%m_%d_%Y")), index=False)

class MergeCsv:
    def __init__(self, csv1, csv2 ):
        self.csv1 = csv1
        self.csv2 = csv2
    def concatenate(self):


if __name__ == "__main__":
    log.info("Starting scrapping")
    tab1_url = "https://online.citi.com/US/JRS/pands/detail.do?ID=CurrentRates&JFP_TOKEN=7JAPCVIC"
    tab2_url = "https://online.citi.com/US/JRS/pands/detail.do?ID=CDRates&JFP_TOKEN=0UYWWGSQ"
    urls = [tab1_url, tab2_url]
    tabs = ["tab1", "tab2"]
    for number in range(len(urls)):
        obj = Citi_bank(urls[number], tabs[number])
        obj.start_driver()
        obj.get_url()
        state = obj.select_state()
        obj.save_page()
        obj.close_driver()
        time.sleep(5)
    for scrab in range(len(tabs)):
        if tabs[scrab] = "tab1" :
            tab1 = ['header', 'switch', 'CPrates']
            extract = ExtractInfo(open("citi_"+tabs[scrab]+".html",'r'),tab1)
            extract.findtables_tab1()
        else:
            tab2 = ['header','switch']
            extract = ExtractInfo(open("citi_"+tabs[scrab]+".html",'r'),tab2)
            extract.findtables_tab2()