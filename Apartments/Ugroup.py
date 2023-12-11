from bs4 import BeautifulSoup
import re
import requests

def get_ugroup(url):
    """
        Scrape information about dorms or properties listed on the Ugroup website.

        Parameters:
        - url (str): The URL of the Ugroup website's building list.

        Returns:
        - list: A list of lists, where each inner list represents information about a dorm.

        Example:
        ```python
        dorms_info = get_ugroup('https://ugroupcu.com/building-list/')
        for dorm in dorms_info:
            print(dorm)
        ```
    """

    session = requests.session()
    req_header = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',}
    name = 'Ugroup'
    re = session.get(url,headers = req_header).text
    soup = BeautifulSoup(re, 'html.parser')
    Dorms = []
    for a in soup.find_all('a', class_='more_detail'):
        if not a.has_attr('href'):
            continue
        link = a['href']
        res = session.get(link,headers = req_header).text
        soup = BeautifulSoup(res, 'html.parser')
        #Some links on the website is invalid, eg. https://ugroupcu.com/property-details/104-e-armory-immediate-move-in-and-january-2024
        if soup.find('div', class_='prop_detil_rgt') is None:
            continue   
        address = soup.find('div', class_='prop_detil_rgt').find('h2').text
        if soup.find('div', class_='prop_detil_rgt') is None:
            continue   
        kinds = soup.find_all('div', class_='tab-content_in_wrapp tab-cntnt_wrap_btm')
        for kind in kinds:
            lookup = {}
            for li in kind.find('div', class_='tab-content_in_rgt').find_all('li'):
                divs = li.find_all('div')
                lookup[divs[0].text.strip()] = divs[1].text.strip()
                price = float(lookup['Price per month:'].replace('$', '').replace(',', ''))
                bathroom = float(lookup.get('Bathrooms:', 0))
                availability = str(lookup.get('Availability:')).lower()
                bedrooms_text = kind.find('h4', class_='propert_head').text.strip()
                bedrooms_text = bedrooms_text.strip('Luxury').strip()
                if 'studio' in bedrooms_text.lower():
                    is_studio = True
                    bedroom = 1
                else:
                    is_studio = False
                    try :
                        bedroom = int(bedrooms_text[0])
                    except ValueError:
                        bedroom = 'Not published'
        
            Dorms.append([address, price, bedroom, bathroom, link, availability, name, is_studio])
    return Dorms

