import os
import functools

from jumble import jumble

import scarsdale_property_inquiry.download as dl
import scarsdale_property_inquiry.read as read

def get_dir():
    _dir = os.path.expanduser('~/dadawarehouse.thomaslevine.com/big/scarsdale-property-inquiry/info')
    if not os.path.exists(_dir):
        os.makedirs(_dir)
    return _dir

def html():
    _dir = get_dir()
    session, street_ids = dl.home()
    street = functools.partial(dl.street, session)
    for street_id in street_ids:
        session, house_ids = street(street_id)
        house = functools.partial(dl.house, session)
        for house_id in house_ids:
            text = house(house_id)
            with open(os.path.join(_dir, house_id + '.html'), 'w') as fp:
                fp.write(text)

def parse():
    session, street_ids = dl.home()
    street = functools.partial(dl.street, session)
    for street_id in street_ids:
        session, house_ids = street(street_id)
        house = functools.partial(dl.house, session)
        for future in jumble(house, house_ids):
            yield read.info(future.result())

def table():
    for row in parse():
        if row != {}:
            flatrow = {}
            for value in row.values():
                if isinstance(value, dict):
                    flatrow.update(value)
            yield flatrow

def main():
    for row in table:
        print(row)
