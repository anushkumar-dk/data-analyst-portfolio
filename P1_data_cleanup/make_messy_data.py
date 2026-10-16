"""Generates a SYNTHETIC messy orders file (duplicates, mixed dates, typos, blanks)."""
import random, pandas as pd
from datetime import date, timedelta
random.seed(42)
cities = {"Hyderabad":["Hyderabad","hyderabad","Hyd","Hyderbad"],"Mumbai":["Mumbai","mumbai","Bombay","MUMBAI"],
          "Bengaluru":["Bengaluru","Bangalore","bengaluru","BLR"],"Delhi":["Delhi","New Delhi","delhi","DELHI"],
          "Chennai":["Chennai","chennai","Madras","Chenai"]}
names = ["Aarav Sharma","Priya Reddy","Rohan Mehta","Sneha Iyer","Vikram Singh","Ananya Rao","Kiran Kumar","Neha Gupta","Arjun Nair","Divya Patel"]
cats = ["Electronics","Clothing","Home","Grocery","Books"]
fmts = ["%d/%m/%Y","%Y-%m-%d","%d-%b-%Y","%B %d, %Y"]
rows=[]
for i in range(1,1301):
    d = date(2025,1,1)+timedelta(days=random.randint(0,364))
    n = random.choice(names)
    if random.random()<.3: n = random.choice(["  ","",""])+n.upper() if random.random()<.5 else " "+n.lower()+" "
    amt = random.randint(200,25000)
    amt = random.choice([f"{amt}", f"₹{amt:,}", f"Rs. {amt}", f"{amt:,}"])
    rows.append({"order_id":f"ORD{i:05d}","customer_name":n,
        "email":random.choice([n.split()[0].lower()+"@mail.com", ""]) if random.random()<.1 else n.strip().split()[0].lower()+"@mail.com",
        "order_date":d.strftime(random.choice(fmts)),
        "city":random.choice(cities[random.choice(list(cities))]),
        "category":random.choice(cats) if random.random()>.06 else None,
        "amount":amt if random.random()>.07 else None,
        "status":random.choice(["Delivered","delivered","DELIVERED","Shipped","shipped","Cancelled","cancelled"])})
df = pd.DataFrame(rows)
df = pd.concat([df, df.sample(120, random_state=1)]).sample(frac=1, random_state=3).reset_index(drop=True)
df.to_csv("messy_orders.csv", index=False)
print("rows:", len(df))
