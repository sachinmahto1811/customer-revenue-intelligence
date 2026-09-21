import pandas as pd

customers = pd.read_csv("data/customers.csv")
orders = pd.read_csv("data/orders.csv", parse_dates=["order_date"])
df = orders.merge(customers, on="customer_id", how="left")

print("Net revenue:", round(df["net_revenue"].sum(), 2))
print("Return rate:", round((df["return_amount"] > 0).mean() * 100, 2), "%")

rfm = (df.groupby("customer_id", as_index=False)
         .agg(last_order=("order_date","max"),
              frequency=("order_id","count"),
              monetary=("net_revenue","sum")))
snapshot = df["order_date"].max() + pd.Timedelta(days=1)
rfm["recency_days"] = (snapshot - rfm["last_order"]).dt.days

channel = (df.groupby("acquisition_channel", as_index=False)
             .agg(customers=("customer_id","nunique"),
                  net_revenue=("net_revenue","sum")))
channel["revenue_per_customer"] = channel["net_revenue"] / channel["customers"]
print("\nChannel value:")
print(channel.sort_values("revenue_per_customer", ascending=False).to_string(index=False))
