from selenium import webdriver
import time
import re
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
import datetime
today = datetime.datetime.now()
from maks_lib import output_path
path = 'Consolidate_JPMorgan_Data_Mortgage_'+today.strftime('%m_%d_%Y')+'.csv'
table_headers = ['Bank_Product_Name', 'Product_Interest', 'Mortgage_Apr','Mortgage_Loan']
Excel_Data = []
options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(firefox_options=options)#firefox_options=options
driver.maximize_window()
print('Browser Loaded')
print('Please wait scraping is runnning...')
cases = [[125000,25000], [375000, 75000], [625000, 125000]]
for case in cases:
    driver.get('https://apply.chase.com/mortgage/CRQ/CustomRateQuote.aspx')
    driver.find_element_by_xpath('//*[@id="ctl00_CenterContentPlaceHolder_CRQControl_homePrice"]').clear()
    driver.find_element_by_xpath('//*[@id="ctl00_CenterContentPlaceHolder_CRQControl_homePrice"]').send_keys(case[0])
    driver.find_element_by_xpath('//*[@id="ctl00_CenterContentPlaceHolder_CRQControl_downPayment"]').clear()
    driver.find_element_by_xpath('//*[@id="ctl00_CenterContentPlaceHolder_CRQControl_downPayment"]').send_keys(case[1])
    driver.find_element_by_xpath('//*[@id="ctl00_CenterContentPlaceHolder_CRQControl_pointsList"]/option[1]').click()
    driver.find_element_by_xpath('//*[@id="ctl00_CenterContentPlaceHolder_CRQControl_stateList"]/option[34]').click()
    driver.find_element_by_xpath('//*[@id="ctl00_CenterContentPlaceHolder_CRQControl_creditRatingList"]/option[3]').click()
    driver.find_element_by_xpath('//*[@id="ctl00_CenterContentPlaceHolder_RateandPayment"]').click()
    time.sleep(15)
    # print(driver.page_source)
    dataTable = BeautifulSoup(driver.page_source).find('div', attrs={'class':'dataTable'})
    if dataTable is not None:
        tables = dataTable.find_all('table', attrs={'class':'rowData'})
        if tables is not None:
            for table in tables:
                try:
                    tds = table.find('tr').find_all('td', attrs={'class':'dataRowTxt'})

                    a = [re.sub(r'[^\x00-\x7F]', '', tds[0].text).strip(), re.sub(r'[^\x00-\x7F]', '', tds[1].text).strip(), re.sub(r'[^\x00-\x7F]', '', tds[4].text).strip(), case[0]-case[1]]
                    print(a)
                    Excel_Data.append(a)
                    # print(table)
                    # break
                except:
                    pass
    else:
        print('Table not found')
def getYear(x):
    x = re.search('\d.*yr',x,re.IGNORECASE)
    if x is not None:
        return re.sub('[^0-9]', '', x.group(0))
    else:
        return  30
df = pd.DataFrame(Excel_Data, columns=table_headers)
df['Product_Term'] = df['Bank_Product_Name'].apply(getYear)
df['Bank_Product_Name'] = df['Bank_Product_Name'].apply(lambda x:'Mortgage_'+str(x[:x.index(' ')]) if ' ' in x else x)
df['Date'] = ' '+today.strftime("%m-%d-%Y")
df['Bank_Name'] = 'JP MORGAN CHASE & Co.'
df['Bank_Product'] = 'Mortgages'
df['Bank_Product_Type'] = 'Mortgages'
df['Bank_Offer_Feature'] = 'Offline'
df['Balance'] = None
df['Product_Apy'] = None
df['Mortgage_Down_Payment'] = '20%'
df['Min_Credit_Score_Mortagage'] = '720+'
order = ["Date","Bank_Name","Bank_Product","Bank_Product_Type","Bank_Offer_Feature","Bank_Product_Name","Product_Term","Balance","Product_Interest","Product_Apy","Mortgage_Down_Payment","Mortgage_Loan","Min_Credit_Score_Mortagage","Mortgage_Apr"]
df = df[order]
df.to_csv(path, index=False)
driver.close()