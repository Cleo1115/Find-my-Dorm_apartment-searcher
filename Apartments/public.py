import requests


class Apartment:
    def __init__(self, address, price, bedrooms, bathrooms, link, available_date, agency_name, is_studio):
        self.address = address
        self.price = price
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.link = link
        self.available_date = available_date
        self.agency_name = agency_name
        self.is_studio = is_studio

    def __str__(self):
        bed_bath_info = 'Studio' if self.is_studio else f'{self.bedrooms} beds/{self.bathrooms} baths'
        return f"<Apartment ${self.price}/month {bed_bath_info} {self.available_date} {self.agency_name}>"

    __repr__ = __str__


class ApartmentScraper:
    def __init__(self, url, agency_name):
        self.url = url
        self.agency_name = agency_name
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'})

    def fetch_data(self):
        response = self.session.get(self.url)
        return response.text