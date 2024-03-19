import streamlit as st
import plotly.express as px
import pandas as pd
from purchaser_details_analysis import (load_data, analyze_purchasers, analyze_purchaser_sum,
                                        sum_denomination_year, sum_denomination_month, plot_graph_of_purchasers)


def display_purchaser_details():
    st.write("## Purchaser Details Analysis")
    st.write(
        "This section analyzes the details of purchasers who bought electoral bonds.")
    st.write("---")
    st.write("### CSV Dataset")
    st.write(
        "The dataset used for this analysis is the `01_Purchaser_Details.csv` file.")
    pd_df = pd.read_csv('./01_Purchaser_Details.csv')
    st.dataframe(pd_df, hide_index=True)
    st.write("---")
    df = load_data(file_name='./01_Purchaser_Details.csv')  # Load data
    st.write(f"#### Number of Unique Purchasers: {analyze_purchasers(df)[0]}")
    st.write(f"#### Mean Denomination: ₹ {analyze_purchasers(df)[1]}")
    st.write(f"#### Median Denomination: ₹ {analyze_purchasers(df)[2]}")
    st.write(
        f"#### 1st Quantile of Denomination: ₹ {analyze_purchasers(df)[3]}")
    st.write(
        f"#### 3rd Quantile of Denomination: ₹ {analyze_purchasers(df)[4]}")
    st.write(
        f"#### Interquantile Range of Denomination: ₹ {analyze_purchasers(df)[5]}")
    st.write(f"#### Quantiles over all data:")
    st.table(analyze_purchasers(df)[6])
    st.write(
        f"Read more about Quartiles [here](https://stats.stackexchange.com/questions/156778/percentile-vs-quantile-vs-quartile)")
    st.write(
        f"Quantiles are a measure of dispersion or spread of a set of data values. They divide the data set into four equal parts. Read about pandas.quantile [here](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.quantile.html)")

    st.write("---")
    st.subheader(
        'Sum of Purchases (Denomination) grouped by Purchaser Name, along with Dates of Purchase')
    st.write(analyze_purchaser_sum(df))
    st.write("---")
    st.subheader('Sum of Purchases (Denomination) by Year')
    yearly_sum = sum_denomination_year(df)
    fig_yearly = px.line(yearly_sum, x='Year', y='Denomination',
                         title='Sum of Denomination per Year', markers=True)
    st.plotly_chart(fig_yearly)
    st.write("---")

    st.subheader('Sum of Purchases (Denomination) by Month-Year')
    monthly_sum = sum_denomination_month(df)
    fig_monthly = px.line(monthly_sum, x='Month-Year', y='Denomination',
                          title='Sum of Denomination per Month', markers=True)
    st.plotly_chart(fig_monthly)
    st.write("---")
    names = st.text_input(
        "Enter names of purchasers, comma separated, to view their history", "FUTURE GAMING AND HOTEL SERVICES PR,QWIKSUPPLYCHAINPRIVATELIMITED", placeholder="FUTURE GAMING AND HOTEL SERVICES PR,QWIKSUPPLYCHAINPRIVATELIMITED",
        key='purchaser_name',)
    if names:
        names = names.strip().split(',')
        st.plotly_chart(plot_graph_of_purchasers(names))


def display_encasher_details():
    # Placeholder for Encasher Details Analysis
    st.write("## Encasher Details Analysis")
    st.write("This section is under development.")


def display_about():
    st.write("""
        ## About This Analysis

        This Streamlit application is designed to analyze and visualize electoral bond data.
        Users can switch between different types of analyses such as Purchaser Details Analysis and Encasher Details Analysis.

        ### How to Use:
        - Select the analysis you want to view using the options on the sidebar.
        - Interact with the visuals or tables presented for deeper insights.

        ### Data Details:
        The analyses include unique purchaser count, total denomination by purchaser, and temporal denomination summaries.

        ### Run the App:
        To run this app, use the command: `streamlit run main.py`.

        For more information on electoral bonds, visit [Electoral Commission's website](https://www.eci.gov.in/disclosure-of-electoral-bonds).
    """)
    st.write("---")


def main():
    st.set_page_config(page_title="Electoral Bonds Analysis",
                       page_icon=":bar_chart:", layout="wide")

    # Sidebar for analysis selection
    analysis_option = st.sidebar.radio(
        'Navigation',
        ('About', 'Purchaser Details Analysis', 'Encasher Details Analysis')
    )

    # Conditional display based on sidebar selection
    if analysis_option == 'About':
        display_about()
    elif analysis_option == 'Purchaser Details Analysis':
        display_purchaser_details()
    elif analysis_option == 'Encasher Details Analysis':
        display_encasher_details()


if __name__ == "__main__":
    main()
