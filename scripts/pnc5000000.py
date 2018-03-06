from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup as bs
import pandas as pd
import datetime
import warnings
from maks_lib import output_path
warnings.simplefilter(action='ignore')

now = datetime.datetime.now()

class App:

    def __init__(self, url = 'https://www.synchronybank.com/banking/high-yield-savings/ '):
        self.driver = webdriver.Firefox()
        self.driver.get(url)
        sleep(5)
        self.data_page()



    def data_page(self):
        html = self.driver.execute_script("return document.documentElement.outerHTML")
        soup = bs(html, 'html.parser')
        li = soup.find_all('li')
        min_open = li[29].getText()
        Pd = soup.find_all('h2', attrs={'class':'heading-level-1'})
        Pd = Pd[1].getText()
        li = soup.find_all('span',attrs={'id':['mmaLowApy','mmaMidApy','mmaHighApy']})
        Apy_li=[]
        for apy in li:
            if apy.getText() is not None:
                Apy_li.append(apy.getText())

        bal = soup.find_all('div', attrs={'class':'deposit-range'})
        bal_li = []
        for brange in bal:
            if brange.getText() is not None:
                bal_li.append(brange.getText())
        # print(li[32].getText())
        # print(li[33].getText())
        return  Apy_li, Pd, bal_li, min_open




if __name__ == '__main__':
    app = App()
    Apy_li, Pd, bal_li, min_open = app.data_page()
    df = pd.DataFrame({'Date':now.strftime("%m/%d/%Y"),"Bank Name":'Synchrony','Product Name':Pd,
                       "Minimum Open Balance":min_open,"Deposite":bal_li,"APY":Apy_li})
    df = df.reindex(
        columns=["Date", "Bank Name", "Product Name", "Minimum Open Balance","Deposite", "APY"])
    df.to_csv(output_path +"Sync_Data_Deposit_High_Yield{}.csv".format(now.strftime("%m_%d_%Y")), index=False)

    df1 = pd.read_csv(output_path+"Sync_Data_Deposit03_06_2018.csv")
    df2 = pd.read_csv(output_path+"Sync_Data_Deposit_High_Yield03_06_2018.csv")
    df3 = pd.read_csv(output_path+"Sync_Data_Make_Money03_06_2018.csv")
    df = pd.concat([df1, df2, df3])
    df.to_csv(output_path + "Sync_Data_Deposit_03_06_2018{}.csv".format(now.strftime("%m_%d_%Y")), index=False)
