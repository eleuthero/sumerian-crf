# sumerian-crf

Generation of Sumerian sources for named entity extraction via Conditional Random Fields.

To use, run `make all` at the command line.  The following files will be downloaded, generated, or regenerated as needed:

- *cdli_atffull.atf*: CDLI sources provided by http://cdli.ucla.edu.

- *cdli_atffull_lemma.atf*: The portion of the CDLI sources that have been lemmatized extracted into a single file.  This is an intermediate step for further processing, but you may find the interlinear lemmata to be useful for your own purposes.

- *cdli_atffull_tagged.atf*: A file in which each word of each lemmatized tablet is rendered on its own line along with the part of speech with which it was tagged in the lemmata, delimited by tabs.  Lines on a tablet are delimited by the special tokens `<l>` to begin a line and `</l>` to end it; tablets are delimited by blank spaces.

Further things to note:
  - No comments or tablet metadata appear in this file.
  - Glosses are suppressed in this file; any word with a citation form is rendered with the synthetic tag `W`, which does not appear in the lemmata.  For instance, the gloss `geme[worker]` appearing in the lemmata is replaced with the tag `W`.
  - In cases where more than one lemma is associated with a word, only the most commonly attributed lemma for that word is included in the tag.  For instance, in some tablets, the word `{d}dumu-zi-[sze3]` is given as `DN|MN|FN`, meaning that the word can appear in any of those contexts.  When multiple lemmata are available for a single word, only the most frequently attested one will be used.
  - Common professions will be replaced with the synthetic tag `PF`, which does not occur in the lemmata.

- *cdli_atffull_tagged_crf.atf*: This is most likely to be the file of most immediate use.  It extends the fields in *cdli_atffull_tagged.atf* by including the following tab-delimited fields:
  - Word, with any transliteration noise removed
  - Citation form/gloss.  You may choose to ignore this; it is provided for readability by humans with some familiarity with the language.
  - Line context.  Every word in the current line is provided; transliteration noise has been removed.
  - Boolean PN indicator.  1 if the current word is lemmatized as a personal name (PN); 0 if not.
  - Most frequent tag for this word.  This is usually also the tag provided by the lemmata, but not always.
  - Tag for this word provided by the lemmata.

- *cdli_atffull_wordtagfreq.txt*: a sorted list of all words appearing in the corpus and the frequency with which the tags for these words appear.  Presented in JSON format.

- *pos_frequency/*: a directory containing per-tag word inventory and related frequency analysis presented for your convenience.  Per-tag analysis is provided, as well as all-word and non-PN analysis.

# Lemmata tags

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
