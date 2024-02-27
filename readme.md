## Visualizing Covid-19 Through Tweets

This project is a Dash application designed to visualize **COVID-19 sentiment and word usage** in tweets across different countries. It allows users to explore **sentiment analysis and word frequency** on a **global scale** through interactive **choropleth maps and bar charts**.

## Getting Started

### Prerequisites

Before running the application, ensure you have Python installed on your system. You will also need to install the necessary Python libraries listed in the `requirements.txt` file.

### Installation

1. Clone the repository or download the source code.
2. Navigate to the project directory.
3. Install the required dependencies by running the following command:

```bash
pip install -r requirements.txt
```

### Data Files

The application requires three data files for processing, each containing **clean COVID-19 tweets** from different timeframes:

* `Covid-19 Twitter Dataset (Apr-Jun 2020) clean.csv`
* `Covid-19 Twitter Dataset (Aug-Sep 2020) clean.csv`
* `Covid-19 Twitter Dataset (Apr-Jun 2021) clean.csv`

Additionally, it uses:

* `world-countries.json` to define the choropleth map regions.
* `countries.csv` for country-specific data.

Ensure these files are placed in the correct location within your project directory.

### Running the Application

To start the Dash server and run the application, execute:

```bash
python map-to-bar-final.py
```

Navigate to the URL provided by Dash (typically http://127.0.0.1:8050/) in your web browser to access the application.

## Interactive Exploration

The application offers a range of interactive features:

**1. Dataset Selection:** Choose from three datasets representing different timeframes of COVID-19 tweets.

**2. Sentiment Map:**

* View the **average sentiment (positive, negative, neutral)** for each country on a world map.
* **Zoom in** to specific countries for a closer look at sentiment distribution.
* Click on a country to see a **bar chart** displaying the sentiment breakdown within that country's tweets.

**3. Word Search Map:**

* Enter a word in the search bar and click "Search tweet text" to see its **frequency** across different countries, visualized on a **choropleth map**.
* Optionally, **filter the word search map** to a specific country for a more focused analysis.

## Further Enhancements

This project serves as a foundation for further exploration:

* Implement functionalities to **compare and contrast** different datasets.
* Allow users to **download** visualizations as images for reports or presentations.
* Add a **time slider** to track sentiment and word usage trends over time.
* Consider incorporating **network analysis** to visualize relationships between countries based on tweet content.

