#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Filters the output from "00 download freebase.json" to match
the MovieWar JSON format. Removes movies with no release date
or no director/s, etc...
"""


import json
import sys

from operator import itemgetter


# Information and error messages:

def outln(line):
    """ Write 'line' to stdout, using the platform encoding and newline format. """
    print(line, flush = True)


def errln(line):
    """ Write 'line' to stderr, using the platform encoding and newline format. """
    print('01 convert freebase.py: error:', line, file = sys.stderr, flush = True)


# Entry point:

def main():
    input_movies = open('00 download freebase.json', 'r', encoding = 'utf-8').read().splitlines()
    output_movies = []

    for index, line in enumerate(input_movies):
        movie = json.loads(line)

        # validate name:
        name = movie.get('name') or ''
        name = name.strip()

        if name == '':
            errln('Empty name, skipping line: {}'.format(index))
            continue

        # validate date:
        date = movie.get('initial_release_date') or ''
        date = date.strip()

        if date == '':
            errln('Empty date, skipping movie: {}'.format(name))
            continue

        # 'initial_release_date' is in the following format: (YYYY-MM-DD)
        # for the trivia we need the year (and sometimes only the year is present)
        year = date[:4]

        # validate the date:
        try:
            year_as_number = int(year)

            # all the movies in the 9200 movie set are supposed to be between those dates:
            if (year_as_number < 1900) or (year_as_number > 2000):
                errln('Invalid year range: {} for movie: {}, skipping...'.format(year, name))
                continue

        except ValueError:
            errln('Invalid date: {}, for movie: {}'.format(date, name))
            continue

        # create a new JSON value, using the trivia format:
        movie = { 'name': name, 'year': year }
        output_movies.append(movie)

    # sort the movies by name:
    output_movies = sorted(output_movies, key = itemgetter('name'))

    # save:
    with open('01 convert freebase.json', 'wb') as descriptor:
        for movie in output_movies:
            jsonbytes = json.dumps(movie).encode('utf-8')
            descriptor.write(jsonbytes)
            descriptor.write(b'\n')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass

