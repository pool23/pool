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