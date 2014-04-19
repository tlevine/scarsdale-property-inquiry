import lxml.html
import nose.tools as n

import scarsdale_property_inquiry.read as read
import scarsdale_property_inquiry.test.fixtures.read as fixtures

def check(function_name, expected):
    if isinstance(expected, list):
        assertion = n.assert_list_equal
    else:
        assertion = n.assert_dict_equal
    html = lxml.html.fromstring(getattr(fixtures, function_name))
    observed = getattr(read, function_name)(html)
    assertion(observed, expected)

def test_sections():
    yield check, 'property_information', {}
    yield check, 'assessment_information', {}
    yield check, 'building_information', {}
    yield check, 'structure_information', []
    yield check, 'tax_information', []
    yield check, 'permits', []
