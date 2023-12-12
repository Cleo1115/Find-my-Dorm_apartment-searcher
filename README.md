# UIUC Housing and Transportation Explorer

## Motivation

Before enrolling at UIUC, upperclassmen recommended choosing housing from specific property management companies. However, the existing rental apps primarily cover nearby houses rather than apartments. To address this inconvenience, we decided to collect a dataset consolidating details of properties from prominent agencies near UIUC. This dataset allows users to explore and select desirable housing based on various criteria.
![image](https://github.com/Cleo1115/Find-my-Dorm_apartment-searcher/assets/143035786/19de219f-8ac5-4cc4-a11c-30cefa33e528)

## Overview

1. **Web Scraping Apartments:**
   - The project involves web scraping official websites of major agencies near UIUC to gather apartment details such as pricing, bedrooms, bathrooms, etc.
   - The collected data is consolidated into a single table for easy comparison and selection.

2. **Dataset Exploration:**
   - Users can explore the consolidated dataset to select their desired housing based on various criteria, including price, bedroom count, and agency.

3. **Transportation Visualization:**
   - Recognizing the importance of transportation, the project includes a visualization of nearby bus stops. Public transportation is crucial for students, especially those without cars.

4. **Ranking Visualization:**
   - To quickly identify the most popular apartments in Champaign, the final part of the analysis involves integrating additional data from Google Maps and visualizing the rankings.

## Project Packages

This project utilizes several Python packages to perform web scraping, data analysis, visualization, and geocoding. Below is an overview of the key packages and their roles:

### Web Scraping Packages

1. **Beautiful Soup (bs4):**
   - *Description:* Beautiful Soup is used for web scraping purposes, allowing the extraction of data from HTML and XML files.
   - *Role in Project:* Beautiful Soup facilitates the parsing and extraction of relevant information from the HTML structure of property management company websites.

2. **Requests:**
   - *Description:* The Requests library is used for making HTTP requests to retrieve HTML content from web pages.
   - *Role in Project:* Requests is employed to fetch HTML content from property management company websites, enabling subsequent parsing with Beautiful Soup.

### Data Manipulation and Analysis Packages

3. **Pandas:**
   - *Description:* Pandas is a powerful data manipulation and analysis library, providing data structures like DataFrames for efficient data handling.
   - *Role in Project:* Pandas is extensively used to transform scraped data into structured DataFrames, enabling easy analysis and visualization of apartment details.

### Visualization Packages

4. **Folium:**
   - *Description:* Folium is a Python wrapper for Leaflet.js, a leading JavaScript library for interactive maps. Folium simplifies the creation of interactive maps within Python.
   - *Role in Project:* Folium is employed to visualize the geographical locations of apartments and nearby bus stops on an interactive map.

5. **Matplotlib:**
   - *Description:* Matplotlib is a versatile data visualization library in Python, providing functionalities for creating static plots and charts.
   - *Role in Project:* Matplotlib is used to generate static visualizations, such as apartment pricing trends and the apartment ranking table.

6. **Contextily:**
   - *Description:* Contextily is a library that facilitates the integration of basemaps into Matplotlib plots.
   - *Role in Project:* Contextily is used to add a basemap to the static plots, enhancing the geographic context of the visualizations.

### Geocoding and Mapping Packages

7. **Geopy:**
   - *Description:* Geopy is a Python library for geocoding (converting addresses into geographic coordinates) and reverse geocoding (finding addresses from coordinates).
   - *Role in Project:* Geopy is employed for converting apartment addresses into latitude and longitude coordinates for mapping.

8. **OSMnx:**
   - *Description:* OSMnx is a Python library for working with OpenStreetMap (OSM) data. It simplifies the retrieval and analysis of street networks.
   - *Role in Project:* OSMnx is used to retrieve street network data for calculating distances and optimizing bus routes.

### Routing and Optimization Packages

9. **OR-Tools:**
   - *Description:* OR-Tools is an open-source library for combinatorial optimization, providing solutions for routing and scheduling problems.
   - *Role in Project:* OR-Tools is utilized to optimize bus routes, ensuring efficient transportation options for users.

10. **NetworkX:**
    - *Description:* NetworkX is a Python library for the creation, manipulation, and study of complex networks.
    - *Role in Project:* NetworkX is employed for analyzing street networks and optimizing bus routes.

### Google Maps Integration

11. **Google Maps API (via the Google Maps Python Client):**
    - *Description:* The Google Maps API is utilized to fetch place details, including ratings, based on apartment addresses.
    - *Role in Project:* The Google Maps API, accessed through the Google Maps Python Client, provides apartment ratings to enhance user decision-making.

## Getting Started

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Cleo1115/Find-my-Dorm_apartment-searcher.git
   cd Find-my-Dorm_apartment-searcher
   ```
   
2. **Run the :**
   ```bash
   python main.py
   ```
   
3. **Explore the Dataset:**
   Input the requirements of apartments to explore the consolidated dataset and transportation visualizations.

## How to Use in Python Code
1. **Example: Search for apartments with more than 2 bathrooms:**
```python
All_apt[All_apt['Bathroom'] > 2]
```
<img width="979" alt="image" src="https://github.com/Cleo1115/Find-my-Dorm_apartment-searcher/assets/143035786/36cfee48-9bbd-450c-bd65-03c530fc3945">

2. **Example: Search for apartments with rents under 1000:**
```python
All_apt[All_apt['Price'] < 1000]
```
<img width="890" alt="image" src="https://github.com/Cleo1115/Find-my-Dorm_apartment-searcher/assets/143035786/935dcf85-1cff-4e18-a1e8-e565ec859a5d">

3. **Check Transportation Condition:**
```python
bus_map = bus_stops_searcher('501 E. Healey')
```
<img width="827" alt="image" src="https://github.com/Cleo1115/Find-my-Dorm_apartment-searcher/assets/143035786/8b0dba02-6fbd-462e-9ba9-07b0f97a3c95">

4. **Search Apartment Rankings:**
```python
Rated_apt = append_ratings_to_listings(All_apt)
Ranked_apt = create_apartment_ranking_table(Rated_apt)
```

Note: Ensure that you have the required modules installed and that the necessary data sources are accessible. Adjust URLs, addresses, and numbers as needed for your specific use case.

Feel free to customize these examples by changing the numbers to fit your criteria for exploring apartments and checking transportation conditions.

## Project Hypotheses, Conclusions and Findings

### Hypotheses:

1. **Apartment Features and Pricing:**
   - *Scenario:* Different property management companies offer apartments with varying features and pricing structures.
   - *Hypothesis:* Apartments managed by the same company are likely to share similarities in features (e.g., number of bedrooms, bathrooms) and exhibit pricing trends.
   - *Conclusion:* The project's findings align with the hypothesis, confirming that apartments managed by the same company indeed share similarities in features and pricing trends. This insight provides valuable information for students looking for specific features or expecting consistent pricing from a particular property management company.

2. **Budget-Friendly Options:**
   - *Scenario:* Students often have budget constraints and seek affordable housing options.
   - *Hypothesis:* There is a correlation between the number of bedrooms and the rent, allowing the identification of budget-friendly options based on bedroom count.
   - *Conclusion:* The correlation between the number of bedrooms and rent supports the hypothesis, enabling students to identify budget-friendly options based on their desired bedroom count. This finding facilitates informed decision-making for those with financial constraints.

3. **Studio Apartment Demand:**
   - *Scenario:* Some students prefer the simplicity and cost-effectiveness of studio apartments.
   - *Hypothesis:* Studio apartments are in high demand and may have a different pricing trend compared to apartments with multiple bedrooms.
   - *Conclusion:* The limited availability of studio apartments supports the hypothesis of high demand for this housing type. Understanding this demand can guide property management companies in diversifying their offerings to meet student preferences.

### Key Findings:

1. **Apartment Exploration:**
   - Apartments with more than 2 bathrooms are available, providing options for those seeking additional bathroom amenities.
   - Apartments with rents under $1000 are accessible, offering affordable housing choices for budget-conscious individuals.
   - The availability of studio apartments is limited, suggesting a potential gap in meeting the demand for this housing type.

2. **Transportation Conditions:**
   - The transportation map provides a clear visualization of nearby bus stops, aiding users in assessing public transportation accessibility.
   - Bus stops near popular housing areas are well-distributed, contributing to convenient access for residents.

3. **Property Management Companies:**
   - Certain property management companies dominate the market, indicating their influence on the rental landscape.
   - Apartments managed by specific companies consistently exhibit certain features, allowing for informed expectations by prospective tenants.

## Meet the Team

- **[Cleo1115]:** Web Scraping and Transportation Visualization
- **[Moiralala]:** Web Scraping and Apartment Ranking

## Future Enhancements

- **User Authentication:**
  - Implement user authentication to provide personalized experiences, such as saving favorite apartments.

- **Dynamic Data Updates:**
  - Incorporate automated mechanisms to update the dataset regularly, ensuring information remains accurate.

- **Interactive Maps:**
  - Enhance the transportation visualization with interactive maps for a more immersive experience.

**Happy apartment hunting!**

