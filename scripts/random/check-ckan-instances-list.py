#!/usr/bin/env python

from __future__ import print_function

from urlparse import urljoin
import json
import sys

import requests


INSTANCES_FILE = \
    "https://github.com/okfn/ckan-instances/raw/gh-pages/config/instances.json"
# or use the deployed version: http://instances.ckan.org/config/instances.json


print("Getting list from {0}".format(INSTANCES_FILE), file=sys.stderr)
response = requests.get(INSTANCES_FILE)
instances_json = response.json()
print("Got {0} instances to check".format(len(instances_json)), file=sys.stderr)

results = {}

for instance in instances_json:
    print("Checking instance: {0} ({1})"
          .format(instance['id'], instance['url']),
          file=sys.stderr)
    result = {
        'url': instance['url'],
    }

    urls_to_check = [
        ('main_url', instance['url']),
        ('api_v2', urljoin(instance['url'], '/api/2/rest/dataset')),
        ('api_v3', urljoin(instance['url'], '/api/3/action/package_list')),
    ]

    for name, url in urls_to_check:
        try:
            response = requests.get(url, stream=True)

        except Exception as e:
            print("    * {0} FAILURE".format(name), file=sys.stderr)
            result[name] = {
                'success': True,
                'exception': repr(e),
            }

        else:
            print("    * {0} SUCCESS".format(name), file=sys.stderr)
            result[name] = {
                'success': response.ok,
                'http_status': response.status_code,
            }

    results[instance['id']] = result

print(json.dumps(results))
