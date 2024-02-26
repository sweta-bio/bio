import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load your dataset
@st.cache_data
def load_data():
    # Ensure this path is correct when running in your environment
    data = pd.read_excel("filtered_data.xlsx")
    return data

def plot_pie_chart(data, selected_year):
    # Filter data for the selected year
    year_data = data[data['Year'] == selected_year]
    
    # Count the occurrences of each "Omics Study" type
    study_counts = year_data['Study'].value_counts()
    
    # Plotting
    fig, ax = plt.subplots()
    ax.pie(study_counts, labels=study_counts.index, autopct='%1.1f%%', startangle=140)
    ax.set_title(f'Distribution of Omics Studies in {selected_year}')
    
    return fig

def main():
    st.title("Dataset Viewer")
    
    # Load the data
    data = load_data()

    # Sidebar - Year selection dropdown
    st.sidebar.markdown("### Explore Data")
    selected_year = st.sidebar.selectbox("Select Year", sorted(data['Year'].unique(), reverse=True))

    # Independent Display of Filtered Data based on selected year
    filtered_data = data[data['Year'] == selected_year]
    
    st.header(f"Data for {selected_year}")
    for index, row in filtered_data.iterrows():
        st.subheader(row['Title'])
        st.write(f"PubMed ID: {row['PubMed ID']}")
        st.write(f"Accession Number: {row['Accession Number']}")
        st.write(f"Link: [{row['LINK']}]({row['LINK']})")
        st.write(f"Description: {row['Description']}")
        st.write(f"Research Gap: {row['Research gap']}")
        st.markdown("---")

    # Plot and display the pie chart in the main area, below the filtered data
    if 'Study' in data.columns:
        st.write(f"Distribution of Omics Studies in {selected_year}")
        fig = plot_pie_chart(data, selected_year)
        st.pyplot(fig)
    else:
        st.write("The 'Omics Study' column is not found in the dataset.")

if __name__ == "__main__":
    main()

