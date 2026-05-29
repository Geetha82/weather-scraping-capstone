import pandas as pd
import os
import re
import sqlite3

def clean_and_transform_weather():
    raw_path = 'data/raw_weather.csv'
    db_path = 'data/weather_capstone.db'
    
    if not os.path.exists(raw_path):
        print(f"Error: Target data dependency '{raw_path}' is missing.")
        return

    # 1. Load the raw data
    df = pd.read_csv(raw_path)

    print("\n =====STAGE 1: BEFORE CLEANING DIAGNOSTIC SUMMARY=====")
    print(f"Dimensions: {df.shape}")
    print(df.head(5))

    # 2. Remove duplicates
    df = df.drop_duplicates()
    
    if 'Condition' in df.columns and df['Temperature'].isnull().all():
        # 'Condition' contains the temperature strings, copy it over to Temperature
        df['Temperature'] = df['Condition']
        # Reset Condition to a default placeholder value since the main overview text was missed
        df['Condition'] = 'Reported' 


     # 3. Clean and convert Temperature values (extracting digits from strings like '84 °F')
    def parse_temperature(val):
        if pd.isna(val) or str(val).strip().upper() == "NAN":
            return None
        clean_str = str(val).replace('\xa0', '').strip()
        match = re.search(r'(-?\d+)', clean_str)
        return float(match.group(1)) if match else None

    df['Temperature'] = df['Temperature'].apply(parse_temperature)
    df = df.dropna(subset=['Temperature'])

    # 4. Standardaize Text
    df['Humidity'] = df['Humidity'].fillna('N/A').astype(str).str.strip()
    df['Condition'] = df['Condition'].fillna('Reported').astype(str).str.strip()
    df['Country'] = df['Country'].fillna('Global Hub').astype(str).str.strip()
    df['City'] = df['City'].fillna('Unknown').astype(str).str.strip()

    print("\n =====STAGE 2: AFTER CLEANING DIAGNOSTIC SUMMARY======")
    print(f"Dimensions: {df.shape}")
    print(df.head(5))
  

    # 5. Write in seperate SQLite Tables
    os.makedirs('data', exist_ok=True)
    conn = sqlite3.connect(db_path)
    try:
        # Table 1: Granular revords
        df.to_sql('cleaned_weather', conn, if_exists='replace', index=False)

        # Table 2: Transformed Aggregations
        summary_df = df.groupby('Country')['Temperature'].mean().reset_index()
        summary_df.columns = ['Country', 'Average_Temperature']
        summary_df = summary_df.round(2)
        summary_df.to_sql('country_weather_summary', conn, if_exists='replace', index=False)

        print(f"\nSuccessfully populated database: {db_path}")
    except Exception as e:
        print(f"Database error encountered: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    clean_and_transform_weather()
