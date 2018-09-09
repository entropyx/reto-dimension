import requests
from bs4 import BeautifulSoup
import csv
import datetime
from pymongo import MongoClient



client = MongoClient('localhost', 27017)
db = client['property']

def extract_data_from_listing(url, db):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    r = requests.get(url, headers=headers)

    if r.status_code == 200:
        html = r.text
        property = BeautifulSoup(html, "html.parser")
        try:
            name = property.find("h1").text.strip()
        except AttributeError:
            name = ""
            pass

        try:
            price = property.find("strong", attrs={"class": "venta"}).text.strip()
        except AttributeError:
            price = ""
            pass

        try:
            m2 = property.find("strong", attrs={"class": "datos-valor"}).text.strip()
        except AttributeError:
            m2 = ""
            pass

        try:
            address = property.find("a", attrs={"id": "go_to_map"}).text.strip()
        except AttributeError:
            address = ""
            pass

        try:
            metadata = property.find("div", attrs={"class": "aviso-datos"}).find_all("li")
            metadata_clean = []
            for data in metadata:
                metadata_clean.append(data.text.strip())

        except AttributeError:
            metadata_clean = []
            pass

        try:
            description = property.find("span", attrs={"id": "id-descipcion-aviso"}).text.strip()
        except AttributeError:
            description = ""
            pass

        try:
            advertiser = property.find("div", attrs={"class": "aviso-datos-anunciante"}).find("h4").text.strip()
        except AttributeError:
            advertiser = ""
            pass

        try:
            advertiser_meta = property.find("div", attrs={"class": "aviso-datos-anunciante"}).find_all("li")
            advertiser_meta_clean = []
            for data in advertiser_meta:
                advertiser_meta_clean.append(data.text.strip())
        except AttributeError:
            advertiser_meta_clean = []
            pass


        db.listings
        listing = {"url": url,
                   "name": name,
                   "price": price,
                   "m2": m2,
                   "address": address,
                   "metadata": metadata_clean,
                   "description": description,
                   "advertiser": advertiser,
                   "advertiser_meta": advertiser_meta_clean,
                   "timestamp": datetime.datetime.utcnow()}

        print(listing)

        listing_id = db.listings.insert_one(listing).inserted_id
        print(listing_id)

    else:
        print(r.status_code)



url_lists = []

with open('property_paths.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        url_lists.append(row[0])


for url in url_lists:
    extract_data_from_listing(url, db)
