import os
import functools

import pi.download as dl

_dir = os.path.expanduser('~/dadawarehouse.thomaslevine.com/scarsdale-property-inquiry/info')

def main():
    session, street_ids = dl.home()
    street = functools.partial(dl.street, session)
    for street_id in street_ids:
        session, house_ids = street(street_id)
        house = functools.partial(dl.house, session)
        for house_id in house_ids:
            property_number, text = house(house_id)
            with open(os.path.join(_dir, property_number + '.html'), 'w') as fp:
                fp.write(text)
