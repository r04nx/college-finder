import streamlit as st
import pandas as pd

# Load the CSV data
@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

# File path to the CSV file (adjust this path as needed)
file_path = 'demo.csv'
data = load_data(file_path)

# Sidebar filters
st.sidebar.header("Filter Criteria")

# Filter by cutoff percentage
cutoff_percentage = st.sidebar.number_input("Maximum Cutoff Percentage", min_value=0.0, max_value=100.0, value=90.0)

# Filter by branch (optional)
branches = data['Course Name'].unique().tolist()
branches.insert(0, "All Branches")  # Option to select all branches
selected_branch = st.sidebar.selectbox("Select Branch (Optional)", options=branches)

# Filter by category
categories = ['GOPEN', 'GSC', 'GNTA', 'GNTB', 'GNTC', 'GOBC', 'LOPEN', 'LSC', 'LNTA', 'LOBC', 'EWS']
selected_category = st.sidebar.selectbox("Select Category", options=categories)

# Mapping category to respective columns
category_to_column_index = {
    'GOPEN': 4,
    'GSC': 5,
    'GNTA': 6,
    'GNTB': 7,
    'GNTC': 8,
    'GOBC': 9,
    'LOPEN': 10,
    'LSC': 11,
    'LNTA': 12,
    'LOBC': 13,
    'EWS': 14
}

# Filtering logic
if selected_branch != "All Branches":
    filtered_data = data[data['Course Name'] == selected_branch]
else:
    filtered_data = data.copy()  # Copy all data if "All Branches" is selected

# Get the column name corresponding to the selected category
category_column_index = category_to_column_index[selected_category]
category_column = data.columns[category_column_index]

# Extract percentage from a string containing a number and a percentage in parentheses
def extract_percentage(value):
    try:
        return float(value.split('(')[1].replace('%)', ''))
    except (IndexError, ValueError):
        return None

def get_filtered_data(data, column_name, cutoff_percentage):
    def meets_cutoff(row):
        if isinstance(row[column_name], str):
            values = row[column_name].split()  # Split the cell by whitespace
            return any(extract_percentage(value) <= cutoff_percentage for value in values if extract_percentage(value) is not None)
        return False
    
    filtered = data[data.apply(meets_cutoff, axis=1)]
    return filtered

filtered_data_cutoff = get_filtered_data(filtered_data, category_column, cutoff_percentage)

# Extract only percentages from the filtered data for the selected category
def format_percentages(value):
    try:
        return ', '.join([v.split('(')[1].replace('%)', '') for v in value.split() if '(' in v and v.endswith('%)')])
    except AttributeError:
        return ''

# Create a column for percentages to sort by
filtered_data_cutoff['Percentages'] = filtered_data_cutoff[category_column].apply(lambda x: [float(v.split('(')[1].replace('%)', '')) for v in x.split() if '(' in v and v.endswith('%)')])

# Expand the list of percentages into separate rows for sorting
expanded_data = filtered_data_cutoff.explode('Percentages')

# Sort by the highest percentage in the expanded data
sorted_data = expanded_data.sort_values(by='Percentages', ascending=False).drop_duplicates(subset=['Choice Code', 'Course Name', 'College Information'])

# Remove the 'Percentages' column as it's no longer needed
sorted_data = sorted_data.drop(columns=['Percentages'])

# Display filtered and sorted data
st.header("Filtered and Sorted Colleges Based on Criteria")
st.write(sorted_data[['Choice Code', 'Course Name', 'College Information', category_column]])

if sorted_data.empty:
    st.write("No colleges found with the given criteria.")
else:
    st.write(f"Found {len(sorted_data)} colleges matching the criteria.")
