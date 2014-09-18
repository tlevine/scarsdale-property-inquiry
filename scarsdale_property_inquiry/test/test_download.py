from ..download import _post_args

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
    yield n.assert_list_equal, list(observed_kwargs.keys()), list(expected_kwargs.keys())
    for key in expected_kwargs.keys():
        yield n.assert_list_equal, list(observed_kwargs[key].items()), expected_kwargs[key]
