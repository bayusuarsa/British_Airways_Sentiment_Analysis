import requests
import re
from bs4 import BeautifulSoup
import pandas as pd

base_url = "https://www.airlinequality.com/airline-reviews/british-airways/"
headers = { "user-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}

# looking from the page url, you can choose [10, 20, 50, 100]
show_page = 100
# if you look at right bottom there count of the review
next_pages = 30

#--------------------------------------------------------------#

url = f"{base_url}"


new_data = {
    "header":[],
    "review":[],}

#------------------------------------------------------------------#

def get_data_scraping(url):
    """
    This function is to looping through element html to get the value.
    ------------------------------------------------------------------
    url : base url 
    """
    response = requests.get(url, headers=headers).content
    # print(content)
    soup = BeautifulSoup(response, 'html.parser')

    # Scraping Header Title
    for title in soup.find_all('h2', attrs={"class":"text_header"}):
        new_data["header"].append(title.get_text())

    # Scraping review text
    for text in soup.find_all("div", attrs={"class":"text_content"}):
        new_data["review"].append(text.get_text())
        # if len(new_data['review']) == 3000:
        #     break

    # Scraping Rating of the airlines
    # for data in soup.find_all("span", attrs={"itemprop":"ratingValue"}):
    #     new_data["rating"].append(data.get_text())
    #     if len(new_data['rating']) == 3000:
    #         break

    # for item in soup.find_all("td", {"class": "review-value rating-yes"}):
    #     new_data["recommend"].append(item.get_text())    
    # for item in soup.find_all("td", {"class": "review-value rating-no"}):
    #     new_data['recommend'].append(item.get_text())
    
    return new_data

# --------------------------------------------------------------------------- #
# This i s only get 10 of scraping
# dt = get_data_scraping(base_url)
# print(dt)
# # print(raw.get_text())

# --------------------------------------------------------------------------- #

# TODO Let's get more data by scraping until the end of pages

for page in range(1, next_pages + 1):

    print(f"Now Scraping Page Number {page}")

    url = f"{base_url}/page/{page}/?sortby=post_date%3ADesc&pagesize={show_page}"

    get_data_scraping(url=url)

    print(f" ---->{len(new_data['review'])} Total Scraping")


# print(len(new_data["header"]), len(new_data["rating"]), len(new_data["recommend"]), len(new_data['review']))

filename="BA_Scraping.csv"
csv_export = pd.DataFrame.from_dict(new_data).to_csv(filename)
# csv_export.to_csv(filename)




