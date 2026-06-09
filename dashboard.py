"""
Program 4: Dynamic Interactive Analysis Dashboard Web App
Author: Capstone Student
Description: Connects to your SQLite backend to display 3 responsive user filters
             and 3 distinct charts built completely with Streamlit and Plotly.
"""

import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# Rubric Configuration: App layout styling and user-guidance text headers
st.set_page_config(page_title="Global Climate Analytics Panel", layout="wide")

st.title("🌎 Global Weather & Climate Visualization Panel")
st.markdown("""
### Student Capstone Analytics Portal Dashboard
* **User Instructions**: Modify any of the interactive filter widgets located in the left sidebar configuration panel. 
* The metric KPI counter nodes and all three dynamic graphical data stories will update instantly.
""")

def fetch_stored_db_data():
    try:
        conn = sqlite3.connect("weather_data.db")
        loaded_df = pd.read_sql_query("SELECT * FROM cleaned_weather", conn)
        conn.close()
        return loaded_df
    except Exception:
        return pd.DataFrame()

df = fetch_stored_db_data()

if df.empty:
    st.error("⛔ Database missing or empty! Ensure your scraper and data processing pipelines are compiled first.")
else:
    # ─── SIDEBAR FILTER INTERACTIONS ───
    st.sidebar.header("🎛️ Dashboard Controls")
    st.sidebar.markdown("Filter options:")
    
    # Widget Control 1: Text box keyword search string input
    city_search = st.sidebar.text_input("🔍 Search specific City Name", value="")
    
    # Widget Control 2: Safe, crash-proof Slider boundaries validation guard
    min_val = int(df["Temperature_C"].min()) if not df["Temperature_C"].isnull().all() else 0
    max_val = int(df["Temperature_C"].max()) if not df["Temperature_C"].isnull().all() else 45
    
    # FIX: Check for overlapping boundaries (e.g., 21 and 21) to prevent StreamlitAPIException
    if min_val == max_val:
        min_slider_bound = min_val - 5
        max_slider_bound = max_val + 5
        initial_user_selection = (min_val, max_val)
    else:
        min_slider_bound = min_val - 2
        max_slider_bound = max_val + 2
        initial_user_selection = (min_val, max_val)
    
    user_temp_bounds = st.sidebar.slider(
        "🌡️ Select Temperature Boundaries (°C)",
        min_value=int(min_slider_bound),
        max_value=int(max_slider_bound),
        value=initial_user_selection
    )
    
    # Widget Control 3: Multi-Select structural token dropdown tags mapped to exact SQLite column key
    unique_conditions = df["Condition"].unique()
    selected_conditions = st.sidebar.multiselect(
        "☁️ Filter Weather Condition Profiles",
        options=unique_conditions,
        default=unique_conditions
    )

    # Sync and filter database elements in real-time
    processed_df = df[
        (df["City"].str.contains(city_search, case=False)) &
        (df["Temperature_C"] >= user_temp_bounds[0]) &
        (df["Temperature_C"] <= user_temp_bounds[1]) &
        (df["Condition"].isin(selected_conditions))
    ]

    # Generate layout dashboard summary cards
    card_1, card_2, card_3 = st.columns(3)
    card_1.metric("Locations Matching Filters", len(processed_df))
    card_2.metric("Mean Temp of Selection", f"{processed_df['Temperature_C'].mean():.1f} °C" if len(processed_df) > 0 else "N/A")
    card_3.metric("Highest Selected Temperature", f"{processed_df['Temperature_C'].max():.1f} °C" if len(processed_df) > 0 else "N/A")

    st.markdown("---")

    if processed_df.empty:
        st.warning(" No data columns fit your chosen sidebar configuration. Adjust parameters to view charts.")
    else:
        # ─── THREE DISTINCT VISUALIZATIONS ───
        
        # Chart Layout 1: Horizontal sorted distribution bar chart
        st.subheader("📊 Chart 1: Global Temperature Distribution Ranking")
        st.caption("Displays temperature attributes for selected metrics, ranked from highest to lowest.")
        
        sorted_top = processed_df.sort_values(by="Temperature_C", ascending=False).head(25)
        fig_bar = px.bar(
            sorted_top,
            x="City",
            y="Temperature_C",
            color="Temperature_C",
            color_continuous_scale="Viridis",
            labels={"Temperature_C": "Temperature (°C)", "City": "Location"}
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        # Split space into two neat horizontal grid blocks
        left_chart_block, right_chart_block = st.columns(2)

        with left_chart_block:
            # Chart Layout 2: Proportional composition donut pie chart
            st.subheader(" Chart 2: Climate Tier Composition Mix")
            st.caption("Proportion of selected cities categorised as Hot, Moderate, or Cold.")
            
            fig_pie = px.pie(
                processed_df,
                names="Climate_Tier",
                hole=0.45,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        with right_chart_block:
            # Chart Layout 3: Frequency aggregate conditions histogram chart
            st.subheader("Chart 3: Atmospheric State Frequency Overview")
            st.caption("Histogram measuring the occurrences of distinct weather parameters.")
            
            fig_hist = px.histogram(
                processed_df,
                x="Condition",
                color="Climate_Tier",
                labels={"Condition": "Observed Outer Condition Text", "count": "Record Occurrences"}
            )
            st.plotly_chart(fig_hist, use_container_width=True)

        # Deep Dive SQL Raw Explorer Grid table view area
        st.markdown("---")
        st.subheader("🔍 Complete Filtered SQL Database Explorer Table View")
        st.caption("Explore individual database attributes or export customized rows locally.")
        st.dataframe(processed_df, use_container_width=True)
