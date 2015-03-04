#!/usr/bin/python

import argparse
import operator
import random
import re
import fileinput
from itertools import tee, izip
from sys import stdout
from collections import Counter

from tablet import Line
from context import Context

# TODO: Remove INDEX
# TODO: Remove args.bestlemma [except maybe for dumpindex]

# Lines read from input stream.
# We'll be doing two passes over the input stream so we need to save
# what we read.

LINES = list()

# Index dictionary mapping words to their attested parts of speech and
# the count for each of those POS.  

INDEX = { }              # { 'x': { 'u' : 0 } }

# List of professions.  If the --pf switch is provided, any lemma
# with the following roots will be marked with the PF part-of-speech
# tag.

professions = [
                "aga'us[soldier]",
                "arad[slave]",
                "aszgab[leatherworker]",
                "azlag[fuller]",
                "bahar[potter]",
                "bisajdubak[archivist]",
                "damgar[merchant]",
                "dikud[judge]",
                "dubsar[scribe]",
                "en[priest]",
                "ereszdijir[priestess]",
                "ensik[ruler]",
                "engar[farmer]",
                "enkud[tax-collector]",
                "gaba'asz[courier]",
                "galamah[singer]",
                "gala[singer]",
                "geme[worker]",
                "gudug[priest]",
                "guzala[official]",
                "idu[doorkeeper]",
                "iszib[priest]",
                "kaguruk[supervisor]",
                "kasz[runner]",
                "kijgia[messenger]",
                "kinkin[miller]",
                "kuruszda[fattener]",        # (of animals)
                "kusz[official]",
                "lu2-mar-sa-me[unknown]",
                "lugal[king]",
                "lukur[priestess]",
                "lungak[brewer]",
                "malah[sailor]",
                "maszkim[administrator]",
                "muhaldim[cook]",
                "muszendu[bird-catcher]",
                "nagada[herdsman]",
                "nagar[carpenter]",
                "nar[musician]",
                "nin[lady]",
                "nubanda[overseer]",
                "nukirik[horticulturalist]",
                "sajDUN[recorder]",
                "sajja[official]",
                "simug[smith]",
                "sipad[shepherd]",
                "sukkal[secretary]",
                "szabra[administrator]",
                "szagia[cup-bearer]",
                "szakkanak[general]",
                "szej[cook]",
                "szesz[brother]",
                "szidim[builder]",
                "szu'i[barber]",
                "szukud[fisherman]",
                "tibira[sculptor]",
                "ugula[overseer]",
                "unud[cowherd]",
                "urin[guard]",
                "ujjaja[porter]",
                "uszbar[weaver]",
                "zabardab[official]",
                "zadim[stone-cutter]"
              ]

# Initializer arg parser.

def init_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument('--nogloss',
                        action='store_true',
                        help='Suppress translation glosses.  Glosses '
                             'will be replaced by a W tag.')

    parser.add_argument('--bestlemma',
                        action='store_true',
                        help='Include only the most commonly attested '
                             'lemma for tagged word.')

    parser.add_argument('--pf',
                        action='store_true',
                        help='Replace common titles and professions with '
                             'PF part-of-speech tag.')

    parser.add_argument('--bare',
                        action='store_true',
                        help='Include only lemmatized lines in output.')

    parser.add_argument('--crf',
                        action='store_true',
                        help='Include some features for conditional ' \
                             'random fields analysis.')

    parser.add_argument('--dumpindex',
                        type=str,
                        default='',
                        help='Writes a word/tag frequency matrix in CSV ' \
                             'format to the specified filename')

    return parser.parse_args()


# Funny pattern for iterating via a pair of elements.
# (0, 1), (1, 2), (2, 3), ... (n, None).
# This is useful because we need to peek at the next line during forward
# iteration to parse the lines in the .atf file efficiently.

def pairwise(iter):
    a, b = tee(iter)
    next(b, None)
    return izip(a, b)


def readLines():
    global LINES

    LINES = list()
    for line in fileinput.input('-'):
        LINES.append(line)


