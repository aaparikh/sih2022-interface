import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from bs4 import BeautifulSoup
import requests

st.set_page_config(
     page_title="SIH - 2022",
     page_icon="👀",
     layout="wide",
 )

st.title('Smart India Hackathon 2022')
st.subheader('Made with 💻  by [Atharva Parikh](https://www.linkedin.com/in/aaparikh/) 😛')
st.markdown("""
This app retrieves the list of the **Problem statements** from sih website
* **Python libraries:** base64, pandas, streamlit, numpy, matplotlib, seaborn, requests, bs4
* **Data source:** [SIH website](https://www.sih.gov.in/sih2022PS).
""")

st.sidebar.header('Filters')

@st.cache
def load_data():
    url = "https://sih.gov.in/sih2022PS"
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "lxml")

    # titles of resulting table
    titles = [
        "Organization",
        "Description",
        "Category",
        "Domain_Bucket",
        "YTLink",
        "DataLink",
        "PSNo",
        "Submitted_Idea_Count"
    ]

    table = soup.find("table", {"id":"dataTablePS"})
    #recursive = False is needed to avoid reading the inner tr tags
    table_data = table.tbody.find_all("tr",recursive=False)
    print("Total rows are - ", len(table_data))
    data = []
    for i,row in enumerate(table_data):
        each_row = []
        table_start = row.find_all("td", {"class":"colomn_border"}, recursive=False)
        #need to dig deep in second item
        inner_table = table_start[1].find("table", {"id":"settings"})
        inner_table_rows = inner_table.thead.find_all("tr")
        #now seperately extract the data from inner table
        inner_row1 = inner_table_rows[0].find("div",{"class":"style-2"})
        description = inner_row1.text.strip()
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
        ps_number,submitted_idea_count = tds[-3].text.strip(), int(tds[-2].text.strip())
        each_row.append(organization)
        each_row.append(description)
        each_row.append(category)
        each_row.append(domain_bucket)
        each_row.append(yt_link)
        each_row.append(dataset_link)
        each_row.append(ps_number)
        each_row.append(submitted_idea_count)
        # print(each_row)
        data.append(each_row)
        print(f"Row number {i} done")

    df = pd.DataFrame(data, columns=titles)

    print(df.head())
    return df

df = load_data()

max_submissions = df['Submitted_Idea_Count'].values.max()
if(max_submissions==0):
    max_submissions = 1
submissions = st.sidebar.slider('Submitted Idea Count', value=[0,100])

categories = sorted(df['Category'].unique())
selected_categories = st.sidebar.multiselect("Category", categories, default=categories)

domains = sorted(df['Domain_Bucket'].unique())
selected_domains = st.sidebar.multiselect("Domain Bucket", domains, default=domains)

organizations = sorted(df['Organization'].unique())
selected_organizations = st.sidebar.multiselect("Organizations", organizations, default=organizations)

col1, col2, col3 = st.columns(3)
with col1:
    search1 = st.text_input('Search by PS Number')

df_filtered = df[(df.Category.isin(selected_categories)) & (df.Domain_Bucket.isin(selected_domains)) & (df['Submitted_Idea_Count']>=submissions[0]) & (df['Submitted_Idea_Count']<=submissions[1]) & (df['Organization'].isin(selected_organizations)) & (df['PSNo'].str.contains(search1))]
st.write("Hover over the cell to see more details")
st.dataframe(df_filtered)

# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="SIH2022.csv">Download CSV File</a>'
    return href
st.download_button(
     "Download this data as CSV",
     filedownload(df_filtered)
 )
df = df.groupby(['Category','Domain_Bucket']).agg({'Submitted_Idea_Count':'sum'}).reset_index()
st.dataframe(df)