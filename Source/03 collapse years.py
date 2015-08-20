#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Checks movies from "02 movies.json" and collapses movies with the
same title but different years into one record with the years
as a list.

e.g.

Input:

{"name": "Jane Eyre", "year": "2011"}
{"name": "Jane Eyre", "year": "1996"}

Output:

{"name": "Jane Eyre", "years": ["2011", "1996"]}

The output is saved as: "03 movies (years collapsed).json"
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
    names = OrderedDict()
    input_movies = open('02 movies.json', 'r', encoding = 'utf-8').read().splitlines()

    for line in input_movies:
        movie = json.loads(line)

        name = movie['name']
        year = movie['year']

        names.setdefault(name, [])

        if year in names[name]:
            errln('Skipping duplicate year for movie: {}...'.format(name))
        else:
            names[name].append(year)

    # save:
    with open('03 movies (years collapsed).conf', mode = 'wb') as descriptor:
        for name in names:
            movie = { 'name': name, 'years': names[name] }

            jsonbytes = json.dumps(movie).encode('utf-8')
            descriptor.write(jsonbytes)
            descriptor.write(b'\n')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass

