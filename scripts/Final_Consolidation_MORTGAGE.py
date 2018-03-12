
# coding: utf-8

# In[267]:


import glob
import os
import pandas as pd
import numpy as np
import datetime
import warnings
from maks_lib import output_path
from maks_lib import input_path
warnings.simplefilter(action='ignore')
now = datetime.datetime.now()

extension = 'csv'


# In[268]:


all_files = glob.glob(output_path+'*.{}'.format(extension))
all_mortage_files  = [file for file in all_files if file.split("\\")[-1].startswith("Cons") and "Mortgage" in file.split("\\")[-1]]
all_deposite_files = [file for file in all_files if file.split("\\")[-1].startswith("Cons") and file not in all_mortage_files]


# In[269]:


COLUMN_NAMES = list(pd.read_csv(all_mortage_files[0]).columns)
df_mortgage = pd.DataFrame(columns=COLUMN_NAMES) 
df_deposit = pd.DataFrame(columns=COLUMN_NAMES)


# In[270]:


df_mortgage


# In[271]:


for idx, file in enumerate(all_mortage_files):
    print(file)
    print(pd.read_csv(all_mortage_files[idx]).shape[1])


# In[272]:


for file in all_mortage_files:
    df_temp =pd.read_csv(file)
    df_temp.columns = ['Date', 'Bank_Name', 'Bank_Product', 'Bank_Product_Type',
       'Bank_Offer_Feature', 'Bank_Product_Name', 'Product_Term', 'Balance',
       'Product_Interest', 'Product_Apy', 'Mortgage_Down_Payment',
       'Mortgage_Loan', 'Min_Credit_Score_Mortagage', 'Mortgage_Apr']
    df_mortgage = pd.concat([df_mortgage, df_temp])


# In[273]:


df_mortgage.shape


# In[274]:


df_mortgage


# In[275]:


df_mortgage.dropna(axis=0, how='all', inplace=True)


# In[276]:


df_mortgage.drop(columns=["Product_Apy"], inplace=True)


# In[277]:


df_mortgage.rename(columns={"Balance": "Min_Loan_Amount", "Product_Term": "Term_in_Year","Product_Interest": "Interest","Mortgage_Loan": "Mortgage_Loan_Amt","Min_Credit_Score_Mortagage":"Credit_Score", "Mortgage_Apr":"APR"}, inplace = True,index=str)


# In[278]:


df_mortgage['Date'] = now.strftime("%m/%d/%Y")
df_mortgage['Bank_Native_Country'] = "US"
df_mortgage['State'] = "New York"
df_mortgage['Bank_Local_Currency'] = "USD"
df_mortgage['Bank_Type'] = "Bank"
df_mortgage['Bank_Product'] = "Mortgages"
df_mortgage['Bank_Product_Type'] = "Mortgages"
df_mortgage['Bank_Product_Code'] = np.NAN
df_mortgage['Min_Loan_Amount'] = np.NAN
df_mortgage['Interest_Type'] = "Fixed"
df_mortgage['Mortgage_Category'] = "New Purchase"
df_mortgage['Mortgage_Reason'] = "Primary Residence"
df_mortgage['Mortgage_Pymt_Mode'] = "Principal + Interest"


# In[279]:


df_mortgage.columns


# In[280]:


arranged_cols = ['Date', 'Bank_Native_Country','State','Bank_Name', 'Bank_Local_Currency','Bank_Type','Bank_Product', 'Bank_Product_Type','Bank_Product_Code','Bank_Product_Name','Min_Loan_Amount','Bank_Offer_Feature','Term_in_Year','Interest_Type','Interest','APR','Mortgage_Loan_Amt','Mortgage_Down_Payment', 'Credit_Score','Mortgage_Category', 'Mortgage_Reason','Mortgage_Pymt_Mode']


# In[281]:


df_mortgage = df_mortgage.reindex(columns= arranged_cols)


# In[282]:


for idx in range(len(df_mortgage.index)):
    if "ARM" in df_mortgage['Bank_Product_Name'].iloc[idx] or "Adjustable Rate" in df_mortgage['Bank_Product_Name'].iloc[idx]:
        df_mortgage['Interest_Type'].iloc[idx] = "Variable"


# In[283]:


for idx in range(len(df_mortgage.index)):
    #print(df_mortgage['Bank_Product_Name'].iloc[idx])
    #print(type(df_mortgage['Bank_Product_Name'].iloc[idx]))
    df_mortgage['Bank_Product_Code'].iloc[idx] = "{0}{1}{2}{3}".format(int(df_mortgage['Term_in_Year'].iloc[idx]),"Y", "M", df_mortgage['Interest_Type'].iloc[idx][0])
    #print(df_mortgage['Interest_Type'].iloc[idx])


# In[284]:


df_mortgage.to_csv(output_path+"US\\" + "US_Mortgage_Data_{}.csv".format(now.strftime("%m_%d_%Y")), index=False )

