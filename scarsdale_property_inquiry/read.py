import warnings
from collections import OrderedDict

from lxml.html import fromstring

def info(text):
    html = fromstring(text)

    if int(html.xpath('count(id("dnn_ctl07_lblHeading"))')) == 1:
        # There was an error
        return None
    elif int(html.xpath('count(id("dnn_ctr1381_ViewPIRPS_lblOwner")/text())')) == 0:
        open('/tmp/a.html', 'w').write(text)
        # Weird property
        return {'property_number': str(html.xpath('id("dnn_ctr1381_ViewPIRPS_lblProperty")/text()')[0])}
    else:
        output = {}
        funcs = [
            property_information, assessment_information,
            building_information, structure_information,
            tax_information, permits,
        ]
        tables = html.xpath('id("dnn_ctr1381_ViewPIRPS_Panel1")/table')
        return {func.__name__: func(table) for func, table in zip(funcs, tables)}

def flatten(row):
    if row != {}:
        flatrow = {}
        for value in row.values():
            if isinstance(value, dict):
                flatrow.update(value)
        for key, value in list(flatrow.items()):
            if isinstance(value, list):
                del(flatrow[key])
        if 'Lot Area' in flatrow:
            flatrow['acreage'] = float(flatrow['Lot Area'].split(' ')[0])
            del(flatrow['Lot Area'])
        return {key.lower().replace(' ','_'): value for key, value in flatrow.items()}


def two_column_table(table):
    tds = table.xpath('descendant::td[not(@style)]')
    text_contents = [td.text_content() for td in tds]
    keys = [key.rstrip(':') for key in text_contents[::2]]
    values = [value.replace('\xa0', ' ') for value in text_contents[1::2]]
    # I could read lot area as an acreage.
    return OrderedDict(zip(keys, values))

def property_information(table):
    return two_column_table(table)

def assessment_information(table):
    matrix = [[td.text_content().replace('\xa0','') for td in tr.xpath('td')] for tr in table.xpath('tr')]
    def to_int(comma):
        nocomma = comma.replace(',','')
        if nocomma == '':
            warnings.warn('Missing a number in the assessment information for %s' % table.xpath('id("dnn_ctr1381_ViewPIRPS_lblProperty")/text()'))
            return ''
        else:
            return int(nocomma)

    av_land = list(map(to_int, matrix[3][1:4]))
    av_total = list(map(to_int, matrix[4][1:4]))
    av = {
        'assessed_land_2014': av_land[0],
        'assessed_land_2013_fmv': av_land[1],
        'assessed_land_2013': av_land[2],
        'assessed_total_2014': av_total[0],
        'assessed_total_2013_fmv': av_total[1],
        'assessed_total_2013': av_total[2],
    }
    
    taxable_values = {'taxable_' + key.lower().rstrip(':'):to_int(value) for key, value in [
        matrix[7][:2],
        matrix[7][-2:],
        matrix[8][:2],
        matrix[8][-2:],
        matrix[9][:2],
    ]}
    if 'taxable_' in taxable_values:
        del(taxable_values['taxable_'])
    
    excemption_keys = matrix[11][:3]
    excemptions = [OrderedDict(zip(excemption_keys, row[:3])) for row in matrix[12:] if row[0] != '']

    results = {}
    results.update(av)
    results.update(taxable_values)
    results['excemptions'] = excemptions
    return results

def building_information(table):
    untyped = two_column_table(table)
    try:
        typed = {
            'Year Built': int(untyped['Year Built']),
            'Bldg Style': untyped['Bldg Style'],
            'Bathrooms': int(untyped['Bathrooms']),
            'Bedrooms': int(untyped['Bedrooms']),
            'Fireplaces': int(untyped['Fireplaces']),
            'Central Air': {'Yes':True,'No':False}[untyped['Central Air']],
            'Living Area': int(untyped['Living Area']),
            'No Stories': float(untyped['No. Stories']),
            'Half Bathrooms': int(untyped("Half-Bathrooms")),
            'Bsmt Type': untyped['Bsmt Type'],
        }
    except:
        print(untyped)
        raise
    else:
        return typed

def structure_information(table):
    keys = table.xpath('descendant::td[not(@style)]/text()')[1:]
    return {str(key[:3]):True for key in keys}

def tax_information(table):
    trs = table.xpath('tr[not(td[@style] or td[@colspan])]')
    keys = table.xpath('tr[position()=2]/td/text()')
    return [OrderedDict(zip(keys, tr.xpath('td/text()'))) for tr in trs]

def permits(table):
    return []
