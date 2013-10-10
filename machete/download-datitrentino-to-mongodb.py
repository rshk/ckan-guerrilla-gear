"""
Download all the data from a CKAN 1.8 installation
and store in MongoDB.
"""

from __future__ import print_function

import posixpath
import sys
import traceback
import urllib
import urlparse

import pymongo
import requests


CKAN_URL = 'http://dati.trentino.it'
MONGODB_URL = 'mongodb://database.local'
DATABASE_NAME = 'opendata_crawl_20131010'


def url(*parts, **query):
    url = urlparse.urljoin(CKAN_URL, posixpath.join(*parts))
    if len(query):
        url += u'?' + urllib.urlencode(query)
    return url


def get(*parts, **query):
    return requests.get(url(*parts))


def get_json(*parts, **query):
    return get(*parts).json()


mongo = pymongo.MongoClient(MONGODB_URL)
coll = mongo[DATABASE_NAME]['dati_trentino_it']


def do_crawl():
    datasets_names = get_json('/api/rest/dataset', limit=100000)
    for dataset_id in datasets_names:
        print("Downloading dataset: {}".format(dataset_id))
        resp = get('/api/rest/dataset/', dataset_id)
        try:
            if not resp.ok:
                raise Exception("HTTP Error: {}".format(resp.status_code))
                data = resp.json()
                data['_id'] = dataset_id
                coll['dataset'].save(data)
        except Exception:
            print("    Error while downloading dataset!")
            traceback.print_exc()
            print("")
        else:
            print("    Downloaded with success.")


def do_print_report():
    print("---- Report ------------------------------------------------")
    print("Datasets: {}".format(coll['dataset'].count()))


def do_shell():
    try:
        import IPython
    except ImportError:
        import code
        code.InteractiveConsole(locals=globals()).interact()
    else:
        IPython.embed()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Commands: shell,report,crawl")
        sys.exit(1)
    command = sys.argv[1]
    if command == 'shell':
        do_shell()
    elif command == 'report':
        do_print_report()
    elif command == 'crawl':
        do_crawl()
        do_print_report()
