import lxml.html
import nose.tools as n

import scarsdale_property_inquiry.read as read
import scarsdale_property_inquiry.test.fixtures.read as fixtures

def check(assertion, function_name, expected):
    html = lxml.html.fromstring(getattr(fixtures, function_name))
    observed = getattr(read, function_name)(html)
    assertion(observed, expected)

def test_sections():
    yield check, n.assert_dict_equal, 'property_information', {}
    yield check, n.assert_dict_equal, 'assessment_information', {}
    yield check, n.assert_dict_equal, 'building_information', {}
    yield check, n.assert_list_equal, 'structure_information', {}
    yield check, n.assert_list_equal, 'tax_information', {}
    yield check, n.assert_list_equal, 'permits', {}
