import requests
from selenium import webdriver
import time
from bs4 import BeautifulSoup
from tabulate import tabulate
import pandas as pd
import numpy as np
import datetime
today = datetime.datetime.now()
import pandas as pd
import time
import re
start_time = time.time()
from maks_lib import output_path
path = output_path+"Consolidate_BankRate_Data_Deposit"+today.strftime('%Y_%m_%d')+".csv"
# path = "Consolidate_BankRate_Data_Deposit"+today.strftime('%Y_%m_%d')+".csv"
online_bank = ['Synchrony Bank', 'Ally Bank', 'Capital One 360']
neededBanks = {
    "Ally Bank":'ALLY',
    "Bank of America":"BANK OF AMERICA CORP",
    "Capital One":"CAPITAL ONE",
    "Capital One 360":"CAPITAL ONE",
    "Chase":"JP MORGAN CHASE & Co.",
    "Chase Bank":"JP MORGAN CHASE & Co.",
    "Citibank":"CITIGROUP INC",
    "PNC":"PNC FINANCIAL SERVICES GROUP INC",
    "Synchrony Bank":"SYNCHRONY",
    "Wells Fargo":"WELLS FARGO",
    "SunTrust":"SUNTRUST BANKS INC"

}
print("Execution Started Please Wait....")
table_headers = ['Bank_Name', 'Bank_Product_Type', 'Bank_Product_Name', 'Balance', 'Bank_Offer_Feature', 'Term_in_Months', 'Interest', 'APY']
Excel_Table = []
# Excel_Table.append(table_headers)

driver = webdriver.Firefox()
driver.maximize_window()

#=========================Savings==============================================
try:
    driver.get("https://www.bankrate.com/banking/savings/rates/")
    driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div[2]/div[3]/div/div[1]/div/div/input').clear()
    driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div[2]/div[3]/div/div[1]/div/div/input').send_keys(10004)
    driver.find_element_by_tag_name('body').click()
    time.sleep(5)
    size = driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div[3]/div[1]/p/strong').text
    print(size)
    for i in range(5):
        try:
            # driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[2]/button').click()
            element = driver.find_element_by_css_selector('button.button')#.click()
            driver.execute_script("arguments[0].click();", element)
            # print('element found')
            time.sleep(3)
        except Exception as e:
            print(e)
    # resp = requests.get("https://www.bankrate.com/banking/savings/rates/").content
    # print(driver.page_source)
    jsoup = BeautifulSoup(driver.page_source)
    trs = jsoup.find('table', attrs={'class':'table --bordered-rows rate-table rate-table-savings'}).find('tbody').find_all('tr')
    for tr in trs:
        print('-'.center(100,'-'))
        # print(tr)
        try:
            tds = tr.find_all('td')
            Bank_name = tds[0].find('a', attrs={'data-name':'advertiserlink'})
            if Bank_name is None:
                Bank_name = tds[0].find('div', attrs={'class':'rate-table__row-copy --dark-gray'})
            apy = tds[1].find('a', attrs={'data-name': 'advertiserAPY'})
            if apy is None:
                apy = tds[1].find('div', attrs={'class':'numeral --beta'})
            amount = tds[2].find('div',attrs={'class':'numeral --beta'})
            Bank_name  = Bank_name.text if Bank_name is not None else None
            apy = apy.text if apy is not None else None
            amount = amount.text if amount is not None else None
            bank = Bank_name.strip().split('\n')
            # print(bank)
            if len(bank)>=2:
                bank_name = bank[0].strip()
                bank_product = bank[1].strip()
            else:
                bank_name = bank[0].strip()
                bank_product = None
            print([bank_name,bank_product, apy.strip(), amount.strip()])

            if bank_name in neededBanks:
                if bank_name in online_bank:
                    Bank_Offer_Feature = 'Online'
                else:
                    Bank_Offer_Feature = 'Offline'
                if '|' in bank_product:
                    bank_product = bank_product.split('|')[0].capitalize()

                a = [neededBanks[bank_name], 'Savings', 'Savings' if bank_product is None else bank_product, amount.strip(), Bank_Offer_Feature, None, 'Interest',apy.strip()]
                Excel_Table.append(a)
            print('-'.center(100,'-'))
        except Exception as e:
            print(e)


