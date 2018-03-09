import pandas as pd
import numpy as np
import datetime
import warnings
from maks_lib import input_path
from maks_lib import output_path
warnings.simplefilter(action='ignore')
now = datetime.datetime.now()
df=pd.read_excel(input_path+"JP Morgan Rate Sheet.xlsx")
df1=df[8:14]
df1.drop(df1.columns[[0,6]], axis=1, inplace=True)
df1["Bank_Product_Name"]="Chase Premier Plus Checking SM"
df1=df1[df1.columns[2:]]
df1= df1.rename(columns={'Unnamed: 3': 'Balance','Unnamed: 4': 'Product_Interest', 'Unnamed: 5': 'Product_Apy'})
df1=df1[2:]
df1['Product_Interest'] = (df1['Product_Interest']*100).astype(str)+'%'
df1['Product_Apy'] = (df1['Product_Apy']*100).astype(str)+'%'

df2=df[16:17]
df2.drop(df2.columns[[4,5,6]], axis=1, inplace=True)
df2= df2.rename(columns={'Consumer Deposit Rates': 'Bank_Product_Name','Unnamed: 1': 'Balance','Unnamed: 2': 'Product_Interest', 'Unnamed: 3': 'Product_Apy'})
df2['Product_Interest'] = (df2['Product_Interest']*100).astype(str)+'%'
df2['Product_Apy'] = (df2['Product_Apy']*100).astype(str)+'%'
df2["Bank_Product_Name"]="Chase Savings SM"

df3=df[48:49]
df3.drop(df3.columns[[1,2,3,4,5]], axis=1, inplace=True)
df6=pd.DataFrame(df3["Unnamed: 6"].str.rsplit(None,1).tolist(),columns=["Interest","APY"])
df3["Product_Interest"] = df6["Interest"].values
df3["Product_Apy"]= df6["APY"].values
df3= df3.rename(columns={'Consumer Deposit Rates': 'Product_Term'})
df3["Bank_Product_Name"]="CERTIFICATES OF DEPOSIT (CD)"
df3.drop(df3.columns[[1]], axis=1, inplace=True)
df3["Balance"]=df.iloc[43,6]

df4=df[50:51]
df4.drop(df4.columns[[1,2,3,4,5]], axis=1, inplace=True)
df6=pd.DataFrame(df4["Unnamed: 6"].str.rsplit(None,1).tolist(),columns=["Interest","APY"])
df4["Product_Interest"] = df6["Interest"].values
df4["Product_Apy"]= df6["APY"].values
df4.drop(df4.columns[[1]], axis=1, inplace=True)
df4= df4.rename(columns={'Consumer Deposit Rates': 'Product_Term'})
df4["Bank_Product_Name"]="CERTIFICATES OF DEPOSIT (CD)"
df4["Balance"]=df.iloc[43,6]

df5=df[54:55]
df5.drop(df5.columns[[1,2,3,4,5]], axis=1, inplace=True)
df6=pd.DataFrame(df5["Unnamed: 6"].str.rsplit(None,1).tolist(),columns=["Interest","APY"])
df5["Product_Interest"] = df6["Interest"].values
df5["Product_Apy"]= df6["APY"].values
df5.drop(df5.columns[[1]], axis=1, inplace=True)
df5= df5.rename(columns={'Consumer Deposit Rates': 'Product_Term'})
df5["Bank_Product_Name"]="CERTIFICATES OF DEPOSIT (CD)"
df5["Balance"]=df.iloc[43,6]

frames = [df1,df2,df3,df4,df5]
result = pd.concat(frames)
df_final=pd.DataFrame(columns=["Date","Bank_Name",'Bank_Product',"Bank_Product_Type",'Bank_Offer_Feature', 'Bank_Product_Name', 'Product_Term', 'Balance','Product_Interest',
                         'Product_Apy','Mortgage_Down_Payment','Mortgage_Loan','Min_Credit_Score_Mortagage','Mortgage_Apr'])
df_final['Bank_Product_Name'] = result['Bank_Product_Name'].values
df_final['Product_Term'] =  result['Product_Term'].values
df_final['Balance'] =  result['Balance'].values
df_final['Product_Interest'] = result['Product_Interest'].values
df_final['Product_Apy'] = result['Product_Apy'].values
df_final['Date'] = now.strftime("%m-%d-%Y")
df_final['Bank_Name']="JP MORGAN CHASE & Co."
df_final['Bank_Product'] = 'Deposits'
df_final['Bank_Offer_Feature'] = 'Offline'
df['Balance']=(df_final['Balance']).astype(str,copy=True)

for index in range(len(result.index)):
    if "Checking" in result['Bank_Product_Name'].iloc[index]:
        df_final.ix[index,'Bank_Product_Type'] = "Checking"
    elif "Savings" in result['Bank_Product_Name'].iloc[index]:
        df_final.ix[index,'Bank_Product_Type'] = "Savings"
    elif "CERTIFICATES" in result['Bank_Product_Name'].iloc[index]:
        df_final.ix[index,'Bank_Product_Type'] = "CD"

df_final.to_excel(output_path + "Consolidate_JPM_Data_Deposit_{}.xlsx".format(now.strftime("%m_%d_%Y")), index=False )