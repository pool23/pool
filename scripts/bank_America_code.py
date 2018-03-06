# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
import datetime
import warnings
from maks_lib import output_path
warnings.simplefilter(action='ignore')

df0=pd.read_excel("DigitalDeposit_MD.xlsx",sheet_name="page-1")
df1=pd.read_excel("DigitalDeposit_MD.xlsx",sheet_name="page-2")
df2=pd.read_excel("DigitalDeposit_MD.xlsx",sheet_name="page-3")
df01=df0[4:9]
df01["Product"]="Rewards Savings"
df01=df01[3:5]
df01.drop(df01.columns[[3]], axis=1, inplace=True)
df02=df0[12:14]
df02["Product"]="Rewards Savings Gold"
df02["Deposit Interest Rates & Annual Percentage Yields (APYs)"]=df02["Unnamed: 1"]
df02["Unnamed: 1"]=df02["Unnamed: 2"]
df02["Unnamed: 2"]=df02["Unnamed: 3"]
df02.drop(df02.columns[[3]], axis=1, inplace=True)
df03=df0[14:17]
df03["Product"]="Rewards Savings Platinum"
df03.drop(df03.columns[[3]], axis=1, inplace=True)
df03=df03[1:]
df04=df0[17:20]
df04["Product"]="Rewards Savings Platinum Honors"
df04.drop(df04.columns[[3]], axis=1, inplace=True)
df04=df04[1:]
df05=df0[20:24]
df05["Product"]="Banking Rewards for Wealth Management"
df05.drop(df05.columns[[3]], axis=1, inplace=True)
df05=df05[2:]
frames_page1 = [df01,df02,df03,df04,df05]
result_page1 = pd.concat(frames_page1)
result_page1= result_page1.rename(columns={'Deposit Interest Rates & Annual Percentage Yields (APYs)': 'Balance','Unnamed: 2': 'APY','Unnamed: 1': 'Interest'})
result_page1=result_page1.reindex(columns=["Balance","Interest","APY","Product"])

df11=df1[16:21]
df11["Product"]="Bank of America Interest Checking"
df11=df11[2:]
df11= df11.rename(columns={'The Interest Rate Booster ("Booster") is included in the "Rate %" and "APY %" shown above for the Preferred Rewards': 'Balance','Unnamed: 1': 'Interest', 'Unnamed: 2': 'APY'})
result_page2 = df11

df21=df2[0:12]
df22 = df21.iloc[:,0:4]
df22.drop(df22.columns[[1]], axis=1, inplace=True)
df22["Product"]="Fixed Term CD/IRA Products"
df22=df22[1:]
df22["Balance"]="Less than $10,000"
df22=df22[3:]
df22= df22.rename(columns={'Fixed Term CD/IRA Products':'Terms','Unnamed: 3': 'APY','Unnamed: 2': 'Interest'})
df22=df22.reindex(columns=["Balance","Interest","APY","Product","Terms"])

df23=df2[0:12]
df23.drop(df23.columns[[1,2,3,4,6,7]], axis=1, inplace=True)
df23["Product"]="Fixed Term CD/IRA Products"
df23=df23[1:]
df23["Balance"]="$10,000 - $99,999"
df23=df23[3:]
df3=pd.DataFrame(df23["Unnamed: 5"].str.rsplit(None,1).tolist(),columns=["Interest","APY"])
df23["Interest"] = df3["Interest"].values
df23["APY"]= df3["APY"].values
df23.drop(df23.columns[[1]], axis=1, inplace=True)
df23= df23.rename(columns={'Fixed Term CD/IRA Products':'Terms'})
df23=df23.reindex(columns=["Balance","Interest","APY","Product","Terms"])

df24=df2[0:12]
df24.drop(df24.columns[[1,2,3,5,4,6]], axis=1, inplace=True)
df24["Product"]="Fixed Term CD/IRA Products"
df24=df24[1:]
df24["Balance"]="$100,000 and over"
df24=df24[3:]
df3=pd.DataFrame(df24["Unnamed: 7"].str.rsplit(None,1).tolist(),columns=["Interest","APY"])
df24["Interest"] = df3["Interest"].values
df24["APY"]= df3["APY"].values
df24.drop(df24.columns[[1]], axis=1, inplace=True)
df24= df24.rename(columns={'Fixed Term CD/IRA Products':'Terms'})
df24=df24.reindex(columns=["Balance","Interest","APY","Product","Terms"])
frames_page3 = [df22,df23,df24]
result_page3 = pd.concat(frames_page3)

frames=[result_page1,result_page2,result_page3]
result=pd.concat(frames)
result["Bank Name"]="Bank of America"
result=result.reindex(columns=["Bank Name","Balance","Interest","APY","Product","Terms"])
now = datetime.datetime.now()
result["Date"]=now.strftime("%m/%d/%Y")
result=result.reindex(columns=["Date","Bank Name","Balance","Interest","APY","Product","Terms"])
result.to_csv(output_path + "BOA_Data_Deposit_{}.csv".format(now.strftime("%m_%d_%Y")), index=False )
