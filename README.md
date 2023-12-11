# UIUC Housing and Transportation Explorer

## Motivation

Before enrolling at UIUC, upperclassmen recommended choosing housing from specific property management companies. However, the existing rental apps primarily cover nearby houses rather than apartments. To address this inconvenience, we decided to collect a dataset consolidating details of properties from prominent agencies near UIUC. This dataset allows users to explore and select desirable housing based on various criteria.

## Overview

1. **Web Scraping Apartments:**
   - The project involves web scraping official websites of major agencies near UIUC to gather apartment details such as pricing, bedrooms, bathrooms, etc.
   - The collected data is consolidated into a single table for easy comparison and selection.

2. **Dataset Exploration:**
   - Users can explore the consolidated dataset to select their desired housing based on various criteria, including price, bedroom count, and agency.

3. **Transportation Visualization:**
   - Recognizing the importance of transportation, the project includes a visualization of nearby bus stops. Public transportation is crucial for students, especially those without cars.

## Getting Started

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/uiuc-housing-transportation-explorer.git
   cd uiuc-housing-transportation-explorer
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

Note: Ensure that you have the required modules installed and that the necessary data sources are accessible. Adjust URLs, addresses, and numbers as needed for your specific use case.

Feel free to customize these examples by changing the numbers to fit your criteria for exploring apartments and checking transportation conditions.

## Meet the Team

- **[Cleo1115]:** Web Scraping and Transportation Visualization
- **[Teammate 2 Name]:** Web Scraping and Apartment Ranking

## Future Enhancements

- **User Authentication:**
  - Implement user authentication to provide personalized experiences, such as saving favorite apartments.

- **Dynamic Data Updates:**
  - Incorporate automated mechanisms to update the dataset regularly, ensuring information remains accurate.

- **Interactive Maps:**
  - Enhance the transportation visualization with interactive maps for a more immersive experience.

**Happy apartment hunting!**

