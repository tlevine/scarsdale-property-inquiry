import os

import lxml.html
import nose.tools as n

import scarsdale_property_inquiry.assessment as read
import scarsdale_property_inquiry.test.fixtures.assessment as fixtures

def check(function_name, expected):
    if isinstance(expected, list):
        assertion = n.assert_list_equal
    else:
        assertion = n.assert_dict_equal
    html = lxml.html.fromstring(getattr(fixtures, function_name))
    observed = getattr(read, function_name)(html)
    assertion(observed, expected)

TESTCASES = [
    ('property_information', {}),
    ('assessment_information', {}),
    ('building_information', {}),
    ('structure_information', []),
    ('tax_information', []),
    ('permits', []),
]

def test_sections():
    for section, expectation in TESTCASES:
        yield check, section, expectation
