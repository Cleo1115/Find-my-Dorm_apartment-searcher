from bs4 import BeautifulSoup
import re
import requests

def get_MHM(url):
    #url = 'https://www.mhmproperties.com/apartments/?_sft_types=apartments'
    session = requests.session()
    req_header = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',}
    name = 'MHM'
    res = session.get(url,headers = req_header).text
    soup = BeautifulSoup(res, 'html.parser')
    units = soup.find_all('div', class_='propgridc')
    Dorms = []
    for unit in units:
        link = unit.find('a')['href']
        address = unit.find('h2').text
        items = unit.find_all('p', class_='ppricebox')
        is_studio = False
        for item in items:
            item = item.text 
            #1 Bed format:1 Bed: 2024-2025  LEASED!
            if int(item[0][0]) == 1:
                bedroom = 1
                bathroom = 1
                is_studio = True
                if item[-7:] == 'LEASED!':
                    availability = False
                    price = 'Not Available'
                
            #other format is 2 Bed/2 Bath: 2024-2025  LEASED!
            else:
                item = item.split("/")
                #['2 Bed', '2 Bath: 2024-2025  LEASED!']
                bedroom = int(item[0][0].strip(' '))
                bathroom = int(item[1].strip(' ')[0])
                last_letters = item[-1][-7:].strip(' ')
                #There are lots of typo on mhmproperties website
                if last_letters == 'LEASED!' or last_letters == 'LSESED!' or last_letters == 'LEASED':
                    availability = False
                    price = 'Not Available'
                
                else:
                    availability = '2024-2025'
                    price = item[1].split(':')[1].strip(' ')
                    #price = int(item.strip('$'))      
            Dorms.append([address, price, bedroom, bathroom, link, availability, name, is_studio])
    return Dorms

