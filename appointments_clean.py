import sys
import numpy as np
import pandas as pd

def main():
    if len(sys.argv) != 3:
        raise ValueError("Incorrect no. arguments passed.\nUsage: appointments_clean.py 'input_file.xlsx' 'output_file.xlsx'")

    # Read in input excel file
    input_df = pd.read_excel(sys.argv[1])

    # Drop unneccesary columns
    input_df.drop(['Total', 'Additional Comments'], axis=1, inplace=True)

    # Create a list of unique practices
    practices = input_df['Practice'].unique().tolist()

    # Create empty DataFrame
    full_df = pd.DataFrame()

    for practice in practices:

        # Filter input_df by practice
        practice_df = input_df.loc[input_df['Practice'] == practice]

        # Identify the Division and Practice name from the first row
        division = practice_df.iloc[0, 0]
        practice = practice_df.iloc[0, 1]

        # Drop Div and Practice columns (will re-add later)
        practice_df.drop(['Div', 'Practice'], axis=1, inplace=True)

        # Transpose remaining time-series data
        new_df = practice_df.T

        # Reasign the headers to transposed DataFrame
        header = new_df.iloc[0].tolist()
        new_df.columns = header
        new_df = new_df[1:]

        # Insert relevant data back into transposed DataFrame and reset index
        new_df.insert(0, 'Practice', practice)
        new_df.insert(0, 'Div', division)
        new_df.insert(0, 'Month', new_df.index)
        new_df.reset_index(drop=True, inplace=True)

        # Remove whitespace from from column headers
        new_df.columns = new_df.columns.str.strip()

        # Align columns that are the same but named differently
        new_df = new_df.rename(columns={'Video Consults':'Video Consults (not Push Dr)'})

        # Append practice data to full DataFrame
        full_df = full_df.append(new_df)

    # Reset full_df index and export to excel
    full_df.reset_index(drop=True, inplace=True)
    full_df.to_excel(sys.argv[2], index=False)

    print("File sucessfully cleaned.")

if __name__ == "__main__":
    main()
