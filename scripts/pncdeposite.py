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

    def __init__(self, url = 'https://apps.pnc.com/rates/servlet/DepositRatesSearchVW?productGroup=growth ', zipcode='10004'):
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
        getrate_button = self.driver.find_element_by_xpath('//*[@id="submitBtn"]')
        getrate_button.click()



    def data_page(self):
        html = self.driver.execute_script("return document.documentElement.outerHTML")
        soup = bs(html, 'lxml')
        Pro_name = soup.find('h3',attrs={'class':'orangeText'})
        vw = Pro_name.getText()
        vwp = soup.find_all('div', attrs={'class':'orangeText'})
        vwp = vwp[0].getText()
        df = pd.read_html(html)
        return  df,vw,vwp






if __name__ == '__main__':
    app = App()
    df, vw, vwp = app.data_page()
    df_0 = tuple(df[3].iloc[6, :])
    df_0 = pd.DataFrame.from_records(data=[df_0], columns=["Balance", "Interest Rate", "APY"])
    df_0["Date"] = now.strftime("%m/%d/%Y")
    df_0["Bank Name"] = "PNC"
    df_0["TAB Name"] = "Spend/Reserve"
    df_0["Product Name"] = vw
    df_0 = df_0.reindex(columns=["Date", "Bank Name", "TAB Name", "Product Name", "Balance", "Interest Rate", "APY"])
    df_1 = df[3].iloc[10:14, :]
    df_1.columns = ["Balance", "Interest Rate", "APY"]
    df_1["Date"] = now.strftime("%m/%d/%Y")
    df_1["Bank Name"] = "PNC"
    df_1["TAB Name"] = "Spend/Reserve"
    df_1["Product Name"] = vwp
    df_1 = df_1.reindex(columns=["Date", "Bank Name", "TAB Name", "Product Name", "Balance", "Interest Rate", "APY"])
    df_2 = tuple(df[3].iloc[17, :])
    df_2 = pd.DataFrame.from_records(data=[df_2], columns=["Balance", "Interest Rate", "APY"])
    df_2["Date"] = now.strftime("%m/%d/%Y")
    df_2["Bank Name"] = "PNC"
    df_2["TAB Name"] = "Spend/Reserve"
    df_2["Product Name"] = vwp
    df_2 = df_2.reindex(columns=["Date", "Bank Name", "TAB Name", "Product Name", "Balance", "Interest Rate", "APY"])
    df_3 = df[3].iloc[21:25, :]
    df_3.columns = ["Balance", "Interest Rate", "APY"]
    df_3["Date"] = now.strftime("%m/%d/%Y")
    df_3["Bank Name"] = "PNC"
    df_3["TAB Name"] = "Spend/Reserve"
    df_3["Product Name"] = vwp
    df_3 = df_3.reindex(columns=["Date", "Bank Name", "TAB Name", "Product Name", "Balance", "Interest Rate", "APY"])
    df_4 = tuple(df[3].iloc[28, :])
    df_4 = pd.DataFrame.from_records(data=[df_4], columns=["Balance", "Interest Rate", "APY"])
    df_4["Date"] = now.strftime("%m/%d/%Y")
    df_4["Bank Name"] = "PNC"
    df_4["TAB Name"] = "Spend/Reserve"
    df_4["Product Name"] = vwp
    df_4 = df_4.reindex(columns=["Date", "Bank Name", "TAB Name", "Product Name", "Balance", "Interest Rate", "APY"])
    df_0_gr = df[9].iloc[2:4, :]
    df_0_gr.columns = ["Balance", "Interest Rate", "APY"]
    df_0_gr["Date"] = now.strftime("%m/%d/%Y")
    df_0_gr["Bank Name"] = "PNC"
    df_0_gr["TAB Name"] = "Growth"
    df_0_gr["Product Name"] = vw
    df_0_gr = df_0_gr.reindex(columns=["Date", "Bank Name", "TAB Name", "Product Name", "Balance", "Interest Rate", "APY"])
    df_1_gr = df[12].iloc[2:10, :]
    df_1_gr.columns = ["Balance", "Interest Rate", "APY"]
    df_1_gr["Date"] = now.strftime("%m/%d/%Y")
    df_1_gr["Bank Name"] = "PNC"
    df_1_gr["TAB Name"] = "Growth"
    df_1_gr["Product Name"] = vwp
    df_2_gr = df_1_gr.reindex(columns=["Date", "Bank Name", "TAB Name", "Product Name", "Balance", "Interest Rate", "APY"])
    df_2_gr = df[15].iloc[2:10, :]
    df_2_gr.columns = ["Balance", "Interest Rate", "APY"]
    df_2_gr["Date"] = now.strftime("%m/%d/%Y")
    df_2_gr["Bank Name"] = "PNC"
    df_2_gr["TAB Name"] = "Growth"
    df_2_gr["Product Name"] = vwp
    df_2_gr = df_2_gr.reindex(columns=["Date", "Bank Name", "TAB Name", "Product Name", "Balance", "Interest Rate", "APY"])
    df = pd.concat([df_0, df_1, df_2, df_3, df_4, df_0_gr, df_1_gr, df_2_gr])
    df.to_csv(output_path + "PNC_Data_Deposit_{}.csv".format(now.strftime("%m_%d_%Y")), index=False)


