#!/usr/bin/env python

from __future__ import print_function

import anydbm
from collections import defaultdict
import hashlib
import json
import os
import pickle
import sys
import urlparse

import requests


target = 'http://dati.trentino.it'
cache_dir = os.path.join(os.path.dirname(__file__), '.cache')

if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)

cache = anydbm.open(os.path.join(cache_dir, 'cache.db'), flag='c')


def cached_get(url):
    cache_key = url.encode('utf-8')
    data = cache.get(cache_key)
    if data is not None:
        return pickle.loads(data)
    response = requests.get(url)
    data = {
        'status_code': response.status_code,
        'content': response.content,
        'headers': dict(response.headers.iteritems()),
    }
    cache[cache_key] = pickle.dumps(data)
    return data


def list_datasets(group):
    url = urlparse.urljoin(target, '/api/rest/group/{}'.format(group))
    return json.loads(cached_get(url)['content'].decode('utf-8'))['packages']


def get_dataset(name):
    url = urlparse.urljoin(target, '/api/rest/dataset/' + name)
    return json.loads(cached_get(url)['content'].decode('utf-8'))


def get_all_datasets(group):
    dataset_names = list_datasets(group)
    dataset_count = len(dataset_names)
    all_datasets = {}
    for i, name in enumerate(dataset_names):
        print("[{}/{}] Downloading dataset {}".format(
            i, dataset_count, name), file=sys.stderr)
        all_datasets[name] = get_dataset(name)
    return all_datasets


all_datasets = get_all_datasets('statistica')

# print(json.dumps(all_datasets, indent=4))

print('-' * 80, file=sys.stderr)


## url: [dataset, ..]
url_usage_in_dataset = defaultdict(set)

## file_sha1: [dataset, ..]
file_usage_in_dataset = defaultdict(set)

## file_sha1: [url, ..]
urls_for_file = defaultdict(set)

responses = {}


def title(text):
    print("\n\n")
    print("-" * 80)
    print("  {}".format(text))
    print("-" * 80)
    print("\n")


print("=" * 80)
print("    Duplicate datasets report")
print("=" * 80)


title("Downloading datasets for: statistica")
for key, dataset in all_datasets.iteritems():
    assert key == dataset['name']
    print(u"{0}: {1}".format(key, len(dataset['resources'])))
    for resource in sorted(dataset['resources'], key=lambda x: x['url']):
        print(u"    {}".format(resource['url']).encode('utf-8'))

        resp = cached_get(resource['url'])
        responses[resource['url']] = resp

        data = resp['content']
        data_sha = hashlib.sha1(data).hexdigest()

        url_usage_in_dataset[resource['url']].add(key)
        file_usage_in_dataset[data_sha].add(key)
        urls_for_file[data_sha].add(resource['url'])


title("URLs appearing in more than one dataset")
for key, val in url_usage_in_dataset.iteritems():
    if len(val) > 1:
        print(u"    {0} {1}".format(
            responses[key]['status_code'], key).encode('utf-8'))
        for v in sorted(val):
            print (u"        {}".format(v).encode('utf-8'))

title("Files appearing in more than one dataset")
for key, val in file_usage_in_dataset.iteritems():
    if len(val) > 1:
        print(u"    {}".format(key))
        for v in sorted(val):
            print (u"        {}".format(v).encode('utf-8'))

title("The same file appearing at a different URL")
for key, val in urls_for_file.iteritems():
    if len(val) > 1:
        print(u"    {}".format(key).encode('utf-8'))
        for v in sorted(val):
            print (u"        {0} {1}".format(
                responses[v]['status_code'], v
                ).encode('utf-8'))

title("Failing URLs")
for key, val in sorted(responses.iteritems()):
    if val['status_code'] != 200:
        print(u"    {0} {1}".format(val['status_code'], key))
