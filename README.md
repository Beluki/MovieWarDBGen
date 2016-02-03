
## About

This repository contains four Python scripts that can be used to
generate a movie database for the trivia game [MovieWar][].

You probably don't need to use them, the generated JSON files are
already available in the [Releases][] tab.

[MovieWar]: https://github.com/Beluki/MovieWar
[Releases]: https://github.com/Beluki/MovieWarDBGen/releases

## How it works

The first script, [00 download freebase.py][], uses the [Freebase API][]
to download information for about 9200 movies, using Brad Bourland's
[top movies list][] as a source.

[Freebase API]: https://developers.google.com/freebase/
[top movies list]: http://www.nytimes.com/2010/04/18/movies/18bourland.html?_r=0

This is a great starting point for a trivia game. It's a big enough
number of movies to avoid repetition. All the movies are reasonably
popular. No Bollywood or obscure titles.

Sample output:

```text
Total requests: 1 Total movies: 3000
Total requests: 2 Total movies: 6000
Total requests: 3 Total movies: 9000
Total requests: 4 Total movies: 9174
All data gathered, saving...
```

Freebase is a great resource, but nothing is perfect.

The second script, [01 convert freebase.py][], sanitizes the list.
It removes movies with no title or release date and sorts the movies by name.
It also checks the release date to be between 1900 and 2000, which should be
true for all the movies in the list.

5 of the 9174 movies are removed due to invalid name/dates.

Sample output:

```text
Invalid year range: 2002 for movie: Stevie, skipping...
Empty date, skipping movie: Siddhartha
Invalid year range: 2003 for movie: Johnny Thunders: What About Me, skipping...
Invalid year range: 2004 for movie: The Big Bounce, skipping...
Invalid year range: 2004 for movie: Grizzly Falls, skipping...
```

The third script, [02 match omdb.py][], uses the [OMDB API][] to check
that the movie names/dates are actually correct. Only the movies that have the
exact same title and date on both Freebase and OMDB are kept.

[OMDB API]: http://www.omdbapi.com

In a trivia game, quality is more important than quantity.
Using multiple sources of information guarantees correctness.
From the 9169 movies, 7601 match in both databases.

Sample output:

```text
1 - ok: 0 miss: 1 - movie title mismatch.
2 - ok: 0 miss: 2 - movie title mismatch.
3 - ok: 1 miss: 2 - movie ok.
4 - ok: 2 miss: 2 - movie ok.
5 - ok: 3 miss: 2 - movie ok.
6 - ok: 4 miss: 2 - movie ok.
7 - ok: 4 miss: 3 - movie title mismatch.
8 - ok: 4 miss: 4 - movie title mismatch.
9 - ok: 5 miss: 4 - movie ok.
10 - ok: 6 miss: 4 - movie ok.
```

The fourth script, [03 collapse years.py][], looks for duplicate movie names
and years. For example, it converts this:

```json
{"name": "Jane Eyre", "year": "2011"}
{"name": "Jane Eyre", "year": "1996"}
```

Into this:

```json
{"name": "Jane Eyre", "years": ["2011", "1996"]}
```

It also checks for duplicate years.
Only one movie in the entire dataset produces this error.

Sample output:

```text
Skipping duplicate year for movie: A Doll's House...
```

[00 download freebase.py]: "Source/00 download freebase.py"
[01 convert freebase.py]: Source/01 convert freebase.py
[02 match omdb.py]: Source/02 match omdb.py
[03 collapse years.py]: Source/03 collapse years.py

## Portability

Information and error messages are written to stdout and stderr
respectively, using the current platform newline format and encoding.

Note that since the scripts were a one-off effort (once we have the JSON
there's no need to run them again), they actually do very little to no
error checking.

There are no options or arguments.

The output JSON is written as UTF-8 without BOM, using Unix newlines.

I wrote and ran them on Windows 7 x86-64, using Python 3.5.0 and
requests 2.9.1.

## Status

This program is finished!

Those scripts served their purpose, generating a good, basic database
for MovieWar. I plan no further development on them.

## License

Like all my hobby projects, this is Free Software. See the [Documentation][]
folder for more information. No warranty though.

[Documentation]: Documentation

