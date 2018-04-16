import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
import  pandas as pd
import datetime
import re
import numpy as np
import time
from maks_lib import output_path
print('Execution Started Please Wait..')
start_time = time.time()
today = datetime.datetime.now()
path = output_path+'Consolidate_WellsF_Data_Mortgage_'+today.strftime("%m_%d_%Y")+'.csv'
# path = 'Consolidate_WellsF_Data_Mortgage_'+today.strftime("%m_%d_%Y")+'.csv'
table_headers = ["Bank_Product_Name", "Product_Term", "Balance", "Product_Interest", "Product_Apy", "Mortgage_Down_Payment", "Mortgage_Loan", "Min_Credit_Score_Mortagage", "Mortgage_Apr"]
ExceTable = []
# ExceTable.append(table_headers)
for i in range(1,21):
    try:
        resp  = requests.get('https://www.wellsfargo.com/mortgage/rates/purchase-assumptions?prod='+str(i)).content
        table = BeautifulSoup(resp,'html.parser').find('div', attrs={'class':'mainContentCol'})
        if table is not  None:
            Min_Credit_Score_Mortagage = table.find('p').text if table.find('p') is not None else None
            table = table.find('table')
            Bank_Product_Name = table.find('thead').find('th', attrs={'id':'productName'}).text
            tbody = table.find('tbody')
            Product_Interest = tbody.find('td', attrs={'headers':'productName intRate'}).text
            Mortgage_Apr = tbody.find('td', attrs={'headers': 'productName apr'}).text
            Mortgage_Loan = tbody.find('td', attrs={'headers': 'productName lAmt'}).text
            Mortgage_Down_Payment = tbody.find('td', attrs={'headers': 'productName dPayment'}).text.strip()
            Product_Term = tbody.find('td', attrs={'headers': 'productName term'}).text
            a = [Bank_Product_Name, re.sub('[^0-9.]','', Product_Term), np.NaN, Product_Interest, np.NaN, Mortgage_Down_Payment,Mortgage_Loan, Min_Credit_Score_Mortagage, Mortgage_Apr]
            ExceTable.append(a)
    except Exception as e:
        print(e)

print(tabulate(ExceTable))
df = pd.DataFrame(ExceTable, columns=table_headers)
df["Date"] = ' '+today.strftime("%m-%d-%Y")
df["Bank_Name"] = "WELLS FARGO"
df["Bank_Product"] = "Mortgages"
df["Bank_Product_Type"] = "Mortgages"
df["Bank_Offer_Feature"] = "Offline"
df["Balance"] = np.NAN
df["Product_Apy"] = np.NAN
df['Min_Credit_Score_Mortagage'] = df['Min_Credit_Score_Mortagage'].apply(lambda x: re.sub('[^0-9.]','',re.findall('score of \d.*,',x, re.IGNORECASE)[0]) if len(re.findall('score of \d.*,',x, re.IGNORECASE))!=0 else np.NaN)
order = ["Date", "Bank_Name", "Bank_Product", "Bank_Product_Type", "Bank_Offer_Feature", "Bank_Product_Name", "Product_Term", "Balance", "Product_Interest", "Product_Apy", "Mortgage_Down_Payment", "Mortgage_Loan", "Min_Credit_Score_Mortagage", "Mortgage_Apr"]
df = df[order]
df.to_csv(path, index=False)
print('Execution Completed...')
print('Total Execution Time is ',(time.time()-start_time)/60, 'Seconds')
