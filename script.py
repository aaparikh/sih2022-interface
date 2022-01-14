import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.title('Smart India Hackathon 2022')

st.markdown("""
This app retrieves the list of the **Problem statements** from sih website
* **Python libraries:** base64, pandas, streamlit, numpy, matplotlib, seaborn
* **Data source:** [SIH website](https://www.sih.gov.in/sih2022PS).
""")
# https://en.wikipedia.org/wiki/List_of_S%26P_500_companies
# https://www.sih.gov.in/partner
# https://www.sih.gov.in/sih2022PS
st.sidebar.header('Filters')

@st.cache
def load_data():
    url = 'https://www.sih.gov.in/sih2022PS'
    html = pd.read_html(url, header = 0)
    print(len(html))
    df1,df2,df3 = html
    return df1,df2,df3

url = 'https://www.sih.gov.in/sih2022PS'
html = pd.read_html(url, header = 0)
html
st.write("Total entries - ", len(html))