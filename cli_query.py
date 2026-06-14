"""
Program 3: Command Line Interface (CLI) Query Tool
Description: Standardizes custom SQL queries against the local weather 
             database table straight from the machine terminal window.
"""

import os
import sqlite3
import argparse

def execute_terminal_query(min_temp, condition_filter):
    db_file = "data/weather_data.db"
    
    if not os.path.exists(db_file):
        print(f"Error: Database file '{db_file}' missing. Run 'pipeline.py' first.")
        return

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Parametrized SQL statement structure to securely slice data rows
    base_query = "SELECT Country, City, Temperature_C, Condition, Climate_Tier FROM cleaned_weather WHERE 1=1"
    query_arguments = []
    
    if min_temp is not None:
        base_query += " AND Temperature_C >= ?"
        query_arguments.append(min_temp)
        
    if condition_filter:
        base_query += " AND Condition LIKE ?"
        query_arguments.append(f"%{condition_filter}%")
        
    cursor.execute(base_query, query_arguments)
    query_results = cursor.fetchall()
    
    # Construct command-line horizontal grids to view your database items
    print(f"\n[3/4] Database Query Match Results ({len(query_results)} records found):")
    print("+" + "-"*18 + "+" + "-"*20 + "+" + "-"*12 + "+" + "-"*20 + "+" + "-"*15 + "+")
    print(f"| {'Country':<16} | {'City':<18} | {'Temp (°C)':<10} | {'Condition':<18} | {'Climate Tier':<13} |")
    print("+" + "-"*18 + "+" + "-"*20 + "+" + "-"*12 + "+" + "-"*20 + "+" + "-"*15 + "+")
    
    for row in query_results:
        temp_display = f"{row[2]:.1f}" if row[2] is not None else "N/A"
        print(f"| {row[0]:<16} | {row[1]:<18} | {temp_display:<10} | {row[3]:<18} | {row[4]:<13} |")
        
    print("+" + "-"*18 + "+" + "-"*20 + "+" + "-"*12 + "+" + "-"*20 + "+" + "-"*15 + "+\n")
    conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query the Cleaned SQLite Weather Database Repository via Terminal inputs.")
    parser.add_argument("--min-temp", type=float, help="Displays matching results greater than or equal to this temperature value.")
    parser.add_argument("--condition", type=str, help="Filters data results by weather condition keyword matches.")
    
    args = parser.parse_args()
    execute_terminal_query(args.min_temp, args.condition)
