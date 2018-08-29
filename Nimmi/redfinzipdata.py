from bs4 import BeautifulSoup as b
import pandas as pd
import requests as r
import re
import json

m = ''
id = ''
sf = ''
status= ''
house = []
price = []
beds = []
baths = []
sqft = []
redfin = []
state = []
avg_price = []
avg_bed = []
avg_bath = []
avg_sqft = []
total_home = []
not_found = []

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/53'
                         '7.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
           'authority': 'www.redfin.com', 'scheme': 'https', 'accept': '*/*', 'content-type': 'application/json',
           'origin': 'https://www.redfin.com', 'referer': 'https://www.redfin.com/',
           'cookie': 'RF_BROWSER_CAPABILITIES=%7B%22css-transitions%22%3Atrue%2C%22css-columns%22%3Atrue%2C%22css-generated-content%22%3Atrue%2C%22css-opacity%22%3Atrue%2C%22events-touch%22%3Afalse%2C%22geolocation%22%3Atrue%2C%22screen-size%22%3A4%2C%22screen-size-tiny%22%3Afalse%2C%22screen-size-small%22%3Afalse%2C%22screen-size-medium%22%3Afalse%2C%22screen-size-large%22%3Afalse%2C%22screen-size-huge%22%3Atrue%2C%22html-prefetch%22%3Afalse%2C%22html-range%22%3Atrue%2C%22html-form-validation%22%3Atrue%2C%22html-form-validation-with-required-notice%22%3Atrue%2C%22html-input-placeholder%22%3Atrue%2C%22html-input-placeholder-on-focus%22%3Atrue%2C%22ios-app-store%22%3Afalse%2C%22google-play-store%22%3Afalse%2C%22ios-web-view%22%3Afalse%2C%22android-web-view%22%3Afalse%2C%22activex-object%22%3Atrue%2C%22webgl%22%3Atrue%2C%22history%22%3Atrue%2C%22localstorage%22%3Atrue%2C%22sessionstorage%22%3Atrue%2C%22position-fixed-workaround%22%3Afalse%7D; RF_UNBLOCK_ID=B4Pwzgom; RF_BROWSER_ID=pBks4lWTSxKbtCBwOeAoMA; RF_BID_UPDATED=1; _ga=GA1.2.1370949285.1535465154; _gid=GA1.2.704614574.1535465154; G_ENABLED_IDPS=google; __utmx=222895640.WTKnaAxUS8WuBy9wsrWkyg$0:0; RF_GOOGLE_ONE_TAP_DISMISSED=lastDismissalDate%3D1535465168633; displayMode=1; sortOrder=1; sortOption=special_blend; RF_CORVAIR_LAST_VERSION=225.0.1; AKA_A2=A; ak_bmsc=2BC3A37E9BB3874CE7EC8378F297D8AC17D432997F200000D221865B1C3DC079~plJDoufhUH/wt3D9cvoVCegYKm/mju45uGRRqmq1GYNJRXyGWU7Keez0D4x8uLzZO0uY2KNr3eLHW84A/HqF1bl/MNTVIj9AuIiyEswvS6EQHmCm3zEGwfDWb6SYRthiuHRWvujh4ur78xHRP31x20vEyzCNcq35L15W4KGNZm3Vf+uZI9DlnBDkRYmKdBa9wTaJyJi6jAtA26o84XZhtSZyWp8LLTg3egWeSZYrarUYg=; bm_sz=BF7CA3BD2922BD52E05A831FD73900A7~QAAQmTLUF2LlaINlAQAAtx30g1FjHjPloonWOiViNOhP69cuOCe1INCye4s71dMsAON01rw6sbrPSzkH3Q2jIJTlRx0E+CjV0bFzxLKnv+mJyDuui7GsM27WlcUPRZEIP91miDGyIZrzUWnWMuQj9QOy7UijRMYzbWgckcJ8hX9s2lyoJlwSE7IRhiOi; _abck=DC5C2BF1B513E59B2CA730C5377CC6C117D432997F200000D221865BB274C844~0~1kyaOPEvwz/DZ3mgBZD2GHyPe16j8HhchRqgXscCeRQ=~-1~-1; RF_MARKET=alabama; _dc_gtm_UA-294985-1=1; userPreferences=parcels%3Dtrue%26schools%3Dfalse%26mapStyle%3Ds%26statistics%3Dtrue%26agcTooltip%3Dfalse%26agentReset%3Dfalse%26ldpRegister%3Dfalse%26afCard%3D2%26schoolType%3D0%26viewedSwipeableHomeCardsDate%3D1535518398488; _gat_UA-294985-1=1; bm_sv=C6DEDCDED98718169903EF9604C02867~e/FBkchJ2XVtvx+G9864eci9oxxeevT3Bxb0Jr4bCMy0TUftBmNu4mcdanHf63UE81/K/KHWPdzW7jCSDVK7pe3dH3KU351F06+SFTrM5miVi3Hk8vQ3H9D2pkh5Ucar2BI1Dp2JfDhwYxPkkD7wmdvKanHpQzS7ZqvUb/Nin9Q=; RF_VISITED=null; __utmxx=222895640.WTKnaAxUS8WuBy9wsrWkyg$0:1535518429:8035200'}
