#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Checks each movie date from "01 convert freebase.json"
against the OMDB API, removing movies where the title and the date
do not match.

Running this script can take one, two hours or more, since there
are about 9200 movies to check.

After running, two output files are created:
   02 match omdb.json - the movies that matched.
   02 mismatch omdb.json - the movies that didn't match, for logging.
"""


import json
import sys

from urllib.parse import quote


# Information and error messages:

def outln(line):
    """ Write 'line' to stdout, using the platform encoding and newline format. """
    print(line, flush = True)


def errln(line):
    """ Write 'line' to stderr, using the platform encoding and newline format. """
    print('02 match omdb.py: error:', line, file = sys.stderr, flush = True)


# Non-builtin imports:

try:
    import requests

except ImportError:
    errln('This script requires the following modules:')
    errln('requests 2.7.0+ - <https://pypi.python.org/pypi/requests>')
    sys.exit(1)


# Making requests:

OMDB_API = 'http://www.omdbapi.com/'


def request_json(title, year):
    """
    Make a OMDB request for a given movie title, released on a particular year.
    """
    query = OMDB_API + '?t=' + quote(title) + '&?y=' + year
    request = requests.get(query)

    return request.json()


# Writing:

def write_results(results, filename):
    """
    Write the results from our checks to a given file.
    Each record is written in a separate line.
    """
    with open(filename, mode = 'wb') as descriptor:
        for result in results:
            jsonbytes = json.dumps(result).encode('utf-8')
            descriptor.write(jsonbytes)
            descriptor.write(b'\n')


# Entry point:

def main():
    input_movies = open('01 convert freebase.json', 'r', encoding = 'utf-8').read().splitlines()

    match_movies = []
    mismatch_movies = []

    total_match = 0
    total_mismatch = 0

    for index, line in enumerate(input_movies, 1):
        movie = json.loads(line)

        title = movie['name']
        year = movie['year']

        omdbjson = request_json(title, year)

        # validate title match:
        omdbtitle = omdbjson.get('Title', '') or ''
        omdbtitle = omdbtitle.strip()

        if omdbtitle == '' or omdbtitle != title:
            mismatch_movies.append(movie)
            total_mismatch += 1
            outln('{} - ok: {} miss: {} - movie title mismatch.'.format(index, total_match, total_mismatch))
            continue

        # validate year match:
        omdbyear = omdbjson.get('Year', '') or ''
        omdbyear = omdbyear.strip()
        omdbyear = omdbyear[:4]

        if omdbyear == '' or omdbyear != year:
            mismatch_movies.append(movie)
            total_mismatch += 1
            outln('{} - ok: {} miss: {} - movie year mismatch.'.format(index, total_match, total_mismatch))
            continue

        # ok in both:
        match_movies.append(movie)
        total_match += 1
        outln('{} - ok: {} miss: {} - movie ok.'.format(index, total_match, total_mismatch))

    write_results(match_movies, '02 match omdb.json')
    write_results(mismatch_movies, '02 mismatch omdb.json')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass

