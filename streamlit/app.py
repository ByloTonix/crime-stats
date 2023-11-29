import pandas as pd
import streamlit as st
import plotly.express as px

data = pd.read_csv("data\crime.csv", parse_dates=["month"], dayfirst=True)
date = data["month"].dt.year
month_list = data["month"].dt.strftime("%B")

if __name__ == "__main__":
    st.set_page_config(
        page_title="Crime Statistics",
        page_icon="💀",
        initial_sidebar_state="collapsed",
        layout="wide",
        menu_items={
            'Get help': 'https://t.me/ByloTonix',
            'Report a bug': 'https://github.com/ByloTonix/crime-stats',
            'About': '# This is a header. This is an *extremely* cool app!'
        }
    )
    
    with st.sidebar:
        st.write("Some information about my project:")
        st.link_button(
            "Dataset link",
            "https://www.kaggle.com/datasets/tsarkov90/crime-in-russia-20032020",
        )
        st.link_button(
            "Project Sources",
            "https://github.com/ByloTonix/crime-stats"
        )
        
    st.title("Crime Statistics")

    # statistic part
    st.subheader("Dataset statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        _value = f"{date.unique()[0]} - {date.unique()[-1]}, {len(date.unique())} years"
        st.metric(label="Period:", value=_value)
    with col2:
        _value = int(data.Total_crimes.sum())
        st.metric(label="Crimes:", value=_value)
    with col3:
        _value = len(data[data.columns[2:]].axes[1])
        st.metric(label="Types:", value=_value)
        
    # selectboxes for year and month
    year = st.selectbox("Select a :blue[year]", date.unique())
    month = st.selectbox("Select a :orange[month]", month_list.unique())

    filtered_data = data[
        (date == year) &
        (month_list == month)
    ]

    if len(filtered_data) > 0:

        # most popular crimes
        crime_data = filtered_data.iloc[:, 2:].sum().sort_values(ascending=False)

        fig_bar = px.bar(
            x=crime_data.index,
            y=crime_data.values,
            labels={"x": "Crime Types", "y": "Total Crimes"},
            title=f"Crimes in {month} {year}",
            color=crime_data.index,
            height=500
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    else:
        st.write("No data available for the selected year and month.")

    fig = px.bar(
        data,
        x='month',
        y=['Serious', 'Huge_damage', 'Ecological', 'Terrorism', 'Extremism', 'Murder', 'Harm_to_health', 'Rape', 'Theft', 'Vehicle_theft', 'Fraud_scam', 'Hooligan', 'Drugs', 'Weapons'],
        labels={"x": "Year", "y": "Total Crimes"},
        title='Distribution of Different Types of Crimes'
    )
    st.plotly_chart(fig, use_container_width=True)
