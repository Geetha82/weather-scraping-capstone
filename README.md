# 🌎 Web Scraping & Dynamic Weather Dashboard Capstone

## Project Summary
This end-to-end analytical framework systematically collects live worldwide atmospheric statistics, normalizes raw inputs using Pandas data engineering procedures, persists structured data tables into a relational SQLite database schema, and presents interactive insights through an adaptive web dashboard app.

## Project Structure
* **`scrapper.py`**: Automated data ingestion module using Selenium browser processes to harvest live data points from web structures without tripping connection firewalls.
* **`pipeline.py`**: Data transformations engine. Cleans missing or malformed rows, calculates metric distributions, and saves attributes to SQLite.
* **`cli_query.py`**: Command Line Interface utility engine allowing users to test parameterized relational lookups straight from standard console prompts.
* **`dashboard.py`**: Streamlit presentation web app featuring multi-widget configurations, live responsive component scaling, and Plotly visualization charts.

## Environment Installation & Setup
Follow these quick commands in order inside your terminal to boot up the environment:

```bash
# 1. Install framework dependencies deterministically
pip install selenium webdriver-manager pandas plotly streamlit

# 2. Extract live metrics rows out of web directories
python scrapper.py

# 3. Clean records, build climate tiers, and save to SQLite
python pipeline.py

# 4. Verify local database tables from console prompt
python cli_query.py --min-temp 15.0 --condition "Passing"

# 5. Spin up the graphic dashboard visualization platform
streamlit run dashboard.py
```

## Production Application Interface View
![Dynamic Analytical Dashboard View](dashboard_capture.png)
