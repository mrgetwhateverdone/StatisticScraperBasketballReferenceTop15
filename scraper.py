# Basketball Reference Top 15 Leaders Scraper

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import sys
import datetime
import time
from urllib.error import URLError, HTTPError
import logging

# This part of the code sets up logging configuration for tracking errors and important events.
# It helps in debugging and maintaining the application.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scraper.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("basketball_scraper")

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

# This part of the code creates a directory to store CSV files if it doesn't already exist.
# It organizes the data output files in a structured manner.
def create_output_directory():
    """Create directory for storing CSV outputs if it doesn't exist."""
    os.makedirs('data', exist_ok=True)
    logger.info("Created output directory if it didn't exist.")

# This part of the code implements a function to fetch data from the Basketball Reference website.
# It includes error handling for various network issues and retries on temporary failures.
def fetch_data(url, max_retries=3, delay=2):
    """Fetch data from the specified URL with retry mechanism."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    for attempt in range(max_retries):
        try:
            logger.info(f"Fetching data from {url}, attempt {attempt+1}/{max_retries}")
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()  # Raise exception for 4XX/5XX responses
            return response.text
        except requests.exceptions.RequestException as e:
            logger.warning(f"Request failed: {e}")
            if attempt < max_retries - 1:
                wait_time = delay * (attempt + 1)  # Exponential backoff
                logger.info(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                logger.error(f"Failed to fetch data after {max_retries} attempts.")
                raise

# This part of the code parses the HTML content to extract the relevant statistics table.
# It converts the raw HTML into structured data that can be analyzed.
def parse_data(html_content, stat_id):
    """Parse HTML content and extract the relevant statistics table."""
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.find('div', {'id': stat_id})
        
        if not table:
            logger.error(f"Could not find table with ID: {stat_id}")
            return None
            
        players = []
        teams = []
        values = []
        
        rows = table.find_all('tr')[1:16]  # Top 15 players, skipping header row
        
        for row in rows:
            player_cell = row.find('td', {'class': 'who'})
            if player_cell:
                # Extract just the player name without team info
                player_name = player_cell.find('a').text.strip() if player_cell.find('a') else ""
                
                # Extract team abbreviation from the text
                team_span = player_cell.find('span', {'class': 'desc'})
                if team_span:
                    team_text = team_span.text.strip()
                    # The text is in format like "(PHO)", so we extract just the team code
                    team_abbr = team_text.strip('()') if team_text else ""
                else:
                    team_abbr = ""
                
                value_cell = row.find('td', {'class': 'value'})
                value = float(value_cell.text.strip()) if value_cell else None
                
                players.append(player_name)
                teams.append(team_abbr)
                values.append(value)
        
        return pd.DataFrame({
            'Player': players,
            'Team': teams,
            'Value': values
        })
    except Exception as e:
        logger.error(f"Error parsing HTML: {e}")
        return None

# This part of the code saves the extracted data to a CSV file for future use.
# It provides data persistence and allows for easy sharing or further analysis.
def save_to_csv(df, stat_name):
    """Save the dataframe to a CSV file."""
    if df is None or df.empty:
        logger.warning("No data to save to CSV.")
        return None
    
    # Create a valid filename from the stat name
    filename = stat_name.replace(" ", "_").lower()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = f"data/{filename}_{timestamp}.csv"
    
    try:
        df.to_csv(filepath, index=False)
        logger.info(f"Data saved to {filepath}")
        return filepath
    except Exception as e:
        logger.error(f"Error saving CSV: {e}")
        return None

# This part of the code combines all the functions to scrape a specific statistic.
# It orchestrates the data retrieval, processing, and storage process.
def scrape_statistic(stat_name):
    """Scrape data for the specified statistic and save to CSV."""
    if stat_name.lower() not in STAT_MAP:
        logger.error(f"Invalid statistic name: {stat_name}")
        return None, None
    
    stat_id = STAT_MAP[stat_name.lower()]
    
    try:
        html_content = fetch_data(BASE_URL)
        df = parse_data(html_content, stat_id)
        
        if df is not None and not df.empty:
            # Rename Value column to the actual statistic name
            df = df.rename(columns={'Value': stat_name.title()})
            
            csv_path = save_to_csv(df, stat_name)
            
            return df, csv_path
        else:
            logger.warning(f"No data found for {stat_name}")
            return None, None
    except Exception as e:
        logger.error(f"Error scraping {stat_name}: {e}")
        return None, None

# This part of the code displays available statistics to the user when prompted.
# It helps users understand their options and make valid selections.
def display_available_stats():
    """Display the available statistics that can be scraped."""
    print("\nAvailable Statistics:")
    for i, stat in enumerate(sorted(STAT_MAP.keys()), 1):
        print(f"{i}. {stat.title()}")

# This part of the code runs the main program loop, collecting user input and displaying results.
# It creates an interactive interface for users to select statistics to view.
def main():
    """Main function to run the scraper."""
    try:
        create_output_directory()
        
        print("Basketball Reference Top 15 Leaders Scraper")
        print("===========================================")
        
        while True:
            display_available_stats()
            
            choice = input("\nWhat statistic would you like to see? (type 'quit' to exit): ").strip().lower()
            
            if choice == 'quit':
                print("Exiting program. Goodbye!")
                break
                
            # Handle numeric input (convert to stat name)
            if choice.isdigit():
                stats_list = sorted(STAT_MAP.keys())
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(stats_list):
                    choice = stats_list[choice_idx]
                else:
                    print(f"Invalid choice. Please enter a number between 1 and {len(stats_list)}.")
                    continue
            
            if choice in STAT_MAP:
                print(f"\nFetching top 15 leaders for {choice}...")
                
                try:
                    df, csv_path = scrape_statistic(choice)
                    
                    if df is not None:
                        print(f"\nTop 15 {choice.title()} Leaders:")
                        print("===============================")
                        
                        # Format the output for better readability
                        for i, (_, row) in enumerate(df.iterrows(), 1):
                            stat_value = row[choice.title()]
                            if "percentage" in choice:
                                formatted_value = f"{stat_value:.1f}%"
                            else:
                                formatted_value = f"{stat_value:.1f}"
                                
                            print(f"{i}. {row['Player']} ({row['Team']}): {formatted_value}")
                        
                        if csv_path:
                            print(f"\nData saved to: {csv_path}")
                    else:
                        print(f"Could not retrieve data for {choice}.")
                        
                except Exception as e:
                    print(f"An error occurred: {e}")
            else:
                print("Invalid choice. Please select from the available statistics.")
            
            print("\n" + "-" * 50)
    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting gracefully.")
    except Exception as e:
        logger.critical(f"Unhandled exception: {e}")
        print(f"An unexpected error occurred: {e}")
    finally:
        print("Thank you for using the Basketball Reference Scraper!")

# This part of the code ensures the script runs as a standalone program when executed directly.
# It's the entry point for the application.
if __name__ == "__main__":
    main() 