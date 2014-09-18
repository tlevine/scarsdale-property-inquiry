import os, pickle

import nose.tools as n

from ..download import _post_args

with open(os.path.join('scarsdale_property_inquiry', 'test', 'fixtures', 'home.p'), 'rb') as fp:
    _, home = pickle.load(fp)

def test_post_args():
    observed_args, observed_kwargs = _post_args('house', 'the house id', home)

    expected_args = ('http://', )
    expected_kwargs = {
        'headers': [
            (),
        ],
        'files': [
            (),
        ],
        'cookies': [
            (),
        ]
    }

    yield n.assert_tuple_equal, observed_args, expected_args
    yield n.assert_list_equal, list(observed_kwargs.keys()), ['headers', 'files', 'cookies']
    yield n.assert_list_equal, observed_kwargs['files'], expected_kwargs['files']
    for key in ['headers','cookies']:
        yield n.assert_list_equal, list(observed_kwargs[key].items()), expected_kwargs[key]
