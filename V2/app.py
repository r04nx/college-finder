import streamlit as st
import pandas as pd

# Load the data from CSV
df = pd.read_csv('data.csv')

# Clean column names to remove '_Column'
df.columns = [col.replace('_Column', '') for col in df.columns]

# Function to clean and extract cutoff percentages from strings
def extract_cutoff(value):
    if isinstance(value, str):
        try:
            return float(value.split('(')[-1].strip('%)'))
        except (IndexError, ValueError):
            return None
    elif isinstance(value, float) or isinstance(value, int):
        return value
    else:
        return None

# Streamlit App
def main():
    st.title("College Admission Filter")

    # Sidebar inputs for filtering
    st.sidebar.header("Filter Criteria")
    
    # Cutoff percentage input
    cutoff_percentage = st.sidebar.number_input("Cutoff Percentage", min_value=0.0, max_value=100.0, value=85.0)
    
    # Category selection
    category = st.sidebar.selectbox("Category", options=df.columns[3:])
    
    # Branch selection
    branches = df['Course Name'].unique().tolist()
    preferred_branch = st.sidebar.selectbox("Preferred Branch", options=[""] + branches)

    # Filter the data
    filtered_df = df.copy()

    # Filter by branch if selected
    if preferred_branch:
        filtered_df = filtered_df[filtered_df['Course Name'].str.contains(preferred_branch, case=False, na=False)]

    # Extract and filter based on cutoff percentage
    filtered_df[category] = filtered_df[category].apply(extract_cutoff)
    filtered_df = filtered_df[filtered_df[category] <= cutoff_percentage]

    # Display results
    if not filtered_df.empty:
        st.write(f"Found {len(filtered_df)} colleges where admission is possible with a cutoff <= {cutoff_percentage}% for category {category}:")

        # Display data in a tabular format
        st.dataframe(filtered_df[['Choice Code', 'Course Name', 'College Information', category]])

        # Button to download data as CSV
        csv = filtered_df.to_csv(index=False)
        st.download_button(label="Download data as CSV", data=csv, mime='text/csv')

    else:
        st.write("No colleges found matching the criteria.")

if __name__ == "__main__":
    main()
