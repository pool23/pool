from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from bs4 import  BeautifulSoup as bs
import pandas as pd
import time
import warnings
import datetime
import os
from maks_lib import output_path

now = datetime.datetime.now()

warnings.simplefilter(action='ignore')

driver = webdriver.Firefox()
driver.maximize_window()
class Citi_mortgage:
    global driver
    def __init__(self, url, eprice, dprice):
        self.url = url
        self.eprice = eprice
        self.dprice = dprice

    def start_driver(self):
        self.driver = webdriver.Firefox()

    def close_driver(self):
        return self.driver.close()

    def get_url(self):
        return driver.get(self.url)

    def fillform(self):
        time.sleep(6)
        select = Select(driver.find_element_by_id("propertyKind"))
        select.select_by_visible_text("Single Family Home")
        select = Select(driver.find_element_by_id("propertyUse"))
        select.select_by_value("P")
        inutelement = driver.find_element_by_id("propCity")
        inutelement.clear()
        inutelement.send_keys('New York')
        select = Select(driver.find_element_by_id("propState"))
        select.select_by_value("NY")
        select = Select(driver.find_element_by_id("propCounty"))
        select.select_by_value("36061")
        inutelement = driver.find_element_by_id("purchPrice")
        inutelement.clear()
        inutelement.send_keys(self.eprice[1])
        inutelement = driver.find_element_by_id("desiredLoanAmount")
        inutelement.clear()
        inutelement.send_keys(self.dprice[1])
        driver.find_element_by_id("creditScoreGoodLabel").click()
        driver.find_element_by_id("submit-purchase").click()
        time.sleep(15)


    def get_current_url(self):
        return driver.current_url

    def save_page(self):
        page = driver.page_source
        with open("citi_mortgage_"+self.eprice[0]+".html", 'w')as file:
            file.write(page)

    def unhide(self):
        pass

class ExtractInfo(Citi_mortgage):

    def __init__(self, page,tab, eprice, dprice):
        self.page = page
        self.tab = tab
        self.eprice = eprice
        self.dprice = dprice

    def findtables_tab1(self):
        soup = bs(self.page, "lxml")
        file = open("test.txt",'w')
        h = [ f.text for f in soup.find_all('h1', {'class':self.tab[0]})]
        d = [j.text for j in soup.find_all('div', {'class':self.tab[1]})]
        for l in zip(h,d):
            la= l[1].split('\n')
            if 'points' in la[30]:
                f = l[0] + "\t" + la[5] + "\t" + la[12]+'\n'
                file.write(f)

            elif "points" in la[27]:
                f = l[0]+"\t"+la[5]+"\t"+la[12]+'\n'
                file.write(f)
        file.close()
        time.sleep(3)
        dataset = pd.read_table('test.txt',sep='\t',delimiter=None, header=None)
        #dataset['Expected_Price'] = self.eprice[1]
        dataset['Mortgage_Loan'] = self.dprice
        dataset["Product_Term"] = dataset.iloc[:,0].str.replace("Year Fixed","")
        for i in range(0, len(dataset)):
            if "Libor ARM" in dataset.ix[i]['Product_Term']:
                dataset.ix[i]['Product_Term'] = 30 #dataset.iloc[i]['Product_Term']

        loan_type = pd.DataFrame(dataset.iloc[:,0].str.split(" ").tolist())
        dataset["Loan_Type"] = loan_type.iloc[:,2].str.replace("ARM","Variable")
        dataset.columns = ['Bank_Product_Name','Product_Interest','Mortgage_Apr',"Mortgage_Loan","Product_Term",'Loan_Type']
        dataset.to_csv("Citi_Mortgage_"+self.eprice[0]+".csv",index=False)

if __name__ == "__main__":
    print("Starting scraping")

    expected_price = [('case1','125000'),('case2','375000'),('case3','625000')]
    desired_price = [('case1','100000'),('case2','300000'),('case3','500000')]
    url = "https://online.citi.com/US/nccmi/purchase/ratequote/flow.action?fromLanding=true&selectedOption=CUSTOM&selectedOptionValue=CUSTOMpurChaseLanding&JFP_TOKEN=3GBHQLZG"
    for i in range(len(expected_price)):
        obj = Citi_mortgage(url, expected_price[i], desired_price[i])
        obj.get_url()
        obj.fillform()
        obj.save_page()
        time.sleep(1)
    driver.close()
    tab1 = ['header-3 rate-card-panel-header-white', 'row rate-card-panel-items tb-hide']
    for i in range(len(expected_price)):
        page = open("citi_mortgage_" + expected_price[i][0] + ".html", 'r')
        extract = ExtractInfo(page, tab1, expected_price[i], desired_price[i][1])
        extract.findtables_tab1()
        page.close()
    df1 = pd.read_csv("Citi_Mortgage_case1.csv")
    df2 = pd.read_csv("Citi_Mortgage_case2.csv")
    df3 = pd.read_csv("Citi_Mortgage_case3.csv")
    df = pd.concat([df1, df2, df3])

    df['Date'] = now.strftime("%m-%d-%Y")
    df['Bank_Name'] = "CITIGROUP INC"
    df['Bank_Product'] = "Mortgage"
    df['Bank_Product_Type'] = "Mortgage"
    df["Bank_Offer_Feature"] = "Offline"
    df['Mortgage_Down_Payment'] = "20%"
    df['Min_Credit_Score_Mortagage'] = "720+"

    #print(df['Product_Term'])

    # for val, row in df.iterrows():
    #     if "Libor ARM" in row["Product_Term"]:
    #         #df.loc[val,'Product_Term'] = 30
    #         #print(df.at[val,'Product_Term'])
    #         pass


    #print(df['Product_Term'])
    dff = df.reindex(columns=["Date", "Bank_Name" , "Bank_Product" ,
                              'Bank_Product_Type', 'Bank_Offer_Feature' ,
                              'Bank_Product_Name' , 'Product_Term' , 'Balance',
                              'Product_Interest','Product_Apy',
                              'Mortgage_Down_Payment','Mortgage_Loan',
                              'Min_Credit_Score_Mortagage', 'Mortgage_Apr','Loan_Type'])

    dff_consolidate = df.reindex(columns=["Date", "Bank_Name", "Bank_Product",
                              'Bank_Product_Type', 'Bank_Offer_Feature',
                              'Bank_Product_Name', 'Product_Term', 'Balance',
                              'Product_Interest', 'Product_Apy',
                              'Mortgage_Down_Payment', 'Mortgage_Loan',
                              'Min_Credit_Score_Mortagage', 'Mortgage_Apr'])

    dff.to_csv(output_path + "CITI_Data_Mortgage_{}.csv".format(now.strftime("%m_%d_%Y")), index=False)
    dff_consolidate.to_csv(output_path + "Consolidate_CITI_Data_Mortgage_{}.csv".format(now.strftime("%m_%d_%Y")), index=False)

    for rm in range(len(expected_price)):
        os.remove("Citi_Mortgage_"+expected_price[rm][0]+".html")
        os.remove("Citi_Mortgage_"+expected_price[rm][0]+".csv")

    print("Finished Scraping ")
