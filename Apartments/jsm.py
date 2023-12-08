from bs4 import BeautifulSoup
from public import Apartment, ApartmentScraper


class JSM(ApartmentScraper):
    def parse_data(self):
        # Set base URL for the JSM website
        self.base_url = 'https://jsmliving.com'
        apartments = []

        # Fetch the webpage content
        page_content = self.session.get(self.url).text
        soup = BeautifulSoup(page_content, 'html.parser')

        # Find all articles with the specified role attribute
        articles = soup.find_all('article', role='article')

        for article in articles:
            apartment_data = self.extract_apartment_data(article)
            if apartment_data:
                apartments.append(Apartment(*apartment_data))

        return apartments

    def extract_apartment_data(self, article):
        """Extracts apartment data from an article element."""
        address = article.find('a', hreflang='en').text.strip()
        link = self.base_url + article.find('a', class_='call-to-action')['href']

        rent_text = article.find('div', class_='unit__card-rent').text
        rent = self.parse_rent(rent_text)
        if rent is None:
            return None

        bedrooms, is_studio = self.parse_bedrooms(article)
        bathrooms = self.parse_bathrooms(article)
        available_date = '2024-08-01'  # Default available date

        return address, rent, bedrooms, bathrooms, link, available_date, self.agency_name, is_studio

    def parse_rent(self, rent_text):
        """Parse rent from the given text, returns None if no units are available."""
        if 'No Units Available' in rent_text:
            return None
        rent = rent_text.split('RENT:')[1].split('-')[-1].replace('$', '').strip()
        return int(rent)

    def parse_bedrooms(self, article):
        """Parse the number of bedrooms and determine if it's a studio."""
        bedrooms_text = article.find('div', class_='unit__card-bedrooms').find('p').text
        bedrooms = int(bedrooms_text.split(' ')[0])
        is_studio = bedrooms == 0
        if is_studio:
            bedrooms = 1
        return bedrooms, is_studio

    def parse_bathrooms(self, article):
        """Parse the number of bathrooms."""
        bathrooms_text = article.find('div', class_='unit__card-bathrooms').find('p').text
        return float(bathrooms_text.split(' ')[0])

"""
# Usage
scraper = JSM('https://jsmliving.com/search-available-units', 'JSM')
apartments = scraper.parse_data()
for apt in apartments:
    print(apt.address, apt.price, apt.bedrooms, apt.bathrooms, apt.link, apt.available_date, apt.agency_name, apt.is_studio)
"""


