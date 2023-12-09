from bs4 import BeautifulSoup
import re
import requests

def get_wampler(url):
    #url = 'https://wamplerapartments.com/our-properties/'
    session = requests.session()
    req_header = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',}
    name ='Wampler'
    re = session.post(url,headers=req_header).text
    soup = BeautifulSoup(re, 'html.parser')
    Dorms = []
    for a in soup.find_all('a', class_='more-link'):
        link = a['href']
        res = session.get(link).text
        soup = BeautifulSoup(res, 'html.parser')
        address = soup.find('h3', class_='listing-address').text.strip(',Illinois').strip('/ Urb')
        lookup = {}
        for div in soup.find_all('div', class_='single-detail'):
            spans = div.find_all('span')
            lookup[spans[0].text.strip()] = spans[1].text.strip()
        if lookup['Bedrooms:'] == 'Studio':
            bedroom = 1
            is_studio = True
        else:
            bedroom = int(lookup['Bedrooms:'].split(' ')[0])
            is_studio = False
        bathroom = float(lookup['Bathrooms:'])
        available = lookup['Rent:'].upper() != 'LEASED'
        if available:
            availability = '2024-08'
            if lookup['Rent:'][0].isalpha():
                price = 'Not published'
            else:
                price = float(lookup['Rent:'].replace('$', '').replace(',', '').split('-')[-1].strip('/mo'))
        else:
            available_date = None
            price = 0
            continue
        Dorms.append([address, price, bedroom, bathroom, link, availability, name, is_studio])
    return Dorms

