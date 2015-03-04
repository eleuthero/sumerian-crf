#!/usr/bin/python

from tablet import Line
from sys import stdout

class Context:

    @staticmethod
    def get_left_context(line, index, word, args, offset = 1):

        (leftword, leftlem) = (None, None)
        if (index - offset) >= 0:
            (leftword, leftlem) = line.words[index - offset]

        if args.nogloss:
            leftlem = Context.remove_gloss(leftlem)

        return (leftword, leftlem)


    @staticmethod
    def get_right_context(line, index, word, args, offset = 1):

        (rightword, rightlem) = (None, None)
        if (len(line.words) - 1) >= (index + offset):
            (rightword, rightlem) = line.words[index + offset]

        if args.nogloss:
            rightlem = Context.remove_gloss(rightlem)

        return (rightword, rightlem)


    @staticmethod
    def remove_gloss(lem):
        if lem:
            lem = list( set( [ l if not '[' in l
                               else 'W' 
                               for l in lem ] ))
        return lem


    @staticmethod
    def format_context(lem):
        if not lem:
            return None
        else:
            return ','.join(lem)


    @staticmethod
    def write_header():
        stdout.write( '\tWord/Lemma'
                      '\tWord Index'
                      '\tLeft Context Word'
                      '\tLeft Context Lemma'
                      '\tRight Context Word'
                      '\tRight Context Lemma'
                      '\tLine Context'
                      '\tIs Word Alone On Line'
                      '\tLeft context is dumu'
                      '\tRight context is dumu'
                      '\tNone ki (word) None'
                      '\tNone igi (word) None'
                      '\tNone igi (word)-sze3 None'
                      '\tPersonnenkeil'
                      '\tNone kiszib3 (word)'
                      '\tNone jiri3 (word)'
                      '\tFirst syllable repeated'
                      '\tLast syllable repeated'
                      '\tAny syllable repeated'
                      '\tStarts with ur-'
                      '\tStarts with lu2-'
                      '\tEnds with -mu'
                      '\tContains {d}'
                      '\tContains {ki}'
                      '\tContains any determinative'
                      '\tContains q sound'
                      '\tContains lugal'
                      '\tContains number'
                      '\tFollowed by sag'
                      '\tFollowed by zarin'
                      '\tPreceded by numeric classifier'
                      '\titi at head of sentence'
                      '\tmu at head of sentence'
                      '\tIs PN'
                      '\n' )
                      

    @staticmethod
    def test(tests):
        for t in tests:
            if not t:
                stdout.write( '\t{}'.format(0) )
                return
        stdout.write( '\t{}'.format(1) )


    @staticmethod
    def write(line, index, word, args):

        # Variables that we may use as part of other features.

        lemmata = line.get_lemmata(word)
        signs = word.split('-')

        (leftcx, leftlem) = \
            Context.get_left_context(line, index, word, args)

        (leftcx2, leftlem2) = \
            Context.get_left_context(line, index, word, args, offset = 2)

        (rightcx, rightlem) = \
            Context.get_right_context(line, index, word, args)

        # Print raw lemma tag.  May include gloss, even when
        # --nogloss switch is provided.  This is for the benefit
        # of human readers with some familiarity with Sumerian.
 
        stdout.write( '\t"{}/{}"'.format( word,
                                          Context.format_context(lemmata) ))

        # Index of word in line.  0-based.

        stdout.write( '\t{}'.format(index) )

        # Left context and tag.

        stdout.write( '\t{}\t{}'.format( leftcx,
                                         Context.format_context(leftlem) ))

        # Right context and tag.

        stdout.write( '\t{}\t{}'.format( rightcx,
                                         Context.format_context(rightlem) ))

        # Print line context.

        stdout.write( '\t"{}"'.format(line.line) )

        # Is word alone on line ?

        Context.test([ (leftcx, rightcx) == (None, None) ])
        
        # Left context is dumu.

        Context.test([ (leftcx == 'dumu') ])

        # Right context is dumu.

        Context.test([ (rightcx == 'dumu') ])

        # ^ ki <word> $

        Context.test([ (leftcx2, leftcx, rightcx) == (None, 'ki', None) ])
            
        # ^ igi <word> $

        Context.test([ (leftcx2, leftcx, rightcx) == (None, 'igi', None) ])

        # ^ igi <word>-sze $

        Context.test([ (leftcx2, leftcx, rightcx) == (None, 'igi', None),
                        word.endswith('-sze3') ])

        # Personnenkeil: ^ 1(disz) <word> $

        Context.test([ (leftcx2, leftcx, rightcx) == (None, '1(disz)', None) ])

        # ^ kiszib3 <word> $

        Context.test([ (leftcx2, leftcx, rightcx) == (None, 'kiszib3', None) ])

        # ^ jiri3 <word> $

        Context.test([ (leftcx2, leftcx, rightcx) == (None, 'jiri3', None) ])

        # First syllable repeated

        if len(signs) > 1:
            Context.test([ signs[0] == signs[1] ])
        else:
            Context.test([ False ])

        # Last syllable repeated

        signs = word.split('-')
        if len(signs) > 1:
            Context.test([ signs[-2] == signs[-1] ])
        else:
            Context.test([ False ])

        # Any syllable repeated

        if len(signs) > 1:
            Context.test([ True in [ a == b for (a, b)
                                     in zip(signs, signs[1:]) ] ])
        else:
            Context.test([ False ])

        # Starts with ur-

        Context.test([ word.startswith('ur-') ])
        
        # Starts with lu2-

        Context.test([ word.startswith('lu2-') ])
        
        # Ends with -mu

        Context.test([ word.endswith('-mu') ])
        
        # Contains {d}

        Context.test([ '{d}' in word ])

        # Contains {ki}

        Context.test([ '{ki}' in word ])

        # Contains any determinative

        Context.test([ '{' in word ])

        # Contains q sound

        Context.test([ 'q' in word ])

        # Contains lugal

        Context.test([ 'lugal' in word ])

        # Contains numeric elements

        Context.test([ '(asz)' in word \
                       or '(disz)' in word \
                       or '(u)' in word ])

        # Followed by sag

        Context.test([ rightcx == 'sag' ])

        # Followed by zarin

        Context.test([ rightcx == 'zarin' ])

        # Preceded by numeric classifier

        Context.test([ leftcx in ( 'ba-an', 'ba-ri2-ga', 'bur3', 'da-na',
                                   'gin2-tur', 'gin2', 'gur-lugal', 
                                   'gur-sag-gal2', 'gur', 'iku', 'GAN2',
                                   'ku-li-mu', 'ku-li-kam', 'kusz3',
                                   'sar', 'sila3' ) ])

        # iti at head of sentence

        Context.test([ 'iti' == line.words[0][0] ])

        # mu at head of sentence

        Context.test([ 'mu' == line.words[0][0] ])

        # Print boolean feature, 1 if word is PN, 0 if not.

        if 'PN' in lemmata:
            stdout.write( '\t{}'.format(1) )
        else:
            stdout.write( '\t{}'.format(0) )

        """
        # Print most common tag for this word.

        # Actually, don't print the most common tag for this word.
        # This is not a good feature for CRF (or any feature-based
        # NLP algorithm) since it's # not immediately calculable
        # from context as a feature should be, but rather requires
        # reference to the index of the entire corpus.

        if word in INDEX:
        (bestlem, _) = INDEX[word].most_common(1)[0]
        else:
        bestlem = 'X'

        stdout.write('\t{}'.format( formatLems([ bestlem ], args) )) """


