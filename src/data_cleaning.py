"""This is a dataset cleaning script for unclean data"""
import warnings
warnings.filterwarnings("ignore", category=UserWarning, message="Could not infer format")

import pandas as pd

def clean_parts_data(filepath):
    """
    Load and clean parts sales data from a CSV file exported from Tekion.
    """
    # Load CSV
    df = pd.read_csv(filepath)

    # Clean and standardize column names
    df.columns = [col.strip().lower().replace(" ", "_").replace("'", "") for col in df.columns]

    # Rename known columns for consistency
    df.rename(columns={
        "sale_qty": "quantity_sold"
    }, inplace=True)

    # Drop completely empty rows
    df.dropna(how='all', inplace=True)

    # Drop rows missing critical fields
    df.dropna(subset=["part_number", "quantity_sold"], inplace=True)

    # Convert quantity_sold to numeric
    df["quantity_sold"] = pd.to_numeric(df["quantity_sold"], errors="coerce").fillna(0)

    # Standardize part number format
    df["part_number"] = df["part_number"].astype(str).str.upper().str.strip()

    # Convert sale_date to datetime
    if "sale_date" in df.columns:
        df["sale_date"] = pd.to_datetime(df["sale_date"], errors="coerce")

    return df