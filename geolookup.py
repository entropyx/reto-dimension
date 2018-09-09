from geopy.geocoders import GoogleV3
from pymongo import MongoClient

geolocator = GoogleV3(api_key="AIzaSyBbMw4qB4TKK-M36Qk4gXZUD6T18IZbs-Q")

client = MongoClient('localhost', 27017)
db = client['property']

property = db.listings.find()
for p in property:
    address = p['address']
    if len(address) != 0:
        try:
            location = geolocator.geocode(address)
            print(location.latitude, location.longitude)
            coordinates = ({
                 "coordinates": {
                     "longitude": location.longitude,
                     "latitude": location.latitude
                 }
            })

            db.listings.update({"_id": p['_id']},{"$set": coordinates})
            print(p['_id'])
        except Exception as e:
            print(e)
            pass


