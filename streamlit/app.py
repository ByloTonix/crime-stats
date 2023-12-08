import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

data = pd.read_csv("./data/crime.csv", parse_dates=["month"], dayfirst=True)
date = data["month"].dt.year
month_list = data["month"].dt.strftime("%B")

if __name__ == "__main__":
    st.set_page_config(
        page_title="Crime Statistics",
        page_icon="💀",
        initial_sidebar_state="collapsed",
        layout="wide",
    )

    with st.sidebar:
        st.write("Some information about my project:")
        st.link_button(
            "Dataset link",
            "https://www.kaggle.com/datasets/tsarkov90/crime-in-russia-20032020",
        )
        st.link_button("Project Sources", "https://github.com/ByloTonix/crime-stats")
        
    # Remove Streamlit buttons and "made by Streamlit" text from the webpage
    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    st.title("Crime Statistics")
    
    st.subheader("Dataset statistics")
    col1, col2, col3 = st.columns(3)
    period_value = f"{date.unique()[0]} - {date.unique()[-1]}, {len(date.unique())} years"
    crimes_value = int(data.Total_crimes.sum())
    types_value = len(data[data.columns[2:]].axes[1])
    
    with col1:
        st.metric(label="Period:", value=period_value)
    with col2:
        st.metric(label="Crimes:", value=crimes_value)
    with col3:
        st.metric(label="Types:", value=types_value)

    year = st.selectbox("Select a :blue[year]", date.unique())
    ignore_month = st.checkbox("Ignore :red[month selection]")

    filtered_data = data[(date == year)]

    if ignore_month:
        month = st.selectbox("Select a :orange[month]", month_list.unique(), disabled=True)
        crime_data = filtered_data.iloc[:, 2:].sum().sort_values(ascending=False)
        fig_bar = px.bar(
            x=crime_data.index,
            y=crime_data.values,
            labels={"x": "Crime Types", "y": "Total Crimes"},
            title=f"Crimes in {year}",
            color=crime_data.index,
            height=500,
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        st.dataframe(filtered_data, use_container_width=True, hide_index=True)
    else:
        month = st.selectbox("Select a :orange[month]", month_list.unique())
        filtered_data = data[(date == year) & (month_list == month)]

        if len(filtered_data) > 0:
            crime_data = filtered_data.iloc[:, 2:].sum().sort_values(ascending=False)
            fig_bar = px.bar(
                x=crime_data.index,
                y=crime_data.values,
                labels={"x": "Crime Types", "y": "Total Crimes"},
                title=f"Crimes in {month} {year}",
                color=crime_data.index,
                height=500,
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.write("No data available for the selected year and month.")

    # Distribution of Different Types of Crimes
    fig = px.bar(
        data,
        x="month",
        y=data[data.columns[2:]].axes[1],
        labels={"x": "Year", "y": "Total Crimes"},
        title="Distribution of Different Types of Crimes",
    )
    st.plotly_chart(fig, use_container_width=True)

    # Select and display specific crimes over time
    crimes = st.multiselect("Select a crime", data[data.columns[2:]].axes[1])
    filtered_data = data[["month"] + crimes]
    filtered_data["month"] = pd.to_datetime(filtered_data["month"], format="%d.%m.%Y")
    filtered_data.set_index("month", inplace=True)
    fig = go.Figure()

    for crime in crimes:
        fig.add_trace(
            go.Scatter(x=filtered_data.index, y=filtered_data[crime], name=crime)
        )

    fig.update_layout(
        title="Crime Stats", xaxis_title="Year", yaxis_title="Total crimes"
    )

    st.plotly_chart(fig, use_container_width=True)
