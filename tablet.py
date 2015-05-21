#!/usr/bin/python

import re

class Line:

    COMMENT = '&$@#'

    NOISE = '[]!?#*<>'

    # Regular expressions used in massaging transliteration noise in lines.

    re_slash = re.compile(r"(/)[^0-9]")

    """
    Word regex; if a word doesn't match this regex, just ignore it; don't
    try to tag it.  This is necessary because of some transliterational
    typos, especially in older tablets, to prevent noise like commas from
    appearing as their own words.
    """

    re_word = re.compile(r"[A-Za-z0-9-]")

    """
    Implied signs: <<...>> indicates that the transliterator believes that
    the scribe has left out one or more signs.  These omitted signs will
    not appear in the lemmatization and so we need to remove the implied
    signs.
    """

    re_impl = re.compile(r"\<\<([A-Za-z0-9-()/#?*{}|@+ ]+)\>\>")

        
    """
    __init__():
    ===========
    Constructor.
    ===========
    Accepts:
        line:   Line from tablet.
        lem:    Corresponding lemma for line.  If line is a comment,
                    lem may be None.
    ===========
    """
    def __init__(self, line, lem):
        self.line = line
        self.lem = lem
        self.valid = None
        self.damaged = False
        self.damaged_and_tagged = False

        if lem:

            # The first five characters of a lemma line are "#lem:";
            # ignore these.

            self.lem = lem[5:].strip()

        self.words = [ ]
        self.parse()


    def get_lemmata(self, word):

        for (w, lemmata) in self.words:
            if word == w:
                return lemmata
        return None


    def parse(self):

        if not self.lem:
            self.valid = True
            return

        if self.line[0] in Line.COMMENT:
            self.valid = True
            self.lem = None
            return

        if '_' in self.line:

            # _ occurs in lemmata for Akkadian signs; if we see this
            # anywhere in the line, we need different rules to parse the
            # entire line.  We didn't sign up for that.

            self.valid = False
            self.lem = None
            return

        self.line = self.clean(self.line, self.lem)

        words = [ s.strip()
                  for s in self.line.split() ]
        lemtok = [ s.strip()
                   for s in self.lem.split(';') ]

        # Ensure same number of lemma tokens as words.

        self.valid = ( len(words) == len(lemtok) )

        if self.valid:

            in_comment = False

            for i in range(len(words)):
                word = words[i]
                tokens = lemtok[i]

                if ('%a' == word) or ('=' == word):

                    # This indicates that the language has switched
                    # (most likely to Akkadian) for the rest of the line.
                    # Stop parsing this line at this point.

                    break

                in_comment = self.add_word(word, tokens, in_comment)

            # Now that all of the words have been added to the line,
            # scan for damaged signs.

            self.scan_for_damage()


    def add_word(self, word, tokens, in_comment):

        # There is some additional transliteration noise in
        # the form of bare colons.  I'm not sure what they
        # mean, but they are consistently lemmatized as X,
        # so they're not merely typos.  Let's remove them.

        if (':' == word):
            return in_comment

        """
        The lines of text may contain inline comments in the form
        ($ ... $).  Oddly, the individual tokens in the inline
        comments are lemmatized individually:

        ki ($ blank space $)-ta
        ki[place]; X; X; X; X

        so we don't want to use a regex to remove the comments;
        rather, we'll just look for the inline comment delimiters
        and use the to set a processing flag.  Any signs
        interrupted by one of these inline comments (like the
        remaining -ta above) become noise in the lemma and we'll
        ignore them.
        """

        if '($' in word:

            # Just started a comment.

            return True

        if '$)' in word:

            # Just finished a comment.

            return False

        if in_comment:

            # Nothing to do.  Still in a comment.

            return True

        elements = [ ]
        self.words.append( (word, elements) )

        for element in tokens.split('|'):

            # Tag the word with the lemma token.

            elements.append(element)

        # Not in a comment.

        return False


    def scan_for_damage(self):

        self.damaged = False
        self.damaged_and_tagged = False

        for (word, lemtokens) in self.words:
            if ('x' == word) or ('-x' in word) or ('x-' in word) \
                             or ('}x' in word) or ('x{' in word):

                # Set the damaged flag for this line.

                self.damaged = True

                # However, some damaged signs have been tagged by the
                # transliterators, who felt confident in the strength of
                # the context to say that the damaged sign wasn't
                # unlemmatizable.  That lessens the effect of the damage
                # from our perspective.

                if 'u' not in lemtokens:

                    # Ok, great; this word is damaged but not tagged as
                    # 'u' (unlemmatizable due to damage).

                    self.damaged_and_tagged = True

                else:

                    # Uh oh.  There's unrecoverable damage to the line.
                    # That pretty much ruins this line for our purposes.
                    # No point in continuing.

                    self.damaged_and_tagged = False
                    return


    def removeAdditions(self, line):

        """
        Sometimes, scribes will leave out words that are implied by 
        context, or may simply have left out a word that the transliterator
        felt was recoverable from context.  For example,

        mu ha-ar-szi{ki} <<masz>> ki-masz{ki} ba-hul
        #lem: mu[year]; GN; GN; hulu[destroy]

        However, since these words aren't in the original text, any such
        additions by the transliterator are not lemmatized; as such,
        remove them from the line.
        """

        start = line.find("<<")
        while -1 != start:
            end = line.find(">>", start + 1)
            if -1 == end:

                # Hruh.  No closing angle brackets.  Chances are this
                # is going to invalidate the line since it'll throw the
                # line out of alignment with its corresponding lemma.
                # No really good options here, so we'll just remove
                # all the angle brackets and hope for the best.

                line = line.translate(None, "<<")
                break

            line = line[:start + 1] + line[end + 1:]
            start = line.find("<<")

        return line;


    def removeErasures(self, line):
        start = line.find("!(")

        # Obliterate any erased signs where they are specified; for instance,
        # replace "ma-na!(KI)-ag2" with "ma-na!-ag2".  We'll deal with the
        # remaining ! metacharacter elsewhere.

        while -1 != start:
            end = line.find(")", start + 1)
            if -1 != end:
                line = line[:start + 1] + line[end + 1:]
            start = line.find("!(")

        return line;
      
    def clean(self, line, lem):

        # Remove first word from line.

        line = ' '.join( [ word for word
                           in line.split(' ') ]
                         [1:] )

        # Remove any independent comma tokens.

        line = line.replace(' , ', ' ')

        # Remove commas at the end of the line.

        if line.endswith(','):
            line = line[:-1]

        # Delete any implied signs <<...>>.

        line = Line.re_impl.sub('', line)

        # Replace s, (Akkadian soft sz) with sz.

        line = line.replace('s,', 'sz')

        # Remove any signs that were erased and corrected by the scribe.

        line = self.removeErasures(line)

        # Remove any signs that were omitted by the scribe but added by
        # the transliterator.

        line = self.removeAdditions(line)

        # [...] indicates the loss of an indeterminate number of
        # signs.  Reduce this to x, a single lost sign, for our purposes.

        line = re.sub(r'\.\.\.', 'x', line)

        """
        # Deal with slashes; they may be either " " or "-".
        # Note: This has been commented out because the lemmata always
        # treat "erroneous" slashes as sign separators, even when the
        # signs are clearly meant to be word-broken, so there must be some
        # lemmatization rule that is being adhered to that I just don't
        # understand, as evidenced by the fact that the number of lemma tokens
        # is always equal to the number of words in the line when there is
        # a slash present.  We'll treat the slash as a sign separator.

        m = Line.re_slash.search(line)

        if m:
   
            words  = [ s.strip().translate(None, '[]!?#*<>') \
                       for s in line.split()[1:] ]
            lemtok = [ s.strip()
                       for s in lem.split(';') ]

            stdout.write("!!! matched bad slash: %i %i %s\n" % \
                         ( len(words), len(lemtok), line ))
            # line = Line.re_slash.sub('', line)
        """
            
        # Now that we're done with all of the processing of the line,
        # make one last cleaning pass on it to remove all of the
        # transliteration noise.

        line = line.translate(None, Line.NOISE)

        return line
