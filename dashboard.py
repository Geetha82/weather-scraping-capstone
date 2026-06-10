"""
Program 4: Weather Analytics Dashboard
"""
import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Global Climate Analytics Panel", layout="wide")
st.title("Global Weather & Climate Visualization Panel")
st.markdown("### Web-Scraping Capstone Analytics Portal Dashboard\n* Use the sidebar widgets to filter the charts live.")

# 1. Database Ingestion
def load_data():
    try:
        # FIXED: Added the data/ folder prefix to match your directory layout structure
        conn = sqlite3.connect("data/weather_data.db")
        df = pd.read_sql_query("SELECT * FROM cleaned_weather", conn)
        conn.close()
        return df
    except Exception:
        return pd.DataFrame()


df = load_data()

if df.empty:
    st.error("Database missing or empty! Ensure weather_data.db is compiled and in the root folder.")
else:
    # 2. Sidebar Filters
    st.sidebar.header("🎛️ Dashboard Controls")
    city_search = st.sidebar.text_input("🔍 Search City Name", "")
    
    # Crash-proof slider boundary logic
    min_t, max_t = int(df["Temperature_C"].min()), int(df["Temperature_C"].max())
    bounds = (min_t - 5, max_t + 5) if min_t == max_t else (min_t - 2, max_t + 2)
    
    user_temp = st.sidebar.slider("🌡️ Temperature Range (°C)", int(bounds[0]), int(bounds[1]), (min_t, max_t))
    
    conditions = df["Condition"].unique()
    selected_conds = st.sidebar.multiselect("☁️ Weather Conditions", options=conditions, default=conditions)

    # 3. Real-time Filtering
    filtered_df = df[
        (df["City"].str.contains(city_search, case=False)) &
        (df["Temperature_C"] >= user_temp[0]) &
        (df["Temperature_C"] <= user_temp[1]) &
        (df["Condition"].isin(selected_conds))
    ]

    # 4. KPI Scorecards
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Matching Locations", len(filtered_df))
    kpi2.metric("Mean Selection Temp", f"{filtered_df['Temperature_C'].mean():.1f} °C" if len(filtered_df) > 0 else "N/A")
    kpi3.metric("Highest Temp", f"{filtered_df['Temperature_C'].max():.1f} °C" if len(filtered_df) > 0 else "N/A")

    st.markdown("---")

    if filtered_df.empty:
        st.warning("No data points fit your chosen sidebar parameters.")
    else:
        # 5. Visualizations
        st.subheader("📊 Chart 1: Global Temperature Distribution Ranking")
        fig_bar = px.bar(
            filtered_df.sort_values(by="Temperature_C", ascending=False).head(25),
            x="City", y="Temperature_C", color="Temperature_C",
            color_continuous_scale="Viridis", labels={"Temperature_C": "Temp (°C)"}
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        col_left, col_right = st.columns(2)
        with col_left:
            st.subheader("🍕 Chart 2: Climate Tier Mix")
            fig_pie = px.pie(filtered_df, names="Climate_Tier", hole=0.45, color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with col_right:
            st.subheader("📈 Chart 3: Condition Frequency")
            fig_hist = px.histogram(filtered_df, x="Condition", color="Climate_Tier", labels={"count": "Occurrences"})
            st.plotly_chart(fig_hist, use_container_width=True)

        # 6. Data Explorer Table Matrix
        st.markdown("---")
        st.subheader("🔍 SQL Cleaned Database Table Explorer")
        st.dataframe(filtered_df, use_container_width=True)
