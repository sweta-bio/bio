import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Assuming seaborn is installed for color palette
import seaborn as sns

# Function to load the dataset
@st.cache_data
def load_data():
    # Adjust the path as per your Streamlit app's file structure
    data = pd.read_excel("filtered_data.xlsx")
    return data

# Function to plot a pie chart for a given year
def plot_pie_chart(data, selected_year):
    year_data = data[data['Year'] == selected_year]
    study_counts = year_data['Study'].value_counts()
    colors = sns.color_palette('pastel')[0:len(study_counts)]
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.pie(study_counts, labels=study_counts.index, autopct='%1.1f%%', startangle=140, shadow=True, colors=colors)
    ax.set_title(f'Distribution of Omics Studies in {selected_year}', fontsize=14)
    return fig

if 'page' not in st.session_state:
    st.session_state.page = 'Home'

# Home Page
if st.session_state.page == "Home":
    st.title("Bioinformatics Omics Project")
    
    # Center images using columns. Adjust file paths as necessary.
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image(["python.png", "h.jpeg"], width=300)  # Adjust paths and width as necessary
        
        # Center the "Explore Data" button
        if st.button("Explore Data"):
            st.session_state.page = 'Explore Data'
            st.experimental_rerun()

# Data Exploration Page
elif st.session_state.page == "Explore Data":
    st.sidebar.title("Explore Settings")

    # Sidebar - Introduction/Instructional Text
    st.sidebar.markdown("### Instructions")
    st.sidebar.text("Select a year and explore\nthe omics study distribution.\nUse filters to refine results.")

    data = load_data()
    
    # Sidebar - Year selection dropdown
    selected_year = st.sidebar.selectbox("Select Year", sorted(data['Year'].unique()), key='year_selector')
    
    # Main Area
    st.title("Omics Dataset Viewer")
    filtered_data = data[data['Year'] == selected_year]
    
    st.header(f"Data for {selected_year}")
    if not filtered_data.empty:
        for index, row in filtered_data.iterrows():
            st.subheader(row['Title'])
            st.write(f"PubMed ID: {row['PubMed ID']}")
            st.write(f"Accession Number: {row['Accession Number']}")
            st.write(f"Link: [{row['LINK']}]({row['LINK']})")
            st.write(f"Description: {row['Description']}")
            st.write(f"Research Gap: {row['Research gap']}")
            st.markdown("---")
    else:
        st.write("No records found for this year.")

    if 'Study' in data.columns:
        fig = plot_pie_chart(data, selected_year)
        st.pyplot(fig)
    else:
        st.write("The 'Omics Study' column is not found in the dataset.")






