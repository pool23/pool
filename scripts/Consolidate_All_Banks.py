import glob
import os
import glob
import pandas as pd
import numpy as np
import datetime
import warnings
from maks_lib import output_path
from maks_lib import input_path
warnings.simplefilter(action='ignore')

now = datetime.datetime.now()

consolidate_path = output_path+"Consolidated_Data\\"
extension = 'csv'
os.chdir(consolidate_path)
all_files = glob.glob('*.{}'.format(extension))
df = pd.read_csv(input_path+"Data_Template.csv")
"""
#Check for no. of attributes
for file in all_files:
    df_temp = pd.read_csv(file)
    print(df_temp.shape[1])
    print(file)
"""
for file in all_files:
    if file.startswith("Data_Template"):
        continue
    df_temp =pd.read_csv(file)
    df = pd.concat([df, df_temp])
df["Bank_Native_Country"] = "USA"
df["Bank_Type"] = "BANK"
df["Bank_Local_Currency"] = "USD"
df["State"] = "New York"
df['Date'] = now.strftime("%m-%d-%Y")
temp = ['Date','Bank_Native_Country','State','Bank_Name','Bank_Local_Currency','Bank_Type','Bank_Product','Bank_Product_Type','Bank_Product_Name','Balance','Bank_Offer_Feature','Product_Term','Product_Interest','Product_Apy','Mortgage_Loan','Mortgage_Down_Payment','Min_Credit_Score_Mortagage','Mortgage_Apr']
df =df.reindex(columns =temp )
records_tobe_removed = list(df[df.Bank_Product_Name.isnull()].index)
df.drop(records_tobe_removed, inplace=True)
df.rename(columns={'Product_Apy': 'APY', 'Mortgage_Apr': 'APR'}, inplace=True)
df.to_csv(output_path + "US_BanksData_{}.csv".format(now.strftime("%m_%d_%Y")), index=False)