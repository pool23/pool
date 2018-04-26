import requests
import re
from tabulate import tabulate
import pandas as pd
from bs4 import BeautifulSoup
from maks_lib import output_path
import datetime
today = datetime.datetime.now()
path = output_path+'Consolidate_SunTrust_Data_Mortgage_'+today.strftime('%m_%d_%Y')+'.csv'
Excel_Data = []
table_headers = ['Bank_Product_Name', 'Product_Term', 'Product_Interest', 'Mortgage_Apr', 'Mortgage_Loan', 'Mortgage_Down_Payment', 'Min_Credit_Score_Mortagage']
# Excel_Data.append(table_headers)
resp = requests.get('https://www.suntrust.com/home-mortgages/current-rates')
jsoup = BeautifulSoup(resp.content).find('div', attrs={'class':'suntrust-rowContainer'})
for div in jsoup.find_all('div', attrs={'class':re.compile('mortgagerates')}):
    try:
        col = div.find_all('div', attrs={'class':re.compile('col')})
        Bank_Product_Name = col[0].text.strip()
        # print(Bank_Product_Name)
        subDiv = col[1].find_all('div', attrs={'class':re.compile('col')})
        text1 = subDiv[0].text
        IrAr = re.findall('[0-9.%]*',text1)
        t = [k for k in IrAr if len(k)!=0]
        # print(t)
        interest = t[0]
        apr = t[1]
        Bal = subDiv[1].find('p').text
        # print(Bal)
        Balance = re.search('\$[0-9.,]*',Bal)
        if Balance is not  None:
            Balance = Balance.group(0).strip(',')

        credits = re.search('score of [0-9.]*',Bal)
        if credits is not None:
            credits = credits.group(0)
        downPayment = re.search('[0-9]*% down',Bal)
        if downPayment is not None:
            downPayment = downPayment.group(0)

        # print([Balance,credits,downPayment])
        # for tr in subDiv[1].find('table').find('tbody').find_all('tr')[1:]:
            # # print(tr)
            # tds = tr.find_all('td')
            # Month = tds[2].text
            # try:
            #     Month = int(Month)/12 if int(Month)!=0 else None
            # except:
            #     Month = None
            # # a = [Bank_Product_Name, interest, apr, Balance ,Month, credits, downPayment]
            # years = [15,30]
            # # if Month in years:
        Month = re.search('[0-9 ]*year', Bank_Product_Name, re.IGNORECASE)
        Month = int(re.sub('[^0-9]','',Month.group(0))) if Month is not None else None
        a = [Bank_Product_Name, Month, interest, apr, Balance.strip('$').replace(',',''), re.sub('[^0-9%]', '', downPayment)if downPayment is not None else '0%', re.sub('[^0-9]','',credits)if credits is not None else None]
        Excel_Data.append(a)
        print(a)
            # break
    except Exception as e:
        print(e)
    # break
order = ["Date","Bank_Name","Bank_Product","Bank_Product_Type","Bank_Offer_Feature","Bank_Product_Name","Product_Term","Balance","Product_Interest","Product_Apy","Mortgage_Down_Payment","Mortgage_Loan","Min_Credit_Score_Mortagage","Mortgage_Apr"]
df = pd.DataFrame(Excel_Data,columns=table_headers)
df['Date'] = ' '+today.strftime("%m-%d-%Y")
df['Bank_Name'] = 'SUNTRUST BANKS INC'
df['Bank_Product'] = 'Mortgages'
df['Bank_Product_Type'] = 'Mortgages'
df['Bank_Offer_Feature'] = 'Offline'
df['Product_Apy'] = None
df['Balance'] = None
df = df[order]
df.to_csv(path, index=False)
print(tabulate(Excel_Data))