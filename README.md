# Sports Betting Arbitrage Detection System

This project automates the aggregation and analysis of live sports betting odds from multiple bookmakers to identify real-time arbitrage opportunities. Leveraging modern Python tools for web scraping, data processing, and database management, the system enables efficient, data-driven betting decisions.

---

## Features

- **Automated Odds Aggregation:** Scrapes live odds from 5+ bookmakers using Selenium, BeautifulSoup, and APIs.
- **Parallel Processing:** Uses Python’s multiprocessing to collect data concurrently for faster updates.
- **Data Analysis:** Processes and analyzes large datasets with Pandas to detect arbitrage opportunities.
- **Real-Time Alerts:** Sends desktop notifications when profitable arbitrage scenarios are found.
- **Robust Storage:** Stores aggregated odds and analysis results in a PostgreSQL database for reliable, scalable access.

---

## Tech Stack

- **Python 3**
- **Selenium** (browser automation)
- **BeautifulSoup** (HTML parsing)
- **Pandas** (data manipulation and analysis)
- **Multiprocessing** (parallel execution)
- **PostgreSQL** (relational database)
- **Plyer** (desktop notifications)

---

## Setup Instructions

1. **Clone the Repository**
    ```
    git clone https://github.com/your-username/your-repo.git
    cd your-repo
    ```

2. **Install Dependencies**
    ```
    pip install -r requirements.txt
    ```
    *Ensure you have [PostgreSQL](https://www.postgresql.org/download/) installed and running.*

3. **Configure Database**
    - Update your database credentials in the configuration file or environment variables as needed.

4. **Run the Program**
    ```
    python main.py
    ```

---

## Usage

- The script will automatically scrape odds from supported bookmakers, process the data, and notify you if an arbitrage opportunity is detected.
- Aggregated data and results are stored in the PostgreSQL database for further analysis or reporting.
