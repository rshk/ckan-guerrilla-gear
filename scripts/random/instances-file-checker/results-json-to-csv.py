#!/usr/bin/env python

import json
import csv
import sys


data = json.loads(sys.stdin.read())
csvw = csv.writer(sys.stdout)

csvw.writerow(('ID', 'URL', 'Ckan URL', 'Main website?', 'API v2?', 'API v3?'))
for key, item in data.iteritems():
    csvw.writerow((
        key,
        item['url'],
        item['url'] if item['api_v2']['success'] else '',
        item['main_url']['success'],
        item['api_v2']['success'],
        item['api_v3']['success'],
    ))
