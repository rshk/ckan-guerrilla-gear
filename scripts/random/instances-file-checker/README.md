Ckan instances link checker
###########################

Checks all the instances listed in [instances.json](https://github.com/okfn/ckan-instances/raw/gh-pages/config/instances.json):

- check whether the main URL is reachable
- check whether API v2 is available
- check whether API v3 is available


Usage
#####

```
% check-instances-list.py > results.json
```

If you want a CSV file:

```
% results-json-to-csv.py < results.json > results.csv
```
