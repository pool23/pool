#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Purpose: This program scrapes numbers of property type for US states, Country and India's top 50 cities from
             Booking.com

              ************************************************************************
             #    Author                        Date                Version          #
             # --------------------------------------------------------------------- #
             #  Moody's Analytics            11-4-2018                 V1            #
              ************************************************************************
"""

# importing required libraries
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import pandas as pd
import re
import time

start = time.time()
# Created an empty dictionary using default dic module and two empty lists state and total
d = defaultdict(list)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}

# opening a text file booking_id_US_State which contains id for each US state
file = open('booking_id_US_State.txt', 'r')
total = []
# Iterating over each state id using variable i
for i in file:
    print(i)
    # static list of category is taken in variable L
    L = ['hotels', 'campgrounds', 'condos', 'homestays', 'resorts', 'apartments', 'villas',
         'bed and breakfasts', 'holiday homes', 'lodges', 'hostels', 'boats', 'luxury tents', 'farm stays',
         'chalets', 'country houses', 'economy hotels', 'motels', 'resort villages', 'cruises', 'capsule hotels',
         'cottages', 'love hotels', 'riads', 'guest houses', 'campsites','b&bs;/guest houses','camping','holiday parks']

    # creating an empty list as label, l_count and N
    label = []
    l_count = []
    N = []
    # sending request to given URL using function requests.get()

    # r = requests.get('https://www.booking.com/searchresults.en-gb.html?region ='+ str(i)+';offset = 15', headers = headers)
    r = requests.get('https://www.booking.com/searchresults.html?dest_id=' + str(i) + ';dest_type=region;offset=15', headers = headers)
    # getting response from url and feeding into BeautifulSoup and getting HTML page
    soup = BeautifulSoup(r.content, 'html.parser')
    # trying to find total number of properties, Name of state and other information from html content
    try:
        # fetching name of state and removing whitespaces and newline and appending it to state list
        st = soup.find('h1', attrs={'class': 'sorth1'})
        total.append(st.text.lstrip('\n').rstrip('\n'))
        print(total)
        # total.append(st)
        # finding all the category present for each state on site and iterating it on each category, adding it to list


        labels = soup.find('p',attrs={'class':'filtercategory-title'} ,text=re.compile('Property type')).parent.parent.find_all('div',attrs={'class': re.compile('filter_item')})


        for g in labels:
            span = g.find_all('span')
            print(span)
            label.append(span[0].text.strip().lower())
            l_count.append(span[1].text.strip())
        print(l_count)
        print('label=', label)
        # Comparing category found with static list and assign not found categories to main list same for category count
        main_list = [item for item in L if item not in label]
        value_list = [N.append(None) for item in L if item not in label]
        print('main_list=',main_list)
        print(value_list)
        # Appending missing category and counts to label and count list
        for j in main_list:
            label.append(j)
        for m in N:
            l_count.append(m)
        print(label)
        print(l_count)
        print(len(label))
        print(len(l_count))
        print(len(total))
    # if try block fails then printing exception as e
    except Exception as e:
        print(soup)
        print(e)
        break
    # Making two list as dictionary and appending dictionary as key value to empty dictionary
    for key, value in zip(label, l_count):
        d[key].append(value)
# Using pandas making DataFrame and saving result to csv
df = pd.DataFrame.from_dict(d)
df['Total properties'] = total
df.to_csv("booking_try.com.csv", index=False)

print("**********************************Scraping data for Global************************************")
# Taking again an empty dictionary
d = defaultdict(list)
# Making requests to given URL using requests.get()
r = requests.get('https://www.booking.com/country.en-gb.html?label=gen173nr-1FCAEoggJCAEoggJCAlhYSONYBHlFdXNfbnmIAQGYAT'
                 'G4AQblAQzYAQH4AQKSAgF5qAID;sid=db23e9ff70eb44d7a9d04846ad2dd;inac=0&')
# getting response from url and feeding into BeautifulSoup and getting HTML page
# Created three empty lists state, total, N
soup = BeautifulSoup(r.content, 'lxml')
total = []
state = []
N = []
# static list of category is taken in variable L
L = ['holiday rentals', 'apartments', 'homestays', 'guest houses', 'resorts', 'hostels', 'inns',
     'serviced apartments', 'villas', 'motels', 'B&Bs', 'cabins', 'lodges', 'economy hotels',
     'country houses', 'capsule hotels', 'farm stays', 'holiday parks', 'luxury tents', 'campsites', 'budget hotels',
     'boutique hotels', 'spa hotels', 'golf hotels', 'boats', 'cottages', 'romantic hotels', 'love hotels',
     'riads', 'ryokans', 'glamping sites']
# Fetching all the content of divs having class block_third block_third--flag-module
regions = soup.find_all('div', attrs={'class': 'block_third block_third--flag-module'})
print(len(L))
# iterating from 0 to 199 div
for i in range(0, 200):
    # Created empty list category and count
    category = []
    count = []
    # trying to fetch content
    try:
        # Appending total number to total
        total.append(regions[i].find('span', attrs={'class': 'number_hotels'}).text.strip())
        # Appending country name to total list
        state.append(regions[i].find('h2').find('a').text)
        # Selecting Accommodation category for each state
        oth_acc = regions[i].find_all('div', attrs={'class': 'inner_block'})
        # When accommodation category  are two append each and category and count
        if len(oth_acc) > 1:
            count0 = (re.findall('\d+(?:,\d+)? +', oth_acc[0].find('ul').text.strip()))
            category0 = (re.findall('[a-zA-Z].+', oth_acc[0].find('ul').text.strip()))
            oth_acc = regions[i].find_all('div', attrs={'class': 'inner_block'})
            count1 = (re.findall('\d+(?:,\d+)? +', oth_acc[1].find('ul').text.strip()))
            category1 = (re.findall('[a-zA-Z].+', oth_acc[1].find('ul').text.strip()))
            category = sum([category1, category0], [])
            count = sum([count1, count0], [])
            main_list = [item for item in L if item.strip() not in category]
            value_list = [N.append(None) for item in L if item.strip() not in category]
            for j in main_list:
                category.append(j)
            for m in N:
                count.append(m)
            print("Final category", category)
            print(len(category))
        # When there is no accommodation category
        elif len(oth_acc) == 0:
            main_list = [item for item in L]
            print("mainlist", len(main_list))
            value_list = [N.append(None) for item in L]
            print(len(value_list))
            for j in main_list:
                category.append(j)
            for m in N:
                count.append(m)
            print(len(category))
            print("No More hotel theme")
        # When accommodation category  is one append each and category and count
        else:
            count0 = (re.findall('\d+(?:,\d+)? +', oth_acc[0].find('ul').text.strip()))
            category0 = (re.findall('[a-zA-Z].+', oth_acc[0].find('ul').text.strip()))
            category = category0
            count = count0
            main_list = [item for item in L if item.strip() not in category0]
            print("mainlist", len(main_list))
            value_list = [N.append(None) for item in L if item.strip() not in category0]
            for j in main_list:
                category.append(j)
            for m in N:
                count.append(m)
            print("Final category", category)
            print(len(category))
            print("No More hotel theme")
    # if try block fails then printing exception as e
    except Exception as e:
        print(e)
    print("i", i)
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    # Making two list as dictionary and appending dictionary as key value to empty dictionary
    for key, value in zip(category, count):
        d[key].append(value)
# Using pandas making DataFrame and saving result to csv
df = pd.DataFrame.from_dict(d)
df['States'] = state
df['Total Properties'] = total
df.to_csv("booking_global_Previous.csv", index=False)

# print("**********************************Scraping data for top 50 states in India************************************")
# # Created an empty dictionary using default dic module and two empty lists state and total
# d = defaultdict(list)
#
# total = []
#
# # opening a text file booking_id_US_State which contains id for each US state
# file = open('booking_india.txt', 'r')
# # Iterating over each state id using variable i
# for i in file:
#     # static list of category is taken in variable L
#     L = ['hotels', 'campgrounds', 'condos', 'homestays', 'resorts', 'apartments', 'villas',
#          'bed and breakfasts', 'holiday homes', 'lodges', 'hostels', 'boats', 'luxury tents', 'farm stays',
#          'chalets', 'country houses', 'economy hotels', 'motels', 'resort villages', 'cruises', 'capsule hotels',
#          'cottages', 'love hotels', 'riads', 'guest houses', 'campsites','b&bs;/guest houses','camping','holiday parks','guesthouses',
#          'vacation homes']
#     # creating an empty list as label, l_count and N
#     label = []
#     l_count = []
#     N = []
#     # sending request to given URL using function requests.get()
#     r = requests.get('https://www.booking.com/searchresults.html?city=' + str(i))
#     print(i)
#     # getting response from url and feeding into BeautifulSoup and getting HTML page
#     soup = BeautifulSoup(r.content, 'html.parser')
#     # trying to find total number of properties, Name of state and other information from html content
#     try:
#         # fetching name of state and removing whitespaces and newline and appending it to state list
#         st = soup.find('h1', attrs={'class': 'sorth1'})
#         total.append(st.text.lstrip('\n').rstrip('\n'))
#         print(total)
#         # total.append(st)
#         # finding all the category present for each state on site and iterating it on each category, adding it to list
#         # print(soup)
#         labels = soup.find('p', attrs={'class': 'filtercategory-title'},text=re.compile('Property type',re.IGNORECASE)).parent.parent.find_all('div',attrs={'class': re.compile('filter_item')})
#         for g in labels:
#             span = g.find_all('span')
#             label.append(span[0].text.strip().lower())
#             l_count.append(span[1].text.strip())
#         print(l_count)
#         print('label=', label)
#         # Comparing category found with static list and assign not found categories to main list same for category count
#         main_list = [item for item in L if item not in label]
#         value_list = [N.append("0") for item in L if item not in label]
#         # Appending missing category and counts to label and count list
#         print('main_list=', main_list)
#         for j in main_list:
#             label.append(j)
#         for m in N:
#             l_count.append(m)
#         # if try block fails then printing exception as e
#         print(len(label))
#         print(len(l_count))
#         print(len(total))
#     except Exception as e:
#         # print(soup)
#         print(e)
#         break
#     for key, value in zip(label, l_count):
#         d[key].append(value)
# df = pd.DataFrame.from_dict(d)
# df['Total Properties'] = total
# df.to_csv("booking_india.com.csv", index=False)
# #
# # Storing the finishing time of program
# end = time.time()
# # Printing out the  total time of Execution
# print("--- %s seconds ---" % (end - start))