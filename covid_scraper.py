from bs4 import BeautifulSoup
import requests
import pandas as pd

#define the URL we are extracting from

url="https://www.worldometers.info/coronavirus/"

# Make a GET request to fetch the raw HTML content
html_content = requests.get(url).text

# Parse HTML code for the entire site
soup = BeautifulSoup(html_content, "lxml")

# print(soup.prettify()) # print the parsed data of html

#we pick the id of the table we want to scrape and extract HTML code for that particular table only
covid_table = soup.find("table", attrs={"id": "main_table_countries_today"})

#the head will form our columns
head = covid_table.thead.find_all("tr") 
# print(head) #the headers are contained in this HTML code


# Extract the headers from the HTML code so that we have the headers in a list 'headings'

headings = []
for th in head[0].find_all("th"):
    # remove any newlines and extra spaces from left and right
    print(th.text)
    #headings.append(td.b.text.replace('\n', ' ').strip())
    headings.append(th.text.replace("\n","").strip())
#print(headings)


# extract rows
body = covid_table.tbody.find_all("tr")

print("\n", body[0])


# Append the values of the rows into a list. Note that we have lists within a list here.

#declare empty list that will hold all row data
data = []
for r in range(1,len(body)):
    row = [] # empty list to hold one row data
    for tr in body[r].find_all("td"):
        row.append(tr.text.replace("\n","").strip())
        #append row data to row after removing newlines escape and trimming unnecessary spaces
    data.append(row)
    
# data contains all the rows excluding header
# row contains data for one row


# Finally we convert the list into Pandas Dataframe

df = pd.DataFrame(data,columns=headings)
# print(df.head(10))

#Worldometer contains data for 3 days - remove duplicate values from last two days

data = df[df["#"]!=""].reset_index(drop=True) # Data points with # value are the countries of the world while the data points with
# null values for # columns are features like continents totals etc

data = data.drop_duplicates(subset = ["Country,Other"])


# filter down columns

# Columns to keep
cols = ['Country,Other', 'TotalCases', 'NewCases', 'TotalDeaths',
       'NewDeaths', 'TotalRecovered', 'NewRecovered', 'ActiveCases',
       'Serious,Critical', 'TotalTests']

# Extract the columns we are interested in a display the first 5 rows
data_final = data[cols]
print(data_final.head())

# i want to export the table to a csv file

# Define the style
style = data_final.style \
    .background_gradient(cmap='Blues') \
    .highlight_max(color='lightgreen') \
    .highlight_min(color='pink') \
    .set_properties(**{'text-align': 'center', 'font-size': '12pt'}) \
    .set_table_styles([{
        'selector': 'th',
        'props': [
            ('background-color', '#d9d9d9'),
            ('border', '1px solid #bfbfbf')
        ]
    }])


data_final.to_csv("covid_data.csv", index=False)