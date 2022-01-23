import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests

url = "https://sih.gov.in/viewAllProblemStatements22-12"
html_content = requests.get(url).text
soup = BeautifulSoup(html_content, "lxml")

table = soup.find("table", {"id":"dataTablePS"})
print(table)