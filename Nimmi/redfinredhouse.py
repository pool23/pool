from selenium import webdriver
from bs4 import BeautifulSoup as b
import pandas as pd
import time


driver = webdriver.Firefox()
df = pd.DataFrame()
file = open('redfinredhouse.txt', 'r')
for loc in file:
    loc = loc.strip()
    print(loc)
    driver.get('https://www.redfin.com/state/' + loc)
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="sidepane-header"]/div[3]/button[2]/span').click()
    driver.execute_script("window.scrollBy(0, document.documentElement.scrollHeight)")
    time.sleep(2)
    count = int(
        b(driver.page_source, 'lxml').find('div', attrs={'data-rf-test-id': 'paging-controls'}).find_all('a')[-1].text)
    print(count)
    try:
        found = b(driver.page_source, 'lxml').find_all('div', attrs={'class': 'property redfin'})
        print(len(found))
        df = df.append({'Found Red House': len(found), 'Total_Listings':
            b(driver.page_source, 'lxml').find('div', attrs={'class': 'descriptionSummary'})
                       .find('div', attrs={'data-rf-test-id': 'homes-description'}).text.replace('Showing 20 of ', '').rstrip(' Homes•').strip(),
                        'State': loc}, ignore_index=True)
        for link in range(2, count + 1):
            print(str(link))
            driver.get('https://www.redfin.com/state/' + loc + '/page-' + str(link))
            time.sleep(2)
            driver.find_element_by_xpath('//*[@id="sidepane-header"]/div[3]/button[2]/span').click()
            driver.execute_script("window.scrollBy(0, document.documentElement.scrollHeight)")
            time.sleep(2)
            try:
                found = b(driver.page_source, 'lxml').find_all('div', attrs={'class': 'property redfin'})
                print(len(found))
            except Exception as e:
                print(e)
                print('Not found')
            try:
                while found:
                    df = df.append({'Found Red House': len(found), 'Total_Listings':
                        b(driver.page_source, 'lxml').find('div', attrs={'class': 'descriptionSummary'})
                                   .find('div', attrs={'data-rf-test-id': 'homes-description'}).text.replace(
                            'Showing 20 of ', '').rstrip(
                            ' Homes•').strip(), 'State': loc}, ignore_index=True)
                    # print(df)
                    break
            except:
                pass
    except:
        pass
    print(df)
df.to_csv('RedfinRedHouse.csv', index=False)
driver.close()