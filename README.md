# 🌐 Global Weather Analytics Engine & Interactive Dashboard

An end-to-end automated data pipeline and browser-based analytics workspace. This capstone project orchestrates a four-phase data engineering architecture: leveraging **Selenium** for live data collection, **Pandas** for advanced layout transformation, **SQLite** for structural data storage, and **Streamlit** for interactive multi-dimensional dashboards.

---

## 📂 Project Repository Blueprint

```text
weather-scraping-capstone/
├── scraper.py       # Phase 1: Selenium Web Automation & Harvesting Engine
├── pipeline.py      # Phase 2: Advanced Positional Pandas Data Cleaning 
├── database.py      # Phase 2: Structural SQLite Database Finalizer & Ingestion
├── app.py           # Phase 4: Streamlit Interactive Visual Dashboard Interface
└── data/            # Local Persistent Storage Matrix (Automated Build)
    ├── raw_weather.csv
    ├── cleaned_weather.csv
    └── weather_data.db
```

---

## 🛠️ Multi-Phase System Architecture

### 1. Web Scraping & Extraction Engine (`scraper.py`)
* **Technology Layer:** Selenium WebDriver (Configured with stealth Browser mimics)
* **Target Domain:** Live data tracking from the Time and Date Weather engine.
* **Pipeline Logic:** Launches a secure, headless Chrome background engine to harvest unrendered page sources. It bypasses aggressive Cloudflare edge-protection drops and outputs a 5-column unparsed raw CSV layout context.

### 2. Data Cleaning & Transformation Pipeline (`pipeline.py`)
* **Technology Layer:** Pandas DataFrame Matrix Engine & Python RegEx
* **Pipeline Logic:** Loads the raw dataset and enforces strict structural sanitization. It scans row arrays using flexible positional indices to address layout column shifts and isolates hidden HTML symbols (such as `&nbsp;` and `°`). Unparsable data artifacts are safely removed before the script outputs a production-ready CSV dataset.

### 3. SQLite Database Engine Finalizer (`database.py`)
* **Technology Layer:** Python `sqlite3`, Transact-SQL, and Pandas Integration
* **Pipeline Logic:** Establishes a secure relational connection block to `weather_data.db`. It cleans up old schemas, processes column tracking, and executes a bulk append to pipe records into the `global_weather` table. Search optimization keys (`INDEX`) are applied, and native SQL arithmetic filters compute global data summaries before shutting down connections cleanly.

### 4. Streamlit User Interface Dashboard (`app.py`)
* **Technology Layer:** Streamlit Web Framework & Plotly Express Charts
* **Pipeline Logic:** Opens an active connection to your SQLite database, loading structural tables straight into the web space. It sets up dynamic sidebar layout controls—enabling users to sort and filter records by country, sky pattern, and climate variance—and renders responsive, interactive graphs.

---

## 📈 System Metrics & Ingestion Verification

Upon executing the pipeline chain, the integrated Transact-SQL summary report confirms perfect data schema compliance:
* **Total Unique Locations Harvested & Ingested:** `69 Rows`
* **Natively Calculated Global Average Temperature:** `71.3°F`
* **Database File Lock Status:** Verified, compiled, and closed cleanly.

---

## 🚀 Execution Guide

To launch this automated environment locally on your machine, open your terminal window and execute these specific commands sequentially:

### 1. Set Up Your System Dependencies
```bash
pip install selenium pandas streamlit plotly
```

### 2. Run the Data Retrieval and Storage Engine Chain
```bash
# Move directly into your capstone folder
cd /Users/abhinaavbalaji/python_class/weather-scraping-capstone

# Step A: Harvest raw live content via Selenium
python scraper.py

# Step B: Sanitize HTML text blocks and align columns using Pandas
python pipeline.py

# Step C: Populate schemas and run SQL verification math
python database.py
```

### 3. Mount the Web Presentation Server
```bash
streamlit run app.py
```

Streamlit will instantly spin up a local development web-server session and open a fresh tab within your default internet browser at **`http://localhost:8501`** to showcase your live interactive global metrics!
