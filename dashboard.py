import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Mishra's Profit Dashboard", layout="wide")

# -----------------------------
# 📊 LOAD DATA (REAL-LIKE)
# -----------------------------
df = pd.DataFrame({
    "Date": pd.date_range(start="2024-01-01", periods=12, freq="M"),
    "Product": ["A","B","C","D","E","A","B","C","D","E","A","B"],
    "Category": ["Tech","Tech","Office","Office","Furniture","Tech","Tech","Office","Office","Furniture","Tech","Tech"],
    "Region": ["North","South","East","West","North","South","East","West","North","South","East","West"],
    "Revenue": [10000,12000,9000,15000,17000,20000,18000,16000,14000,13000,21000,22000],
    "Cost": [7000,8000,6000,9000,10000,12000,11000,9500,8000,7000,15000,16000]
})

df["Profit"] = df["Revenue"] - df["Cost"]
df["Profit Margin %"] = (df["Profit"] / df["Revenue"]) * 100

# -----------------------------
# 🎛️ SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("Filters")

date_range = st.sidebar.date_input("Select Date Range", [df["Date"].min(), df["Date"].max()])
category = st.sidebar.multiselect("Category", df["Category"].unique(), default=df["Category"].unique())
region = st.sidebar.multiselect("Region", df["Region"].unique(), default=df["Region"].unique())

# Apply filters
filtered_df = df[
    (df["Date"] >= pd.to_datetime(date_range[0])) &
    (df["Date"] <= pd.to_datetime(date_range[1])) &
    (df["Category"].isin(category)) &
    (df["Region"].isin(region))
]

# -----------------------------
# 🔝 KPI CARDS
# -----------------------------
total_profit = filtered_df["Profit"].sum()
total_revenue = filtered_df["Revenue"].sum()
total_cost = filtered_df["Cost"].sum()
avg_margin = filtered_df["Profit Margin %"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Profit", f"₹{total_profit}")
col2.metric("📈 Revenue", f"₹{total_revenue}")
col3.metric("💸 Cost", f"₹{total_cost}")
col4.metric("📊 Margin %", f"{avg_margin:.2f}%")

# 🚨 Alert
if total_profit < 5000:
    st.error("⚠️ Warning: Profit is very low!")

# -----------------------------
# 📈 CHARTS
# -----------------------------
col5, col6 = st.columns(2)

# Profit Trend
fig1 = px.line(filtered_df, x="Date", y="Profit", title="Profit Trend", markers=True)
fig1.update_layout(template="plotly_dark")

# Combo Chart
fig2 = go.Figure()
fig2.add_trace(go.Bar(x=filtered_df["Date"], y=filtered_df["Revenue"], name="Revenue"))
fig2.add_trace(go.Scatter(x=filtered_df["Date"], y=filtered_df["Profit"], name="Profit", mode="lines+markers"))
fig2.update_layout(title="Revenue vs Profit", template="plotly_dark")

col5.plotly_chart(fig1, use_container_width=True)
col6.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# 📊 SECOND ROW
# -----------------------------
col7, col8 = st.columns(2)

# Top 5 Products
top_products = filtered_df.groupby("Product")["Profit"].sum().sort_values(ascending=False).head(5)
fig3 = px.bar(top_products, title="Top 5 Products by Profit")
fig3.update_layout(template="plotly_dark")

# Distribution
fig4 = px.histogram(filtered_df, x="Profit", title="Profit Distribution")
fig4.update_layout(template="plotly_dark")

col7.plotly_chart(fig3, use_container_width=True)
col8.plotly_chart(fig4, use_container_width=True)

# -----------------------------
# 🧠 BUSINESS INSIGHTS (IMPORTANT)
# -----------------------------
st.subheader("📌 Business Insights")

if len(filtered_df) > 0:
    best_product = top_products.index[0]
    worst_region = filtered_df.groupby("Region")["Profit"].sum().idxmin()

    st.write(f"✅ Most profitable product: **{best_product}**")
    st.write(f"⚠️ Lowest performing region: **{worst_region}**")

    if avg_margin < 30:
        st.write("📉 Profit margin is low — reduce cost or increase price.")
    else:
        st.write("📈 Business is performing well with good margins.")

# -----------------------------
# 📋 DATA TABLE
# -----------------------------
st.subheader("📄 Data")
st.dataframe(filtered_df)