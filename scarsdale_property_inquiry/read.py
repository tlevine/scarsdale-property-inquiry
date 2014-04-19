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
    matrix = [[td.text_content().replace('\xa0','') for td in tr.xpath('td')] for tr in table.xpath('tr')]
    def to_int(comma):
        return int(comma.replace(',',''))

    av_land = list(map(to_int, matrix[3][1:4]))
    av_total = list(map(to_int, matrix[4][1:4]))
    av = {
        'av_land_2014': av_land[0],
        'av_land_2013_fmv': av_land[1],
        'av_land_2013': av_land[2],
        'av_total_2014': av_total[0],
        'av_total_2013_fmv': av_total[1],
        'av_total_2013': av_total[2],
    }
    
    taxable_values = {'taxable_' + key.lower().rstrip(':'):to_int(value) for key, value in [
        matrix[7][:2],
        matrix[7][-2:],
        matrix[8][:2],
        matrix[8][-2:],
        matrix[9][:2],
    ]}
    
    excemption_keys = matrix[11][:3]
    excemptions = [OrderedDict(zip(excemption_keys, row[:3])) for row in matrix[12:]]

    results = {}
    results.update(av)
    results.update(taxable_values)
    results.update(excemptions)
    return results

building_information = two_column_table

def structure_information(table):
    return table.xpath('descendant::td[not(@style)]/text()')

def tax_information(table):
    trs = table.xpath('tr[not(td[@style] or td[@colspan])]')
    keys = table.xpath('tr[position()=2]/td/text()')
    return [OrderedDict(zip(keys, tr.xpath('td/text()'))) for tr in trs]

def permits(table):
    return []
