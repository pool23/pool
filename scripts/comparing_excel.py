import os, sys
import pandas as pd
from maks_lib import US
path = US
os.chdir(path)


# df1 = pd.read_csv('US_Deposits_Data_2018_04_13.csv')
# df2 = pd.read_csv('US_FINAL_Deposits_Data_2018_04_16.csv')
#
# difference = df1[df1!=df2]
# print(difference)
#
# A = pd.read_csv("US_Deposits_Data_2018_04_13.csv", header=None, usecols=[0], names=['col']).drop_duplicates()
# B = pd.read_csv("US_FINAL_Deposits_Data_2018_04_16.csv", header=None, usecols=[0], names=['col']).drop_duplicates()
# # A - B
# df = pd.merge(A, B, on='col', how='left', indicator=True).query("_merge == 'left_only'")
# # B - A
# df1 = pd.merge(A, B, on='col', how='right', indicator=True).query("_merge == 'right_only'")
# # print(df)
# differnce = df[df!=df1]
# print(differnce)

# old_csv = "US_Deposits_Data_2018_04_13.csv"
# new_csv = "US_FINAL_Deposits_Data_2018_04_16.csv"
#
# with open('US_Deposits_Data_2018_04_13.csv', 'r') as t1:
#     old_csv = t1.readlines()
# with open('US_FINAL_Deposits_Data_2018_04_16.csv', 'r') as t2:
#     new_csv = t2.readlines()
#
# with open('compared.csv', 'w') as out_file:
#     line_in_new = 0
#     line_in_old = 0
#     while line_in_new < len(new_csv) and line_in_old < len(old_csv):
#         if old_csv[line_in_old] != new_csv[line_in_new]:
#             out_file.write(new_csv[line_in_new])
#         else:
#             line_in_old += 1
#         line_in_new += 1

import pandas as pd

df0 = pd.read_csv("US_Deposits_Data_2018_04_17.csv")
df1 = pd.read_csv("US_FINAL_Deposits_Data_2018_04_18.csv")
df0 = df0.set_index("Ticker")
df1 = df1.set_index("Ticker")
df0
a0, a1 = df0.align(df1)
different = (a0 != a1).any(axis=1)
comp = a0[different].join(a1[different], lsuffix='_old', rsuffix='_new')
comp.to_csv('example.csv', index=False)







#-*- coding:utf-8 -*-
import re


old_file = "" #Please enter the path of Old file
new_file = ""#Please enter the path of New file
outputFile = "" #Please enter the path of output file


table_rows = ''
old_data_date = ''
old_data = []
new_data_date = ''
new_data = []
table_found = False
with open(old_file, 'r') as t1, open(new_file, 'r') as t2:
    for k in t1.readlines():
        # print(k)
        if not table_found:
            table_rows = k
            table_found = True
        old_data_date = k[:k.index(',')]
        k = re.sub(r'[^\x00-\x7F]', '', k[k.index(',') + 1:])
        old_data.append(k)
    for l in t2.readlines():
        new_data_date = l[:l.index(',')]
        l = re.sub(r'[^\x00-\x7F]','',l[l.index(',')+1:])
        new_data.append(l)

# print(table_rows)
with open(outputFile, 'w') as outFile:
    outFile.write(table_rows)
    for line in new_data:
        if line not in old_data:
            print(line)
            outFile.write(new_data_date+','+line)
