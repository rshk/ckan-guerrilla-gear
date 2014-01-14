#!/bin/bash

COMMAND="$1"
if [ -z "$COMMAND" ]; then
    echo "Usage: $0 <command> [<args>]"
    echo "Will run: paster --plugin=ckan \$COMMAND --conf=path/to/ckan.ini \$ARGS"
    exit 1
fi
shift
exec paster --plugin=ckan "$COMMAND" --conf="$VIRTUAL_ENV"/etc/ckan/production.ini "$@"
