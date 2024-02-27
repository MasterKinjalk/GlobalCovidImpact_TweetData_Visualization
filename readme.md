# Visualizing Covid-19 Through Tweets

This project is a Dash application designed to visualize COVID-19 sentiment and word usage in tweets across different countries. It allows users to view sentiment analysis and word frequency on a global scale through interactive choropleth maps and bar charts.

## Getting Started

### Prerequisites

Before running the application, ensure you have Python installed on your system. You will also need to install the necessary Python libraries listed in `requirements.txt`.

### Installation

1. Clone the repository or download the source code.
2. Navigate to the project directory.
3. Install the required dependencies by running the following command:

```bash
pip install -r requirements.txt
```

### Data Files

The application requires three data files for processing:

- `Covid-19 Twitter Dataset (Apr-Jun 2020) clean.csv`
- `Covid-19 Twitter Dataset (Aug-Sep 2020) clean.csv`
- `Covid-19 Twitter Dataset (Apr-Jun 2021) clean.csv`

In addition, it uses `world-countries.json` for the choropleth maps and `countries.csv` for country-specific data. Ensure these files are placed in the correct location within your project directory.

### Running the Application

To start the Dash server and run the application, execute:

```bash
python map-to-bar-final.py
```

Navigate to the URL provided by Dash (typically http://127.0.0.1:8050/) in your web browser to access the application.

## Features

- **Sentiment Map**: Displays the average sentiment towards COVID-19 in tweets from different countries.
- **Word Search Map**: Visualizes the frequency of specific words used in tweets across the globe.