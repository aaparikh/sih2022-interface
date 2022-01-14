import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.title('Smart India Hackathon 2022')

st.markdown("""
This app retrieves the list of the **Problem statements** from 
* **Python libraries:** base64, pandas, streamlit, numpy, matplotlib, seaborn
* **Data source:** [SIH website](https://www.sih.gov.in/sih2022PS).
""")

st.sidebar.header('Filters')

@st.cache
def load_data():
    url = 'https://www.sih.gov.in/sih2022PS'
    html = pd.read_html(url, header = 0)
    print(len(html))
    df = html[0]
    return df

df = load_data()
df