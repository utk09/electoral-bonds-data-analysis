import PyPDF2
import pandas as pd
import re


def process_text(texts):
    all_rows = []  # Initialize a list to hold all processed data rows
    # Loop through each text chunk (usually each page of the PDF)
    for text in texts:
        # Find all start positions of dates in the text using regular expression
        date_starts = [match.start() for match in re.finditer(
            r'\d{2}/[A-Za-z]{3}/20\d{2}', text)]
        # Segment the text into individual records, because each new date marks the start of a new record
        segments = [text[date_starts[i]:date_starts[i + 1]]
                    for i in range(len(date_starts) - 1)]
        # If there are dates found, add the segment from the last date to the end of the text
        if date_starts:
            segments.append(text[date_starts[-1]:])

        for segment in segments:  # Loop through each segmented text
            # Search for the date and denomination within each text segment
            date_match = re.search(r'\d{2}/[A-Za-z]{3}/20\d{2}', segment)
            denomination_match = re.search(
                r'(1,000|10,000|1,00,000|10,00,000|1,00,00,000|10,00,00,000)', segment)
            # Check if both a date and a denomination are found
            if date_match and denomination_match:
                # Extract the date and denomination information
                date_of_purchase = date_match.group()
                denomination = denomination_match.group().replace(
                    ',', '')  # Remove commas for numerical conversion
                # Extract the purchaser name by removing the date and denomination from the segment
                purchaser_name = segment.replace(date_of_purchase, '').replace(
                    denomination_match.group(), '').strip()
                # Append the processed data row to the all_rows list
                all_rows.append(
                    [date_of_purchase, purchaser_name, int(denomination)])

    return all_rows  # Return the list of processed data rows


def convert_pdf_to_csv(pdf_path, csv_path):
    with open(pdf_path, 'rb') as file:  # Open the PDF file
        reader = PyPDF2.PdfReader(file)  # Create a PDF reader object
        texts = []  # List to hold text extracted from each page

        # Loop through each page in the PDF
        for i, page in enumerate(reader.pages):
            text = page.extract_text()  # Extract text from the current page
            print(f"Page {i + 1} completed")  # Print status message
            texts.append(text)  # Add the extracted text to the texts list

            # Perform consistency checks between dates and denominations
            date_matches = re.findall(r'\d{2}/[A-Za-z]{3}/20\d{2}', text)
            denomination_matches = re.findall(
                r'(1,000|10,000|1,00,000|10,00,000|1,00,00,000|10,00,00,000)', text)
            # Check if counts of dates and denominations match
            if len(date_matches) != len(denomination_matches):
                # Print warning if there is a mismatch on the current page
                print(
                    f"Mismatch found on Page {i + 1}: Date of Encashment Length = {len(date_matches)}, Denomination Length = {len(denomination_matches)}")

        # Process the extracted text to get data rows
        data = process_text(texts)
        # Convert the data rows into a pandas DataFrame
        df = pd.DataFrame(
            data, columns=['Date of Purchase', 'Purchaser Name', 'Denomination'])
        # Convert 'Denomination' column to numerical format
        df['Denomination'] = df['Denomination'].replace(
            {',': ''}, regex=True).astype(int)
        # Insert a 'Sr No.' column as the first column
        df.insert(0, 'Sr No.', range(1, 1 + len(df)))
        # Write the DataFrame to a CSV file
        df.to_csv(csv_path, index=False)
        # Print completion message
        print("\nConversion to CSV completed for Purchaser PDF Data.")


if __name__ == "__main__":
    # Set the path to Purchaser Details PDF and output CSV file
    pdf_path = './pdf_data/Purchaser_Details_Final.pdf'
    csv_path = '01_Purchaser_Details.csv'

    # Convert the PDF to CSV
    convert_pdf_to_csv(pdf_path, csv_path)
