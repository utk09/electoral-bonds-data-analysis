import streamlit as st
import plotly.express as px
import pandas as pd
from purchaser_details_analysis import (load_data_purchaser, analyze_purchasers, analyze_purchaser_sum,
                                        sum_denomination_year_purchaser, sum_denomination_month_purchaser, plot_graph_of_purchasers)
from encasher_details_analysis import (load_data_encasher, analyze_encashers, analyze_encasher_sum,
                                       sum_denomination_year_encasher, sum_denomination_month_encasher, plot_graph_of_encashers)


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
    df = load_data_purchaser(
        file_name='./01_Purchaser_Details.csv')  # Load data
    st.write(
        f"#### Number of Unique Purchasers: :blue[{analyze_purchasers(df)[0]}]")
    st.write(
        f"#### Total Denomination: :red[₹ {analyze_purchasers(df)[1]}] :green[(twelve thousand one hundred fifty-five crores and fifty-one lakhs thirty-two thousand)]")
    st.write(f"#### Mean Denomination: :orange[₹ {analyze_purchasers(df)[2]}]")
    st.write(f"#### Median Denomination: ₹ {analyze_purchasers(df)[3]}")
    st.write(
        f"#### 1st Quantile of Denomination: ₹ {analyze_purchasers(df)[4]}")
    st.write(
        f"#### 3rd Quantile of Denomination: ₹ {analyze_purchasers(df)[5]}")
    st.write(
        f"#### Interquantile Range of Denomination: ₹ {analyze_purchasers(df)[6]}")
    st.write(f"#### Quantiles over all data:")
    st.table(analyze_purchasers(df)[7])
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
    yearly_sum = sum_denomination_year_purchaser(df)
    fig_yearly = px.line(yearly_sum, x='Year', y='Denomination',
                         title='Sum of Denomination per Year', markers=True)
    st.plotly_chart(fig_yearly)
    st.write("---")

    st.subheader('Sum of Purchases (Denomination) by Month-Year')
    monthly_sum = sum_denomination_month_purchaser(df)
    fig_monthly = px.line(monthly_sum, x='Month-Year', y='Denomination',
                          title='Sum of Denomination per Month', markers=True)
    st.plotly_chart(fig_monthly)
    st.write("---")
    purchaser_names = st.text_input(
        "Enter names of purchasers, pipe separated (|), to view their history", "FUTURE GAMING AND HOTEL SERVICES PR | QWIKSUPPLYCHAINPRIVATELIMITED", placeholder="FUTURE GAMING AND HOTEL SERVICES PR | QWIKSUPPLYCHAINPRIVATELIMITED",
        key='purchaser_name',)
    if purchaser_names:
        purchaser_names = [x.strip() for x in purchaser_names.split('|')]
        st.plotly_chart(plot_graph_of_purchasers(purchaser_names))


