import requests
from bs4 import BeautifulSoup as bs
import json
import pandas as pd
from collections import defaultdict
import itertools
import time
import datetime

d = defaultdict(list)

# Taking today's date
now = datetime.datetime.now()
start = time.time()
category_ID = ['1', '26051', '3', '4', '5', '6', '7', '21', '25', '20', '9', '26', '10', '24', '11', '8', '14',
               '12',
               '15', '5326', '16', '17', '18']

url_list = "https://www.viator.com/New-York-City/d687-ttd"
r = requests.get(url_list).content
soup = bs(r, 'lxml')
s = soup.find('div', attrs={'class':"menu-dropdown-box small"})
ul_list = s.find_all('a')
for i in ul_list:
    try:
        id = i['did']
        Country = i.text
        print("id", id)
        print(Country)
        for ids in category_ID:
            c = []
            category = []
            location = []
            state = []
            price = []
            r = requests.get('https://www.viator.com/api/destProdFilter.jspa?destinationID=' + str(id) +
                             '&currency=USD&pageLister.pageSize=45&criteria.groupId='
                             + str(ids) + '&criteria.sortBy=002')
            print('https://www.viator.com/api/destProdFilter.jspa?destinationID=' + str(id)
                  + '&currency=USD&pageLister.pageSize=45&criteria.groupId='
                  + str(ids) + '&criteria.sortBy=002')
            counts = json.loads(r.content)
            print(counts)
            for i in range(0, (len(counts['pagedList']))):
                category.append(counts['pagedList'][i]['s_primaryGroupName'][0])
                print(counts['pagedList'][i]['s_primaryGroupName'][0])
                p_c = counts['pagedList'][i]['priceFrom'][0]
                price.append(p_c)
                print(p_c)
                location.append(counts['pagedList'][i]['s_entryName'][0] +
                                str('^') + str(Country) + str('^') + str(p_c))
                state.append(counts['pagedList'][0]['s_commences'][0].split()[-1])
                print(counts['pagedList'][i]['s_primaryDestName'][0])
                print(counts['pagedList'][i]['s_entryName'][0])
                c.append(counts['pagedList'][i]['s_entryName'][0])
            print(counts['pageLister']['totalPages'])
            print("Location", len(location))
            print("Category", len(category))
            print("State", len(state))
            print("Price", len(price))
            print(len(c))
            try:
                print(counts['links'][0]['href'])
                print(counts['links'][0]['rel'])
                for next in range(2, counts['pageLister']['totalPages'] + 1):
                    next_link = 'https://www.viator.com/api/destProdFilter.jspa?' \
                                'destinationID=' + str(id) + '&currency=USD&pageLister.' \
                                                            'pageSize=45&criteria.groupId=' + str(ids) \
                                + '&criteria.sortBy=002&pageLister.page=' + str(next)
                    print(next_link)
                    a = requests.get(next_link)
                    counts = json.loads(a.content)
                    for k in range(0, (len(counts['pagedList']))):
                        state.append(counts['pagedList'][0]['s_commences'][0])
                        print(counts['pagedList'][k]['s_primaryGroupName'][0])
                        category.append(counts['pagedList'][k]['s_primaryGroupName'][0])
                        print(counts['pagedList'][k]['s_entryName'][0])
                        p_c = counts['pagedList'][i]['priceFrom'][0]
                        price.append(p_c)
                        print(p_c)
                        location.append(counts['pagedList'][k]['s_entryName'][0] +
                                        str('^') + str(Country) + str('^') + str(p_c))
                        c.append(counts['pagedList'][k]['s_entryName'][0])
                        print(counts['pagedList'][i]['priceFrom'])
                        state.append(counts['pagedList'][0]['s_commences'][0].split()[-1])
                        price.append(counts['pagedList'][k]['priceFrom'][0])
                print(len(c))
                print("Location", len(location))
                print("Category", len(category))
                print("State", len(state))
                print("Price", len(price))
            except Exception as e:
                print("Single Page")
                print(e)

            location = set(location)
            for key, value in zip(category, location):
                d[key].append(value)
            print(d)
    except Exception as e:
        print(e)

df = pd.DataFrame(list(itertools.zip_longest(*d.values())), columns=d.keys()).sort_index(axis=1)


df.to_excel("Viator_global_try.xlsx", index=False)
# Storing the finishing time of program
end = time.time()
# Printing out the  total time of Execution
print("--- %s seconds ---" % (end - start))
from pandasql import sqldf
pysqldf = lambda q: sqldf(q, globals())
import pandas as pd
# df = pd.read_csv("viator_global.csv", encoding='ISO-8859-1',  low_memory=False)
# query = """SELECT Country, count(Country) AS country_count, sum(Price) AS Total_Price, sum(Price)/count(Country) AS AVG_Price
#             FROM df
#             GROUP BY Country
#             ;
#            """
# df_temp = pysqldf(query)
# df_temp.to_csv('Average_price_viator.csv', index= False)