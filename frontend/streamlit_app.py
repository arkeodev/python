import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import time

# Page configuration
st.set_page_config(page_title="Production-Level Data Dashboard", layout="wide")

# Sample data
@st.cache_data
def load_data():
    data = pd.DataFrame({
        'A': np.random.randn(100),
        'B': np.random.rand(100),
        'C': np.random.randint(1, 10, 100),
        'D': np.random.choice(['X', 'Y', 'Z'], 100)
    })
    data['index'] = data.index
    return data

data = load_data()

# Sidebar filters
st.sidebar.header('Filters')
if data is not None:
    category = st.sidebar.multiselect('Select category:', options=['X', 'Y', 'Z'], default=['X', 'Y', 'Z'])
    value_range = st.sidebar.slider('Select value range for A:', min_value=float(data['A'].min()), max_value=float(data['A'].max()), value=(float(data['A'].min()), float(data['A'].max())))

    # Filter data
    filtered_data = data[(data['D'].isin(category)) & (data['A'].between(value_range[0], value_range[1]))]

    # Main content
    st.title('Data Dashboard')

    # Display data
    st.subheader('Filtered Data')
    st.write(filtered_data)

    # Line chart
    st.subheader('Line Chart')
    line_chart = alt.Chart(filtered_data).mark_line().encode(
        x='index:Q',
        y='A:Q'
    )
    st.altair_chart(line_chart, use_container_width=True)

    # Bar chart
    st.subheader('Bar Chart')
    bar_chart = alt.Chart(filtered_data).mark_bar().encode(
        x='D:N',
        y='C:Q'
    )
    st.altair_chart(bar_chart, use_container_width=True)

    # Progress bar simulation
    st.subheader('Simulating a Long Process')
    progress_bar = st.progress(0)
    for i in range(100):
        time.sleep(0.05)
        progress_bar.progress(i + 1)
    st.write('Process complete!')
else:
    st.error('Error loading data. Please try again later.')