def display_encasher_details():
    # Placeholder for Encasher Details Analysis
    st.write("## Encasher Details Analysis")
    st.write(
        "This section analyzes the details of encashers who encashed electoral bonds.")
    st.write("---")
    st.write("### CSV Dataset")
    st.write(
        "The dataset used for this analysis is the `02_Encasher_Details.csv` file.")
    pd_df = pd.read_csv('./02_Encasher_Details.csv')
    st.dataframe(pd_df, hide_index=True)
    st.write("---")
    df = load_data_encasher(file_name='./02_Encasher_Details.csv')  # Load data
    st.write(
        f"#### Number of Unique Encashers: :blue[{analyze_encashers(df)[0]}]")
    st.write(
        f"#### Total Denomination: :red[₹ {analyze_encashers(df)[1]}] :green[(twelve thousand seven hundred sixty-nine crores and eight lakhs ninety-three thousand)]")
    st.write(f"#### Mean Denomination: :orange[₹ {analyze_encashers(df)[2]}]")
    st.write(f"#### Median Denomination: ₹ {analyze_encashers(df)[3]}")
    st.write(
        f"#### 1st Quantile of Denomination: ₹ {analyze_encashers(df)[4]}")
    st.write(
        f"#### 3rd Quantile of Denomination: ₹ {analyze_encashers(df)[5]}")
    st.write(
        f"#### Interquantile Range of Denomination: ₹ {analyze_encashers(df)[6]}")
    st.write(f"#### Quantiles over all data:")
    st.table(analyze_encashers(df)[7])
    st.write(
        f"Read more about Quartiles [here](https://stats.stackexchange.com/questions/156778/percentile-vs-quantile-vs-quartile)")
    st.write(
        f"Quantiles are a measure of dispersion or spread of a set of data values. They divide the data set into four equal parts. Read about pandas.quantile [here](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.quantile.html)")
    st.write("---")
    st.subheader(
        'Sum of Encashments (Denomination) grouped by Encasher Name, along with Dates of Encashment')
    st.write(analyze_encasher_sum(df))
    st.write("---")
    st.subheader('Sum of Encashments (Denomination) by Year')
    yearly_sum = sum_denomination_year_encasher(df)
    fig_yearly = px.line(yearly_sum, x='Year', y='Denomination',
                         title='Sum of Denomination per Year', markers=True)
    st.plotly_chart(fig_yearly)
    st.write("---")

    st.subheader('Sum of Encashments (Denomination) by Month-Year')
    monthly_sum = sum_denomination_month_encasher(df)
    fig_monthly = px.line(monthly_sum, x='Month-Year', y='Denomination',
                          title='Sum of Denomination per Month', markers=True)
    st.plotly_chart(fig_monthly)
    st.write("---")
    encasher_names = st.text_input(
        "Enter names of encashers, pipe separated(|), to view their history", "JAMMU AND KASHMIR NATIONAL CONFERENCE | JHARKHAND MUKTI MORCHA", placeholder="BHARTIYA JANTA PARTY | PRESIDENT, ALL INDIA CONGRESS COMMITTEE",
        key='encasher_name',)
    if encasher_names:
        encasher_names = [x.strip() for x in encasher_names.split('|')]
        st.plotly_chart(plot_graph_of_encashers(encasher_names))


def display_about():
    st.write("""
        ## Introduction

        Electoral Bonds are a financial instrument for making donations to political parties. These bonds are issued by the Reserve Bank of India and can be purchased by any person or company incorporated in India. These bonds can be donated to any eligible political party, which has secured at least 1% of the votes polled in the most recent Lok Sabha or State election. The identity of the donor is not disclosed to the receiver or the public. The bonds are redeemable within 15 days and can be encashed by an eligible political party only through a designated bank account with the State Bank of India.

        ## Objective

        With the latest landmark decision by Hon'ble Supreme Court of India to make the details of Electoral Bonds public, the objective of this project is to analyze the data and understand the trends and patterns of donations to political parties through Electoral Bonds.

        ## Analysis

        The biggest hurdle in this analysis is the data being available in the form of PDFs. The data has been extracted from the PDFs and converted to CSV format for analysis. The GitHub repository for this project contains the code for extracting the data from PDFs.

        ## Data

        The data is obtained from the [Election Commision of India](https://www.eci.gov.in/disclosure-of-electoral-bonds) website. The data is available in the form of PDFs.

        ### How to Use:

        - Select the analysis you want to view using the options on the sidebar.
        - Interact with the visuals or tables presented for deeper insights.

        ### Contribute to the Project:

        - The source code for this project is available on [GitHub](https://github.com/utk09/electoral-bonds-data-analysis)
        - Detailed README is available here: [README](https://github.com/utk09/electoral-bonds-data-analysis/blob/main/README.md)
        - Feel free to contribute to the project by opening an issue or a pull request.
        - If you have any other analysis ideas, please open an issue and we can discuss it.

    """)
    st.write("---")

    st.write("### Notes and Observations about the data:")
    st.write(
        f"""##### The difference in total denominations between :orange[encashers] and :orange[purchasers] (₹127,690,893,000 - ₹121,555,132,000) is: :red[₹613,57,61,000] :green[(six hundred thirteen crores fifty-seven lakhs sixty-one thousand)]. This indicates that data regarding the :red[purchasers of bonds] worth over ₹600 crores remains :red[unidentified].""")
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
