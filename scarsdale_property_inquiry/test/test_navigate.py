import pickle, os
import json

from lxml.html import fromstring
import nose.tools as n

from ..navigate import street_ids, house_ids, parse_session

def test_parse_session():
    with open(os.path.join('scarsdale_property_inquiry', 'test', 'fixtures', 'home.p'), 'rb') as fp:
        _, response = pickle.load(fp)
    with open(os.path.join('scarsdale_property_inquiry', 'test', 'fixtures', 'home.json'), 'r') as fp:
        exectation = json.load(fp)
    n.assert_dict_equal(parse_session(response), expectation)

def test_street_ids():
    with open(os.path.join('scarsdale_property_inquiry', 'test', 'fixtures', 'home.p'), 'rb') as fp:
        _, response = pickle.load(fp)
    html = fromstring(response.text)
    observed = street_ids(html)
    n.assert_in('WINDSOR LA', observed)

@n.nottest
def test_house_ids():
    with open(os.path.join('scarsdale_property_inquiry', 'test', 'fixtures', 'WALWORTH AVE'), 'rb') as fp:
        response = pickle.load(fp)
    html = fromstring(response.text)
    observed = house_ids(html)
    n.assert_in('6 WALWORTH AVE', observed)
