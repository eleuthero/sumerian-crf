#!/usr/bin/python

from tablet import Line
from sys import stdout

class Context:

    @staticmethod
    def write(line, index, word, args):
        pass

        # Print raw lemma tag.  May include gloss, even when
        # --nogloss switch is provided.
 
        stdout.write( '\t"{}/{}"'.format( word,
                                      '|'.join(line.get_lemmata(word)) ))

        # Index of word in line.  0-based.

        stdout.write( '\t{}'.format(index) )

        # Left context and tag.

        (leftword, leftlem) = (None, None)
        if index > 0:
            (leftword, leftlem) = line.words[index - 1]
        stdout.write( '\t{}\t{}'.format(leftword, leftlem) )

        # Right context and tag.

        (rightword, rightlem) = (None, None)
        if (len(line.words) - 1) > index:
            (rightword, rightlem) = line.words[index + 1]
        stdout.write( '\t{}\t{}'.format(rightword, rightlem) )

        # Print line context.

        stdout.write( '\t"{}"'.format(line.line) )

        # Print boolean feature, 1 if word is PN, 0 if not.

        if 'PN' in line.get_lemmata(word):
            stdout.write( '\t{}'.format(1) )
        else:
            stdout.write( '\t{}'.format(0) )

        """
        # Print most common tag for this word.

        # Actually, don't print this, the most common tag for this word.
        # This is not a good feature for CRF, since it's # not immediately
        # calculable from context as a feature should be, but rather
        # requires reference to the index of the entire corpus.

        if word in INDEX:
        (bestlem, _) = INDEX[word].most_common(1)[0]
        else:
        bestlem = 'X'

        stdout.write('\t{}'.format( formatLems([ bestlem ], args) ))
        """
