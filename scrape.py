from bs4 import BeautifulSoup
import requests

url = "https://sih.gov.in/sih2022PS"
html_content = requests.get(url).text

soup = BeautifulSoup(html_content, "lxml")
# print(soup.title)

# titles of resulting table
titles = [
    "Organization",
    "Description",
    "Category",
    "Domain Bucket",
    "Youtube Link",
    "Dataset Link",
    "PS No.",
    "Submitted Idea Count"
]
table = soup.find("table", {"id":"dataTablePS"})
table_data = table.tbody.find_all("tr")
print("Total rows are - ", len(table_data))
data = []
for i,row in enumerate(table_data):
    each_row = []
    #test
    test = row.find("td", {"class":"colomn_border"})
    print('Row organization - ',test.text)
    table_start = row.find_all("td", {"class":"colomn_border"})
    print(len(table_start))
    print(table_start[0].text)
    #need to dig deep in second item
    inner_table = table_start[1].find("table", {"id":"settings"})
    inner_table_rows = inner_table.thead.find_all("tr")
    #now seperately extract the data from inner table
    inner_row1 = inner_table_rows[0].find("div",{"class":"style-2"})
    description = inner_row1.text.strip()
    organization = inner_table_rows[1].td.text.strip()
    category = inner_table_rows[2].td.text.strip()
    domain_bucket = inner_table_rows[3].td.text.strip()
    yt_link = inner_table_rows[4].td.a.text.strip() if inner_table_rows[4].td.a.text!="" else "NA"
    dataset_link = inner_table_rows[5].td.a.text.strip() if inner_table_rows[5].td.a else "NA"
    tds = row.find_all("td")
    #from the outer table we need last third and last second field values
    ps_number,submitted_idea_count = tds[-3].text.strip(), tds[-2].text.strip()
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
    if i==1:
        break