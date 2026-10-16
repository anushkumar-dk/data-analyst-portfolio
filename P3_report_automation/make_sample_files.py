"""Creates 3 SYNTHETIC monthly sales files with inconsistent headers, like real client exports."""
import random, pandas as pd
random.seed(11)
prods=["Laptop","Headphones","Monitor","Keyboard","Printer"]; regs=["North","South","East","West"]
heads=[("Date","Product","Region","Qty","Revenue"),("date","product name","region","quantity","revenue (inr)"),("DATE","PRODUCT","REGION","QTY","REVENUE")]
for mo,h in zip(["2025-01","2025-02","2025-03"],heads):
    rows=[]
    for _ in range(60):
        q=random.randint(1,9)
        rows.append([f"{mo}-{random.randint(1,28):02d}",random.choice(prods)+random.choice(["",""," "]),random.choice(regs),q,q*random.choice([2500,4000,12000,1800,9000])])
    rows.append(list(rows[0])); rows[5][3]=None
    pd.DataFrame(rows,columns=h).to_csv(f"data/sales_{mo}.csv",index=False)
