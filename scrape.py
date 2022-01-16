from bs4 import BeautifulSoup
import pandas as pd
import requests


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
        # yt_link = inner_table_rows[4].td.a.href.text if inner_table_rows[4].td.a.href!="_" else "NA"
        
        # if(inner_table_rows[5].td.text):
        #     dataset_link = "NA"    
        # else:
        #     a = inner_table_rows[5].td.find("a",href=True,text=True)
        #     dataset_link = a['href'].strip()
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