import pickle, os
import json

from lxml.html import fromstring
import nose.tools as n
n.assert_dict_equal.__self__.maxDiff = None

from ..navigate import street_ids, house_ids, parse_session, compose_postback

def test_parse_session():
    with open(os.path.join('scarsdale_property_inquiry', 'test', 'fixtures', 'home.p'), 'rb') as fp:
        _, response = pickle.load(fp)

    with open(os.path.join('scarsdale_property_inquiry', 'test', 'fixtures', 'home.json'), 'r') as fp:
        expectation = json.load(fp)
    observed_cookies, *observed_other = parse_session(response)
    expected_cookies, *expected_other = expectation
    n.assert_dict_equal(dict(observed_cookies), expected_cookies)
    n.assert_list_equal(observed_other, expected_other)

def test_compose_postback_home():
    with open(os.path.join('scarsdale_property_inquiry', 'test', 'fixtures', 'home.html'), 'r') as fp:
        raw = fp.read()
    html = fromstring(raw)
    event_target = 'blahBlah$$1234'
    event_argument = ''
    value = 'CROSSWAY FIELD'
    observation = compose_postback(html, event_target, event_argument, value)
    with open('/tmp/a.json', 'w') as fp:
         json.dump(observation, fp, indent = 2, separators = (',', ':'))
    with open(os.path.join('scarsdale_property_inquiry', 'test', 'fixtures', 'postback_home.json'), 'r') as fp:
        expectation = json.load(fp)
    n.assert_dict_equal(observation, expectation)

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
