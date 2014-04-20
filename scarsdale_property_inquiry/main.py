import os
import functools

from jumble import jumble
import dataset

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

def main():
    db = dataset.connect('sqlite:///scarsdale-property-inquiry.db')
    table = db['properties']

    session, street_ids = dl.home()
    street = functools.partial(dl.street, session)
    for street_id in street_ids:
        session, house_ids = street(street_id)
        house = functools.partial(dl.house, session)
        for future in jumble(house, house_ids):
            text = future.result()
            try:
                row = read.flatten(read.info(text))
            except Exception as e:
                print(street_id, e)
            else:
                if row != None:
                    table.upsert(row, ['property_number'])
