#!/usr/bin/env python3

import argparse
import csv
import os
import sys

'''
candidates = ('A', 'B', 'C', 'D')

prefs = [
    ('A', 'B', 'C', 'D'),
    ('D', 'C', 'B', 'A'),
    ('B', 'C', 'A', 'D'),
    ('A', 'B', 'C', 'D'),
    ('A', 'B', 'C', 'D'),

    ('A', 'B', 'C', 'D'),
    ('B', 'C', 'A', 'D'),
    ('A', 'B', 'C', 'D'),
    ('B', 'C', 'A', 'D'),
    ('B', 'C', 'A', 'D'),

    ('B', 'C', 'A', 'D'),
    ('C', 'B', 'A', 'D'),
    ('C', 'B', 'A', 'D'),
    ('C', 'B', 'A', 'D'),
    ('D', 'C', 'B', 'A'),

    ('C', 'B', 'A', 'D'),
    ('D', 'C', 'B', 'A'),
    ('A', 'B', 'C', 'D')
]
'''


class InputError(Exception):

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


class PreferenceSchedule():

    def __init__(self, candidates, prefs):
        # check whether the candidates list consists of only strings
        if type(candidates) != tuple:
            raise InputError('Candidates must be a tuple')
        if not all(map(lambda x: type(x) == str, candidates)):
            raise InputError('Candidate must be a string')

        # check the validity of the preferences
        for pref in prefs:
            # check whether the number of candidates in the preference schedule
            # is valid
            if len(pref) != len(candidates):
                raise InputError('Invalid preference schedule')

            # check whether the candidates in the preference schedule are unique
            if len(pref) != len(candidates):
                raise InputError('Invalid preference schedule')

            # check whether the candidates in the preference schedule are also
            # in the candidates list
            for candidate in pref:
                if candidate not in candidates:
                    raise InputError('Invalid preference schedule')

        self.prefs = prefs

    def original(self):
        '''Returns the original preference schedule as a printable string'''

        res = ''
        for i in range(len(self.prefs)):
            res += 'Voter {}: '.format(i+1) + ', '.join(self.prefs[i]) + '\n'

        return res[:-1]

    def detailed(self):
        '''Returns the detailed preference schedule as a printable string'''

        # count the number of occurences of each preference
        prefs = self.prefs[:]
        counts = {}
        while prefs:
            pref = prefs.pop(0)
            count = 1
            while pref in prefs:
                prefs.remove(pref)
                count += 1
            counts[pref] = count

        res = ''
        for pref in counts:
            res += str(counts[pref]) + ' Voters: ' + ', '.join(pref) + '\n'

        return res[:-1]


class Aggregator():

    def __init__(self, file):
        try:
            candidates, prefs = csv_to_preference_schedule(args.csv)
            self.candidates = candidates
            self.pref_schedule = PreferenceSchedule(candidates, prefs)
        except InputError as e:
            print('Error:', e.msg)
            sys.exit()

    def __str__(self):
        res = ''
        res += 'Preference Schedule:\n'
        res += self.pref_schedule.original() + '\n\n'
        res += 'Detailed Preference Schedule:\n'
        res += self.pref_schedule.detailed() + '\n'

        return res

    def plurality(self):
        '''Prints who wins by the plurality method'''

        counts = {}
        for pref in self.pref_schedule.prefs:
            highest = pref[0]
            if highest in counts:
                counts[highest] += 1
            else:
                counts[highest] = 1

        winner = []
        highest_votes = max(counts.values())
        for candidate in counts:
            if counts[candidate] == highest_votes:
                winner.append(candidate)

        print('The number of votes for each candidate:', counts)
        print('The winner(s) is(are)', find_winner(counts))

    def runoff(self):
        '''Prints who wins by the runoff method'''
        pass

    def elimination(self):
        '''Prints who wins by the elimination method'''
        pass

    def borda(self):
        '''Prints who wins by the Borda count'''

        counts = {}
        candidates = list(self.pref_schedule.prefs[0])
        for candidate in candidates:
            counts[candidate] = 0

        max_point = len(candidates)
        for pref in self.pref_schedule.prefs:
            for i in range(len(pref)):
                counts[pref[i]] += max_point - i

        print('Borda scores:', counts)
        print('The winner(s) is(are)', find_winner(counts))

    def pairwise_comparison(self):
        '''Prints who wins by the pairwise comparison method'''

        points = {candidate: 0 for candidate in self.candidates}
        candidates = list(self.candidates)
        for candidate in candidates[:]:
            candidates.remove(candidate)
            for rival in candidates:
                candidate_points = 0
                for pref in self.pref_schedule.prefs:
                    if pref.index(candidate) < pref.index(rival):
                        candidate_points += 1
                    else:
                        candidate_points -= 1
                if candidate_points > 0:
                    points[candidate] += 1
                else:
                    points[rival] += 1

        print('Pairwise comparison points:', points)
        print('The winner(s) is(are)', find_winner(points))


def find_winner(aggregated_result):
    max_point = 0
    for point in aggregated_result.values():
        if point > max_point:
            max_point = point

    winner = []  # winner can be many, so use a list here
    for candidate in aggregated_result.keys():
        if aggregated_result[candidate] == max_point:
            winner.append(candidate)

    return winner


def csv_to_preference_schedule(file):
    '''Reads a csv file and returns candidates and preferences'''

    file_name, ext = os.path.splitext(file)
    if file not in os.listdir('.'):
        raise InputError('File does not exist')
    if ext != '.csv':
        raise InputError('File must be a csv file')

    with open(file) as f:
        candidates = None
        prefs = []
        reader = csv.reader(f)
        for row in reader:
            if candidates is None:
                candidates = tuple(row)
            else:
                prefs.append(tuple(row))

        return candidates, prefs


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('csv', help='a csv file containing preferences', type=str)
    parser.add_argument('-m', '--method', type=str,
                        help='specify a winner selection method by a name')
    args = parser.parse_args()

    aggr = Aggregator(args.csv)

    if args.method:
        method = args.method
        try:
            if method == 'borda':
                print('Borda count\n')
                print(aggr)
                aggr.borda()
            elif method == 'elimination':
                print('Elimination method (not yet)')
                # print(aggr)
            elif method == 'pairwise':
                print('Pairwise comparison method\n')
                print(aggr)
                aggr.pairwise_comparison()
            elif method == 'plurality':
                print('Plurality method\n')
                print(aggr)
                aggr.plurality()
            elif method == 'runoff':
                print('Runoff method (not yet)')
                # print(aggr)
            else:
                raise InputError('Invalid method name')
        except InputError as e:
            print('Error:', e.msg)
            sys.exit()
    else:
        # examine all winner selection methods
        print(aggr)
        print('Plurality method:')
        aggr.plurality()
        print('\nBorda count:')
        aggr.borda()
        print('\nPairwise comparison method:')
        aggr.pairwise_comparison()