def buildIndex():
    global LINES

    for line1, line2 in pairwise(LINES):
        line1 = line1.strip()
        line2 = line2.strip()

        # If we see a lemmatization ...

        if line2.startswith('#lem:'):
            line = Line(line1, line2)
            if line.valid:
                for (word, _) in line.words:

                    if ':' == word:
                        print 'line: {}'.format(line.line)
                        print 'lem:  {}'.format(line.lem)
                        raise

                    if not word in INDEX:
                        INDEX[word] = Counter()

                    # Track lemma token count.

                    for lem in line.get_lemmata(word):
                        INDEX[word][lem] += 1


def dumpIndex(args):
    if args.dumpindex:

        # Write the index to JSON format for use in other applications.

        with open(args.dumpindex, 'w') as fout:
            fout.write('{\n')
            for word in sorted(INDEX):
                lemmata = dict( INDEX[word] )
                tags = Counter()

                # If it's a lemma, such as "aga'us[soldier]", replace the
                # lemma with our synthetic "W" pos tag.  Multiple lemmata
                # can contribute to a single W-count.

                for key in lemmata:
                    if '[' in key or ']' in key:
                        tags['W'] += lemmata[key]
                    else:
                        tags[key] += lemmata[key]
                        
                fout.write('\t"{}": {},\n'.format(word, dict(tags)))
            fout.write('}\n')
            fout.close()


def optimizeIndex(args):

    if args.bestlemma:

        # Optimize index by throwing away all lemmata except for the
        # most attested one for each word.

        for word in INDEX:

            try:
                (bestlem, bestcount) = INDEX[word].most_common(1)[0]
            except IndexError:
                print 'word:  {}'.format(word)
                print 'index: {}'.format(INDEX[word])
                raise
            INDEX[word] = Counter()
            INDEX[word][bestlem] = bestcount


def formatLems(lems, args):
    f = [ ]

    for lem in lems:
        if ('[' in lem) and (']' in lem):
            if args.pf:
                if lem in professions:
                    lem = 'PF'
            if args.nogloss:
                lem = 'W'
        f.append(lem)
        
    return ','.join(f)


def getLem(line, word, args): 
    if not word in INDEX:

        # Word is not lemmatized anywhere in corpus.
        # Mark with X tag to signify unknown part of speech.

        lems = [ 'X' ]

    else:

        lems = line.get_lemmata(word)

        if len(lems) > 1:
            if args.bestlemma:

                # Show only the best lemma for this word.

                lems = [ INDEX[word].most_common(1)[0][0] ]

            else:

                # Show all lemmata.

                lems = INDEX[word]

    return formatLems(lems, args)


def printWord(line, index, word, args):

    # Token 0: word

    stdout.write(word)

    # CRF fields, if requested.

    if args.crf:
        Context.write(line, index, word, args)

    # Final token: lem with which this word was tagged.

    stdout.write( '\t{}\n'.format( getLem(line, word, args) ))


def process(line, args):

    """
    print
    print 'valid: {}'.format(line.valid)
    print 'dmg:   {}'.format(line.damaged)
    print 'line:  {}'.format(line.line)
    print 'lem:   {}'.format(line.lem)
    print 'words: {}'.format(line.words)
    """

    if not line.lem:

        # Entire line is a comment or directive.

        """
        if not args.bare:
            stdout.write(line)
        """
        return

    if not args.bare:
        stdout.write('<l>\n')

    for (index, (word, _)) in enumerate(line.words):
        printWord(line, index, word, args)

    if not args.bare:
        stdout.write('</l>\n')


def parse(args):
    global LINES

    if args.crf:
        Context.write_header()

    for line1, line2 in pairwise(LINES):
        line1 = line1.strip()
        line2 = line2.strip()

        # Accumulate lines.

        if line1.startswith('&'):

            # Starting a new tablet.  Restart accumulated lines.
            # Emit blank line to delimit tablets.

            stdout.write('\n')
            lines = list()
            lines.append( Line(line1, None) )

        elif line1.startswith('#lem:'):

            # Lemma.  We've already built the lemmata index; skip this.

            pass

        else:
            lines.append( Line(line1, line2) )

        # End of tablet ?

        if line2.startswith('&'):

            # Starting a new tablet.  Process accumulated lines.

            for line in lines:
                process(line, args)

            # Restart accumulated lines.

            lines = list()

# ====
# Main
# ====

args = init_parser()
readLines()

buildIndex()
optimizeIndex(args)

if args.dumpindex:
    dumpIndex(args)

parse(args)
