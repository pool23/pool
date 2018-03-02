from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from maks_lib import output_path
import datetime
import numpy as np

now = datetime.datetime.now()

class App:

    def __init__(self, url = 'https://www.wellsfargo.com/checking/everyday/ ', zipcode='10004'):
        self.zipcode = zipcode
        self.driver = webdriver.Firefox()
        self.driver.get(url)
        sleep(3)
        # write log in function
        self.log_in()
        sleep(5)


    def log_in(self):
        zip_input = self.driver.find_element_by_xpath('//*[@id="zipCode"]')
        zip_input.send_keys(self.zipcode)
        continue_button = self.driver.find_element_by_xpath('//*[@id="c28lastFocusable"]')
        continue_button.click()

    def data_page(self):
        page = self.driver.page_source
        soup = bs(page, 'lxml')
        product_name = soup.find('h1', attrs={'class':'c11'})
        product_name = product_name.getText()
        mini_bal = soup.find('div', attrs={'class':'c89featureList'})
        balance = mini_bal.find_all('p')
        min_open_bal = balance[0].getText()
        m_open_bal = min_open_bal.split("\n")
        min_open_bal = m_open_bal[2]
        min_balance = balance[4].getText()
        return product_name, min_open_bal, min_balance

if __name__ == '__main__':
    app = App()
    product_name, min_open_bal, min_balance = app.data_page()

    data = [(now.strftime("%m/%d/%Y"), "Wells Fargo", product_name, min_open_bal, min_balance)]
    df = pd.DataFrame.from_records(data, columns=["Date", "Bank Name", "Product Name", "Minimum Opening Amount", "Minimum Daily Balance"])
    df.to_csv(output_path + "WellsF_Data_Checking_Acc{}.csv".format(now.strftime("%m_%d_%Y")), index=False)