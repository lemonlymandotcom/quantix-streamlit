import pandas as pd
import matplotlib.pyplot as plt

def clean_labels(df):
    """Create shortened label: 'part_number - part_description' (trimmed)"""
    df["label"] = df["part_number"].astype(str) + " - " + df["part_description"].astype(str).str.slice(0, 40)
    return df

def plot_single_forecast(df, title, color, output_path=None, return_fig=False):
    """Plot a single bar chart for top 25 forecasted parts with value labels."""
    df = df.sort_values("forecast_next_month", ascending=False).head(25)
    df = clean_labels(df)

    plt.figure(figsize=(12, 10))
    bars = plt.barh(df["label"], df["forecast_next_month"], color=color)
    plt.gca().invert_yaxis()
    plt.title(title)
    plt.xlabel("Forecasted Qty")
    plt.ylabel("Part")
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=8)

    # Add forecast value labels to each bar
    for bar in bars:
        width = bar.get_width()
        plt.text(
            width + 1,                          # X position: just after the bar
            bar.get_y() + bar.get_height() / 2, # Y position: vertically centered
            f"{width:.1f}",                     # Format to 1 decimal place
            va='center',
            fontsize=9,
            color='black'
        )

    plt.tight_layout()

    # Save the figure if an output path is provided
    if output_path:
        plt.savefig(output_path, format="pdf", bbox_inches="tight")
        print(f"✅ Saved chart: {output_path}")

    # Return figure for Streamlit if requested
    if return_fig:
        return plt.gcf()

    # Show plot for standalone use
    plt.show()
    plt.close()

def plot_top_forecasts(stocked_csv, not_stocked_csv):
    # Load CSVs
    df_stocked = pd.read_csv(stocked_csv)
    df_not_stocked = pd.read_csv(not_stocked_csv)

    # Plot them separately (local usage)
    plot_single_forecast(
        df_stocked,
        title="Top 25 Forecasted Parts (All Stocked)",
        color="skyblue",
        output_path="outputs/top_stocked_forecast.png"
    )

    plot_single_forecast(
        df_not_stocked,
        title="Top 25 Forecasted Parts (Not In Stock)",
        color="salmon",
        output_path="outputs/top_not_stocked_forecast.png"
    )