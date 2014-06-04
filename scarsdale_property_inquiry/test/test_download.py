import pickle, os

from lxml.html import fromstring
import nose.tools as n

import scarsdale_property_inquiry.download as dl

def test_home_values():
    with open(os.path.join('scarsdale_property_inquiry', 'test', 'fixtures', 'home'), 'rb') as fp:
        response = pickle.load(fp)
    html = fromstring(response.text)
    observed = dl.home_values(html)
    n.assert_list_equal(observed, [3])
