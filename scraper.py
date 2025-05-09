# Basketball Reference Top 25 Leaders Scraper

import requests
from bs4 import BeautifulSoup
import pandas as pd

# This part of the code defines the base URL for the NBA 2025 leaders page on Basketball Reference.
# It sets up the target webpage we will be scraping data from.
BASE_URL = "https://www.basketball-reference.com/leagues/NBA_2025_leaders.html"

# This part of the code creates a dictionary mapping user-friendly statistic names to their respective HTML element IDs on the webpage.
# It helps in identifying which section of the page to scrape based on user selection.
STAT_MAP = {
    "points per game": "leaders_pts_per_g",
    "rebounds per game": "leaders_trb_per_g",
    "assists per game": "leaders_ast_per_g",
    "steals per game": "leaders_stl_per_g",
    "blocks per game": "leaders_blk_per_g",
    "turnovers per game": "leaders_tov_per_g",
    "field goal percentage": "leaders_fg_pct",
    "3 point percentage": "leaders_fg3_pct",
    "free throw percentage": "leaders_ft_pct"
}

def fetch_page(url):
    """
    This part of the code defines a function to fetch the webpage content using the requests library.
    It sends an HTTP GET request to the specified URL and returns the HTML content if successful.
    If there's an error, it prints a message and returns None to indicate failure.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching the page: {e}")
        return None

def parse_leaders(html_content, stat_id):
    """
    This part of the code defines a function to parse the HTML content and extract leader data for a specific statistic.
    It uses BeautifulSoup to navigate the HTML structure, finds the table with the given stat_id,
    and extracts player names and their corresponding statistic values into a list of dictionaries.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    leaders_table = soup.find('div', id=stat_id)
    leaders = []
    
    if leaders_table:
        rows = leaders_table.find_all('tr')[1:16]  # Skip header row, limit to top 15
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 2:
                player = cols[1].text.strip()
                value = cols[2].text.strip()
                leaders.append({'Player': player, 'Value': value})
    return leaders

def display_leaders(leaders, stat):
    """
    This part of the code defines a function to display the scraped data in a formatted table using pandas.
    It converts the list of dictionaries into a DataFrame and prints it with a title based on the selected statistic.
    If no data is available, it informs the user.
    """
    if leaders:
        df = pd.DataFrame(leaders)
        df.index += 1  # Start index from 1 for ranking
        print(f"\nTop 15 Leaders for {stat.title()}:\n")
        print(df.to_string())
    else:
        print(f"No data available for {stat}.")

def main():
    """
    This part of the code defines the main function that orchestrates the scraping process.
    It fetches the webpage, presents a menu for statistic selection to the user, and based on the input,
    it calls functions to parse and display the data for the chosen statistic. It includes error handling for invalid inputs
    and allows the user to exit the program.
    """
    html_content = fetch_page(BASE_URL)
    if not html_content:
        return

    while True:
        print("\nSelect a statistic to view the top 15 leaders:")
        for i, stat in enumerate(STAT_MAP.keys(), 1):
            print(f"{i}. {stat.title()}")
        print(f"{len(STAT_MAP) + 1}. Exit")
        
        try:
            choice = int(input("\nEnter your choice (1-10): "))
            if choice == len(STAT_MAP) + 1:
                print("Exiting program.")
                break
            if 1 <= choice <= len(STAT_MAP):
                selected_stat = list(STAT_MAP.keys())[choice - 1]
                stat_id = STAT_MAP[selected_stat]
                leaders = parse_leaders(html_content, stat_id)
                display_leaders(leaders, selected_stat)
            else:
                print("Invalid choice. Please select a number between 1 and 10.")
        except ValueError:
            print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    """
    This part of the code checks if the script is being run directly (not imported as a module).
    If so, it calls the main function to start the program execution.
    """
    main() 