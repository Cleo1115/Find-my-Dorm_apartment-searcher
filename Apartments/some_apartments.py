from bailey import Bailey
from green_street import Green_Street
from jsj import JSJ
from jsm import JSM

def combine_apartment_lists(scrapers):
    """
    Combines apartment listings from a list of scraper instances.
    Keeps only one record per apartment name.

    Args:
        scrapers (list): A list of scraper instances, each having a 'parse_data' method.

    Returns:
        list[str]: A combined list of formatted string representations of Apartment objects from all scrapers,
                   with duplicates removed based on apartment name.
    """
    combined_apartments = {}
    for scraper in scrapers:
        # Ensure the scraper has a 'parse_data' method
        if hasattr(scraper, 'parse_data') and callable(getattr(scraper, 'parse_data')):
            apartments = scraper.parse_data()
            for apt in apartments:
                # Format each Apartment object as a string
                formatted_apt = f"{apt.address}, {apt.price}, {apt.bedrooms}, {apt.bathrooms}, {apt.link}, {apt.available_date}, {apt.agency_name}, {apt.is_studio}"
                # Use apartment address as the key to avoid duplicates
                combined_apartments[apt.address] = formatted_apt
        else:
            print(f"Scraper {type(scraper).__name__} does not have a parse_data method.")

    # Return the values of the dictionary, which are the unique listings
    return list(combined_apartments.values())


# In[55]:


def get_some_apt():
    bailey_scraper = Bailey('http://baileyapartments.com/amenities/', 'Bailey')
    green_street_scraper = Green_Street('https://www.greenstrealty.com/modules/extended/propertySearch', 'Green Street')
    jsj_scraper = JSJ('https://jsjmanagement.com/on-campus/listing/', 'JSJ')
    jsm_scraper = JSM('https://jsmliving.com/search-available-units', 'JSM')

    # List of scrapers to combine
    scrapers_to_combine = [bailey_scraper, green_street_scraper, jsj_scraper, jsm_scraper]

    # Combine listings
    combined_list = combine_apartment_lists(scrapers_to_combine)
    some_apartments = []
    for data in combined_list:
        data = data.split(',')
        address = data[0]
        price = float(data[1].strip(''))
        bedroom = int(data[2].strip(''))
        bathroom = float(data[3].strip(''))
        link = data[4]
        availability = data[5].strip(' ')
        name = data[6].strip(' ')
        is_studio = eval(data[-1])
        some_apartments.append([address, price, bedroom, bathroom, link, availability, name, is_studio])
    return some_apartments

