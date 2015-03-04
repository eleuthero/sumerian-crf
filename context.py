#!/usr/bin/python

from tablet import Line
from sys import stdout

class Context:

    # List of common professions in the Ur III corpus.

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
                      '\tIs profession'
                      '\tContains profession'
                      '\tLeft Context is profession'
                      '\tLeft Context contains profession'
                      '\tRight Context is profession'
                      '\tRight Context contains profession'
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
    def test_all(tests):
        for t in tests:
            if not t:
                Context.test_fail()
                return
        Context.test_pass()


    @staticmethod
    def test_any(tests):
        for t in tests:
            if t:
                Context.test_pass()
                return
        Context.test_fail()

    
    @staticmethod
    def test_pass():
        stdout.write( '\t{}'.format(1) )


    @staticmethod
    def test_fail():
        stdout.write( '\t{}'.format(0) )
        

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

        Context.test_all([ (leftcx, rightcx) == (None, None) ])
        
        # Left context is dumu.

        Context.test_all([ (leftcx == 'dumu') ])

        # Right context is dumu.

        Context.test_all([ (rightcx == 'dumu') ])

        # ^ ki <word> $

        Context.test_all([ (leftcx2, leftcx, rightcx) == (None, 'ki', None) ])
            
        # ^ igi <word> $

        Context.test_all([ (leftcx2, leftcx, rightcx) == (None, 'igi', None) ])

        # ^ igi <word>-sze $

        Context.test_all([ (leftcx2, leftcx, rightcx) == (None, 'igi', None),
                           word.endswith('-sze3') ])

        # Personnenkeil: ^ 1(disz) <word> $

        Context.test_all([ (leftcx2, leftcx, rightcx) == (None, '1(disz)', None) ])

        # ^ kiszib3 <word> $

        Context.test_all([ (leftcx2, leftcx, rightcx) == (None, 'kiszib3', None) ])

        # ^ jiri3 <word> $

        Context.test_all([ (leftcx2, leftcx, rightcx) == (None, 'jiri3', None) ])

        # First syllable repeated

        if len(signs) > 1:
            Context.test_all([ signs[0] == signs[1] ])
        else:
            Context.test_fail()

        # Last syllable repeated

        signs = word.split('-')
        if len(signs) > 1:
            Context.test_all([ signs[-2] == signs[-1] ])
        else:
            Context.test_fail()

        # Any syllable repeated

        if len(signs) > 1:
            Context.test_any([ a == b for (a, b)
                               in zip(signs, signs[1:]) ])
        else:
            Context.test_fail()

        # Is profession

        Context.test_any([ pf == lemmata 
                           for pf in Context.professions ])

        # Contains profession

        Context.test_any([ pf in lem 
                           for lem in lemmata
                           for pf in Context.professions ])

        # Left context is profession

        if leftlem:
            Context.test_any([ pf == lem
                               for lem in leftlem
                               for pf in Context.professions ])
        else:
            Context.test_fail()

        # Left context contains profession

        if leftlem:
            Context.test_any([ pf in lem
                               for lem in leftlem
                               for pf in Context.professions ])
        else:
            Context.test_fail()

        # Right context is profession

        if rightlem:
            Context.test_any([ pf == lem
                               for lem in rightlem 
                               for pf in Context.professions ])
        else:
            Context.test_fail()


        # Right context contains profession

        if rightlem:
            Context.test_any([ pf in lem
                               for lem in rightlem
                               for pf in Context.professions ])
        else:
            Context.test_fail()

        # Starts with ur-

        Context.test_all([ word.startswith('ur-') ])
        
        # Starts with lu2-

        Context.test_all([ word.startswith('lu2-') ])
        
        # Ends with -mu

        Context.test_all([ word.endswith('-mu') ])
        
        # Contains {d}

        Context.test_all([ '{d}' in word ])

        # Contains {ki}

        Context.test_all([ '{ki}' in word ])

        # Contains any determinative

        Context.test_all([ '{' in word ])

        # Contains q sound

        Context.test_all([ 'q' in word ])

        # Contains lugal

        Context.test_all([ 'lugal' in word ])

        # Contains numeric elements

        Context.test_any([ '(asz)' in word,
                           '(disz)' in word,
                           '(u)' in word ])

        # Followed by sag

        Context.test_all([ rightcx == 'sag' ])

        # Followed by zarin

        Context.test_all([ rightcx == 'zarin' ])

        # Preceded by numeric classifier

        Context.test_all([ leftcx in ( 'ba-an', 'ba-ri2-ga', 'bur3', 'da-na',
                                       'gin2-tur', 'gin2', 'gur-lugal', 
                                       'gur-sag-gal2', 'gur', 'iku', 'GAN2',
                                       'ku-li-mu', 'ku-li-kam', 'kusz3',
                                       'sar', 'sila3' ) ])

        # iti at head of sentence

        Context.test_all([ 'iti' == line.words[0][0] ])

        # mu at head of sentence

        Context.test_all([ 'mu' == line.words[0][0] ])

        # Print boolean feature, 1 if word is PN, 0 if not.

        if 'PN' in lemmata:
            Context.test_pass()
        else:
            Context.test_fail()

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


