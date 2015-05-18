Social Choice
=============

This is a command line program to calculate the winner of
well-known winner selection methods.

Usage
-----

1. Prepare a csv file which represents voters' preference schedule.
  * The first line of the csv file consists of candidates.
    Any string can be used to represent a candidate.
  * The rest of the file consists of voters' preferences.
    The candidate put at the first column is interpreted as the most preffered candidate.
  * For example, if there are 4 candidates and 18 voters, the csv file
    should be like this:
  ```
A,B,C,D
A,B,C,D
D,C,B,A
B,C,A,D
A,B,C,D
A,B,C,D
A,B,C,D
B,C,A,D
A,B,C,D
B,C,A,D
B,C,A,D
B,C,A,D
C,B,A,D
C,B,A,D
C,B,A,D
D,C,B,A
C,B,A,D
D,C,B,A
A,B,C,D
```
2. Run ```sc.py``` at the command line with the csv file as an argument:
  ```bash
$ python3 sc.py preferences.csv
```
  * You can use the ```-m``` or ```--method``` optional argument to specify a
    winner-selection method like this:
  ```bash
$ python3 sc.py preferences.csv -m borda
```
  * The possible options are
    * the plurality method (```plurality```),
    * the runoff method (```runoff```),
    * the elimination method (```elimination```),
    * the Borda count (```borda```),
    * and the pairwise comparison method a.k.a. Condorcet method (```pairwise```).
3. The result will be displayed on the screen like this:
  ```bash
$ python3 sc.py preferences.csv -m borda
Borda count

Preference Schedule:
Voter 1: A, B, C, D
Voter 2: D, C, B, A
Voter 3: B, C, A, D
Voter 4: A, B, C, D
Voter 5: A, B, C, D
Voter 6: A, B, C, D
Voter 7: B, C, A, D
Voter 8: A, B, C, D
Voter 9: B, C, A, D
Voter 10: B, C, A, D
Voter 11: B, C, A, D
Voter 12: C, B, A, D
Voter 13: C, B, A, D
Voter 14: C, B, A, D
Voter 15: D, C, B, A
Voter 16: C, B, A, D
Voter 17: D, C, B, A
Voter 18: A, B, C, D

Detailed Preference Schedule:
5 Voters: B, C, A, D
4 Voters: C, B, A, D
3 Voters: D, C, B, A
6 Voters: A, B, C, D

Borda scores: {'C': 52, 'A': 45, 'B': 56, 'D': 27}
The winner(s) is(are) ['B']
```
