import requests
from bs4 import BeautifulSoup as bs
import pandas as pd



def next_page(soup):
   if not soup.find('a',{'class':'internalLink nuxt-link-exact-active nuxt-link-active no-button pagination-nav text disabled'}) and soup.find('div',{'class':'pagination clickable'}) :
       next_link=page.find('a',{'class':'internalLink nuxt-link-active no-button pagination-nav text active'})
       if(next_link):
           return next_link.get('href')
       else:
           next_link = page.find('a', {'class': 'internalLink no-button pagination-nav text active'})
           return next_link.get('href')
   else:
       return False



def make_new_path(name):
    if (name):
        return "https://www.yad2.co.il/" + name
    else:
         return False


def scrap_info(soup):
    dico={'city':[],'price':[],'size':[],'rooms':[],'floor':[]}
    items=soup.find_all('div',{'class':'feeditem'})
    for item in items:
        if (item.find('div',{'class':'data rooms-item'})):
            dico['rooms'].append(item.find('div',{'class':'data rooms-item'}).text)
        if (item.find('div',{'class':'data floor-item'})):
            dico['floor'].append(item.find('div',{'class':'data floor-item'}).text)
        if (item.find('div',{'class':'data SquareMeter-item'})):
         dico['size'].append(item.find('div',{'class':'data SquareMeter-item'}).text)
        if(item.find('div', {'data-test-id': 'item_price'})):
            dico['price'].append((((item.find('div', {'data-test-id': 'item_price'}).text).split('\n')[1]).strip()))
        if(item.find('span', {'class': 'subtitle'})):
            dico['city'].append((item.find('span', {'class': 'subtitle'}).text))
    return dico


def select_parmaters():
    url='https://www.yad2.co.il/realestate/forsale?propertyGroup=apartments&'
    city=int(input('Chooese between  Tel-Aviv-1, haifa-2, Bat-Yam-3, jeruslam any other'))
    if(city==1):
        url+='city=5000'
    elif(city==2):
        url += 'city=4000'
    elif(city==3):
        url += 'city=6200'
    else:
        url += 'city=3000'
    rooms_start = int(input('room start'))
    rooms_end = int(input('rooms end'))
    url+=f'&rooms={rooms_start}-{rooms_end}'
    Price_until=int(input('Start price?'))
    end_price=int(input('end price'))
    url += f'&price={Price_until}-{end_price}'
    return url

headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
         'Referer':'https://www.yad2.co.il',
         'DNT':'1',
         'Accept-Language':'he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7'}



with requests.session() as session:
    url=select_parmaters()
    respones=session.get(url,headers=headers)
    page=bs(respones.text,'html.parser')
    dict1=scrap_info(page)
    while(next_page(page)):
       respones = session.get(make_new_path(next_page(page)),headers=headers)
       page = bs(respones.text, 'html.parser')
       info=scrap_info(page)
       dict1['city'].extend(info['city'])
       dict1['price'].extend(info['price'])
       dict1['size'].extend(info['size'])
       dict1['rooms'].extend(info['rooms'])
       dict1['floor'].extend(info['floor'])
    df=pd.DataFrame(dict1)
    df.to_csv('data.csv')



