import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

to_csv = []

url = "http://www.inmuebles24.com/inmuebles-en-distrito-federal-pagina-965.html"

def extract_links_for_listings(url, to_csv):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    r = requests.get(url, headers=headers)

    if r.status_code == 200:
        html = r.text
        list = BeautifulSoup(html, "html.parser")
        list_property_paths = list.find_all("a", attrs={"class":"dl-aviso-a"})

        for link in list_property_paths:
            url = 'http://www.inmuebles24.com' + link['href']
            name = link['title']
            to_csv.append([url, name])

        propertyPaths = open('property_paths.csv', 'w')
        with propertyPaths:
            writer = csv.writer(propertyPaths)
            writer.writerows(to_csv)

        extract_links_for_listings(next_link(list), to_csv)
        print("Extracted and saved " + list_property_paths.count + " links")
        print("Next: " + next_link(list))

    else:
        print(r.status_code)


def next_link(listing):
    next = listing.find("a", attrs={"rel":"next"})['href']
    print(next)
    return next

extract_links_for_listings(url, to_csv)



