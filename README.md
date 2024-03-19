# Electoral Bonds Data Analysis

## Introduction

Electoral Bonds are a financial instrument for making donations to political parties. These bonds are issued by the Reserve Bank of India and can be purchased by any person or company incorporated in India. These bonds can be donated to any eligible political party, which has secured at least 1% of the votes polled in the most recent Lok Sabha or State election. The identity of the donor is not disclosed to the receiver or the public. The bonds are redeemable within 15 days and can be encashed by an eligible political party only through a designated bank account with the State Bank of India.

## Objective

With the latest landmark decision by Hon'ble Supreme Court of India to make the details of Electoral Bonds public, the objective of this project is to analyze the data and understand the trends and patterns of donations to political parties through Electoral Bonds.

## Data

The data is obtained from the [Election Commision of India](https://www.eci.gov.in/disclosure-of-electoral-bonds) website. The data is available in the form of PDFs.

## Current Status

The project is in the initial phase of data collection and cleaning. The data is available in the form of PDFs and needs to be converted into a structured format for analysis, in this case, CSV.

The following data has been collected and cleaned/converted so far:

- `Purchaser_Details_Final.pdf` -> `01_Purchaser_Details.csv`
- `Encashment_Details_Final.pdf` -> `02_Encasher_Details.csv`

The pdf files are available in the `pdf_data` directory.

## Analysis

The analysis will be performed using Python and the following libraries:

- PyPDF2
- pandas
- plotly
- streamlit

## Installation

- Clone the repository:

```bash
git clone
```

- Create a virtual environment and install the dependencies:

```bash
cd electoral-bonds-data-analysis # Change to the project directory

python3 -m venv electoralbonds # Create a virtual environment

# Activate the virtual environment
# On Windows
electoralbonds\Scripts\activate

# On macOS and Linux
source electoralbonds/bin/activate
```

- Install the dependencies:

```bash
pip install -r requirements.txt
```

## Usage

The project is divided into two parts:

1. Data Collection and Cleaning
2. Data Analysis

### Data Collection and Cleaning

The data is available in the form of PDFs. The data needs to be converted into a structured format for analysis, in this case, CSV.

- Run the following command to convert the PDFs into CSVs:

```bash
python 01_clean_purchaser_data.py # Convert the Purchaser_Details_Final PDF into CSV
```

```bash
python 02_clean_encasher_data.py # Convert the Encashment_Details_Final PDF into CSV
```

The CSV files will be saved in the root of the project.

### Data Analysis

Run the following command to start the Streamlit app:

```bash
streamlit run main.py
```

Open the URL in the browser to view the app.
