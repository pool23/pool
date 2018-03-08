import pandas as pd
import numpy as np
import datetime
import warnings
#from maks_lib import output_path
warnings.simplefilter(action='ignore')
now = datetime.datetime.now()
df0=pd.read_csv('C:\\Users\\Rupa\\PycharmProjects\\pool-master\\data\\output\\BOA_Data_Deposit_03_07_2018.csv')
df=pd.DataFrame(columns=["Date","Bank_Name",'Bank_Product',"Bank_Product_Type",'Bank_Offer_Feature', 'Bank_Product_Name', 'Product_Term', 'Balance','Product_Interest',
                         'Product_Apy','Mortgage_Down_Payment','Mortgage_Loan','Min_Credit_Score_Mortagage','Mortgage_Apr'])

df['Date'] = df0['Date'].values
df['Bank_Name']="BANK OF AMERICA CORP"
df['Bank_Product'] = 'Deposits'
df['Bank_Offer_Feature'] = 'Offline'
df['Bank_Product_Name'] =  df0['Product'].values
df['Product_Term'] =  df0['Terms'].values
df['Balance'] =  df0['Balance'].values
df['Product_Interest'] = df0['Interest'].astype(str)+'%'
df['Product_Apy'] = df0['APY'].astype(str)+'%'
for index, row in df0.iterrows():
    if "Checking" in row['Product']:
        df.iloc[index,3] = "Checking"
    elif "Savings" in row['Product']:
        df.iloc[index,3] = "Savings"
    elif "Fixed" in row['Product']:
        df.iloc[index,3] = "IRA CDs"
    elif "Wealth" in row['Product']:
        df.iloc[index,3] = "Savings"
df.to_csv( "Consolidated_BOA_Data_Deposit_{}.csv".format(now.strftime("%m_%d_%Y")), index=False )
    