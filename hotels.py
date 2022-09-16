from enum import Enum

import requests


class OrderBy(str, Enum):
    popularity = "popularity"
    class_ascending = "class_ascending"
    class_descending = "class_descending"
    distance = "distance"
    upsort_bh = "upsort_bh"
    review_score = "review_score"
    price = "price"


class Coordinates(dict, Enum):
    Athens = {"latitude": "37.98381", "longitude": "23.727539"}


hotels_url = "https://booking-com.p.rapidapi.com/v1/hotels/search-by-coordinates"

params = {
    "order_by": OrderBy.popularity,
    "adults_number": '2',
    "units": 'metric',
    "room_number": '1',
    "checkout_date": '2022-10-01',
    "filter_by_currency": 'EUR',
    "locale": 'en-gb',
    "checkin_date": '2022-09-30',
    "latitude": Coordinates.Athens["latitude"],
    "longitude": Coordinates.Athens["longitude"],
    "page_number": "0"
}

headers = {
    'x-rapidapi-host': "booking-com.p.rapidapi.com",
    'x-rapidapi-key': "****"
}

response = requests.request("GET", hotels_url, headers=headers, params=params).json()
hotels = response["result"]
for hotel in hotels:
    print(hotel["hotel_name"])
