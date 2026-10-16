"""Generates SYNTHETIC retail sales data and builds a self-contained interactive dashboard.html"""
import random, pandas as pd
random.seed(7)
prod = {"Technology":{"Laptop":55000,"Headphones":3500,"Smartphone":22000,"Monitor":12000,"Keyboard":1800},
        "Furniture":{"Office Chair":9000,"Desk":14000,"Bookshelf":6500,"Lamp":1500,"Filing Cabinet":7000},
        "Office Supplies":{"Notebook":120,"Printer Paper":450,"Pens (box)":250,"Stapler":300,"Binder":200}}
regions = {"North":1.0,"South":1.25,"East":.8,"West":1.1}
rows=[]
for y in (2024,2025):
    for m in range(1,13):
        season = 1+.35*(m in (10,11,12))+.1*(y==2025)
        for r,rw in regions.items():
            for c,ps in prod.items():
                for p,price in ps.items():
                    q = max(0,int(random.gauss(12,4)*rw*season*(3 if price<500 else 1)))
                    disc = random.choice([0,0,.1,.2]); sales = round(q*price*(1-disc))
                    margin = {"Technology":.18,"Furniture":.08,"Office Supplies":.3}[c]-disc*.6+random.uniform(-.03,.03)
                    rows.append([f"{y}-{m:02d}",y,r,c,p,q,sales,round(sales*margin)])
df = pd.DataFrame(rows, columns=["month","year","region","category","product","orders","sales","profit"])
df.to_csv("sales_data.csv", index=False)
html = open("template.html").read().replace("__DATA__", df.to_json(orient="records"))
open("dashboard.html","w").write(html)
print(len(df), "rows | total sales", int(df.sales.sum()))
