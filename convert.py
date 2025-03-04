import pandas as pd
import csv

# Function to read Excel and structure data
def structure_excel_data(file_path):
    # Read Excel file into a DataFrame
    df = pd.read_excel(file_path, header=None)
    
    structured_data = []
    current_entry = {}
    
    for i, row in df.iterrows():
        if pd.notna(row[0]) and str(row[0]).isdigit():  # Check if the first column is a choice code (numeric)
            if current_entry:  # Save previous entry before starting a new one
                structured_data.append(current_entry)
            current_entry = {
                'Choice Code': str(row[0]),
                'Course Name': row[1],
                'College Information': row[2],
                'Categories': {}
            }
        elif pd.notna(row[3]) and 'Stage-I' in row[3]:
            categories = df.iloc[i+1].tolist()
            cutoffs = df.iloc[i+2].tolist()

            for j in range(4, len(categories)):  # Start from index 4 to skip initial columns
                if pd.notna(categories[j]):
                    category_name = categories[j].strip()
                    if pd.notna(cutoffs[j]):
                        current_entry['Categories'][category_name] = cutoffs[j].strip()
    
    if current_entry:  # Append last entry after loop ends
        structured_data.append(current_entry)

    return structured_data

# Function to save structured data into a new CSV file
def save_structured_data_to_csv(structured_data, output_file_path):
    # Define the column headers
    headers = ['Choice Code', 'Course Name', 'College Information', 'Category', 'Cutoff Rank', 'Cutoff Percentage']
    
    # Open the output CSV file for writing
    with open(output_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)  # Write the header row
        
        # Write each entry's data into the CSV file
        for entry in structured_data:
            choice_code = entry['Choice Code']
            course_name = entry['Course Name']
            college_info = entry['College Information']
            
            for category, cutoff in entry['Categories'].items():
                if cutoff:  # Write only if there is cutoff data available
                    if '\n' in cutoff:
                        cutoff_rank, cutoff_percentage = cutoff.split('\n')
                        writer.writerow([choice_code, course_name, college_info, category, cutoff_rank.strip(), cutoff_percentage.strip()])
                    else:
                        writer.writerow([choice_code, course_name, college_info, category, cutoff, ''])

# Path to the input Excel file
input_file_path = './merged.xlsx'
# Path to the output CSV file
output_file_path = './structured_college_data.csv'

# Structuring the Excel data
structured_data = structure_excel_data(input_file_path)

# Saving the structured data to a new CSV file
save_structured_data_to_csv(structured_data, output_file_path)

print(f"Structured data has been saved to '{output_file_path}' successfully.")
