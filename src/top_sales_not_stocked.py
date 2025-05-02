import pandas as pd

def get_non_stocked_parts_ranked(df):
    """
    Return all parts with zero inventory, ranked by total quantity sold.
    Includes part description, number of sale dates, and all sale dates.
    """
    if "part_description" not in df.columns:
        df["part_description"] = ""

    if "inventory_qty" not in df.columns:
        df["inventory_qty"] = 0
    df["inventory_qty"] = pd.to_numeric(df["inventory_qty"], errors="coerce").fillna(0)

    df = df[df["inventory_qty"] == 0]

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
                aggfunc=lambda x: ', '.join(
        sorted(x.dropna().dt.strftime('%m/%d/%Y'))
    )
)
        )
        .sort_values("total_sold", ascending=False)
        .reset_index()
    )

    return grouped