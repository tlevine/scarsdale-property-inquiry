import pickle, os
import json

from lxml.html import fromstring
import nose.tools as n
n.assert_dict_equal.__self__.maxDiff = None

from ..navigate import street_ids, house_ids, _compose_postback

def test_compose_postback():
    with open(os.path.join('scarsdale_property_inquiry', 'test', 'fixtures', 'home.html'), 'r') as fp:
        raw = fp.read()
    html = fromstring(raw)
    event_target = 'blahBlah$$1234'
    event_argument = ''
    value = 'CROSSWAY FIELD'
    observation = _compose_postback(event_target, event_argument, html, value)
    with open(os.path.join('scarsdale_property_inquiry', 'test', 'fixtures', 'compose_postback.json'), 'r') as fp:
        expectation = json.load(fp)
    n.assert_dict_equal(observation, expectation)

def test_street_ids():
    with open(os.path.join('scarsdale_property_inquiry', 'test', 'fixtures', 'home.p'), 'rb') as fp:
        _, response = pickle.load(fp)
    html = fromstring(response.text)
    observed = street_ids(html)
    n.assert_in('WINDSOR LA               ', list(observed))

def test_house_ids():
    with open(os.path.join('scarsdale_property_inquiry', 'test', 'fixtures', 'crossway.htm'), 'r') as fp:
        html = fromstring(fp.read())
    observed = house_ids(html)
    n.assert_in('22.11.28', list(observed))
