#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Checks movies from "02 match omdb.json" and collapses movies with the
same title but different years into one record with the years
as a list.

e.g.

Input:

{"name": "Jane Eyre", "year": "2011"}
{"name": "Jane Eyre", "year": "1996"}

Output:

{"name": "Jane Eyre", "years": ["2011", "1996"]}

The output is saved as: "03 collapse years.json".
It also skips duplicate years.
"""


import json
import sys

from collections import OrderedDict


# Information and error messages:

def outln(line):
    """ Write 'line' to stdout, using the platform encoding and newline format. """
    print(line, flush = True)


def errln(line):
    """ Write 'line' to stderr, using the platform encoding and newline format. """
    print('03 collapse years.py: error:', line, file = sys.stderr, flush = True)


# Entry point:

def main():
    input_movies = open('02 match omdb.json', 'r', encoding = 'utf-8').read().splitlines()
    output_movies = OrderedDict()

    for line in input_movies:
        movie = json.loads(line)

        name = movie['name']
        year = movie['year']

        output_movies.setdefault(name, [])

        if year in output_movies[name]:
            outln('Skipping duplicate year for movie: {}...'.format(name))
        else:
            output_movies[name].append(year)

    # save, years first:
    with open('03 collapse years.json', mode = 'wb') as descriptor:
        for name, years in output_movies.items():
            movie = OrderedDict()

            movie['years'] = years
            movie['name'] = name

            jsonbytes = json.dumps(movie).encode('utf-8')
            descriptor.write(jsonbytes)
            descriptor.write(b'\n')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass

