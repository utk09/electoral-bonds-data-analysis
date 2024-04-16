# purchaser_details_analysis.py

import pandas as pd
import streamlit as st
import plotly.express as px


@st.cache_data
def load_data_purchaser(file_name):
    data = pd.read_csv(file_name)
    data['Date of Purchase'] = pd.to_datetime(
        data['Date of Purchase'], format='%d/%b/%Y')
    data['Year'] = data['Date of Purchase'].dt.year
    data['Year'] = data['Year'].apply(lambda x: int(str(x).replace(',', '')))
    data['Month-Year'] = data['Date of Purchase'].dt.strftime('%b %Y')
    return data


def analyze_purchasers(df):
    # number of unique purchasers
    unique_purchasers = df['Purchaser Name'].nunique()
    # sum of denominations
    sum_denomination = df['Denomination'].sum()
    # Mean, Median, Mode
    mean = df['Denomination'].mean()
    median = df['Denomination'].median()

    # Quantiles
    q1 = df['Denomination'].quantile(0.25)
    q3 = df['Denomination'].quantile(0.75)
    iqr = q3 - q1

    # Quantiles over all data
    qd = df.quantile([.25, 0.50, 0.75], method="table",
                     interpolation="nearest", numeric_only=False)
    # Return results
    return unique_purchasers, sum_denomination, mean, median, q1, q3, iqr, qd


def analyze_purchaser_sum(df):
    # Convert epoch time to normal date
    df['Date of Purchase'] = pd.to_datetime(df['Date of Purchase'], unit='ms')

    # return sum of purchases (denomination) grouped by purchaser name, along with the dates of purchase in dd/mm/yyyy as a list in the same row, sorted by latest date first
    result = df.groupby('Purchaser Name').agg(
        {'Denomination': 'sum', 'Date of Purchase': lambda x: x.sort_values(ascending=False).dt.strftime('%d/%m/%Y').tolist()}).reset_index()
    return result


def sum_denomination_year_purchaser(df):
    return df.groupby('Year')['Denomination'].sum().reset_index()


def sum_denomination_month_purchaser(df):
    monthly_sum = df.groupby('Month-Year')['Denomination'].sum().reset_index()
    monthly_sum['Month-Year'] = pd.to_datetime(
        monthly_sum['Month-Year'], format='%b %Y')
    monthly_sum.sort_values('Month-Year', inplace=True)
    return monthly_sum


def plot_graph_of_purchasers(purchasers_list):
    # take a list of purchasers, and plot a graph of their purchases over time
    df = load_data_purchaser(file_name='./01_Purchaser_Details.csv')
    st.write(purchasers_list)
    df = df[df['Purchaser Name'].isin(purchasers_list)]
    st.dataframe(df, hide_index=True)

    purchaser_name = df.groupby(['Month-Year', 'Purchaser Name'])[
        'Denomination'].sum().reset_index()

    purchaser_name['Month-Year'] = pd.to_datetime(
        purchaser_name['Month-Year'], format='%b %Y')
    purchaser_name.sort_values('Month-Year', inplace=True)

    # write name of month on x-axis
    fig = px.line(purchaser_name, x='Month-Year', y='Denomination',
                  color='Purchaser Name', title='Purchaser Name vs Denomination', markers=True)
    return fig
