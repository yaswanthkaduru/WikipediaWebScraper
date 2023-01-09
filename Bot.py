# Importing all the required libraries
from torpy.http.requests import TorRequests
from bs4 import BeautifulSoup
import urllib3
import random
import string
import csv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Getting the keyword from the user
Search_Word = input("Enter the Keyword: ")

# Generating URL from the entered keyword
Cap_Search_Word = string.capwords(Search_Word)
List_Cap_Search_Word = Cap_Search_Word.split()
URL_Extension = "_".join(List_Cap_Search_Word)
URL = "https://en.wikipedia.org/wiki/" + URL_Extension

# List of random user agents from
# "https://developers.whatismybrowser.com/useragents/explore/operating_system_name/macos/"
user_agent_list = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 "
    "Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 "
    "Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 "
    "Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 "
    "Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 "
    "Safari/605.1.15 "
]

# Generated using "http://httpbin.org/get"
HEADERS = {"User-Agent": random.choice(user_agent_list)}


# Function for sending requests
def send_requests(url, headers):
    with TorRequests() as tor_requests:
        with tor_requests.get_session() as sess:
            # print(sess.get("http://httpbin.org/ip").json())
            html_content = sess.get(url, headers=headers, timeout=10).text
            return html_content


# Function for web scraping wikipedia website
def wikipedia_bot(url):
    page = send_requests(url, HEADERS)
    soup = BeautifulSoup(page, 'html.parser')
    soup1 = BeautifulSoup(soup.prettify(), 'html.parser')
    # print(soup1)
    details = soup1('table', {'class': 'infobox'})
    heading = []
    description = []
    for i in details:
        rows = i.find_all('tr')
        for j in rows:
            for ele in j.find_all('th'):
                heading.append(ele.get_text())
            for ele in j.find_all('td'):
                description.append(ele.get_text())
    if heading is not None and description is not None:
        heading = [item.strip() for item in heading if str(item)]
        description = [item.strip() for item in description if str(item)]
        description = [item.replace('\n', ' ').replace('\r', '') for item in description]
        with open('Wiki_Data.csv', 'w', encoding='UTF8', newline='') as f:
            thewriter = csv.writer(f)
            thewriter.writerow(heading)
            thewriter.writerow(description)


wikipedia_bot(URL)
