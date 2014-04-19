import lxml.html

def info(text):
    html = lxml.html.fromstring(text)

def property_information(table):
    return table.xpath('descendant::td[not(@style)]')

def assessment_information(table):
   return {}

def building_information(table):
   return {}

def structure_information(table):
   return {}

def tax_information(table):
   return {}

def permits(table):
   return {}