except Exception as e:
    print(e)

#==============================================CDS===========================================================================================
try:
    driver.get("https://www.bankrate.com/cd.aspx")
    driver.find_element_by_xpath('//*[@id="csstyle"]/div[5]/div[1]/div[2]/div[4]/div/div[1]/div/div/input').clear()
    driver.find_element_by_xpath('//*[@id="csstyle"]/div[5]/div[1]/div[2]/div[4]/div/div[1]/div/div/input').send_keys(10004)
    driver.find_element_by_tag_name('body').click()
    time.sleep(5)
    for i in range(20):
        try:
            element = driver.find_element_by_xpath('//*[@id="csstyle"]/div[5]/div[2]/div[2]/button')
            # element = driver.find_element_by_css_selector('button.button')#.click()
            driver.execute_script("arguments[0].click();", element)
            # print('element found')
            time.sleep(3)
        except Exception as e:
            print(e)
            break
    time.sleep(3)
    jsoup = BeautifulSoup(driver.page_source)
    trs = jsoup.find('table', attrs={'class': 'table --bordered-rows rate-table rate-table-cd'}).find('tbody').find_all('tr')
    print('trs length : ',len(trs))
    for tr in trs:
        # print('-'.center(100,'-'))
        # print(tr)
        try:
            tds = tr.find_all('td')


            Bank_name = tds[0].find('a', attrs={'data-name':'advertiserlink'})
            if Bank_name is None:
                Bank_name = tds[0].find('div', attrs={'class':'rate-table__row-copy --dark-gray'})
            apy = tds[1].find('a', attrs={'data-name': 'advertiserAPY'})
            if apy is None:
                apy = tds[1].find('div', attrs={'class':'numeral --beta '})
            amount = tds[3].find('div',attrs={'class':'numeral --beta'})
            Bank_name  = Bank_name.text if Bank_name is not None else None
            apy = apy.text if apy is not None else None
            amount = amount.text if amount is not None else None
            bank = Bank_name.strip().split('\n')
            terms_in_month = tds[2].find('div', attrs={'class':'numeral --beta'}).text
            # print('terms_in_month = ',terms_in_month)
            # print(bank)
            if len(bank)>=2:
                bank_name = bank[0]
                bank_product = bank[1]
            else:
                bank_name = bank[0]
                bank_product = None
            # print([bank_name,bank_product, apy, amount])

            if bank_name.strip() in neededBanks:
                if bank_name.strip() in online_bank:
                    Bank_Offer_Feature= 'Online'
                else:
                    Bank_Offer_Feature = 'Offline'
                a = [neededBanks[bank_name], 'CD', 'CD', amount.strip() if amount is not None else None,
                     Bank_Offer_Feature, terms_in_month.strip() if terms_in_month is not None else None, 'Interest',
                     apy.strip() if apy is not None else None]
                Excel_Table.append(a)
            print('-'.center(100,'-'))
        except Exception as e:
            print(e)
    print(len(trs))
except Exception as e:
    print(e)

#=======================================Savings==========================================================

