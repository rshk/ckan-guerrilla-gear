#!/bin/bash

## Script used to merge translations from Ckan + extensions
## To translate your extension you need to configure Babel first
## then you have to extract messages and initialize catalog.

mkdir -p output

HERE="$( readlink -f "$( dirname "$BASH_SOURCE" )")"
BASEDIR="$HOME"/Projects/dati-trentino-2
CKANDIR="$BASEDIR"/ckan
LANGUAGES="it en_GB"
PLUGINSDIR="$BASEDIR"
CKANDIR="$BASEDIR"/ckan
PLUGINS="datitrentinoit"
OUTDIR="${HERE}/output"

set -e


## Extract messages + update catalog
for plugin in $PLUGINS; do
    cd "$BASEDIR"/ckanext-datitrentinoit/ && ((

	## Create .pot file extracting messages
	python setup.py extract_messages

	## Make sure we have .po files for all the interesting
	## languages
        for lang in $LANGUAGES; do
	    PLUGINPKG="$PLUGINSDIR"/ckanext-"$plugin"/ckanext/"$plugin"
	    LANGFILE="$PLUGINPKG"/i18n/"$lang"/LC_MESSAGES/ckanext-"$plugin".po
	    if [ ! -e "$LANGFILE" ]; then
		python setup.py init_catalog -l "$lang"
	    fi
	done

	## Update .po files with strings from the .pot
	python setup.py update_catalog

    ); cd - )
done


## We now need, for each language, to cat the ckan + plugins + custom translations
for lang in $LANGUAGES; do
    ## Prepare list of source .po files
    SOURCES="$CKANDIR"/ckan/i18n/"$lang"/LC_MESSAGES/ckan.po
    for plugin in $PLUGINS; do
	PLUGINPKG="$PLUGINSDIR"/ckanext-"$plugin"/ckanext/"$plugin"
	LANGFILE="$PLUGINPKG"/i18n/"$lang"/LC_MESSAGES/ckanext-"$plugin".po
	SOURCES="${LANGFILE} ${SOURCES}"
    done

    ## Prepare path for the custom translations file
    CUSTOMDIR="$OUTDIR"/"$lang"/LC_MESSAGES
    if [ ! -d "$CUSTOMDIR" ]; then
	mkdir -p "$CUSTOMDIR"
    fi
    CUSTOMFILE="${CUSTOMDIR}"/ckan.po

    ## And add the custom .po as translation source as well
    if [ -f "$CUSTOMFILE" ]; then
	SOURCES="${CUSTOMFILE} ${SOURCES}"
    fi

    ## Prepare the custom translation file
    msgcat --use-first $SOURCES > $CUSTOMFILE

    echo "Custom translation for $lang is in $CUSTOMFILE"
done
