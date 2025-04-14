import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Check if the CSV file exists
if not os.path.exists("clean_startup_funding.csv"):
    st.error("CSV file not found! Make sure it's in the same folder as this script.")
else:
    # Load dataset
    df = pd.read_csv('clean_startup_funding.csv')

    # Clean columns
    df.rename(columns={
        'date_dd/mm/yyyy': 'date',
        'startup_name': 'startup',
        'industry_vertical': 'industry',
        'city__location': 'city',
        'investors_name': 'investors',
        'investmentntype': 'investment_type',
        'amount_in_usd': 'amount'
    }, inplace=True)

    # Clean data
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['amount'] = df['amount'].astype(str).str.replace(',', '')
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    df.dropna(subset=['startup', 'amount'], inplace=True)
    df['year'] = df['date'].dt.year

    # Streamlit UI
    st.title("Indian Startup Funding Analysis")

    # Sidebar Filters
    selected_year = st.sidebar.selectbox("Select Year", sorted(df['year'].dropna().unique()))
    selected_city = st.sidebar.multiselect("Select Cities", df['city'].dropna().unique())

    # Apply filters
    filtered_df = df[df['year'] == selected_year]
    if selected_city:
        filtered_df = filtered_df[filtered_df['city'].isin(selected_city)]

    # Show filtered table
    st.subheader("Filtered Data")
    st.dataframe(filtered_df)

    # Total funding
    st.metric("Total Funding", f"${filtered_df['amount'].sum():,.0f}")

    # Bar chart for top industries
    top_industries = filtered_df.groupby('industry')['amount'].sum().sort_values(ascending=False).head(5)

    st.subheader("Top Industries by Funding")
    fig, ax = plt.subplots()
    top_industries.plot(kind='barh', ax=ax)
    st.pyplot(fig)
