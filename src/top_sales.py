import pandas as pd

def get_all_parts_ranked(df):
    """
    Return all parts ranked by total quantity sold.
    Includes part description, number of sale dates, and all sale dates (formatted).
    """
    # Ensure part_description exists
    if "part_description" not in df.columns:
        df["part_description"] = ""

    # Ensure sale_date is datetime
    if "sale_date" in df.columns:
        df["sale_date"] = pd.to_datetime(df["sale_date"], errors="coerce")

    # Group and aggregate
    grouped = (
        df.groupby(["part_number", "part_description"])
        .agg(
            total_sold=pd.NamedAgg(column="quantity_sold", aggfunc="sum"),
            sale_count=pd.NamedAgg(column="sale_date", aggfunc="nunique"),
            last_date_sold=pd.NamedAgg(
                column="sale_date",
                aggfunc=lambda x: x.max().strftime('%b %d, %Y') if pd.notnull(x.max()) else ''
            ),
            sale_dates=pd.NamedAgg(
                column="sale_date",
                aggfunc=lambda x: ' , '.join(sorted(x.dropna().dt.strftime('%b %d, %Y')))
            )
        )
        .sort_values("total_sold", ascending=False)
        .reset_index()
    )

    return grouped