try:
    driver.get("https://www.bankrate.com/funnel/checking-account/checking-account-results.aspx?prods=31&local=true&market=2")
    jsoup = BeautifulSoup(driver.page_source)
    trs = jsoup.find('div', attrs={'data-ri-table-group':'Interest Checking'}).find_all('ul')
    for ul in trs:
        Bank_Name = ul.find('li', attrs={'class':'rtLender'}).find('a')
        if Bank_Name is not None:
            Bank_Name = Bank_Name.text
        else:
            Bank_Name = ul.find('li', attrs={'class': 'rtLender'}).find('div').text
        # print(Bank_Name)
        Apy = ul.find('span', attrs={'class':'fieldValue rate'}).text
        print([Bank_Name, Apy])

        if Bank_Name.strip() in neededBanks:
            if Bank_name.strip() in online_bank:
                Bank_Offer_Feature = 'Online'
            else:
                Bank_Offer_Feature = 'Offline'
            a = [neededBanks[Bank_Name.strip()], 'Checkings', 'Checkings', None, Bank_Offer_Feature, None, None,
                 Apy.strip() if Apy is not None else None]
            Excel_Table.append(a)
    print(len(trs))
    # print(driver.page_source)
except Exception as e:
    print(e)


driver.close()

order = ["Date", "Bank_Native_Country", "State", "Bank_Name", "Bank_Local_Currency", "Bank_Type", "Bank_Product", "Bank_Product_Type", "Bank_Product_Code", "Bank_Product_Name", "Balance", "Bank_Offer_Feature", "Term_in_Months", "Interest_Type", "Interest", "APY", "Source"]
# driver.close()
print(tabulate(Excel_Table))
df = pd.DataFrame(Excel_Table, columns=table_headers)
df['Interest'] = np.nan
df['Date'] = ' '+today.strftime('%Y-%m-%d')
df['Bank_Native_Country'] = 'US'
df['State'] = 'New York'
df['Bank_Local_Currency'] = 'USD'
df['Bank_Type'] = 'Bank'
df['Bank_Product'] = 'Deposits'
df['Interest_Type'] = 'Fixed'
df['Bank_Product_Code'] = np.nan
# df['Term_in_Months'] = np.nan
# df['Bank_Offer_Feature'] = 'Offline'
df['Balance'] = df['Balance'].apply(lambda x:re.sub('[^0-9,.]','',x) if x is not None else None)
df['Bank_Product_Name'] = df['Bank_Product_Name'].apply(lambda x:re.sub('[^0-9A-Za-z|]','',x) if x is not None else x)

df['Source'] = 'bankrate.com'
def getMonths(x):
    if x is not None:
        if 'm' in x.lower():
            return re.sub('[^0-9.]','',x)
        elif 'y' in x.lower():
            y = re.sub('[^0-9.]', '', x)
            return int(y.split('.')[0]) * 12 + int(y.split('.')[1]) if '.' in y else int(y)*12
        else:
            return x

df['Term_in_Months'] = df['Term_in_Months'].apply(getMonths)
# df['dummy'] = df['Term_in_Months'].apply(lambda x:'CD - '+str(x)+' Months' if x is not None else None)
# df['Bank_Product_Name'] = np.where(df['Bank_Product_Name'] is None, 'hi')
# df['Bank_Product_Name'] = df['Term_in_Months'].apply(lambda x:'CD - '+str(x)+' Months' if x is not None else None)
# df['Bank_Product_Name'] = df['Term_in_Months'].apply(lambda x:'CD - '+ if x is not None else None)
# df['Bank_Product_Name'] = df['Balance'].apply(lambda x: 'Checkings' if x is None)
# df['Bank_Product_Name'] = np.where( ( (df['Bank_Product_Name'] is None) & (df['Term_in_Months'] is not None ) ) | ( (df['Bank_Product_Name'] is None) & (df['Term_in_Months'] is not None ) ), df['Term_in_Months'], df['Term_in_Months'])

df = df[order]
df.to_csv(path, index=False)
print('Exection Completed.')
print('Total Execution Time:',time.time()-start_time,' Seconds')

# df['points'] = np.where( ( (df['gender'] == 'male') & (df['pet1'] == df['pet2'] ) ) | ( (df['gender'] == 'female') & (df['pet1'].isin(['cat','dog'] ) ) ), 5, 0)
