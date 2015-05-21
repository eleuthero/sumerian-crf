#!/usr/bin/python

import argparse
import fileinput
from os import path

# Initializer arg parser.

def init_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument('--count',
                        type = int,
                        default = 10,  
                        help='Number of tablets to include in a single '
                             'file created during the segmentation '
                             'process.')

    parser.add_argument('--directory',
                        type = str,
                        required = True,
                        help='Directory to which to write segmented files.')

    return parser.parse_args()


def get_next_tablet(fin):
    tablet = None

    while True:
        line = fin.readline()

        if not line:

            # Shouldn't happen; the file should end nicely with a
            # newline tablet separator.  However, if it doesn't,
            # fall through and treat it as one.

            break

        else:

            # We've got a line; make sure tablet is a list.

            if not tablet:
                tablet = [ ]

        if '\n' == line:

            # Done with tablet.
            # Include an additional blank line to delimit future tablets.

            tablet.append('\n')
            return tablet

        else:

            tablet.append(line)

    # If there are lines left over (shouldn't happen) ...

    if tablet and len(tablet) > 0:
        tablet.append('\n')

    return tablet


def write_human_file(tablets, index):

    filename = path.join( args.directory,
                          'human_{}.txt'.format(index) ) 

    with open(filename, 'w') as fout:
        for tablet in tablets:
            for line in tablet:
                if '\t' in line:
                    fout.write( line.split('\t')[0] )
                    fout.write(' ')
                elif '</l>' in line:
                    fout.write('\n')
                elif '\n' == line:
                    fout.write(line)


def write_machine_file(tablets, index):

    filename = path.join( args.directory,
                          'machine_{}.csv'.format(index) ) 

    with open(filename, 'w') as fout:

        # Write a blank line at the beginning of the machine-readable
        # file to serve as a tablet delimiter.  Each tablet already ends
        # with a newline.

        fout.write('\n')

        for tablet in tablets:
            for line in tablet:
                fout.write(line)


def write_tablet_files(tablets, index):
    write_human_file(tablets, index)
    write_machine_file(tablets, index)


def segment(args):

    fin = fileinput.input('-')
    tablets = [ ]
    index = 1

    # Skip all lines up to and including the first blank line in the
    # corpus.

    loop = True
    while loop:
        line = fin.readline()
        if '\n' == line:
            loop = False

    tablet = get_next_tablet(fin)

    while tablet:
        tablets.append(tablet)

        if (len(tablets) == args.count):
            write_tablet_files(tablets, index)
            index += 1
            tablets = [ ]

        tablet = get_next_tablet(fin)

    write_tablet_files(tablets, index)
        
    fin.close()


# ====
# Main
# ====

args = init_parser()
segment(args)
