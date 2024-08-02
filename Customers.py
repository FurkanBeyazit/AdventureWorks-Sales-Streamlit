import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


cust = pd.read_pickle('cleaned_customer.pkl')


year = st.sidebar.multiselect('Select Year', options=cust['Year'].unique(), default=cust['Year'].unique())
month = st.sidebar.multiselect('Select Month', options=cust['Month'].unique(), default=cust['Month'].unique())
customer = st.sidebar.multiselect('Select Customer', options=cust['Customer'].unique())
customer_city = st.sidebar.multiselect('Select Customer City', options=cust['City'].unique())
product_category = st.sidebar.multiselect('Select Product Category', options=cust['Category'].unique())


filtered_cust = cust[
    (cust['Year'].isin(year) if year else cust['Year']) &
    (cust['Month'].isin(month) if month else cust['Month']) &
    (cust['Customer'].isin(customer) if customer else cust['Customer']) &
    (cust['City'].isin(customer_city) if customer_city else cust['City']) &
    (cust['Category'].isin(product_category) if product_category else cust['Category'])
]


total_sales = filtered_cust['Sales Amount'].sum()
total_customers = filtered_cust['Customer'].nunique()

st.metric("Sales", f"${total_sales / 1e6:.2f}M")
st.metric("Customers", f"{total_customers}K")


top_cities = filtered_cust.groupby(['City', 'Category'])['Sales Amount'].sum().unstack().fillna(0)
top_cities = top_cities.sum(axis=1).nlargest(10).index
top_cities_data = filtered_cust[filtered_cust['City'].isin(top_cities)].groupby(['City', 'Category'])['Sales Amount'].sum().unstack().fillna(0)

st.subheader('Sales by Top 10 Customer City and Product Category')
fig, ax = plt.subplots()
top_cities_data.plot(kind='barh', stacked=True, ax=ax)
st.pyplot(fig)


top_customers = filtered_cust.groupby('Customer')['Sales Amount'].sum().nlargest(5).index
monthly_sales = filtered_cust[filtered_cust['Customer'].isin(top_customers)].pivot_table(values='Sales Amount', index='Customer', columns='Month', aggfunc='sum', fill_value=0)

st.subheader('Monthly Sales by Top 5 Customers')
fig, ax = plt.subplots(figsize=(12, 8))
sns.heatmap(monthly_sales, cmap='Blues', linewidths=0.1, linecolor='gray', ax=ax, annot=True, fmt=".1f")
st.pyplot(fig)


category_sales = filtered_cust.pivot_table(values='Sales Amount', index='Customer', columns='Category', aggfunc='sum', fill_value=0)

st.subheader('Sales by Customer and Product Category')
fig, ax = plt.subplots(figsize=(12, 8))
category_sales.plot(kind='barh', stacked=True, ax=ax)
st.pyplot(fig)
