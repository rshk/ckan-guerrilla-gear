#!/bin/bash
exec paster --plugin=pylons shell "$VIRTUAL_ENV"/etc/ckan/production.ini
