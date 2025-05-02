import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from io import BytesIO
from src.data_cleaning import clean_parts_data
from src.demand_forecasting import forecast_next_month
from src.demand_forecasting_not_stocked import forecast_next_month_not_stocked
from src.graph_forecasts import plot_single_forecast

st.set_page_config(page_title="Quantix Forecasting Suite", layout="wide")
st.title("📦 Quantix Parts Demand Forecasting")

# Upload section
uploaded_file = st.file_uploader("📁 Upload your exported Tekion CSV", type=["csv"])

if uploaded_file:
    # Read and clean
    raw_df = pd.read_csv(uploaded_file)
    df_clean = clean_parts_data(uploaded_file)

    st.success("✅ Data loaded and cleaned!")
    st.write("Preview of cleaned data:", df_clean.head())

    # Forecasts
    st.subheader("📊 Running Forecast Models...")
    forecast_all = forecast_next_month(df_clean)
    forecast_not_stocked = forecast_next_month_not_stocked(df_clean)

    # Save outputs
    os.makedirs("outputs", exist_ok=True)
    forecast_all_path = "outputs/forecast_next_month.csv"
    forecast_not_stocked_path = "outputs/forecast_not_stocked.csv"
    forecast_all.to_csv(forecast_all_path, index=False)
    forecast_not_stocked.to_csv(forecast_not_stocked_path, index=False)

    # Generate graphs and save to PDF
    graph1_path = "outputs/top_stocked_forecast.pdf"
    graph2_path = "outputs/top_not_stocked_forecast.pdf"

    fig1 = plot_single_forecast(forecast_all, "Top 25 Forecasted Parts (All Stocked)", "skyblue", return_fig=True)
    fig2 = plot_single_forecast(forecast_not_stocked, "Top 25 Forecasted Parts (Not In Stock)", "salmon", return_fig=True)

    fig1.savefig(graph1_path, format='pdf', bbox_inches="tight")
    fig2.savefig(graph2_path, format='pdf', bbox_inches="tight")

    # Display graphs
    st.pyplot(fig1)
    st.pyplot(fig2)

    # Downloads
    st.subheader("📥 Download Forecast Results")
    col1, col2 = st.columns(2)

    with col1:
        with open(forecast_all_path, "rb") as f:
            st.download_button("📥 All Parts Forecast (CSV)", f, file_name="forecast_next_month.csv")
        with open(graph1_path, "rb") as f:
            st.download_button("📥 All Parts Graph (PDF)", f, file_name="forecast_stocked.pdf")

    with col2:
        with open(forecast_not_stocked_path, "rb") as f:
            st.download_button("📥 Not Stocked Forecast (CSV)", f, file_name="forecast_not_stocked.csv")
        with open(graph2_path, "rb") as f:
            st.download_button("📥 Not Stocked Graph (PDF)", f, file_name="forecast_not_stocked.pdf")