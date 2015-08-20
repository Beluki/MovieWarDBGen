# MovieWarDBGen
Scripts to generate and sanitize a movie database for the MovieWar game.

$ "00 download freebase.py"
Total requests: 1 Total movies: 3000
Total requests: 2 Total movies: 6000
Total requests: 3 Total movies: 9000
Total requests: 4 Total movies: 9174
All data gathered, saving...

$ "01 convert freebase.py"
01 convert freebase.py: error: Invalid year range: 2002 for movie: Stevie, skipping...
01 convert freebase.py: error: Empty date, skipping movie: Siddhartha
...

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

$ "03 collapse years.py"
03 collapse years.py: error: Skipping duplicate year for movie: A Doll's House...

