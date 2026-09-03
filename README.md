# Quantix — Parts Demand Forecasting

A Streamlit app that turns a raw dealership DMS export into a next-month parts demand forecast,
split into what you already stock and what you don't.

Built to solve a problem I had in my own job: as parts manager I was ordering against intuition and
a spreadsheet, and the parts we ran out of were rarely the ones I expected.

---

## What it does

1. **Ingests** a CSV export from a dealership management system (Tekion, in my case)
2. **Cleans it** — normalizes column names, coerces types, drops rows missing the fields the model
   needs, and parses sale dates when present
3. **Forecasts** next-month demand per part with linear regression over historical sales
4. **Splits the output** into parts currently stocked and parts not stocked — the second list is
   the interesting one, because those are the orders you would otherwise miss
5. **Charts** the top 25 in each category and offers both as CSV and PDF downloads

Everything is built in memory. Nothing is written to disk — see [Privacy](#privacy-and-data-handling).

---

## Input format

The uploader accepts any CSV whose headers include at least:

| Column | Required | Notes |
|---|---|---|
| `part_number` | yes | Header matching is case- and space-insensitive (`Part Number` works) |
| `quantity_sold` | yes | Numeric |
| `sale_date` | optional | Enables time-series behaviour; without it the model falls back to aggregate volume |

If a required column is missing the app fails with an explicit message naming the column rather
than throwing a stack trace.

---

## Running it

```bash
git clone https://github.com/lemonlymandotcom/quantix-streamlit.git
cd quantix-streamlit
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL Streamlit prints and upload a CSV.

---

## Privacy and data handling

Dealership sales data is commercially sensitive, and this app is public, so the data path is worth
being explicit about:

- **Nothing touches the filesystem.** Forecasts and charts are built in `BytesIO` buffers and
  handed straight to the download button.
- **This was not always true.** An earlier version wrote results to fixed relative paths
  (`outputs/forecast_next_month.csv`) and then served those exact files. Streamlit sessions share
  one process and one working directory, so with two concurrent users the second upload overwrote
  the first, and the first user's download button served someone else's forecast. That's fixed.
- **No sample data is committed**, and `*.csv` is gitignored, so a real export cannot be added by
  accident.
- **Uploads are not persisted or logged.** Data lives in the session and is gone when it ends.

If you deploy this somewhere multi-user, put authentication in front of it. It has none.

---

## Known limitations

Stated plainly, because they matter if you're judging the modelling:

- **Linear regression only.** No seasonality, no trend decomposition, no holiday effects — all of
  which genuinely drive parts demand. It beats intuition; it is not a forecasting system.
- **No model evaluation.** There's no train/test split, no MAE or RMSE reported, no backtest. I
  can't currently tell you how accurate it is, which is the first thing I'd add.
- **No input size limit.** A large enough CSV will exhaust memory.
- **Single-file uploads only.** No incremental history, so each run sees only what you give it.
- **No tests.** The cleaning layer in `src/data_cleaning.py` is pure input/output transformation
  and is the obvious first target.

---

## Layout

```
app.py                                  Streamlit UI and orchestration
src/data_cleaning.py                    Column normalization, type coercion, validation
src/demand_forecasting.py               Forecast for stocked parts
src/demand_forecasting_not_stocked.py   Forecast for non-stocked parts
src/top_sales.py                        Top sellers, stocked
src/top_sales_not_stocked.py            Top sellers, not stocked
src/graph_forecasts.py                  Matplotlib chart generation
```

---

**Casey Shrader** — [linkedin.com/in/casey-shrader](https://www.linkedin.com/in/casey-shrader/)

Licensed MIT — see [LICENSE](LICENSE).
