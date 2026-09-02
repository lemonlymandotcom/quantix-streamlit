import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from src.data_cleaning import clean_parts_data
from src.demand_forecasting import forecast_next_month
from src.demand_forecasting_not_stocked import forecast_next_month_not_stocked
from src.graph_forecasts import plot_single_forecast

st.set_page_config(page_title="Quantix Forecasting Suite", layout="wide")
st.title("📦 Quantix Parts Demand Forecasting")
st.caption("✅ App updated at 10:57 AM")

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

    # Build every artifact in memory. Streamlit sessions share one process
    # and one working directory, so writing to fixed paths like
    # "outputs/forecast_next_month.csv" lets a second user's upload overwrite
    # the first user's results -- and the first user's download button then
    # serves someone else's dealership sales data. Nothing touches disk.
    forecast_all_csv = forecast_all.to_csv(index=False).encode("utf-8")
    forecast_not_stocked_csv = forecast_not_stocked.to_csv(index=False).encode("utf-8")

    fig1 = plot_single_forecast(forecast_all, "Top 25 Forecasted Parts (All Stocked)", "skyblue", return_fig=True)
    fig2 = plot_single_forecast(forecast_not_stocked, "Top 25 Forecasted Parts (Not In Stock)", "salmon", return_fig=True)

    graph1_buf = BytesIO()
    fig1.savefig(graph1_buf, format='pdf', bbox_inches="tight")
    graph1_buf.seek(0)

    graph2_buf = BytesIO()
    fig2.savefig(graph2_buf, format='pdf', bbox_inches="tight")
    graph2_buf.seek(0)

    # Display graphs
    st.pyplot(fig1)
    st.pyplot(fig2)

    # Downloads
    st.subheader("📥 Download Forecast Results")
    col1, col2 = st.columns(2)

    with col1:
        st.download_button("📥 All Parts Forecast (CSV)", forecast_all_csv,
                           file_name="forecast_next_month.csv", mime="text/csv")
        st.download_button("📥 All Parts Graph (PDF)", graph1_buf,
                           file_name="forecast_stocked.pdf", mime="application/pdf")

    with col2:
        st.download_button("📥 Not Stocked Forecast (CSV)", forecast_not_stocked_csv,
                           file_name="forecast_not_stocked.csv", mime="text/csv")
        st.download_button("📥 Not Stocked Graph (PDF)", graph2_buf,
                           file_name="forecast_not_stocked.pdf", mime="application/pdf")