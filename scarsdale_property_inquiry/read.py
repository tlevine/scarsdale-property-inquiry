import lxml.html

def info(text):
    html = lxml.html.fromstring(text)

def property_information(table):
    print(table)
