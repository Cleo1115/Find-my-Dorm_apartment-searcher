import json
from bs4 import BeautifulSoup
from public import Apartment, ApartmentScraper


class JSJ(ApartmentScraper):
    """
    A class to scrape apartment data from JSJ Management's website.
    Inherits from the ApartmentScraper class defined in public.py.
    """

    def process_address(self, address):
        """
        Process the address string to modify its format.

        >>> jsj = JSJ('https://jsjmanagement.com/on-campus/listing/', 'JSJ')
        >>> jsj.process_address("123 Main Street")
        '123 Main St'
        >>> jsj.process_address("456 Elm Avenue")
        '456 Elm Ave'
        >>> jsj.process_address("789 Oak Street-1")
        '789 Oak St'
        >>> jsj.process_address("101 Pine Street Apartment 5")
        '101 Pine St'
        >>> jsj.process_address("202 Birch Road")
        '202 Birch Road'
        """
        address_parts = address.split()
        processed_parts = []

        # Iterate over address parts to process each word
        for part in address_parts:
            if part in ['Street', 'St', 'Street-1']:
                processed_parts.append('St')
                break
            elif part in ['Avenue', 'Ave']:
                processed_parts.append('Ave')
                break
            else:
                processed_parts.append(part)

        return ' '.join(processed_parts)

    def parse_data(self):
        """
        Fetch and process apartment data from JSJ Management's website.

        This method retrieves apartment listings, processes each listing to extract relevant information,
        and returns them as a list of Apartment objects.

        Returns:
            list[Apartment]: A list of Apartment objects containing the scraped data.
        """
        apartments = []
        res = self.session.get(self.url).text
        soup = BeautifulSoup(res, 'html.parser')

        # Extract the JSON data from the webpage's script tag
        script = soup.find('script', type='application/json', id='search-form-config').text
        data = json.loads(script)

        # Iterate over each apartment entry in the JSON data
        for apartment in data['properties']['data']:
            bedrooms = int(apartment['bedrooms'])
            is_studio = True if bedrooms == 0 else False
            bedrooms = 1 if bedrooms == 0 else bedrooms
            bathrooms = float(apartment['bathrooms'])
            address = self.process_address(apartment['address_1'])
            link = 'https://jsjmanagement.com/on-campus/listing/' + apartment['slug']
            price = float(apartment['price'].replace(',', ''))
            avail_date = apartment['avail_date'][-4:]+'-'+apartment['avail_date'][:-5]

            # Create an Apartment object for each entry and add it to the list
            apartments.append(Apartment(address, price, bedrooms, bathrooms, link, avail_date, self.agency_name, is_studio))
        return apartments


if __name__ == "__main__":
    import doctest
    doctest.testmod()


"""
# Usage
scraper = JSJ('https://jsjmanagement.com/on-campus/listing/', 'JSJ')
apartments = scraper.parse_data()
for apt in apartments:
    print(apt.address, apt.price, apt.bedrooms, apt.bathrooms, apt.link, apt.available_date, apt.agency_name, apt.is_studio)
"""