res = r.get('https://www.redfin.com/sitemap/CA', headers=headers).content
zipcode =[zip.find('a')['href'] for zip in b(res, 'lxml').find('div', {'class', 'sitemap-section'}).find_next_sibling().find_all('li')]
for loc in zipcode:
    res = r.get('https://www.redfin.com' + str(loc), headers=headers).content
    try:
        total_homes = b(res, 'lxml').find('div', {'data-rf-test-id': 'homes-description'}).text.lstrip(
            'Showing 20 of ').rstrip(' Homes•')
        data = b(res, 'lxml').find('script', text=re.compile('root.__reactServerState.InitialContext = ')).text
        jdata = re.findall('root.__reactServerState.InitialContext\s=\s.+', data)
        jdata =json.loads(jdata[0].lstrip('root.__reactServerState.InitialContext = ').rstrip(';'))
        zid = str(re.sub('[^0-9]','',loc))
        # print(zid)
        # for k, v in jdata['ReactServerAgent.cache']['dataCache'].items():
            # print(k, v)
        test = '/stingray/api/region?al=1&clustering_threshold=350&ep=true&lpp=20&mpt=1&num_homes=350&page_number=1&region_id='+ zid +'&region_type=2&start=0&tz=true&v=8'
        var = jdata['ReactServerAgent.cache']['dataCache'][test]['res']
        for v in var.items():
            found = re.findall('{}.+', str(v))
            while found:
                print(loc)
                # print(found[0].replace('{}&&', '').strip().rstrip("')"))
                m = json.loads(found[0].replace('{}&&', '').strip().rstrip("')"))['payload']['rootDefaults']['market']
                id = json.loads(found[0].replace('{}&&', '').strip().rstrip("')"))['payload']['rootDefaults']['region_id']
                sf_v = json.loads(found[0].replace('{}&&', '').strip().rstrip("')"))['payload']['rootDefaults']['sf']
                sf = ','.join(str(x) for x in sf_v)
                status = json.loads(found[0].replace('{}&&', '').strip().rstrip("')"))['payload']['rootDefaults']['status']
                # print(status)
                # print(sf)
                # print(m)
                # print(id)
                break
        link = '/stingray/api/gis?al=1&market=' +str(m) +'&num_homes=350&ord=redfin-recommended-asc&page_number=1&region_id=' + str(id) + '&region_type=2&sf=' + str(sf)+'&start=0&status='+ str(status)+'&uipt=1,2,3,4,5,6&v=8'
        for k, v in jdata['ReactServerAgent.cache']['dataCache'][link]['res'].items():
            if k == 'text':
                jdata = str(v).replace('{}&&', '').strip()
                jdata = json.loads(jdata)
                # print(jdata['payload']['homes'])
                try:
                    for i in range(0, len(jdata['payload']['homes'])):
                        if str(jdata['payload']['homes'][i]['isRedfin']) == 'False':
                            pass
                        else:
                            print(jdata['payload']['homes'][i]['isRedfin'])
                            redfin.append(jdata['payload']['homes'][i]['isRedfin'])
                            try:
                                avg_price.append(jdata['payload']['searchMedian']['price'])
                            except:
                                avg_price.append(None)
                            try:
                                avg_bed.append(jdata['payload']['searchMedian']['beds'])
                            except:
                                avg_bed.append(None)
                            try:
                                avg_bath.append(jdata['payload']['searchMedian']['baths'])
                            except:
                                avg_bath.append(None)
                            try:
                                avg_sqft.append(jdata['payload']['searchMedian']['sqFt'])
                            except:
                                avg_sqft.append(None)
                            total_home.append(total_homes)
                            # print('i', i)
                            try:
                                # print(jdata['payload']['homes'][i]['streetLine'])
                                house.append(jdata['payload']['homes'][i]['streetLine']['value'])
                                state.append(loc)
                                # print(house)
                            except:
                                house.append(None)
                                state.append(loc)
                                pass
                            try:
                                # print(jdata['payload']['homes'][i]['price'])
                                price.append(jdata['payload']['homes'][i]['price']['value'])
                                # print(price)
                            except:
                                price.append(None)
                            try:
                                # print(jdata['payload']['homes'][i]['sqFt']['value'])
                                sqft.append(jdata['payload']['homes'][i]['sqFt']['value'])
                                # print(sqft)
                            except:
                                sqft.append(None)
                                # print('not available')
                            try:
                                beds.append(jdata['payload']['homes'][i]['beds'])
                                # print(beds)
                            except:
                                beds.append(None)
                                # print('not available')
                            try:
                                # print(jdata['payload']['homes'][i])
                                baths.append(jdata['payload']['homes'][i]['baths'])
                                # print(baths)
                            except:
                                baths.append(None)
                                # print('not available')
                except Exception as e:
                    print(e)
                break
    except Exception as e:
        print(loc)
        print(e)
    print('State', len(state))
    print('House', len(house))
    print('Beds', len(beds))
    print('Baths',len(baths))
    print('sqft', len(sqft))
    print('redfin', len(redfin))
    print('avg_price', len(avg_price))
    print('avg_bed', len(avg_bed))
    print('avg_bath', len(avg_bath))
    print('avg_sqft', len(avg_sqft))
    print('total_home', len(total_home))
    print('#######################')
df = pd.DataFrame({'State': state, 'Price': price, 'House': house, 'Bedroom': beds, 'Bathroom': baths, 'Sqft': sqft,
               'Redfin_House': redfin, 'Average_Price': avg_price, 'Average_Bath': avg_bath, 'Average_Bed':avg_bed,
               'Average_sqFt':avg_sqft, 'Total_Homes':total_home})
df1 = pd.DataFrame({'Not_Found':not_found}).to_csv('Notfound.csv', index=False)
df.to_csv('RedfinAlabama.csv', index=False)
