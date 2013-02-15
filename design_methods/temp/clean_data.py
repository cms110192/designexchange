# Note that the field order is as follows:
#   n.nid
#   title
#   field_intro_value
#   field_overview_value
#   field_citations_value
#   field_thingsneeded1_value
#   field_howtofield_value
#   field_histofmethod_value
#   field_methodsrelated_value
#   field_casestudy_value
#   field_tips1_value
#   field_cautions1_value
#   created
#   changed

import csv

from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

with open('de_temp_clean.csv', 'rb') as data:
    with open('de_temp_clean2.csv', 'wb') as output:
        for row in csv.reader(data):
            new_row = [ strip_tags(item.replace('\\\"', "")) for item in row ]
            csv.writer(output).writerow(new_row)
