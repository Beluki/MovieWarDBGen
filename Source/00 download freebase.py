#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Downloads the base movie cache dataset from Freebase
using Brad Bourland 9200 top movies list as a source.

Running this script usually takes about 1 to 10 minutes.
"""


import json
import time
import sys


# Information and error messages:

def outln(line):
    """ Write 'line' to stdout, using the platform encoding and newline format. """
    print(line, flush = True)


def errln(line):
    """ Write 'line' to stderr, using the platform encoding and newline format. """
    print('00 download freebase.py: error:', line, file = sys.stderr, flush = True)


# Non-builtin imports:

try:
    import requests

except ImportError:
    errln('This script requires the following modules:')
    errln('requests 2.7.0+ - <https://pypi.python.org/pypi/requests>')
    sys.exit(1)


# MQL READ API url:

MQLREAD_URL = 'https://www.googleapis.com/freebase/v1/mqlread?query='


# QUERY:

MQLREAD_QUERY = '''
[{
    "type": "/film/film",
    "b:type": "/award/ranked_item",

    "/award/ranked_item/appears_in_ranked_lists": [{
        "list": "The Movie List: the first 9200"
    }],

    "name": null,
    "initial_release_date": null,
    "directed_by": [],

    "limit": 3000
}]&html_escape=false&cursor'''.replace('\n', '')


# Requesting and manipulating data:

def request_json(cursor = None):
    """
    Make a Freebase request asking for more movies.
    """
    query = MQLREAD_QUERY

    if cursor is not None:
        query = query + '=' + cursor

    request = requests.get(MQLREAD_URL + query)
    return request.json()


def write_results(results, filename):
    """
    Write the results from a request to a given file.
    Each record is written in a separate line.
    """
    with open(filename, mode = 'wb') as descriptor:
        for result in results:
            jsonbytes = json.dumps(result).encode('utf-8')
            descriptor.write(jsonbytes)
            descriptor.write(b'\n')


# Entry point:

def main():
    results = []
    cursor = None
    total_requests = 0

    while True:

        # request more movies, on an error wait 5 minutes
        # and try again, to respect API usage limits:
        while True:
            total_requests += 1
            data = request_json(cursor)

            if not 'result' in data:
                errorjson = json.dumps(data, indent = 4, sort_keys = True)

                errln('Error while requesting data! Response follows:')
                errln(errorjson)

                errln('Retrying in 5 minutes...')
                time.sleep(300)

            # got the data, stop:
            else:
                break

        results += data['result']
        cursor = data['cursor']

        outln('Total requests: {} Total movies: {}'.format(total_requests, len(results)))

        # wait 10 seconds to make the next request:
        time.sleep(10)

        if not cursor:
            outln('All data gathered, saving...')
            write_results(results, '00 download freebase.json')
            break


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass

