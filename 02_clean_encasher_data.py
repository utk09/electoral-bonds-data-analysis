import PyPDF2  # Import PyPDF2 for reading PDF files
import pandas as pd  # Import pandas for data manipulation
import re  # Import re for regular expressions


def process_text(texts):
    all_rows = []  # List to store all rows of data
    # Loop through each extracted text block (typically one per PDF page)
    for text in texts:
        # Find all starting positions of date strings within the text using a regular expression
        date_starts = [match.start() for match in re.finditer(
            r'\d{2}/[A-Za-z]{3}/20\d{2}', text)]
        # Create segments of text between each pair of dates (assuming each segment is a record)
        segments = [text[date_starts[i]:date_starts[i + 1]]
                    for i in range(len(date_starts) - 1)]
        # If there are dates, add the last segment from the last date to the end of text
        if date_starts:
            segments.append(text[date_starts[-1]:])

        for segment in segments:  # Process each text segment
            # Find the date and denomination in the segment using regular expressions
            date_match = re.search(r'\d{2}/[A-Za-z]{3}/20\d{2}', segment)
            denomination_match = re.search(
                r'(1,000|10,000|1,00,000|10,00,000|1,00,00,000|10,00,00,000)', segment)
            # If both a date and a denomination were found
            if date_match and denomination_match:
                date_of_purchase = date_match.group()  # Extract the date
                # Extract and clean the denomination value
                denomination = denomination_match.group().replace(',', '')
                # Extract the purchaser name by removing the date and denomination from the segment
                purchaser_name = segment.replace(date_of_purchase, '').replace(
                    denomination_match.group(), '').strip()
                # Add the extracted data to the all_rows list
                all_rows.append(
                    [date_of_purchase, purchaser_name, int(denomination)])

    return all_rows  # Return the list of processed rows


def convert_pdf_to_csv(pdf_path, csv_path):
    with open(pdf_path, 'rb') as file:  # Open the PDF file
        reader = PyPDF2.PdfReader(file)  # Create a PDF reader object
        texts = []  # Initialize a list to hold the text of each page

        # Loop through each page in the PDF
        for i, page in enumerate(reader.pages):
            text = page.extract_text()  # Extract text from the page
            # Print the current page being processed
            print(f"Processing Page {i + 1}")
            texts.append(text)  # Append the extracted text to the list

            # Compare the number of date and denomination matches in the current page's text
            date_matches = re.findall(r'\d{2}/[A-Za-z]{3}/20\d{2}', text)
            denomination_matches = re.findall(
                r'(1,000|10,000|1,00,000|10,00,000|1,00,00,000|10,00,00,000)', text)
            # If the number of dates and denominations found does not match
            if len(date_matches) != len(denomination_matches):
                # Print a message indicating a mismatch on the current page
                print(
                    f"Mismatch found on Page {i + 1}: Date of Encashment Length = {len(date_matches)}, Denomination Length = {len(denomination_matches)}")

        # Process the extracted texts to obtain data rows
        data = process_text(texts)

        # Convert the list of data rows into a pandas DataFrame
        df = pd.DataFrame(data, columns=[
                          'Date of Encashment', 'Name of the Political Party', 'Denomination'])

        # Clean the 'Denomination' column by removing commas and converting to integers
        df['Denomination'] = df['Denomination'].replace(
            {',': ''}, regex=True).astype(int)

        # Insert a 'Sr No.' column at the beginning of the DataFrame
        df.insert(0, 'Sr No.', range(1, 1 + len(df)))

        # Write the DataFrame to a CSV file
        df.to_csv(csv_path, index=False)
        # Indicate that the CSV conversion is complete
        print("\nConversion to CSV completed for Encasher PDF Data.")


if __name__ == "__main__":
    # Specify the path to the Encashment PDF file and the output CSV file
    pdf_path = './pdf_data/Encashment_Details_Final.pdf'
    csv_path = '02_Encasher_Details.csv'

    # Call the function to convert the PDF to a CSV file
    convert_pdf_to_csv(pdf_path, csv_path)
