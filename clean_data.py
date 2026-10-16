"""Cleans messy_orders.csv and writes clean_orders.csv, cleaning_log.md and before_after.xlsx."""
import pandas as pd, re
raw = pd.read_csv("messy_orders.csv", dtype=str)
df = raw.copy(); log = []
n0 = len(df)
df = df.drop_duplicates(); d_exact = n0-len(df)
df = df.drop_duplicates(subset="order_id"); d_id = (n0-d_exact)-len(df)
log.append(f"Removed {d_exact+d_id} duplicate rows ({n0} -> {len(df)})")
before = df["customer_name"].copy()
df["customer_name"] = df["customer_name"].str.strip().str.title()
log.append(f"Standardised {int((before!=df['customer_name']).sum())} customer names (trimmed spaces, proper case)")
def pdate(s):
    for f in ("%d/%m/%Y","%Y-%m-%d","%d-%b-%Y","%B %d, %Y"):
        try: return pd.to_datetime(s, format=f)
        except Exception: pass
    return pd.NaT
df["order_date"] = df["order_date"].map(pdate)
log.append(f"Converted 4 mixed date formats to one (YYYY-MM-DD); unparseable dates: {int(df['order_date'].isna().sum())}")
cmap = {"hyd":"Hyderabad","hyderbad":"Hyderabad","bombay":"Mumbai","bangalore":"Bengaluru","blr":"Bengaluru",
        "new delhi":"Delhi","madras":"Chennai","chenai":"Chennai"}
c0 = df["city"].copy()
k = df["city"].str.strip().str.lower()
df["city"] = k.map(cmap).fillna(k.str.title())
log.append(f"Fixed {int((c0!=df['city']).sum())} city spelling variants into 5 clean city names")
df["status"] = df["status"].str.strip().str.title()
df["amount"] = pd.to_numeric(df["amount"].str.replace(r"(?i)rs\.?|₹|,|\s", "", regex=True), errors="coerce")
miss_amt = int(df["amount"].isna().sum())
df["category"] = df["category"].fillna("Unknown")
df["amount"] = df.groupby("category")["amount"].transform(lambda s: s.fillna(s.median()))
log.append(f"Converted amount text (₹, Rs., commas) to numbers; filled {miss_amt} missing amounts with category median")
log.append(f"Filled {int(raw['category'].isna().sum())} missing categories with 'Unknown'")
df["email"] = df["email"].fillna("")
df["order_date"] = df["order_date"].dt.strftime("%Y-%m-%d")
df.to_csv("clean_orders.csv", index=False)
open("cleaning_log.md","w").write("# What I fixed\n\n"+"\n".join(f"- {l}" for l in log)+"\n")
with pd.ExcelWriter("before_after.xlsx") as w:
    raw.head(40).to_excel(w, sheet_name="Before (sample)", index=False); df.head(40).to_excel(w, sheet_name="After (sample)", index=False)
print("\n".join(log))
