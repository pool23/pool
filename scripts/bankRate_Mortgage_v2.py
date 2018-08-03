from selenium import webdriver
from bs4 import BeautifulSoup
import datetime
today = datetime.datetime.now()
import pandas as pd
import time
import re
from tabulate import tabulate
from maks_lib import output_path
path = output_path+"Aggregator_BankRate_Data_Mortgage"+today.strftime('%Y_%m_%d')+".csv"
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
    "SunTrust":"SUNTRUST BANKS INC",
    "Visit Ally Bank site":"ALLY",
    "Visit Citibank, N. A. site":"CITIGROUP INC"

}

Excel_Table = []
table_headers = ['Bank_Name', 'Bank_Product_Name', 'Min_Loan_Amount', 'Bank_Offer_Feature', 'Term (Y)', 'Interest_Type', 'Interest',
                 'APR', 'Mortgage_Loan_Amt']
# Excel_Table.append(table_headers)
driver = webdriver.Firefox()
driver.maximize_window()

cases = [[125000,25000],[375000,75000], [625000,125000]]
for case in cases:
    driver.get("https://www.bankrate.com/mortgage.aspx?propertyvalue="+str(case[0])+"&loan="+str(case[0]-case[1])+"&perc=20&prods=1,2,3,8,6,9,10&fico=740&points=Zero&zipcode=10004&cs=1&type=newmortgage")
    # time.sleep(10)
    # driver.find_element_by_xpath('//*[@id="purchase-price"]').clear()
    # driver.find_element_by_xpath('//*[@id="purchase-price"]').send_keys(case[0])
    driver.find_element_by_tag_name('body').click()
    # driver.find_element_by_xpath('//*[@id="property-downpayment"]').clear()
    # driver.find_element_by_xpath('//*[@id="property-downpayment"]').send_keys(case[1])
    driver.find_element_by_tag_name('body').click()
    driver.find_element_by_css_selector('form.\+mg-bottom-none > input:nth-child(1)').clear()   #/html/body/div[5]/div/div[2]/div/div[1]/div[2]/div/div[1]/div/div/form/input
    driver.find_element_by_css_selector('form.\+mg-bottom-none > input:nth-child(1)').send_keys(10004)    #//*[@id="property-location"]/div/form/input
    driver.find_element_by_tag_name('body').click()
    # time.sleep(8)
    driver.find_element_by_css_selector('button.--primary').click()     #//*[@id="search"]/ul/li[8]/button
    # driver.find_element_by_xpath('//*[@id="search"]/ul/li[8]/button').click()
    time.sleep(5)
    jsoup = BeautifulSoup(driver.page_source)
    # result = jsoup.find('div', attrs={'class': 'offers-list-wrap'})
    table_list = jsoup.find_all('table', attrs={'class':'table --bordered-rows offers-list +mg-bottom-lg +mg-bottom-none'})
    for table in table_list:
        trs = table.find('tbody').find_all('tr')
        for tr in trs:
            try:

                Bank_name = tr.find('img')
                print(Bank_name['alt'])
                Bank_product_name = tr.find('td').find('div',attrs = {'class':'offer__fees-text offer__text --small'}).find('span').text
                print(Bank_product_name)
                Rate = tr.find('td').find('div', attrs = {'class':'offer__rate-caption +mg-bottom-sm +pointer'}).text
                print(Rate)
                Apr = tr.find('td').find('div', attrs = {'class':'numeral --beta +mg-bottom-xs +pointer'}).text
                print(Apr)
                # Year = re.search('[0-9]',Bank_product_name)
                # print(Year)
                if Bank_name['alt'].strip() in neededBanks:

                    if Bank_name['alt'].strip() in online_bank:
                        Bank_Offer_Feature = 'Online'
                    else:
                        Bank_Offer_Feature = 'Offline'
                    a = [neededBanks[Bank_name['alt'].strip()], Bank_product_name.strip(), None, Bank_Offer_Feature, None,'Interest_Type', re.search('[0-9\.]+', Rate.strip()).group(0), re.search('[0-9\.]*',Apr.strip()).group(0), case[0] - case[1]]
                    print(a)
                    Excel_Table.append(a)






            except Exception as e:
                print(e)


    # t = 0
    # for table in table_list:
    #     t = t + len(table.find_all('tr'))
    #     for tr in table.find_all('tr'):
    #
    #         try:
    #             # tds = tr.find('td').find_all('div', attrs={'class': re.compile('grid-cell')})
    #             # if len(tds) == 5:
    #             #     tds.insert(1, 2)
    #             # Bank_name = tds[0].find('h4').text.replace('\n', ' ') if tds[0].find('h4') is not None else None
    #             # if Bank_name is None:



                # Rate = re.sub('[^0-9.,$/a-zA-Z% ]', '', tds[2].find('span').text.replace('\n', ' '))
                # Year = tds[2].find('p').text.strip()
                # Apr = re.sub('[^0-9.,$/a-zA-Z% ]', '', tds[3].find('span').text.replace('\n', ' '))

                # Bank_name = tr.find('figure', attrs={'class':'advertiser-logo_wrapper +pointer'})
                # print(Bank_name)
                # if 'www.brimg.net/system/img/inst/8189_hires_logo_2x.png' in Bank_name:
                #     Bank_name = 'CITIGROUP INC'
                # elif 'www.brimg.net/system/img/inst/10271_hires_logo_2x.png' in Bank_name:
                #     Bank_name = 'ALLY'
                # print(Bank_name)
                # Rate = tr.find('td').find('div').find('div')[1].find_all('div')[1] #re.sub('[^0-9.,$/a-zA-Z% ]', '',
                # print(Rate)
                # Apr = tr.find('td').find('div').find_all('div')[1].find_all('div')[0]  #re.sub('[^0-9.,$/a-zA-Z% ]', '',
                # print(Apr)
                # Year = tr.find.find('td').find('div', attrs={'class':'rate-table__row-child grid --equal-height --align-spread +pd-left-xs'}).find_all('div')[0].find('span')
                # print(Year)

                # Rate = re.sub('[^0-9.,$/a-zA-Z% ]', '', tr.find('span', attrs={'class':'expanded-offer__rate'}))
                # Apr = re.sub('[^0-9.,$/a-zA-Z% ]', '', tr.find('span', text='APR').parent.parent.text)
                # Year = tr.find('p', text=re.compile('year')).text
                #
                #
                # #             print([Bank_name, Rate, Apr, Amount])
                #


            #


