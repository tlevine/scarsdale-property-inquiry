from collections import OrderedDict
from lxml.html import fromstring

def info(text):
    html = fromstring(text)

def two_column_table(table):
    tds = table.xpath('descendant::td[not(@style)]')
    text_contents = [td.text_content() for td in tds]
    keys = [key.rstrip(':') for key in text_contents[::2]]
    values = [value.replace('\xa0', ' ') for value in text_contents[1::2]]
    # I could read lot area as an acreage.
    return OrderedDict(zip(keys, values))

property_information = two_column_table

def assessment_information(table):
    matrix = [[td.text_content() for td in tr.xpath('td')] for tr in table.xpath('tr')]
    print(matrix[3])
    print(matrix[4])
    print(matrix[5])
    print(matrix[6])

building_information = two_column_table

def structure_information(table):
    return table.xpath('descendant::td[not(@style)]/text()')

def tax_information(table):
    trs = table.xpath('tr[not(td[@style] or td[@colspan])]')
    keys = table.xpath('tr[position()=2]/td/text()')
    return [OrderedDict(zip(keys, tr.xpath('td/text()'))) for tr in trs]

def permits(table):
    return []
