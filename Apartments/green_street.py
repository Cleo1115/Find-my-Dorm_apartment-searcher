from bs4 import BeautifulSoup
from public import Apartment, ApartmentScraper


class Green_Street(ApartmentScraper):
    terms = ['Available August 2024']

    def parse_data(self):
        """Fetch and parse apartment listings."""
        response = self.session.post(
            self.url, headers={'content-type': 'application/x-www-form-urlencoded'},
            data={'query': '/'.join(self.terms), 'show_map': False}
        ).text
        soup = BeautifulSoup(response, 'html.parser')
        return [self._parse_div(div) for div in soup.find_all('div', class_='property-item-data') if self._parse_div(div)]

    def _parse_div(self, div):
        """Parse information from a property div."""
        try:
            address = self._extract_address(div)
            link = self._get_link(div)
            for kind in div.find_all('div', class_='property-item-info'):
                beds, baths, rent, is_studio = self._parse_kind(kind)
                return Apartment(address, rent, beds, baths, link, '2024-08-01', self.agency_name, is_studio)
        except (ValueError, AttributeError, TypeError):
            return None  # Skip the div if any parsing errors occur

    def _extract_address(self, div):
        """Extracts the address from a div element and removes the city name."""
        address_div = div.find('div', class_='property-item-title')
        # Strip the city names from the address
        address = address_div.get_text(strip=True).split(',')[0].strip().replace('Champaign  IL', '').replace('Urbana  IL', '')
        return address

    def _get_link(self, div):
        """Extract link to property."""
        a_tag = div.find('a', class_='cms-btn cms-btn-primary')
        return f"https://www.greenstrealty.com{a_tag['href']}" if a_tag else None

    def _parse_kind(self, kind):
        """Extract details like beds, baths, and price from info kind."""
        raw_bed_text = kind.find('div', class_='beds').get_text(strip=True).lower().replace('+', '')
        beds = 1 if 'studio' in raw_bed_text else int(raw_bed_text.split(' ')[0])
        baths = float(kind.find('div', class_='baths').get_text(strip=True).split(' ')[0])
        price_text = kind.find('div', class_='price').get_text(strip=True)
        rent = int(price_text.split('/')[0].replace('$', '').replace(',', '')) * (beds if '/Bed' in price_text else 1)
        is_studio = 'studio' in raw_bed_text
        return beds, baths, rent, is_studio


"""
# Usage
scraper = Green_Street('https://www.greenstrealty.com/modules/extended/propertySearch', 'Green Street')
apartments = scraper.parse_data()
for apt in apartments:
    print(apt.address, apt.price, apt.bedrooms, apt.bathrooms, apt.link, apt.available_date, apt.agency_name, apt.is_studio)
"""



