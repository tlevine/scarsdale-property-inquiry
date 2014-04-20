import os
import functools

from jumble import jumble
import dataset
from pickle_warehouse import Warehouse

import scarsdale_property_inquiry.download as dl
import scarsdale_property_inquiry.read as read

def get_fs(root_dir = os.path.expanduser('~/dadawarehouse.thomaslevine.com/big/scarsdale-property-inquiry/')):
    html_dir = os.path.join(root_dir, 'info')
    warehouse = Warehouse(os.path.join(root_dir, 'requests'))
    if not os.path.exists(html_dir):
        os.makedirs(html_dir)
    return html_dir, warehouse

def html():
    html_dir, _ = get_fs()
    session, street_ids = dl.home()
    street = functools.partial(dl.street, session)
    for street_id in street_ids:
        session, house_ids = street(street_id)
        house = functools.partial(dl.house, session)
        for house_id in house_ids:
            text = house(house_id)
            with open(os.path.join(html_dir, house_id + '.html'), 'w') as fp:
                fp.write(text)

def main():
    db = dataset.connect('sqlite:////tmp/scarsdale-property-inquiry.db')
    _, warehouse = get_fs()
    
    session, street_ids = dl.home(warehouse)
    street = functools.partial(dl.street, warehouse, session)
    for future in jumble(street, street_ids):
        session, house_ids = future.result()
        house = functools.partial(dl.house, warehouse, session)
        for future in jumble(house, house_ids):
            text = future.result()
            bumpy_row = read.info(text)
            if bumpy_row != None:
                excemptions = bumpy_row.get('assessment_information', {}).get('excemptions', [])
                if excemptions != []:
                    for excemption in excemptions:
                        excemption['property_number'] = bumpy_row['property_information']['Property Number']
                        db['excemptions'].upsert(excemption, ['property_number'])
                flat_row = read.flatten(bumpy_row)
                if flat_row != None and 'property_number' in flat_row:
                    try:
                        db['properties'].upsert(flat_row, ['property_number'])
                    except:
                        print(flat_row)
                        raise
