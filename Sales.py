import streamlit as st
import pandas as pd
import numpy as np


cust = pd.read_pickle('cleaned_customer.pkl')


st.title("AdventureWorks - Sales Dashboard")


cust['Profit'] = cust['Sales Amount'] - cust['Total Product Cost']


year = st.sidebar.multiselect('Select Year', options=cust['Year'].unique(), default=cust['Year'].unique())
month = st.sidebar.multiselect('Select Month', options=cust['Month'].unique(), default=cust['Month'].unique())
city = st.sidebar.multiselect('Select City', options=cust['City'].unique())
product = st.sidebar.multiselect('Select Product', options=cust['Product'].unique())
category = st.sidebar.multiselect('Select Category', options=cust['Category'].unique())


filtered_cust = cust[
    (cust['Year'].isin(year) if year else cust['Year']) &
    (cust['Month'].isin(month) if month else cust['Month']) &
    (cust['City'].isin(city) if city else cust['City']) &
    (cust['Product'].isin(product) if product else cust['Product']) &
    (cust['Category'].isin(category) if category else cust['Category'])
]

st.line_chart(filtered_cust.groupby('Month')[['Sales Amount', 'Profit']].sum())


st.subheader('Top 10 Customers by Sales')
st.bar_chart(filtered_cust['Customer'].value_counts().head(10))

st.subheader('Top 10 Products by Sales')
top_products = filtered_cust.groupby('Product')['Sales Amount'].sum().nlargest(10)
st.bar_chart(top_products)