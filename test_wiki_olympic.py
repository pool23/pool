import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_html('https://en.wikipedia.org/wiki/2018_Winter_Olympics_medal_table')
df[1].ix[22,:]= df[1].ix[22,:].shift(1,axis=0)
df[1].ix[27,:]=df[1].ix[27,:].shift(1,axis=0)
df[1].ix[29,:]=df[1].ix[29,:].shift(1,axis=0)
df[1].ix[30,:]=df[1].ix[30,:].shift(1,axis=0)
df[1].ix[31,:]=df[1].ix[31,:].shift(1,axis=0)
df[1].to_csv('wiki_olympic_2018.csv', index=False, header=False)
df = pd.read_csv('wiki_olympic_2018.csv')
df = df[:-1]
valuess=df['NOC'].values
df.plot(x='NOC',y=['Gold','Silver','Bronze'],kind='kde')
plt.xlabel(valuess)
#plt.xticks(df['NOC'])
plt.ylim(0,16)
plt.show()
