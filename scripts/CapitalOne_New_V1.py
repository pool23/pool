import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from tabulate import tabulate
from selenium.webdriver.firefox.options import Options
import pandas as pd
import datetime
from maks_lib import output_path
today = datetime.datetime.now()
options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(firefox_options=options)#firefox_options=options
driver.maximize_window()
print('Browser Loaded')
print('Please wait scraping is runnning...')
table_headers = ['Bank_Product_Type', 'Bank_Product_Name', 'Product_Term', 'Balance', 'Product_Interest', 'Product_Apy']
Excel_Table = []
# Excel_Table.append(table_headers)

path = output_path+'Consolidate_CapitalOne_Data_Deposit_'+today.strftime('%m_%d_%Y')+'.csv'
# headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
# driver.get('https://www.capitalone.com/bank/savings-accounts/')
# print(driver.page_source)
#
# jsoup = BeautifulSoup(driver.page_source).find_all('showcase')
# if len(jsoup)!=0:
#     for div in jsoup:
#         try:
#             for item in div.find_all('div', attrs={'class':'layout-item'}):
#                 ProductName = item.find('h3').text
#                 if item.find('h4') is not None:
#                     ProductName = ProductName+' '+item.find('h4').text
#                 APY = item.find('rates-inline', attrs={'rate-type':'APY'}).text
#                 Balance = item.find('div', attrs={'class':'main-content'}).text
#                 Bank_Offer = 'Online' if 'online' in Balance.lower() else 'Offline'
#                 Balance = re.search('\$[0-9.,]*', Balance).group(0)
#                 print([ProductName, None,APY, Balance, Bank_Offer])
#         except Exception as e:
#             print(e)
        # break

driver.get('https://www.capitalone.com/online-money-market-account/disclosures/')
mma = BeautifulSoup(driver.page_source).find('rates', attrs={'product':'mma'})
if mma is not None:
    ul = mma.find('ul')
    if ul is not  None:
        for p in ul.find_all('p'):
            tag = ''
            p = p.text
            if 'less' in p.lower():
                tag = 'less than '
            elif 'more' in p.lower():
                tag = 'more than '

            Balance = re.search('\$[0-9,\.]*',p).group(0)
            p = re.findall('[0-9\.]*%',p)
            if len(p)!=0 and len(p)==2:
                rate = p[0]
                APY = p[1]
                print(['360 Money Market', rate, APY, str(Balance).strip('.').strip(','), 'Online'])
                Excel_Table.append(['Savings','360 Money Market', None, str(tag+Balance).strip('.').strip(','), rate, APY])


urls = [['360 Savings','savings','https://www.capitalone.com/savings-accounts/online-savings-account/disclosures/'],
        ['360 IRA Savings Traditional','ira','https://www.capitalone.com/terms-ira/']]
        # ['Money Checking','money','https://www.capitalone.com/teen-checking-account-money/disclosures/']]

for url in urls:
    driver.get(url[2])
    jsoup = BeautifulSoup(driver.page_source)
    Balance = jsoup.find('strong', text=re.compile('Initial Deposit Requirement',re.IGNORECASE))
    Balance = Balance.parent.text
    print(Balance)
    Balance = re.search('\$[0-9,\.]*',Balance)
    Balance = Balance.group(0) if Balance is not None else 0
    for p in jsoup.find('rates', attrs={'product':url[1]}).find_all('p'):
        p = p.text
        if Balance!=0:
            Balance = re.search('\$[0-9,\.]*', p)
            if Balance is not  None:
                Balance = Balance.group(0)
        p = re.findall('[0-9\.]*%', p)
        if len(p) != 0 and len(p) == 2:
            rate = p[0]
            APY = p[1]
            print([url[0], rate, APY, Balance, 'Online'])
            Excel_Table.append(['Savings', url[0], None, str(Balance).strip('.').strip(','), rate, APY])

driver.get('https://www.capitalone.com/cds/online-cds/disclosures/')
jsoup = BeautifulSoup(driver.page_source)
Balance = jsoup.find('strong', text='Initial Deposit Requirement')
Balance = Balance.parent.text
print(Balance)
Balance = re.search('\$[0-9,\.]*',Balance)
Balance = Balance.group(0) if Balance is not None else 0
months = [6,12,36]
for tr in jsoup.find('rates', attrs={'product':'cds'}).find('table').find('tbody').find_all('tr'):
    try:
        tds = tr.find_all('td')
        month = int(re.sub('[^0-9]','',tds[0].text))
        if month in months:
            # print(['360 CDs '+str(month)+' months', tds[1], tds[2], Balance, 'Online'])
            Excel_Table.append(['CD', '360 CDs '+str(month)+' months', month, str(Balance).strip('.').strip(','), tds[1].text.strip(), tds[2].text.strip()])
    except Exception as e:
        print(e)
driver.close()

order = ["Date","Bank_Name","Bank_Product","Bank_Product_Type","Bank_Offer_Feature","Bank_Product_Name","Product_Term","Balance","Product_Interest","Product_Apy","Mortgage_Down_Payment","Mortgage_Loan","Min_Credit_Score_Mortgage","Mortgage_APR"]
df = pd.DataFrame(Excel_Table, columns=table_headers)
df["Date"] = ' '+today.strftime("%m-%d-%Y")
df['Bank_Name'] = 'CAPITAL ONE'
df['Bank_Product'] = 'Deposits'
df['Bank_Offer_Feature'] = 'Online'
df['Mortgage_Down_Payment'] = None
df['Mortgage_Loan'] = None
df['Min_Credit_Score_Mortgage'] = None
df['Mortgage_APR'] = None

df = df[order]
df.to_csv(path, index=False)
print(tabulate(Excel_Table))