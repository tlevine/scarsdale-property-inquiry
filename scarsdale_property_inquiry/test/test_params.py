import nose.tools as n

import scarsdale_property_inquiry.params as params

def test_data():
    observed = params.data('31bf3856ad364e35:en:eb198dbd-2212-44f6-bb15-882bde414f00:ea597d4b:b25378d2', 'gobbldygook', 'other gobbldygook', 'dnn$ctr1398$ViewHelloWorld$lstboxAddresses', '05.04.43')
    expected = {
        'StylesheetManager_TSSM': '',
        'ScriptManager_TSM': ';;System.Web.Extensions, Version=3.5.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35:en:eb198dbd-2212-44f6-bb15-882bde414f00:ea597d4b:b25378d2',
        '__EVENTTARGET': 'dnn$ctr1398$ViewHelloWorld$lstboxAddresses',
        '__EVENTARGUMENT': '',
        '__LASTFOCUS': '',
        '__VIEWSTATE': 'gobbldygook',
        '__EVENTVALIDATION': 'other gobbldygook',
        'dnn$SEARCH1$Search': 'SiteRadioButton',
        'dnn$SEARCH1$txtSearch': '',
        'dnn$ctr1398$ViewHelloWorld$lstboxAddresses': '05.04.43',
        'dnn$dnnSEARCH$Search': 'SiteRadioButton',
        'dnn$dnnSEARCH$txtSearch': '',
        'ScrollTop': 228, # how far the page is scrolled
        '__dnnVariable': '{"__scdoff":"1"}',
    }
    n.assert_dict_equal(observed, expected)
