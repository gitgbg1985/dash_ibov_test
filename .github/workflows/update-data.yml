name: Update Ibovespa Data

on:
  schedule:
    # Runs at 06:00 UTC on the 1st of every month
    - cron: '0 6 1 * *'
  workflow_dispatch:  # Allows manual trigger from GitHub UI

jobs:
  update-data:
    runs-on: ubuntu-latest

    permissions:
      contents: write  # Needed to push updated data files

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install yfinance pandas

      - name: Fetch Ibovespa data
        run: python fetch_ibovespa.py

      - name: Commit and push updated data
        run: |
          git config --global user.name "github-actions[bot]"
          git config --global user.email "github-actions[bot]@users.noreply.github.com"
          git add data/ibovespa.json data/ibovespa.csv
          git diff --staged --quiet || git commit -m "chore: update Ibovespa data $(date +'%Y-%m-%d')"
          git push
