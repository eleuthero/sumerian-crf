#!/usr/bin/python


"""
Calculates a baseline score for Sumerian PN recognition by tagging each
word with its most common part of speech.
"""

import argparse
from itertools import tee, izip
from sys import stdout
from collections import Counter

from tablet import Line

# Index dictionary mapping words to their attested parts of speech and
# the count for each of those POS.  

INDEX = { }              # { 'x': { 'u' : 0 } }

# Initializer arg parser.

def init_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument('--train',
                        type = str,
                        required = True,
                        help='File from which to read training portion '
                             'of corpus.')

    parser.add_argument('--test',
                        type = str,
                        required = True,
                        help='File from which to read testing portion '
                             'of corpus.')

    return parser.parse_args()


# Funny pattern for iterating via a pair of elements.
# (0, 1), (1, 2), (2, 3), ... (n, None).
# This is useful because we need to peek at the next line during forward
# iteration to parse the lines in the .atf file efficiently.

def pairwise(iter):
    a, b = tee(iter)
    next(b, None)
    return izip(a, b)


def optimizeIndex(args):
    global INDEX

    for word in INDEX:
        (bestlem, bestcount) = INDEX[word].most_common(1)[0]
        INDEX[word] = bestlem


def get_elements(filename, skip_first = False):
    lines = [ ]

    with open(filename, 'r') as fin:
        for line in fin.readlines():
            lines.append(line)

    if skip_first:
        del lines[0]
        
    for line in lines:
        elts = line.strip().split('\t')

        # Skip blank lines and <l> and </l> metadata.

        if len(elts) > 1:
            yield (elts[0], elts[-1])


def buildIndex(args):
    global INDEX

    # Skip the first line; it's got the feature header descriptions.

    for (word, pos) in get_elements(args.train, skip_first = True):
        if not word in INDEX:
            INDEX[word] = Counter()

        counter = INDEX[word]
        counter[pos] += 1

    # Optimize the index; the baseline uses the most common POS tag
    # for a word.

    optimizeIndex(args)


def print_scores(caption, tp, fp, tn, fn):

    precision = float('nan')
    if (tp + fp) > 0:
        precision = float(tp) / float(tp + fp) 

    recall = float('nan')
    if (tp + fn) > 0:
        recall = float(tp) / float(tp + fn)

    f1 = float('nan')
    if (tp + fp + fn) > 0:
        f1 = float(2 * tp) / float(2 * tp + fp + fn)

    print ('{} ({} words)'.format(caption, tp + fp + tn + fn))
    print ('Precision: {:.3f}%'.format(100 * precision))
    print ('Recall   : {:.3f}%'.format(100 * recall))
    print ('F1 Score : {:.3f}%'.format(100 * f1))
    print


def evaluate(args):
    global INDEX

    (ktp, kfp, ktn, kfn) = (0, 0, 0, 0)    # Known
    (ntp, nfp, ntn, nfn) = (0, 0, 0, 0)    # Novel

    for (word, pos) in get_elements(args.test):
        known = word in INDEX

        if known:
            guess = INDEX[word]
        else:

            # This word is novel, not occurring in the training corpus.
            # Let's guess it's a PN!

            guess = 'PN'
        
        guess = True if ('PN' == guess) else False
        truth = True if ('PN' == pos) else False

        if (guess == truth):
            if guess:
                if known:
                    ktp += 1
                else:
                    ntp += 1
            else:
                if known:
                    ktn += 1
                else:
                    ntn += 1
        else:
            if guess:
                if known:
                    kfp += 1
                else:
                    nfp += 1
            else:
                if known:
                    kfn += 1
                else:
                    nfn += 1

        """
        print 'word: {}, actual_pos: {} ({}), ' \
              'index_pos: {} ({}), correct: {}' \
                  .format( word,
                           pos, truth,
                           INDEX[word], guess,
                           guess == truth )
        """

    print_scores('Total', ktp + ntp, kfp + nfp, ktn + ntn, kfn + nfn)
    print_scores('Known', ktp      , kfp      , ktn      , kfn      )
    print_scores('Novel',       ntp,       nfp,       ntn,       nfn)
        
# ====
# Main
# ====

args = init_parser()
buildIndex(args)
evaluate(args)
