#!/bin/bash

paster --plugin=ckan db --config="$VIRTUAL_ENV"/etc/ckan/production.ini simple-dump-json "$1"
