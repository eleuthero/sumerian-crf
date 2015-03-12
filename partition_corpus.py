#!/usr/bin/python

import argparse
import fileinput
from fractions import gcd
from sys import stdout

# Constants.

DMG_NONE = 0
DMG_RECOVERABLE = 1
DMG_UNRECOVERABLE = 2

# Initializer arg parser.

def init_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument('--train',
                        type = str,
                        required = True,
                        help='File to which to write training portion '
                             'of corpus from stdin.  Only completely '
                             'undamaged lines will be used to form the '
                             'training corpus.')

    parser.add_argument('--test-remove-damage',
                        type = str,
                        required = True,
                        help='File to which to write testing portion '
                             'of corpus from stdin.  Only completely '
                             'undamaged lines will be used to form this '
                             'testing corpus.')

    parser.add_argument('--test-permit-damage',
                        type = str,
                        required = True,
                        help='File to which to write testing portion '
                             'of corpus from stdin.  Lines containing '
                             'damaged words will be included only if '
                             'the damaged words are lemmatized in the '
                             'source transliteration.')

    parser.add_argument('--percent',
                        type = int,
                        default = 80,
                        help='Percentage of input corpus to allocate to '
                             'training corpus.')

    return parser.parse_args()

def get_tablets(lines):

    tablet = [ ]

    for line in lines:

        if '\n' == line:

            # Done with tablet.
            # Include an additional blank line to delimit future tablets.

            tablet.append( ('\n', DMG_NONE) )
            yield tablet

            # Reset tablet.

            tablet = [ ]

        elif line.startswith('<l'):

            # Determine damage state.

            if 'damaged="False"' in line:
                damage_state = DMG_NONE
            elif 'damaged="recoverable"' in line:
                damage_state = DMG_RECOVERABLE
            elif 'damaged="unrecoverable"' in line:
                damage_state = DMG_UNRECOVERABLE

            # Accumulate this line, removing the damage
            # attribute.

            # tablet.append( (line, damage_state) )     # (debugging)
            tablet.append( ('<l>\n', damage_state) )

        else:

            tablet.append( (line, damage_state) )

    # If there are lines left over (shouldn't happen) ...

    if len(tablet) > 0:
        tablet.append( ('\n', DMG_NONE) )
        yield tablet


def partition(args):

    lines = [ ]
    for line in fileinput.input('-'):
        lines.append(line)

    ftrain = open(args.train, 'w')

    # Write all lines up to and including the first blank line in the
    # corpus to the training corpus; it contains the header.
    # Save the rest of the lines away.  We'll be iterating over them soon.

    loop = True
    while loop:
        line = lines.pop(0)
        ftrain.write(line)
        if '\n' == line:
            loop = False

    # Open file handles to the testing corpora files.

    ftest_r = open(args.test_remove_damage, 'w')
    ftest_p = open(args.test_permit_damage, 'w')

    # Make sure that testing output files start with a blank line.
    # Training output file has a header that will include that line for us.

    ftest_r.write('\n')
    ftest_p.write('\n')

    # Set up the counter that will switch between writing lines to the
    # training and testing corpora.

    g = gcd(100, 100 - args.percent)
    (trainmax, testmax) = ( args.percent / g, (100 - args.percent) / g )

    count = trainmax
    fouts = [ ftrain ]

    for tablet in get_tablets(lines):
        for fout in fouts:
            for (line, damage_state) in tablet:

                if ftrain == fout:

                    # Write only undamaged lines to the training corpus;
                    # the tags in the training corpus must be absolutely
                    # certain.

                    if (DMG_NONE == damage_state):
                        fout.write(line)

                elif ftest_r == fout:

                    # Write only undamaged lines to this testing corpus.

                    if (DMG_NONE == damage_state):
                        fout.write(line)

                elif ftest_p == fout:

                    # Permit damaged lines in this testing corpus only
                    # if they are recoverably damaged.

                    if damage_state in (DMG_NONE, DMG_RECOVERABLE):
                        fout.write(line)


        # Tablet has been written to the appropriate corpora.
        # Is it time to switch between writing to training and testing
        # corpora ?

        count -= 1
        if 0 == count:
            if ftrain in fouts:
                (fouts, count) = ( [ ftest_r, ftest_p ],
                                   testmax )
            else:
                (fouts, count) = ( [ ftrain ],
                                   trainmax )


    ftrain.close()
    ftest_r.close()
    ftest_p.close()


# ====
# Main
# ====

args = init_parser()
partition(args)
