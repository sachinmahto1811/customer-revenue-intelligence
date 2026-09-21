import pandas as pd

customers = pd.read_csv("data/customers.csv")
orders = pd.read_csv("data/orders.csv", parse_dates=["order_date"])
df = orders.merge(customers, on="customer_id", how="left")

net_revenue = df["net_revenue"].sum()
return_rate = (df["return_amount"] > 0).mean()

print(f"Net revenue: {net_revenue:,.2f}")
print(f"Return rate: {return_rate:.2%}")

rfm = (
    df.groupby("customer_id", as_index=False)
      .agg(
          last_order=("order_date", "max"),
          frequency=("order_id", "count"),
          monetary=("net_revenue", "sum")
      )
)

snapshot = df["order_date"].max() + pd.Timedelta(days=1)
rfm["recency_days"] = (snapshot - rfm["last_order"]).dt.days

# Quartile scoring: lower recency is better; higher frequency/monetary is better.
rfm["r_score"] = pd.qcut(
    rfm["recency_days"].rank(method="first", ascending=False),
    4,
    labels=[1, 2, 3, 4]
).astype(int)

rfm["f_score"] = pd.qcut(
    rfm["frequency"].rank(method="first"),
    4,
    labels=[1, 2, 3, 4]
).astype(int)

rfm["m_score"] = pd.qcut(
    rfm["monetary"].rank(method="first"),
    4,
    labels=[1, 2, 3, 4]
).astype(int)

rfm["rfm_score"] = rfm["r_score"] + rfm["f_score"] + rfm["m_score"]

def segment(score):
    if score >= 10:
        return "High Value"
    if score >= 7:
        return "Core"
    if score >= 5:
        return "Developing"
    return "Low Engagement"

rfm["segment"] = rfm["rfm_score"].apply(segment)

print("\nRFM segment distribution:")
print(rfm["segment"].value_counts().to_string())

channel = (
    df.groupby("acquisition_channel", as_index=False)
      .agg(
          customers=("customer_id", "nunique"),
          net_revenue=("net_revenue", "sum")
      )
)

channel["revenue_per_customer"] = (
    channel["net_revenue"] / channel["customers"]
)

print("\nAcquisition-channel value:")
print(
    channel.sort_values("revenue_per_customer", ascending=False)
           .to_string(index=False)
)

print("\nTop customers by RFM score and monetary value:")
print(
    rfm.sort_values(["rfm_score", "monetary"], ascending=False)
       [["customer_id", "recency_days", "frequency", "monetary", "rfm_score", "segment"]]
       .head(15)
       .to_string(index=False)
)
