import streamlit as st
import pandas as pd
import base64
import numpy as np
from bs4 import BeautifulSoup
import requests
import plotly.express as px

# Setting Page Configuration 
st.set_page_config(
     page_title="SIH2023",
     page_icon="💡",
     layout="wide",
 )

# Adding a header image and display content
st.image(
    'https://im.rediff.com/news/2016/dec/26smart-india.jpg',
    width=140,
)
st.title('Smart India Hackathon 2023')
st.subheader('Made with :heart:  by [Atharva Parikh](https://www.linkedin.com/in/aaparikh/)')
st.markdown("""
This app retrieves the list of the **Problem statements** from sih website
* **Python libraries:** base64, pandas, streamlit, numpy, matplotlib, seaborn, requests, bs4, plotly
* **Data source:** [SIH website](https://www.sih.gov.in/sih2023PS).
* *All the data is loaded on the go so any changes made on the official website will be reflected here.*
""")

#Adding a sidebar
st.sidebar.header('Filters')

#Function to get the data from the website
@st.cache #cache the data to avoid repeated requests
def load_data():
    url = "https://www.sih.gov.in/sih2023PS"
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "lxml")

    # titles of resulting table
    titles = [
        "SNO",
        "PSNo",
        "Organization",
        "Description",
        "Category",
        "Domain_Bucket",
        "YTLink",
        "DataLink"
    ]

    table = soup.find("table", {"id":"dataTablePS"})
    #recursive = False is needed to avoid reading the inner tr tags
    table_data = table.tbody.find_all("tr",recursive=False)
    # print("Total rows are - ", len(table_data)) #logging
    data = []
    for i,row in enumerate(table_data):
        each_row = []
        table_start = row.find_all("td", {"class":"colomn_border"}, recursive=False)
        each_row.append(table_start[0].text.strip()) #[0] -> S.No.
        #need to dig deep in second item
        inner_table = table_start[2].find("table", {"id":"settings"})
        inner_table_rows = inner_table.thead.find_all("tr")
        #now seperately extract the data from inner table
        description = inner_table_rows[0].find("div",{"class":"style-2"}).text.strip()
        organization = inner_table_rows[1].td.text.strip()
        category = inner_table_rows[2].td.text.strip()
        domain_bucket = inner_table_rows[3].td.text.strip()
        
        #there will be one href link only
        for a in inner_table_rows[4].td.find_all("a",href=True,text=True):
            if a['href'] == "_":
                yt_link = "NA"
            else:
                yt_link = a['href'].strip()

        url_start = "https://www.sih.gov.in/uploads/psData/"
        dataset_link = url_start + inner_table_rows[5].td.a.text if inner_table_rows[5].td.a else "NA"
        
        tds = row.find_all("td")
        #from the outer table we need last third and last second field values
        ps_number = tds[-2].text.strip()
        each_row.append(ps_number)
        each_row.append(organization)
        each_row.append(description)
        each_row.append(category)
        each_row.append(domain_bucket)
        each_row.append(yt_link)
        each_row.append(dataset_link)
        data.append(each_row)
        # print(f"Row number {i} done")

    #convert the list of lists to dataframe
    df = pd.DataFrame(data, columns=titles)

    # print(df.head())
    return df

df = load_data()

# Code for Filtering the data

categories = sorted(df['Category'].unique())
selected_categories = st.sidebar.multiselect("Category", categories, default=categories)

domains = sorted(df['Domain_Bucket'].unique())
selected_domains = st.sidebar.multiselect("Domain Bucket", domains, default=domains)

organizations = sorted(df['Organization'].unique())
selected_organizations = st.sidebar.multiselect("Organizations", organizations, default=organizations)

col1, col2, col3 = st.columns(3)
with col1:
    search1 = st.text_input('Search by PS Number')

df_filtered = df[(df.Category.isin(selected_categories)) & (df.Domain_Bucket.isin(selected_domains)) & (df['Organization'].isin(selected_organizations)) & (df['PSNo'].str.contains(search1))]
st.write("**ℹ️ Hover over/Click a cell to see more details**")
st.write("Showing **{}** of **{}** problem ststements".format(len(df_filtered),len(df)))
st.dataframe(df_filtered)

@st.cache
def convert_df(df):
   return df.to_csv().encode('utf-8')

def summary():
    plot1 = df.groupby(['Domain_Bucket']).size()
    fig = px.bar(plot1, 
                x=plot1.index, 
                y=plot1.values, 
                labels={'y':'Number of PS', 'Domain_Bucket':'Domains'},
                title="Domain-wise Problem Statement(PS) Count",
                text = plot1.values,
            )
    st.plotly_chart(fig, use_container_width=True)

    plot2 = df.groupby(['Category']).size()
    fig2 = px.bar(plot2, 
                x=plot2.index, 
                y=plot2.values,
                labels = {'y':'Number of PS', 'Category':'Categories'},
                title="Category-wise Problem Statement(PS) Count",
                text = plot2.values,
            )  
    st.plotly_chart(fig2, use_container_width=True)

    plot3 = df.groupby(['Organization']).size()
    fig3 = px.bar(plot3,
                x=plot3.values,
                y=plot3.index,
                labels = {'y':'Number of PS', 'Organization':'Organizations'},
                title="Organization-wise Problem Statement(PS) Count",
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
