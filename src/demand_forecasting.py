import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def forecast_next_month(df):
    """
    Forecast next month's demand per part using linear regression.
    Includes part description and urgency flags.
    """
    # Ensure datetime format
    df["sale_date"] = pd.to_datetime(df["sale_date"], errors="coerce")

    # Create year-month column
    df["year_month"] = df["sale_date"].dt.to_period("M").astype(str)

    # Group by part and month, then sum quantity sold
    grouped = df.groupby(["part_number", "year_month"])["quantity_sold"].sum().reset_index()

    # Bring in part descriptions (assumes each part has consistent description)
    part_descriptions = df[["part_number", "part_description"]].drop_duplicates(subset=["part_number"])
    grouped = grouped.merge(part_descriptions, on="part_number", how="left")

    results = []

    for part in grouped["part_number"].unique():
        part_df = grouped[grouped["part_number"] == part].copy()

        part_df["month_idx"] = pd.factorize(part_df["year_month"])[0]
        X = part_df[["month_idx"]]
        y = part_df["quantity_sold"]

        if len(X) < 3:
            continue

        model = LinearRegression()
        model.fit(X, y)

        next_month_idx = X["month_idx"].max() + 1
        forecast = model.predict(pd.DataFrame([[next_month_idx]], columns=["month_idx"]))[0]

        rounded_forecast = max(0, round(forecast, 2))

        # Urgency logic
        if rounded_forecast >= 30:
            urgency = 3
        elif rounded_forecast >= 10:
            urgency = 2
        else:
            urgency = 1

        results.append({
            "part_number": part,
            "part_description": part_df["part_description"].iloc[0],
            "forecast_next_month": rounded_forecast,
            "reorder_urgency": urgency
        })

    return pd.DataFrame(results)