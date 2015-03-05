# sumerian-crf

Generation of Sumerian sources for named entity extraction via Conditional Random Fields.

To use, run `make all` at the command line.  The following files will be downloaded, generated, or regenerated as needed:

- *cdli_atffull.atf*: CDLI sources provided by http://cdli.ucla.edu.

- *cdli_atffull_lemma.atf*: The portion of the CDLI sources that have been lemmatized extracted into a single file.  This is an intermediate step for further processing, but you may find the interlinear lemmata to be useful for your own purposes.

- *cdli_atffull_tagged.atf*: A file in which each word of each lemmatized tablet is rendered on its own line along with the part of speech with which it was tagged in the lemmata, delimited by tabs.  Lines on a tablet are delimited by the special tokens **&lt;l&gt;** to begin a line and **&lt;/l&gt;** to end it; tablets are delimited by blank spaces.

- *cdli_atffull_crf_train.csv* and *cdli_atffull_crf_test.csv*: These are most likely to be the files of most immediate use.  They are a training and a testing corpus that extend the fields in *cdli_atffull_tagged.atf* by including many feature values as tab-delimited fields.  See below for a full description of all features used by this script.  By default, the training set is 80% of the lemmatized Ur III corpus, and the testing set 20%.  Part of speech tags (from which the PN/non-PN tag for each word can be deduced) are left in the training corpus to allow you to gauge the F-measure of your algorithm.

- *cdli_atffull_wordtagfreq.txt*: a sorted list of all words appearing in the corpus and the frequency with which the tags for these words appear.  Presented in JSON format.

- *pos_frequency/*: a directory containing per-tag word inventory and related frequency analysis presented for your convenience.  Per-tag analysis is provided, as well as all-word and non-PN analysis.

Further things to note:
  - No comments or tablet metadata appear in this file.
  - Glosses are suppressed in this file; any word with a citation form is rendered with the synthetic tag **W**, which does not appear in the lemmata.  For instance, the gloss **geme[worker]** appearing in the lemmata is replaced with the tag **W**.
  - In cases where more than one lemma is associated with a word, only the most commonly attributed lemma for that word is included in the tag.  For instance, in some tablets, the word **{d}dumu-zi-[sze3]** is given as **DN|MN|FN**, meaning that the word can appear in any of those contexts.  When multiple lemmata are available for a single word, only the most frequently attested one will be used.
  - Common professions will be replaced with the synthetic tag **PF**, which does not occur in the lemmata.

## Features in *cdli_atffull_tagged_crf.csv*

Type      | Description
--------- | -----------
word/word | Source word and lemma.  **Do not use this in your input**, since the lemma is hidden information that cannot be calculated from context.  It's solely for human readability.
integer   | Word index in line.  0-indexed.
word      | Left context.  None if this is the first word in the line.
word      | Right context.  None if this is the last word in the line.
word+     | Line context.  All words in line, space-delimited.
boolean   | 1 if word is alone on line, else 0.
boolean   | 1 if left context is **dumu** "*child (of)*".  This may suggest a personal name in a patronymic.
boolean   | 1 if right context is **dumu** "*child (of)*".  This may suggest a personal name in a patronymic.
boolean   | 1 if line context is **ki _word_**. This may suggest a seller in a transaction.
boolean   | 1 if line context is **igi _word_**.  This may suggest a witness to a transaction.
boolean   | 1 if line context is **igi _word_-sze3**.  This may suggest a witness to a transaction.
boolean   | 1 if line context is the Personnenkeil **1(disz) _word_**.  This may suggest a list of named individuals.
boolean   | 1 if line context is **kiszib3 _word_**.  This may suggest the individual responsible for sealing a tablet.
boolean   | 1 if line context is **giri3 _word_**.  This may suggest a named intermediary in a transaction doing business on behalf of another.
boolean   | 1 if first sign in word is repeated (implies that word contains more than one sign).  Sumerian names tend to favor repeated syllables.
boolean   | 1 if last sign in word is repeated (implies that word contains more than one sign).  Sumerian names tend to favor repeated syllables.
boolean   | 1 if any sign in word is repeated (implies that word contains more than one sign).  Sumerian names tend to favor repeated syllables.
boolean   | 1 if word is a common profession.
boolean   | 1 if word contains a profession.
boolean   | 1 if left context is a profession.
boolean   | 1 if left context contains a profession.
boolean   | 1 if right context is a profession.
boolean   | 1 if right context contains a profession.
boolean   | 1 if word starts with **ur-**.  This is common in personal names.
boolean   | 1 if word starts with **lu2-**.  This is common in personal names, but is also common in other contexts.
boolean   | 1 if word ends with **-mu**.  This is common in personal names, but is also common in other contexts.
boolean   | 1 if word contains **{d}**, (short for **dingir** "*deity*") the divine determinative.  Personal names strongly favor such theophoric elements but usually include other signs as well.
boolean   | 1 if word contains **{ki}** "*place*".  In formal Sumerian, all city names contain this sign (unless the scribe omits it), but personal names may also contain this sign (cf. Leonardo *da Vinci*).
boolean   | 1 if word contains any determinative.
boolean   | 1 if word's transliteration contains the letter *q*.  This sign (which has phonetic value of *qoppa*) is not native to Sumerian.
boolean   | 1 if word contains **lugal** ("*king*; *large*").  Sumerian names favor elements of praise to the king, but **lugal** appears in many other contexts as well.
boolean   | 1 if word contains a number.  Generally, numeric elements tend to be isolated, but occasionally can agglutinate in names.
boolean   | 1 if word followed by **sag**, a quality modifier usually associated with trade goods.
boolean   | 1 if word followed by **zarin**, a (low-) quality modifier usually associated with trade goods.
boolean   | 1 if word followed by a numeric classifier.  A numeric classifier combines both a quantity (with a different symbol for each base in the Sumerian number system) and a specific type of object (dry measure, liquids, precious metals, land).
boolean   | 1 if line context begins with **iti** "*month*".  Lines of this type strongly correlate with information on the month on which a transaction occurred.
boolean   | 1 if line context begins with **mu** "*year*".  Lines of this type correlate much more weakly with information on the year on which a transaction occurred.
word      | Correct lemma tag.  Use this in training, and use to evaluate the performance of your algorithm in testing.

## Lemmata tags

Tag   | Description 
----- | ----------- 
CN    | celestial name (uncommon)
DN    | divine name (deities)
FN    | field name (agricultural)
GN    | geographical name
MN    | month name
n     | numeric (numbers and number classifiers)
ON    | object names (uncommon; artifacts of cultural significance)
PN    | personal name
RN    | royal name (kings)
TN    | temple name
u     | unlemmatizable (generally due to damage to source tablets)
WN    | watercourse (river) name
X     | unknown word

## Common determinatives

Determinative | Meaning
------------- | -------
**{d}**     | Divine names
**{ki}**    | City and geographical names
**{gesz}**  | Wooden items
**{gi}**    | Objects made of reeds
**{tug2}**  | Garments
**{munus}** | Female names and professions
**{u2}**    | Plants and vegetables
**{kusz}**  | Leather items
**{uruda}** | Copper items
