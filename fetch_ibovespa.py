#!/usr/bin/env python3
"""
Fetches Ibovespa (^BVSP) daily historical data from Yahoo Finance
and saves it as JSON for the dashboard, and CSV for download.
"""

import yfinance as yf
import json
import csv
import os
from datetime import datetime

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(OUTPUT_DIR, "data", "ibovespa.json")
CSV_PATH  = os.path.join(OUTPUT_DIR, "data", "ibovespa.csv")

def fetch_and_save():
    print("Fetching Ibovespa data from Yahoo Finance...")

    ticker = yf.Ticker("^BVSP")
    df = ticker.history(start="1995-01-01", interval="1d")

    if df.empty:
        raise ValueError("No data returned from Yahoo Finance.")

    df = df.reset_index()
    df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")

    # Build JSON for chart
    records = []
    for _, row in df.iterrows():
        records.append({
            "date":  row["Date"],
            "close": round(float(row["Close"]), 2),
            "open":  round(float(row["Open"]), 2),
            "high":  round(float(row["High"]), 2),
            "low":   round(float(row["Low"]), 2),
            "volume": int(row["Volume"]) if row["Volume"] == row["Volume"] else 0,
        })

    os.makedirs(os.path.dirname(JSON_PATH), exist_ok=True)

    meta = {
        "last_updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        "total_records": len(records),
        "source": "Yahoo Finance (^BVSP)",
        "data": records
    }

    with open(JSON_PATH, "w") as f:
        json.dump(meta, f, indent=2)
    print(f"JSON saved: {JSON_PATH} ({len(records)} records)")

    # Build CSV for download
    with open(CSV_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["date","open","high","low","close","volume"])
        writer.writeheader()
        writer.writerows(records)
    print(f"CSV saved: {CSV_PATH}")

if __name__ == "__main__":
    fetch_and_save()
