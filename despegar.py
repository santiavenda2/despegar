API_URL = 'http://api.despegar.com/v1/'
__author__ = 'santiago'

import json
import requests
from pymongo import MongoClient

client = MongoClient()
db = client['despegar']


def load_airports():
    airports = db['airports']
    parameters = {'page': 1, 'pagesize': 100}
    airport_url = '%sairports' % API_URL
    response = requests.get(airport_url, params=parameters)
    while response.status_code == 200:
        json_response = response.json()
        airports_list = json_response['airports']
        for airport in airports_list:
            airport["_id"] = airport["id"]
            del airport["id"]
            airports.save(airport)

        parameters['page'] += 1
        response = requests.get(airport_url, params=parameters)
        print response.url


def load_cities():
    cities = db['cities']
    parameters = {'page': 1, 'pagesize': 100}
    city_url = '%scities' % API_URL
    response = requests.get(city_url, params=parameters)
    while response.status_code == 200:
        json_response = response.json()
        cities_list = json_response['cities']
        for city in cities_list:
            city["_id"] = city["id"]
            del city["id"]
            cities.save(city)

        parameters['page'] += 1
        response = requests.get(city_url, params=parameters)
        print response.url

    print response.status_code
