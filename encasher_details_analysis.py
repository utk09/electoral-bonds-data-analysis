# encasher_details_analysis.py

import pandas as pd
import streamlit as st
import plotly.express as px

"""
Sr No.,Date of Encashment,Name of the Political Party,Denomination
1,12/Apr/2019,ALL INDIA ANNA DRAVIDA MUNNETRA KAZHAGAM,1000000
2,12/Apr/2019,ALL INDIA ANNA DRAVIDA MUNNETRA KAZHAGAM,1000000
3,12/Apr/2019,ALL INDIA ANNA DRAVIDA MUNNETRA KAZHAGAM,10000000
"""


@st.cache_data
def load_data_encasher(file_name):
    data = pd.read_csv(file_name)
    data['Date of Encashment'] = pd.to_datetime(
        data['Date of Encashment'], format='%d/%b/%Y')
    data['Year'] = data['Date of Encashment'].dt.year
    data['Year'] = data['Year'].apply(lambda x: int(str(x).replace(',', '')))
    data['Month-Year'] = data['Date of Encashment'].dt.strftime('%b %Y')
    return data


def analyze_encashers(df):
    # number of unique encashers
    unique_encashers = df['Name of the Political Party'].nunique()
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
    return unique_encashers, mean, median, q1, q3, iqr, qd


def analyze_encasher_sum(df):
    # Convert epoch time to normal date
    df['Date of Encashment'] = pd.to_datetime(
        df['Date of Encashment'], unit='ms')

    # return sum of encashments (denomination) grouped by encasher name, along with the dates of encashment in dd/mm/yyyy as a list in the same row, sorted by latest date first
    result = df.groupby('Name of the Political Party').agg(
        {'Denomination': 'sum', 'Date of Encashment': lambda x: x.sort_values(ascending=False).dt.strftime('%d/%m/%Y').tolist()}).reset_index()
    return result


def sum_denomination_year_encasher(df):
    return df.groupby('Year')['Denomination'].sum().reset_index()


def sum_denomination_month_encasher(df):
    monthly_sum = df.groupby('Month-Year')['Denomination'].sum().reset_index()
    monthly_sum['Month-Year'] = pd.to_datetime(
        monthly_sum['Month-Year'], format='%b %Y')
    monthly_sum.sort_values('Month-Year', inplace=True)
    return monthly_sum


def plot_graph_of_encashers(encashers_list):
    # take a list of encashers, and plot a graph of their encashments over time
    df = load_data_encasher(file_name='./02_Encasher_Details.csv')
    st.write(encashers_list)
    df = df[df['Name of the Political Party'].isin(encashers_list)]
    st.dataframe(df, hide_index=True)

    # plot by month-year, sorted in descending order
    encasher_name = df.groupby(['Month-Year', 'Name of the Political Party'])[
        'Denomination'].sum().reset_index()

    encasher_name['Month-Year'] = pd.to_datetime(
        encasher_name['Month-Year'], format='%b %Y')
    encasher_name.sort_values('Month-Year', inplace=True)

    fig = px.line(encasher_name, x='Month-Year', y='Denomination',
                  color='Name of the Political Party', title='Sum of Encashments (Denomination) by Month-Year', markers=True)
    return fig
