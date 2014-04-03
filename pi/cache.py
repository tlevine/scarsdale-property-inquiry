import os

import requests
from randua import generate as ua
from pickle_warehouse import Warehouse

import pi.params as p

_dir = os.path.expanduser('~/dadawarehouse.thomaslevine.com/scarsdale-property-inquiry/requests')
_warehouse = Warehouse(_dir)

def home():
    if 'home' in _warehouse:
        response = _warehouse['home']
    else:
        response = requests.get(p.url(), headers = p.headers(ua()))
        _warehouse['home'] = response
    return response

def street(publickeytoken, viewstate, eventvalidation, street_id):
    key = ('street', street_id)
    if key in _warehouse:
        response = _warehouse[key]
    else:
        data = p.data(publickeytoken, viewstate, eventvalidation, 'something', street_id)
        response = requests.post(p.url(), headers = p.headers(ua()), data = data)
        _warehouse[key] = response
    return response

def house(house_id):
    key = ('house', house_id)
    if key in _warehouse:
        response = _warehouse[key]
    else:
        data = p.data(publickeytoken, viewstate, eventvalidation, 'something', house_id)
        response = requests.post(p.url(), headers = p.headers(ua()), data = data)
        _warehouse[key] = response
    return response
