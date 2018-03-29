
from selenium import webdriver
from bs4 import BeautifulSoup
import datetime
today = datetime.datetime.now()
import pandas as pd
import time
import re
from tabulate import tabulate
from maks_lib import output_path
path = output_path+"Consolidate_BankRate_Data_Mortgage"+today.strftime('%Y_%m_%d')+".csv"
online_bank = ['Synchrony Bank', 'Ally Bank', 'Capital One 360']
start_time = time.time()
neededBanks = {
    "Ally Bank":'ALLY',
    "Bank of America":"BANK OF AMERICA CORP",
    "Capital One":"CAPITAL ONE",
    "Capital One 360":"CAPITAL ONE",
    "Chase":"JP MORGAN CHASE & Co.",
    "Citibank":"CITIGROUP INC",
    "Citibank, N. A.":"CITIGROUP INC",
    "PNC":"PNC FINANCIAL SERVICES GROUP INC",
    "Synchrony Bank":"SYNCHRONY",
    "Wells Fargo":"WELLS FARGO",
    "SunTrust":"SUNTRUST BANKS INC"

}

Excel_Table = []
table_headers = ['Bank_Name', 'Bank_Product_Name', 'Min_Loan_Amount', 'Bank_Offer_Feature', 'Term (Y)', 'Interest_Type', 'Interest',
                 'APR', 'Mortgage_Loan_Amt']
# Excel_Table.append(table_headers)
driver = webdriver.Firefox()
driver.maximize_window()
cases = [[125000,25000],[375000,75000], [625000,125000]]
for case in cases:
    driver.get("https://www.bankrate.com/mortgage.aspx?prods=1,2,387,388,5,449,3,8,6,9,10&fico=740&points=Zero&cs=1")
    driver.find_element_by_xpath('//*[@id="purchase-price"]').clear()
    driver.find_element_by_xpath('//*[@id="purchase-price"]').send_keys(case[0])
    driver.find_element_by_tag_name('body').click()
    driver.find_element_by_xpath('//*[@id="property-downpayment"]').clear()
    driver.find_element_by_xpath('//*[@id="property-downpayment"]').send_keys(case[1])
    driver.find_element_by_tag_name('body').click()
    driver.find_element_by_xpath('//*[@id="property-location"]/div/form/input').clear()
    driver.find_element_by_xpath('//*[@id="property-location"]/div/form/input').send_keys(10004)
    driver.find_element_by_tag_name('body').click()
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="search"]/ul/li[8]/button').click()
    # driver.find_element_by_xpath('//*[@id="search"]/ul/li[8]/button').click()
    time.sleep(5)
    jsoup = BeautifulSoup(driver.page_source)
    result = jsoup.find('div', attrs={'class': 'offers-list-wrap'})
    table_list = result.find_all('table')
    t = 0
    for table in table_list:
        t = t + len(table.find_all('tr'))
        for tr in table.find_all('tr'):

            try:
                tds = tr.find('td').find_all('div', attrs={'class': re.compile('grid-cell')})
                if len(tds) == 5:
                    tds.insert(1, 2)
                Bank_name = tds[0].find('h4').text.replace('\n', ' ')
                Rate = re.sub('[^0-9.,$/a-zA-Z% ]', '', tds[2].find('span').text.replace('\n', ' '))
                Year = tds[2].find('p').text.strip()
                Apr = re.sub('[^0-9.,$/a-zA-Z% ]', '', tds[3].find('span').text.replace('\n', ' '))

                #             print([Bank_name, Rate, Apr, Amount])

                if Bank_name.strip() in neededBanks:
                    if Bank_name.strip() in online_bank:
                        Bank_Offer_Feature = 'Online'
                    else:
                        Bank_Offer_Feature = 'Offline'

                    a = [neededBanks[Bank_name.strip()],Year.replace('|',' '), None, Bank_Offer_Feature, Year, 'Interest_Type', Rate.strip(),
                         Apr.strip(), case[0] - case[1]]
                    Excel_Table.append(a)
            except Exception as e:
                # print(tr)
                print(e)
driver.close()
print(len(Excel_Table))
print(tabulate(Excel_Table))
print('total length', t)
df = pd.DataFrame(Excel_Table, columns=table_headers)

df['Interest'] = df['Interest'].apply(lambda x: re.sub('[^0-9%.]','',x.split('%')[0])+'%' if '%' in x else None)
df['APR'] = df['APR'].apply(lambda x: re.sub('[^0-9%.]','',x.split('%')[0])+'%' if '%' in x else None)

df['Interest_Type'] = df['Term (Y)'].apply(lambda x: 'Fixed' if 'fixed' in x.lower() else 'Variable')
df['Term (Y)'] = df['Term (Y)'].apply(lambda x: re.sub('[^0-9.]','',re.findall('\d.*yr',str(x),re.IGNORECASE)[0]) if len(re.findall('\d.*yr',str(x),re.IGNORECASE))>=1 else None)
df['Mortgage_Down_Payment'] = '20%'
df['Date'] = ' '+today.strftime('%Y-%m-%d')
df['Term (Y)'] = df['Term (Y)'].apply(lambda x:30 if x is None else x)


df['Bank_Native_Country'] = 'US'
df['State'] = 'New York'
df['Bank_Local_Currency'] = 'USD'
df["Bank_Type"] = "Bank"
df["Bank_Product"] = "Mortgages"
df["Bank_Product_Type"] = "Mortgages"
df["Mortgage_Category"] = "New Purchase"
df["Mortgage_Reason"] = "Primary Residence"
df["Mortgage_Pymt_Mode"] = "Principal + Interest"
df["Bank_Product_Code"] = None
df['Bank_Product_Name'] = df['Bank_Product_Name'].apply(lambda x:re.sub(' +',' ',x))
order = ["Date", "Bank_Native_Country", "State", "Bank_Name", "Bank_Local_Currency", "Bank_Type", "Bank_Product", "Bank_Product_Type", "Bank_Product_Name", "Min_Loan_Amount", "Bank_Offer_Feature", "Term (Y)", "Interest_Type", "Interest", "APR", "Mortgage_Loan_Amt", "Mortgage_Down_Payment", "Mortgage_Category", "Mortgage_Reason", "Mortgage_Pymt_Mode", "Bank_Product_Code"]
df = df[order]
df.to_csv(path, index=False)