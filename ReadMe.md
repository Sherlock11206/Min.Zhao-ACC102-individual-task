# RetailScope: E-Commerce Sales Intelligence Dashboard

## Project Overview

RetailScope is an interactive Python-based data analytics dashboard designed for retail managers and business analysts.
The project uses transactional e-commerce data to identify revenue drivers across countries, products, customers, and purchasing patterns.

The goal of this tool is to transform raw retail transaction records into actionable business insights through data cleaning, feature engineering, exploratory analysis, and interactive visualization.

## Analytical Objective

The main analytical question addressed in this project is:

**Which products, customers, and countries contribute most to e-commerce revenue, and how can these insights support retail decision-making?**

The dashboard is designed to support:

- Revenue monitoring
- Customer value identification
- Product performance analysis
- Time-based sales pattern discovery

## Dataset

This project uses the **Online Retail Dataset**, which contains transactional records from a UK-based online retailer.

**Source:** UCI Machine Learning Repository
**Dataset Name:** Online Retail

Main variables include:

- InvoiceNo
- StockCode
- Description
- Quantity
- InvoiceDate
- UnitPrice
- CustomerID
- Country

## How to Run the Dashboard

Install required packages:

```bash
pip install streamlit pandas plotly openpyxl
```

Run the application:

```bash
streamlit run app.py
```



























