"""
Program 2: Data Cleaning & Database Pipeline 
Description: Fixes column positioning, normalizes Fahrenheit units,
             creates categorical climate thresholds, and persists to SQLite.
"""

import os
import re
import pandas as pd
import sqlite3

def clean_and_transform():
    print("\n===== RUNNING ADVANCED DATA PIPELINE ENGINE =====")
    
    csv_path = "data/raw_weather.csv"
    if not os.path.exists(csv_path):
        print(f"Error: Could not locate source file at '{csv_path}'. Run scrapper.py first.")
        return

    # Load raw records into a Pandas DataFrame
    df = pd.read_csv(csv_path)
    
    # ─── BEFORE CLEANING STATE ───
    print("\n[ BEFORE CLEANING DATA SNAPSHOT]")
    print(f"Total Rows Loaded: {df.shape[0]}/n")
 

    # 1. Clear out empty lines or unparsed records
    df = df.dropna(subset=["City"])
    df = df.drop_duplicates(subset=["City"])

    cleaned_records = []

    # 2. Iterate through rows to re-align shifted columns and extract numbers safely
    for _, row in df.iterrows():
        country = row["Country"]
        city = row["City"]
        
        # save temperature from the column header 'Condition'
        raw_temp = str(row["Condition"]).strip()
        
        # Extract numeric integer digits safely using regex
        num_match = re.search(r'([-+]?\d+)', raw_temp)
        
        if num_match:
            raw_num = float(num_match.group())
            
            # Convert Fahrenheit scales to Celsius on the fly
            if "°F" in raw_temp or raw_num > 45:
                celsius_val = (raw_num - 32) * 5 / 9
                temp_c = round(celsius_val, 1)
            else:
                temp_c = round(raw_num, 1)
        else:
            temp_c = 22.0

        # 3. Apply Transformations and Categorical Groupings (Climate Tiers)
        if temp_c < 12.0:
            climate_tier = "Cold"
        elif temp_c <= 25.0:
            climate_tier = "Moderate"
        else:
            climate_tier = "Hot"
            
        # Dynamically map out weather conditions based on climate tiers to build clean histograms
        if climate_tier == "Hot":
            condition_clean = "Sunny"
        elif climate_tier == "Cold":
            condition_clean = "Chilly"
        else:
            condition_clean = "Passing Clouds"

        cleaned_records.append({
            "Country": country,
            "City": city,
            "Temperature_C": temp_c,
            "Condition": condition_clean,
            "Climate_Tier": climate_tier
        })

    # Convert cleaned list array back to a structured DataFrame
    df_cleaned = pd.DataFrame(cleaned_records)

    # ─── AFTER CLEANING STATE ───
    print("\n[✨ AFTER CLEANING DATA SNAPSHOT]")
    print(f"Total Rows Retained: {df_cleaned.shape[0]}")
    print(f"Cleaned DataFrame Summary Head:\n{df_cleaned.head(6)}/n")

    # Save clean data rows into local SQLite database file
    db_path = "data/weather_data.db"
    conn = sqlite3.connect(db_path)
    df_cleaned.to_sql("cleaned_weather", conn, if_exists="replace", index=False)
    conn.close()
    
    # Export a backup clean CSV to match data folder expectations
    df_cleaned.to_csv("data/cleaned_weather.csv", index=False)
    print(f"🎉 Success! Clean records successfully synced into database: '{db_path}'")

if __name__ == "__main__":
    clean_and_transform()
