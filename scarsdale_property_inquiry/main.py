import sys
import json
import os
import functools
from itertools import chain

from randomsleep import randomsleep
import dataset
import lxml.html

import scarsdale_property_inquiry.download as dl
from .navigate import street_ids, house_ids
from .assessment import info, flatten 
import scarsdale_property_inquiry.schema as schema
from .fs import CACHE_DIRECTORY

readme = '''
This directory contains big stuff that was produced by the following program.
http://pypi.python.org/pypi/scarsdale-property-inquiry

info/
    This directory contains the HTML of the property inquiry pages.
    You might also see "info.tar.gz", which is just an archive of
    this directory.
requests/
    This directory contains pickled response objects from python-requests.
scarsdale-property-inquiry.db
    This is a sqlite3 database that provides structure to the stuff in
    the HTML files.
'''

def get_fs(root_dir = CACHE_DIRECTORY):
    html_dir = os.path.join(root_dir, 'info')
    if not os.path.exists(html_dir):
        os.makedirs(html_dir)
    with open(os.path.join(root_dir, 'README'), 'w') as fp:
        fp.write(readme)
    return root_dir, html_dir

import argparse

def getparser(root_dir):
    default_url = 'sqlite:///' + os.path.join(root_dir, 'scarsdale-property-inquiry.db')
    description = 'Inquire about Scarsdale properties, and save results to a relational database.'
    example = '''For example:

    scarsdale-property-inquiry --database mysql+pymysql://tlevine:password@big.dada.pink/scarsdale
'''
    parser = argparse.ArgumentParser(description=description, epilog = example)
    parser.add_argument('--database', type=str, nargs = '?', default = default_url,
                        help='The database to save to')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--streets', action = 'store_true', default = False,
                               help='List all of the street names.')
    group.add_argument('--street', type=str, nargs = '?',
                       help='Get the houses on a street.')
    group.add_argument('--house', type=str, nargs = '?',
                       help='Get the information about a particular house.')
    group.add_argument('--parallel', action = 'store_true', default = False,
                       help='Run downloads in parallel.')
    return parser

def main():
    stdout = sys.stdout
    root_dir, html_dir = get_fs()
    p = getparser(root_dir).parse_args()

    db = dataset.connect(p.database)
    db.query(schema.properties)
    home_response = dl.home()
    if p.house != None:
        result = house(html_dir, home_response, p.house)
        generator = [] if result == None else [result]
    elif p.street != None:
        generator = street(home_response, p.street)
    elif p.streets:
        generator = chain(street(home_response, s) for s in p.streets)
    else:
        generator = village(html_dir, home_response, p.parallel)
    for response in generator:
        row = flatten_house(response)
        if row != None:
            relational_house(db, response)
            stdout.write(json.dumps(row) + '\n')

def village(html_dir, home_response, parallel):
    if parallel:
        from jumble import jumble
    else:
        from collections import namedtuple
        Future = namedtuple('Future', ['result'])
        jumble = lambda f, xs: (Future(lambda: f(x)) for x in xs)

    _street_ids = street_ids(lxml.html.fromstring(home_response.text))
    for street_future in jumble(functools.partial(street, home_response), _street_ids):
        street_response, _house_ids = street_future.result()
        for house_future in jumble(functools.partial(house, html_dir, home_response), set(_house_ids) - erring_houses):
            yield house_future.result()

erring_houses = {
    '02.04.5',
    '09.05.15.16',
}

def street(prev_response, street_id):
    response = dl.street(street_id, prev_response = prev_response)
    if response.status_code != 200 or 'error has occurred' in response.text:
        with open('/tmp/street.html', 'w') as fp:
            fp.write(response.text)
        raise ValueError('There is an error in the response for %s; see %s.' % \
                         (street_id, '/tmp/street.html'))
    return response, house_ids(lxml.html.fromstring(response.text))

def house(html_dir, prev_response, house_id):
    response = dl.house(house_id, prev_response = prev_response)

    if response.status_code != 200 or 'error has occurred' in response.text:
        with open('/tmp/house.html', 'w') as fp:
            fp.write(response.text)
        raise ValueError('There is an error in the response for %s; see %s.' % \
                         (house_id, '/tmp/house.html'))
    with open(os.path.join(html_dir, house_id + '.html'), 'w') as fp:
        fp.write(response.text)
    return response

def flatten_house(response):
    bumpy_row = info(response.text)
    if bumpy_row != None:
        flat_row = flatten(bumpy_row)
        if flat_row != None and '' in flat_row:
            del(flat_row[''])
        return flat_row

def relational_house(db, response):
    bumpy_row = info(response.text)
    if bumpy_row != None:
        excemptions = bumpy_row.get('assessment_information', {}).get('excemptions', [])
        flat_row = flatten(bumpy_row)
        if excemptions != []:
            for excemption in excemptions:
                excemption['property_number'] = bumpy_row['property_information']['Property Number']
                db['excemptions'].upsert(excemption, ['property_number'])
        if flat_row != None and 'property_number' in flat_row:
            if '' in flat_row:
                del(flat_row[''])
            db['properties'].upsert(flat_row, ['property_number'])