driver.close()
print(len(Excel_Table))
print(tabulate(Excel_Table))
# print('total length', t)
df = pd.DataFrame(Excel_Table, columns=table_headers)

# df['Interest'] = df['Interest'].apply(lambda x: re.sub('[^0-9%.]','',x.split('%')[0])+'%' if '%' in x else None)
# df['APR'] = df['APR'].apply(lambda x: re.sub('[^0-9%.]','',x.split('%')[0])+'%' if '%' in x else None)

df['Interest_Type'] = df['Bank_Product_Name'].apply(lambda x: 'Fixed' if 'fixed' in x.lower() else 'Variable')
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
df["Source"] = "Bankrate.com"
df['Bank_Product_Name'] = df['Bank_Product_Name'].apply(lambda x:re.sub('\n',' ',x))
order = ["Date", "Bank_Native_Country", "State", "Bank_Name", "Bank_Local_Currency", "Bank_Type", "Bank_Product", "Bank_Product_Type", "Bank_Product_Code", "Bank_Product_Name", "Min_Loan_Amount", "Bank_Offer_Feature", "Term (Y)", "Interest_Type", "Interest", "APR", "Mortgage_Loan_Amt", "Mortgage_Down_Payment", "Mortgage_Category", "Mortgage_Reason", "Mortgage_Pymt_Mode","Source"]
df = df[order]
print(df)
df.to_csv(path, index=False)
