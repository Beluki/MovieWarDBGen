
## About

This repository contains four Python scripts that can be used to
generate a movie database for the trivia game [MovieWar][].

You probably don't need to use them, the generated JSON files are
already available in the [Releases][] tab.

[MovieWar]: https://github.com/Beluki/MovieWar
[Releases]: https://github.com/Beluki/MovieWarDBGen/releases

## How it works

The first script, `00 download freebase.py`, uses the [Freebase API][]
to download information for about 9200 movies, using Brad Bourland's
[top movies list][] as a source.

[Freebase API]: https://developers.google.com/freebase/
[top movies list]: http://www.nytimes.com/2010/04/18/movies/18bourland.html?_r=0

This is a great starting point for a trivia game. It's a big enough
number of movies to avoid repetition. All the movies are reasonably
popular. No Bollywood or obscure titles.

Sample output:

```text
$ "00 download freebase.py"
Total requests: 1 Total movies: 3000
Total requests: 2 Total movies: 6000
Total requests: 3 Total movies: 9000
Total requests: 4 Total movies: 9174
All data gathered, saving...
```

Freebase is a great resource, but nothing is perfect.

The second script, `01 convert freebase.py`, sanitizes the list.
It removes movies with no title or release date and sorts the movies by name.
It also checks the release date to be between 1900 and 2000, which should be
true for all the movies in the list.

5 of the 9174 movies are removed due to invalid name/dates.

Sample output:

```text
$ "01 convert freebase.py"
01 convert freebase.py: error: Invalid year range: 2002 for movie: Stevie, skipping...
01 convert freebase.py: error: Empty date, skipping movie: Siddhartha
...
```

The third script, `02 match omdb.py`, uses the [OMDB API][] to check
that the movie names/dates are actually correct. Only the movies that have the
exact same title and date on both Freebase and OMDB are kept.

[OMDB API]: http://www.omdbapi.com

In a trivia game, quality is more important than quantity.
Using multiple sources of information guarantees correctness.
From the 9169 movies, 7616 match in both databases.

Sample output:

```text
$ "02 match omdb.py"
02 match omdb.py: error: 1 0/1 - Movie title mismatch: Pimpernel Smith
02 match omdb.py: error: 2 0/2 - Movie title mismatch: $
3 1/2 - Movie ok: 'Gator Bait
4 2/2 - Movie ok: 'Til We Meet Again
5 3/2 - Movie ok: 'night, Mother
6 4/2 - Movie ok: -30-
02 match omdb.py: error: 7 4/3 - Movie title mismatch: ...And Justice for All
02 match omdb.py: error: 8 4/4 - Movie title mismatch: ...tick...tick...tick...
9 5/4 - Movie ok: 10
10 6/4 - Movie ok: 10 Rillington Place
11 7/4 - Movie ok: 10 Things I Hate About You
...
```

The fourth script, `03 collapse years.py`, looks for duplicate movie names
and years. For example, it converts this:

```json
{"name": "Jane Eyre", "year": "2011"}
{"name": "Jane Eyre", "year": "1996"}
```

Into this:

```json
{"name": "Jane Eyre", "years": ["2011", "1996"]}
```

It also checks for duplicate years. Only one movie in the entire dataset
produces this error.

Sample output:

```text
$ "03 collapse years.py"
03 collapse years.py: error: Skipping duplicate year for movie: A Doll's House...
```

## Portability

Information and error messages are written to stdout and stderr
respectively, using the current platform newline format and encoding.

Note that since the scripts were a one-off effort (once we have the JSON
there's no need to run them again), they actually do very little error checking.

There are no options or arguments.

The output JSON is written as UTF-8 without BOM, using Unix newlines.

I wrote and ran them on Windows 7 x86-64, using Python 3.4.3 and
requests 2.7.0.

## Status

This program is finished!

Those scripts served their purpose, generating a good, basic database
for MovieWar.

I plan no further development on them.

## License

Like all my hobby projects, this is Free Software. See the [Documentation][]
folder for more information. No warranty though.

[Documentation]: https://github.com/Beluki/MovieWarDBGen/tree/master/Documentation

