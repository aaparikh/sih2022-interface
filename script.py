import streamlit as st
import pandas as pd
import base64
import numpy as np
from bs4 import BeautifulSoup
import requests
import plotly.express as px

# Setting Page Configuration 
st.set_page_config(
     page_title="SIH2022",
     page_icon="💡",
     layout="wide",
 )

# Adding a header image and display content
st.image(
    'https://im.rediff.com/news/2016/dec/26smart-india.jpg',
    width=140,
)
st.title('Smart India Hackathon 2022')
st.subheader('Made with :heart:  by [Atharva Parikh](https://www.linkedin.com/in/aaparikh/)')
st.markdown("""
This app retrieves the list of the **Problem statements** from sih website
* **Python libraries:** base64, pandas, streamlit, numpy, matplotlib, seaborn, requests, bs4, plotly
* **Data source:** [SIH website](https://www.sih.gov.in/sih2022PS).
* *All the data is loaded on the go so any changes made on the official website will be reflected here.*
""")

#Adding a sidebar
st.sidebar.header('Filters')
st.sidebar.subheader('Category, Theme, Tech Bucket, Ministry')
#Function to get the data from the website
@st.cache #cache the data to avoid repeated requests
def load_data():
    url = "https://sih.gov.in/sih2022PS"
    df = pd.read_html(url)[0]
    # print(df.head())
    return df

df = load_data()
#rename columns
df.rename(columns={'Sr. No.':'SNo','PS Title':'PS_T','Tech Bucket':'Tech_Bucket','Description & Briefs':'Description'}, inplace=True)
#split description into three columns


# Category ['Software','Hardware']
categories = sorted(df['Category'].unique())
selected_categories = st.sidebar.multiselect("Select Category", categories, default=categories)

themes = sorted(df['Theme'].unique())
selected_themes = st.sidebar.multiselect("Select Theme", themes, default=themes)

tech_buckets = sorted(df['Tech_Bucket'].unique())
selected_tech_buckets = st.sidebar.multiselect("Select Tech Bucket", tech_buckets, default=tech_buckets)

organizations = sorted(df['Ministry'].unique())
selected_organizations = st.sidebar.multiselect("Select Ministry", organizations, default=organizations)

df_filtered = df[(df.Category.isin(selected_categories)) & (df.Theme.isin(selected_themes)) & (df.Tech_Bucket.isin(selected_tech_buckets)) & (df.Ministry.isin(selected_organizations))]
st.write("**ℹ️ Hover over/Click a cell to see more details**")
st.write("Showing **{}** of **{}** problem ststements".format(len(df_filtered),len(df)))
st.dataframe(df_filtered)

@st.cache
def convert_df(df):
   return df.to_csv().encode('utf-8')

def summary():
    plot1 = df.groupby(['Tech_Bucket']).size()
    fig = px.bar(plot1, 
                x=plot1.index, 
                y=plot1.values, 
                labels={'y':'Number of PS', 'Tech_Bucket':'Tech Bucket'},
                title="Tech Bucket-wise Problem Statement(PS) Count",
                text = plot1.values,
            )
    st.plotly_chart(fig, use_container_width=True)

    plot2 = df.groupby(['Theme']).size()
    fig2 = px.bar(plot2, 
                x=plot2.index, 
                y=plot2.values, 
                labels={'y':'Number of PS', 'Theme':'Themes'},
                title="Theme-wise Problem Statement(PS) Count",
                text = plot2.values,
            )
    st.plotly_chart(fig2, use_container_width=True)

    plot4 = df.groupby(['Ministry']).size()
    fig4 = px.bar(plot4,
                x=plot4.index,
                y=plot4.values,
                labels = {'y':'Number of PS', 'Ministry':'Ministries'},
                title="Ministry-wise Problem Statement(PS) Count",
                text = plot4.values,
            )
    st.plotly_chart(fig4, use_container_width=True)

    plot3 = df.groupby(['Category']).size()
    fig3 = px.bar(plot3, 
                x=plot3.index, 
                y=plot3.values,
                labels = {'y':'Number of PS', 'Category':'Categories'},
                title="Category-wise Problem Statement(PS) Count",
                text = plot3.values,
            )  
    st.plotly_chart(fig3, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    csv = convert_df(df)

    st.download_button(
        "Download the entire table as CSV",
        csv,
        "sih_all_PS.csv",
        "text/csv",
        key='download-csv'
    )

with col2:
    csv2 = convert_df(df_filtered)
    st.download_button(
        "Download the filtered table as CSV",
        csv2,
        "sih_filtered_PS.csv",
        "text/csv",
        key='download-csv'
    )

#link to registration process pdf
st.write("[View the Registration Process](https://www.sih.gov.in/pdf/IdeasubmissionprocessSIH2020.pdf)")

flag = st.checkbox("View Data Summary Plots")
if(flag):
    summary()
