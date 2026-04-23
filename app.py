import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------
# Page Configuration
# -------------------------
st.set_page_config(page_title="RetailScope Dashboard", layout="wide")

# -------------------------
# Load Data
# -------------------------
df = pd.read_csv("online_retail.csv")

# -------------------------
# Data Cleaning
# -------------------------
df = df.dropna()
df = df[df['Quantity'] > 0]
df = df[df['UnitPrice'] > 0]
df = df.drop_duplicates()

# -------------------------
# Feature Engineering
# -------------------------
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df['Revenue'] = df['Quantity'] * df['UnitPrice']
df['Month'] = df['InvoiceDate'].dt.to_period('M').astype(str)
df['Weekday'] = df['InvoiceDate'].dt.day_name()

# -------------------------
# Sidebar Filters
# -------------------------
st.sidebar.title("Filter Options")

country = st.sidebar.multiselect(
    "Select Country",
    options=df['Country'].unique(),
    default=df['Country'].unique()
)

month = st.sidebar.multiselect(
    "Select Month",
    options=df['Month'].unique(),
    default=df['Month'].unique()
)

filtered_df = df[
    (df['Country'].isin(country)) &
    (df['Month'].isin(month))
]

# -------------------------
# Title
# -------------------------
st.title("RetailScope: E-Commerce Sales Intelligence Dashboard")

st.markdown("Interactive retail analytics for product, customer, and market performance.")

# -------------------------
# KPI Metrics
# -------------------------
total_revenue = filtered_df['Revenue'].sum()
total_orders = filtered_df['InvoiceNo'].nunique()
total_customers = filtered_df['CustomerID'].nunique()

col1, col2, col3 = st.columns(3)

col1.metric("Total Revenue", f"${total_revenue:,.2f}")
col2.metric("Total Orders", total_orders)
col3.metric("Total Customers", total_customers)

# -------------------------
# Revenue by Country
# -------------------------
country_sales = filtered_df.groupby('Country')['Revenue'].sum().reset_index()

fig1 = px.bar(
    country_sales,
    x='Country',
    y='Revenue',
    title='Revenue by Country'
)

st.plotly_chart(fig1, use_container_width=True)

# -------------------------
# Monthly Revenue Trend
# -------------------------
monthly_sales = filtered_df.groupby('Month')['Revenue'].sum().reset_index()

fig2 = px.line(
    monthly_sales,
    x='Month',
    y='Revenue',
    title='Monthly Revenue Trend'
)

st.plotly_chart(fig2, use_container_width=True)

# -------------------------
# Product Performance Analysis
# -------------------------
st.subheader("Product Performance Analysis")

# Quantity
top_products_qty = filtered_df.groupby('Description')['Quantity'].sum().sort_values(ascending=False).head(10).reset_index()

fig3 = px.bar(
    top_products_qty,
    x='Description',
    y='Quantity',
    title='Top 10 Products by Quantity'
)

st.plotly_chart(fig3, use_container_width=True)

# Revenue
top_products_rev = filtered_df.groupby('Description')['Revenue'].sum().sort_values(ascending=False).head(10).reset_index()

fig4 = px.bar(
    top_products_rev,
    x='Description',
    y='Revenue',
    title='Top 10 Products by Revenue'
)

st.plotly_chart(fig4, use_container_width=True)

# Revenue Share
fig5 = px.pie(
    top_products_rev,
    names='Description',
    values='Revenue',
    title='Top Product Revenue Share'
)

st.plotly_chart(fig5, use_container_width=True)

# Product Trend
selected_product = st.selectbox(
    "Select Product for Trend Analysis",
    filtered_df['Description'].dropna().unique()
)

product_trend = filtered_df[
    filtered_df['Description'] == selected_product
].groupby('Month')['Revenue'].sum().reset_index()

fig6 = px.line(
    product_trend,
    x='Month',
    y='Revenue',
    title='Product Revenue Trend'
)

st.plotly_chart(fig6, use_container_width=True)

# -------------------------
# Customer Analysis
# -------------------------
st.subheader("Customer Value Analysis")

top_customers = filtered_df.groupby('CustomerID')['Revenue'].sum().sort_values(ascending=False).head(10).reset_index()

fig7 = px.bar(
    top_customers,
    x='CustomerID',
    y='Revenue',
    title='Top 10 Customers by Revenue'
)

st.plotly_chart(fig7, use_container_width=True)

# -------------------------
# Order Value Distribution
# -------------------------
order_value = filtered_df.groupby('InvoiceNo')['Revenue'].sum().reset_index()

fig8 = px.histogram(
    order_value,
    x='Revenue',
    nbins=30,
    title='Order Value Distribution'
)

st.plotly_chart(fig8, use_container_width=True)

# -------------------------
# Weekday Revenue
# -------------------------
weekday_sales = filtered_df.groupby('Weekday')['Revenue'].sum().reset_index()

fig9 = px.bar(
    weekday_sales,
    x='Weekday',
    y='Revenue',
    title='Revenue by Weekday'
)

st.plotly_chart(fig9, use_container_width=True)

# -------------------------
# Heatmap
# -------------------------
pivot = filtered_df.pivot_table(
    values='Revenue',
    index='Country',
    columns='Month',
    aggfunc='sum'
).fillna(0)

fig10 = px.imshow(
    pivot,
    title='Country-Month Revenue Heatmap'
)

st.plotly_chart(fig10, use_container_width=True)

# -------------------------
# Business Insights
# -------------------------
st.subheader("Business Insights")

top_country = country_sales.sort_values(by='Revenue', ascending=False).iloc[0]['Country']
top_product = top_products_rev.iloc[0]['Description']
top_customer = top_customers.iloc[0]['CustomerID']

st.write(f"Highest revenue country: **{top_country}**")
st.write(f"Top revenue-generating product: **{top_product}**")
st.write(f"Highest value customer: **{top_customer}**")