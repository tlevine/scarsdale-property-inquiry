import pickle, os

from lxml.html import fromstring
import nose.tools as n

import scarsdale_property_inquiry.download as dl

def test_street_ids():
    with open(os.path.join('scarsdale_property_inquiry', 'test', 'fixtures', 'home'), 'rb') as fp:
        response = pickle.load(fp)
    html = fromstring(response.text)
    observed = dl.street_ids(html)
    n.assert_in('WINDSOR LA', observed)

@n.nottest
def test_house_ids():
    with open(os.path.join('scarsdale_property_inquiry', 'test', 'fixtures', 'WALWORTH AVE'), 'rb') as fp:
        response = pickle.load(fp)
    html = fromstring(response.text)
    observed = dl.house_ids(html)
    n.assert_in('6 WALWORTH AVE', observed)
