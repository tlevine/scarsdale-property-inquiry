from lxml.html import fromstring

def home():
    '() -> [street_id:str]'
    response = cache.home()
    html = fromstring(response.text)

def street():
    'street_id -> [house_id:str]'

def house():
    'house_id -> house_data:dict'
