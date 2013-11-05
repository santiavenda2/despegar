API_URL = 'http://api.despegar.com/v1/'
__author__ = 'santiago'

import json
import requests
import datetime
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


def get_flights(from_city, to_city, departurDate, adults=1, children=0, infants=0):
    parameters = {'page': 1, 'pagesize': 5, "sort":"totalfare", "order":"asc"}
    city_url = '{0}availability/flights/oneWay/{1}/{2}/{3}/{4}/{5}/{6}'.format(API_URL,
        from_city, to_city, departurDate.strftime("%Y-%m-%d"), adults, children, infants)
    response = requests.get(city_url, params=parameters)
    if response.status_code == 200:
        print response.json()
    elif response.status_code == 403:
        print response.json()["errors"]


get_flights("EZ1", "LIM",  datetime.date(2014, 3, 1) )