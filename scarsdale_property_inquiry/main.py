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
    if p.house != None:
        response = dl.home()
        result = house(html_dir, db, response, p.house)
        generator = [] if result == None else [result]
    elif p.street != None:
        response = dl.home()
        generator = street(response, p.street)
    elif p.streets:
        response = dl.home()
        generator = chain(street(response, s) for s in p.streets)
    else:
        generator = village(html_dir, db, p.parallel)
    for row in generator:
        stdout.write(json.dumps(row) + '\n')

def village(html_dir, db, parallel):
    if parallel:
        from jumble import jumble
    else:
        from collections import namedtuple
        Future = namedtuple('Future', ['result'])
        jumble = lambda f, xs: (Future(lambda: f(x)) for x in xs)

    response = dl.home()
    with open('/tmp/home.html', 'w') as fp:
        fp.write(response.text)
    _street_ids = street_ids(lxml.html.fromstring(response.text))
    for future1 in jumble(functools.partial(street, response), _street_ids):
        session, _house_ids = future1.result()
        for future2 in jumble(functools.partial(house, html_dir, db, response), _house_ids):
            row = future2.result()
            if row != None:
                yield row

def street(prev_response, street_id):
    response = dl.street(street_id, prev_response = prev_response)
    if 'error has occurred' in response.text:
        with open('/tmp/street.html', 'w') as fp:
            fp.write(response.text)
        raise ValueError('There is an error in the response for %s; see %s.' % \
                         (street_id, '/tmp/street.html'))
    return parse_session(response), house_ids(lxml.html.fromstring(response.text))

def house(html_dir, db, prev_response, house_id):
    response = dl.house(house_id, prev_response = prev_response)
    with open(os.path.join(html_dir, house_id + '.html'), 'w') as fp:
        fp.write(response.text)
    bumpy_row = info(response.text)
    if bumpy_row != None:
        excemptions = bumpy_row.get('assessment_information', {}).get('excemptions', [])
        if excemptions != []:
            for excemption in excemptions:
                excemption['property_number'] = bumpy_row['property_information']['Property Number']
                db['excemptions'].upsert(excemption, ['property_number'])
        flat_row = flatten(bumpy_row)
        if flat_row != None and 'property_number' in flat_row:
            if '' in flat_row:
                del(flat_row[''])
            db['properties'].upsert(flat_row, ['property_number'])
        return flat_row
