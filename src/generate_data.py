from pathlib import Path
import random
from datetime import datetime, timedelta
import pandas as pd

random.seed(42)
customers = []
for i in range(1200):
    customers.append({
        "customer_id": f"C{i+1:05d}",
        "acquisition_channel": random.choice(["Organic","Paid Search","Social","Referral","Email"]),
        "region": random.choice(["North","West","South","East"])
    })

orders = []
start = datetime(2025, 1, 1)
for i in range(7000):
    customer_id = random.choice(customers)["customer_id"]
    gross = round(random.uniform(250, 6000), 2)
    returned = random.random() < 0.09
    orders.append({
        "order_id": f"O{i+1:06d}",
        "customer_id": customer_id,
        "order_date": start + timedelta(days=random.randint(0, 540)),
        "gross_revenue": gross,
        "return_amount": gross if returned else 0,
        "net_revenue": 0 if returned else gross
    })

Path("data").mkdir(exist_ok=True)
pd.DataFrame(customers).to_csv("data/customers.csv", index=False)
pd.DataFrame(orders).to_csv("data/orders.csv", index=False)
print("Synthetic datasets created.")
