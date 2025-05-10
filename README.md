# Basketball Reference Top 15 Leaders Scraper

This project is a Python-based web scraper that extracts data from the [Basketball Reference 2024-25 NBA Leaders page](https://www.basketball-reference.com/leagues/NBA_2025_leaders.html). It allows users to view the top 15 leaders for various statistics including points per game, rebounds per game, assists per game, and more.

## Features

- **Data Scraping**: Extracts up-to-date statistics from Basketball Reference
- **Interactive CLI**: Easy-to-use command-line interface
- **Data Export**: Automatically saves statistics to CSV files for further analysis
- **Error Handling**: Robust error handling with retry mechanisms and detailed logging
- **Customizable**: View any of the available statistical categories

## Setup

1. **Install Python**: Ensure you have Python 3.8 or higher installed on your system.
2. **Clone Repository**: Clone or download this repository to your local machine.
3. **Install Dependencies**: Navigate to the project directory and run:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Scraper**: From the project directory, execute the script with:
   ```bash
   python scraper.py
   ```
2. **Select Statistic**: Choose a statistic from the displayed menu.
3. **View Results**: The top 15 leaders for the selected statistic will be displayed.
4. **Data Output**: The scraped data is saved as CSV files in the `data/` directory

## Available Statistics

The scraper supports the following NBA statistical categories:

- Points Per Game
- Rebounds Per Game
- Assists Per Game
- Steals Per Game
- Blocks Per Game
- Turnovers Per Game
- Field Goal Percentage
- 3 Point Percentage
- Free Throw Percentage

## Example Output

```
Basketball Reference Top 15 Leaders Scraper
===========================================

Available Statistics:
1. 3 Point Percentage
2. Assists Per Game
3. Blocks Per Game
4. Field Goal Percentage
5. Free Throw Percentage
6. Points Per Game
7. Rebounds Per Game
8. Steals Per Game
9. Turnovers Per Game

What statistic would you like to see? (type 'quit' to exit): 6

Fetching top 15 leaders for points per game...

Top 15 Points Per Game Leaders:
===============================
1. Stephen Curry (GSW): 30.5
2. Luka Dončić (DAL): 29.8
3. Giannis Antetokounmpo (MIL): 29.1
4. Joel Embiid (PHI): 28.7
5. Shai Gilgeous-Alexander (OKC): 28.1
...

Data saved to: data/points_per_game_20250514_123045.csv
```

## Dependencies

- requests: For making HTTP requests
- beautifulsoup4: For parsing HTML content
- pandas: For data manipulation and analysis

## Error Handling

The application includes comprehensive error handling:
- Network error recovery with automatic retries
- Logging of all operations to a log file
- Graceful degradation when services are unavailable
- User-friendly error messages

## License

This project is open source and available under the MIT License.

## Acknowledgements
- Data provided by Basketball Reference(https://www.basketball-reference.com/). 
- No copyright infringement is intended, this is for educational purposes.

## Future Enhancements

- Data visualization features using matplotlib or another visualization library
- Interactive web interface
- Historical data comparison 
