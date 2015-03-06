#!/usr/bin/python

import argparse
import fileinput
from fractions import gcd
from sys import stdout

# Initializer arg parser.

def init_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument('--train',
						type = str,
						required = True,
                        help='File to which to write training portion '
                             'of corpus from stdin.')

    parser.add_argument('--test',
						type = str,
						required = True,
                        help='File to which to write testing portion '
                             'of corpus from stdin.')

    parser.add_argument('--percent',
                        type = int,
                        default = 80,
                        help='Percentage of input corpus to allocate to '
						     'training corpus.')

    return parser.parse_args()

def partition(args):

    ftrain = open(args.train, 'w')
    ftest = open(args.test, 'w')

    g = gcd(100, 100 - args.percent)
    (trainmax, testmax) = ( args.percent / g, (100 - args.percent) / g )

    count = trainmax
    fout = ftrain

    for line in fileinput.input('-'):
        fout.write(line)

        count -= 1
        if 0 == count:
            if fout == ftrain:
                (fout, count) = (ftest, testmax)
            else:
                (fout, count) = (ftrain, trainmax)

    ftrain.close()
    ftest.close()

# ====
# Main
# ====

args = init_parser()
partition(args)
