# Customer & Revenue Intelligence

Synthetic e-commerce analytics project using SQL and Python to analyze revenue quality, customer behavior and acquisition-channel value.

## Business questions

- What is total net revenue after returns?
- What share of orders are returned?
- Which acquisition channels generate stronger customer value?
- How much repeat purchasing exists?
- Which customers fall into stronger or weaker RFM segments?

## Analysis included

- Gross vs net revenue
- Return-rate analysis
- Repeat-customer behavior
- Acquisition-channel revenue per customer
- Recency, Frequency and Monetary (RFM) scoring
- RFM-based customer segmentation

## Run locally

```bash
pip install -r requirements.txt
python src/generate_data.py
python src/analyze.py
```

SQL examples are available in `sql/analysis.sql`.

## Data policy

This is a portfolio analytics lab using **synthetic data only**. No employer, client or production data is included.
