"""
List organizations + dataset count
"""

from __future__ import print_function

import csv
import sys
import requests

BASE_URL = 'http://dati.trentino.it'

csvw = csv.writer(sys.stdout)
csvw.writerow(('Name', 'Title', 'Datasets'))

for orgid in requests.get(BASE_URL + '/api/3/action/organization_list').json()['result']:
    resp = requests.get(BASE_URL + '/api/3/action/organization_show?id={}'.format(orgid))
    data = resp.json()['result']
    csvw.writerow((
        data['name'].encode('utf-8'),
        data['title'].encode('utf-8'),
        str(len(data['packages'])),
    ))
