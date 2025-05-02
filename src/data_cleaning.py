"""This is a dataset cleaning script for unclean data"""
import warnings
warnings.filterwarnings("ignore", category=UserWarning, message="Could not infer format")

import pandas as pd
from io import StringIO

def clean_parts_data(filepath):
    """
    Load and clean parts sales data from a CSV file exported from Tekion.
    Supports both local file paths and Streamlit file uploads.
    """
    # Load CSV
    if hasattr(filepath, 'read'):
        filepath.seek(0)  # ✅ Reset file pointer in case it's already been read
        content = filepath.read()
        if isinstance(content, bytes):
            content = content.decode("utf-8")
        df = pd.read_csv(StringIO(content))
    else:
        df = pd.read_csv(filepath)

    # Clean and standardize column names
    df.columns = [col.strip().lower().replace(" ", "_").replace("'", "") for col in df.columns]

    # Rename known columns for consistency
    df.rename(columns={
        "sale_qty": "quantity_sold"
    }, inplace=True)

    # Drop completely empty rows
    df.dropna(how='all', inplace=True)

    # ✅ Check for required columns before dropping
    required_cols = {"part_number", "quantity_sold"}
    if required_cols.issubset(df.columns):
        df.dropna(subset=["part_number", "quantity_sold"], inplace=True)
    else:
        raise ValueError("❌ The uploaded file is missing required columns: part_number and/or quantity_sold.")

    # Convert quantity_sold to numeric
    df["quantity_sold"] = pd.to_numeric(df["quantity_sold"], errors="coerce").fillna(0)

    # Standardize part number format
    df["part_number"] = df["part_number"].astype(str).str.upper().str.strip()

    # Convert sale_date to datetime
    if "sale_date" in df.columns:
        df["sale_date"] = pd.to_datetime(df["sale_date"], errors="coerce")

    return df
