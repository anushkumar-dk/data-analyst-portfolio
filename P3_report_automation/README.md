# Project 3: Monthly Report Automation (Python)
**Problem:** Every month a team gets several sales files with different column names and spends hours merging and summarising them.
**What I did:** One script merges all CSVs in `data/`, standardises headers, removes duplicates, fixes product names and blanks, then builds `report.xlsx` with live SUMIFS summaries by month, region and product.
**Tools:** Python, pandas, openpyxl
**Result:** New month = drop the file in `data/`, run `python monthly_report.py`. Seconds instead of hours. Data is synthetic.
