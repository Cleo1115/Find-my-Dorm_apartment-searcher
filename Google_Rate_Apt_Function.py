import googlemaps
import matplotlib.pyplot as plt
import pandas as pd


def combine_apartment_lists(scrapers):
    """
    Combines apartment listings from a list of scraper instances.
    Keeps only one record per apartment name.

    Args: scrapers (list): A list of scraper instances, each having a 'parse_data' method.

    Returns: list[str]: A combined list of formatted string representations of Apartment objects from all scrapers,
                   with duplicates removed based on apartment name.
    """
    combined_apartments = {}
    for scraper in scrapers:
        # Ensure the scraper has a 'parse_data' method
        if hasattr(scraper, 'parse_data') and callable(getattr(scraper, 'parse_data')):
            apartments = scraper.parse_data()
            for apt in apartments:
                # Format each Apartment object as a string
                formatted_apt = (f"{apt.address}, {apt.price}, {apt.bedrooms}, {apt.bathrooms}, {apt.link}, "
                                 f"{apt.available_date}, {apt.agency_name}, {apt.is_studio}")
                # Use apartment address as the key to avoid duplicates
                combined_apartments[apt.address] = formatted_apt
        else:
            print(f"Scraper {type(scraper).__name__} does not have a parse_data method.")

    # Return the values of the dictionary, which are the unique listings
    return list(combined_apartments.values())


# Initialize Google Maps client
gmaps = googlemaps.Client(key='')  # input your Google API


def get_place_rating(address):
    """
    Fetches the Google Maps place rating for a given address.

    Args: address (str): The address to search for.

    Returns: str: The rating as a string, or 'null' if not available.
    """
    try:
        place_details = gmaps.places(address)
        if 'results' in place_details and place_details['results']:
            return str(place_details['results'][0].get('rating', 'null'))
        else:
            return 'null'
    except Exception as e:
        print(f"Error fetching place details: {e}")
        return 'null'


def append_ratings_to_listings(combined_list):
    """
    Appends Google Maps ratings to each listing in combined listings.
    Excludes listings with a rating of '0' or 'null'.

    Args: combined_list (list of str): The list of apartment listings.

    Returns: list of str: The updated list with ratings appended, excluding '0' or 'null' ratings.
    """
    updated_list = []

    for listing in combined_list:
        address = listing.split()[0]  # Assuming the address is the first element in the listing
        rating = get_place_rating(address)

        # Skip adding the rating if it's '0' or 'null'
        if rating not in ('0', 'null'):
            updated_list.append(f"{listing}, {rating}")

    return updated_list


def create_apartment_ranking_table(updated_list):
    """
        Generates and displays a table ranking apartments.

        Parameters:
        updated_list (list of str): List of comma-separated strings with apartment details.

        The function processes this list into a DataFrame, then visualizes it as a table,
        sorted by the 'Rating' column. It shows columns for 'Apartment Name', 'Agency Name',
        'Studio', and 'Rating'.

        Example:
        create_apartment_ranking_table(["707 S. Sixth, 1600, 2, 1.0,
        https://jsmliving.com/node/130895?bedrooms=2&unittype=707S-2-1-C, 08-01-2024, JSM, False, 4", ...])
        """

    # Convert the list to a DataFrame
    columns = [
        'Apartment Name', 'Price', 'Bedrooms', 'Bathrooms', 'Link',
        'Available Date', 'Agency Name', 'Studio', 'Rating'
    ]
    df = pd.DataFrame([item.split(', ') for item in updated_list], columns=columns)

    # Correct 'Studio' column
    df['Studio'] = df['Studio'].replace({'False': 'No', 'True': 'Yes'})

    # Remove unwanted columns
    df = df[['Apartment Name', 'Agency Name', 'Studio', 'Rating']]

    # Sort by 'Rating' column
    df.sort_values('Rating', ascending=False, inplace=True)

    # Calculate the figure height dynamically based on the number of rows
    figsize_height = max(4, 0.4 * len(df))  # Increase the height for better visibility

    # Create the figure with the dynamically calculated height
    fig, ax = plt.subplots(figsize=(10, figsize_height))  # Increase the figure width for better spacing

    # Hide the axes
    ax.axis('off')

    # Create the table with more space allocated for each row
    table = ax.table(cellText=df.values,
                     colLabels=df.columns,
                     loc='center',
                     cellLoc='center',
                     colWidths=[0.2 for _ in df.columns])  # Adjust column widths for better text fit

    # Set the fontsize for the table
    table.auto_set_font_size(False)
    table.set_fontsize(14)  # Increase the fontsize for better readability

    # Adjust the scale of the table cells
    table.scale(1.2, 2)  # Increase the height of cells to prevent text overflow

    # Adjust layout to make room for the title regardless of the number of entries
    fig.tight_layout(pad=3.0)  # Add padding to ensure title and table fit within the figure

    # Set the title above the table with adjusted 'y' parameter for positioning
    plt.suptitle('The Ranking of Apartments in Champaign', fontsize=16, weight='bold', y=1.0, va='bottom')

    # Display the plot
    plt.show()

