import pandas as pd
from sklearn.linear_model import LinearRegression

def forecast_next_month_not_stocked(df):
    """
    Forecast next month's demand for parts that are currently out of stock.
    Includes part number, description, and forecasted quantity.
    """
    # Ensure necessary fields exist
    if "inventory_qty" not in df.columns:
        df["inventory_qty"] = 0
    df["inventory_qty"] = pd.to_numeric(df["inventory_qty"], errors="coerce").fillna(0)

    if "sale_date" in df.columns:
        df["sale_date"] = pd.to_datetime(df["sale_date"], errors="coerce")

    if "part_description" not in df.columns:
        df["part_description"] = ""

    # Filter to only parts that are currently out of stock
    df = df[df["inventory_qty"] == 0].copy()

    # Add year_month
    df.loc[:, "year_month"] = df["sale_date"].dt.to_period("M").astype(str)

    # Group monthly sales
    grouped = df.groupby(["part_number", "year_month"])["quantity_sold"].sum().reset_index()

    # Merge in descriptions
    part_descriptions = df[["part_number", "part_description"]].drop_duplicates(subset=["part_number"])
    grouped = grouped.merge(part_descriptions, on="part_number", how="left")

    results = []

    for part in grouped["part_number"].unique():
        part_df = grouped[grouped["part_number"] == part].copy()

        # Encode month order
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

        # Assign urgency level
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