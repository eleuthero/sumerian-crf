#!/bin/bash

# To do all of the above, type ``make all'.
# To remove all automatically-generated files, type ``make clean''.

SHELL=/bin/bash
WGET=/usr/bin/wget
UNZIP=/usr/bin/unzip

CORPUS_FILE_ZIP=./cdli_atffull.zip
CORPUS_FILE_URL= http://www.cdli.ucla.edu/tools/cdlifiles/$(CORPUS_FILE_ZIP)
CORPUS_FILE=./cdli_atffull.atf

CORPUS_TRAINING_PERCENT=85
CORPUS_COUNT=1
CORPUS_RNGSEED=1

CORPUS_LEMMA_FILE=./cdli_atffull_lemma.atf
CORPUS_TAGGED_FILE=./cdli_atffull_tagged.atf
CORPUS_WORDTAGFREQ_FILE=./cdli_atffull_wordtagfreq.txt
CORPUS_POSFREQUENCY_DIR=./pos_frequency
CORPUS_BARETAGGED_FILE=./$(CORPUS_POSFREQUENCY_DIR)/cdli_atffull_bare.atf


all: corpus tagfreq 

# Generate corpus
# ===============

corpus:	\
    $(CORPUS_TAGGED_FILE)

# Fetch compressed CDLI Ur III corpus from source.
# ================================================

$(CORPUS_FILE_ZIP):

	@echo "Getting full corpus file from CDLI..."
	$(WGET) $(CORPUS_FILE_URL) -O $(CORPUS_FILE_ZIP)

# Uncompress CDLI corpus.

$(CORPUS_FILE): $(CORPUS_FILE_ZIP)

	if [ ! -f "$(CORPUS_FILE)" ]; then \
		$(UNZIP) $(CORPUS_FILE_ZIP); \
	fi

# Filter corpus to generate lemmatized portion.

$(CORPUS_LEMMA_FILE): $(CORPUS_FILE)

	cat $(CORPUS_FILE) \
		| python ./generate_corpus.py \
			--lang sux \
		> $(CORPUS_LEMMA_FILE)

# From the lemmatized corpus, generate a tagged corpus.

$(CORPUS_TAGGED_FILE): $(CORPUS_LEMMA_FILE)

	cat $(CORPUS_LEMMA_FILE) \
		| python ./tag_corpus.py \
			--nogloss --bestlemma --pf \
			--dumpindex $(CORPUS_WORDTAGFREQ_FILE) \
		> $(CORPUS_TAGGED_FILE)



# Corpus statistics by part of speech.
# ====================================

# Generate a bare tagged file containing only the words in the lemmatized
# corpus and their associated parts of speech.

tagfreq: \
    $(CORPUS_POSFREQUENCY_DIR) \
    ./$(CORPUS_POSFREQUENCY_DIR)/fn_frequency.txt \
    ./$(CORPUS_POSFREQUENCY_DIR)/gn_frequency.txt \
    ./$(CORPUS_POSFREQUENCY_DIR)/mn_frequency.txt \
    ./$(CORPUS_POSFREQUENCY_DIR)/n_frequency.txt \
    ./$(CORPUS_POSFREQUENCY_DIR)/on_frequency.txt \
    ./$(CORPUS_POSFREQUENCY_DIR)/pn_frequency.txt \
    ./$(CORPUS_POSFREQUENCY_DIR)/tn_frequency.txt \
    ./$(CORPUS_POSFREQUENCY_DIR)/u_frequency.txt \
    ./$(CORPUS_POSFREQUENCY_DIR)/wn_frequency.txt \
    ./$(CORPUS_POSFREQUENCY_DIR)/w_frequency.txt \
    ./$(CORPUS_POSFREQUENCY_DIR)/x_frequency.txt

$(CORPUS_POSFREQUENCY_DIR):

	mkdir --parents ./$(CORPUS_POSFREQUENCY_DIR)

$(CORPUS_BARETAGGED_FILE): $(CORPUS_LEMMA_FILE)

	cat $(CORPUS_LEMMA_FILE) \
		| python ./tag_corpus.py \
			--nogloss --bestlemma --pf --bare \
		> $(CORPUS_BARETAGGED_FILE)

# FN (field name) frequency analysis.

./$(CORPUS_POSFREQUENCY_DIR)/fn.txt: \
    $(CORPUS_BARETAGGED_FILE)

	cat $(CORPUS_BARETAGGED_FILE) \
		| sed -e 's/ /\n/g' \
		| grep '\$$FN\$$' \
		| sed -e '/^$$/d' \
		| awk 'BEGIN { FS="$$"; } { print $$1; }' \
		> ./$(CORPUS_POSFREQUENCY_DIR)/fn.txt

./$(CORPUS_POSFREQUENCY_DIR)/fn_frequency.txt: \
    ./$(CORPUS_POSFREQUENCY_DIR)/fn.txt

	cat ./$(CORPUS_POSFREQUENCY_DIR)/fn.txt \
		| grep -v "x" \
		| sort | uniq -c | sort -rn \
		> ./$(CORPUS_POSFREQUENCY_DIR)/fn_frequency.txt

	sort -k2.1 ./$(CORPUS_POSFREQUENCY_DIR)/fn_frequency.txt \
		> ./$(CORPUS_POSFREQUENCY_DIR)/fn_sorted.txt

# GN (geographical name) frequency analysis.

./$(CORPUS_POSFREQUENCY_DIR)/gn.txt: \
    $(CORPUS_BARETAGGED_FILE)

	cat $(CORPUS_BARETAGGED_FILE) \
		| sed -e 's/ /\n/g' \
		| grep '\$$GN\$$' \
		| sed -e '/^$$/d' \
		| awk 'BEGIN { FS="$$"; } { print $$1; }' \
		| sed -e 's/{ki}.*/{ki}/g' \
		> ./$(CORPUS_POSFREQUENCY_DIR)/gn.txt

./$(CORPUS_POSFREQUENCY_DIR)/gn_frequency.txt: \
    ./$(CORPUS_POSFREQUENCY_DIR)/gn.txt

	cat ./$(CORPUS_POSFREQUENCY_DIR)/gn.txt \
		| sort | uniq -c | sort -rn \
		> ./$(CORPUS_POSFREQUENCY_DIR)/gn_frequency.txt

	sort -k2.1 ./$(CORPUS_POSFREQUENCY_DIR)/gn_frequency.txt \
		> ./$(CORPUS_POSFREQUENCY_DIR)/gn_sorted.txt

# MN (month name) frequency analysis.

./$(CORPUS_POSFREQUENCY_DIR)/mn.txt: \
    $(CORPUS_BARETAGGED_FILE)

	cat $(CORPUS_BARETAGGED_FILE) \
		| sed -e 's/ /\n/g' \
		| grep '\$$MN\$$' \
		| sed -e '/^$$/d' \
		| awk 'BEGIN { FS="$$"; } { print $$1; }' \
		> ./$(CORPUS_POSFREQUENCY_DIR)/mn.txt

./$(CORPUS_POSFREQUENCY_DIR)/mn_frequency.txt: \
    ./$(CORPUS_POSFREQUENCY_DIR)/mn.txt

	cat ./$(CORPUS_POSFREQUENCY_DIR)/mn.txt \
		| sort | uniq -c | sort -rn \
		> ./$(CORPUS_POSFREQUENCY_DIR)/mn_frequency.txt

	sort -k2.1 ./$(CORPUS_POSFREQUENCY_DIR)/mn_frequency.txt \
		> ./$(CORPUS_POSFREQUENCY_DIR)/mn_sorted.txt

# n (number) frequency analysis.

./$(CORPUS_POSFREQUENCY_DIR)/n.txt: \
    $(CORPUS_BARETAGGED_FILE)

	cat $(CORPUS_BARETAGGED_FILE) \
		| sed -e 's/ /\n/g' \
		| grep '\$$n\$$' \
		| sed -e '/^$$/d' \
		| awk 'BEGIN { FS="$$"; } { print $$1; }' \
		> ./$(CORPUS_POSFREQUENCY_DIR)/n.txt

./$(CORPUS_POSFREQUENCY_DIR)/n_frequency.txt: \
    ./$(CORPUS_POSFREQUENCY_DIR)/n.txt

	cat ./$(CORPUS_POSFREQUENCY_DIR)/n.txt \
		| sort | uniq -c | sort -rn \
		> ./$(CORPUS_POSFREQUENCY_DIR)/n_frequency.txt

	sort -k2.1 ./$(CORPUS_POSFREQUENCY_DIR)/n_frequency.txt \
		> ./$(CORPUS_POSFREQUENCY_DIR)/n_sorted.txt

# ON (object name) frequency analysis.

./$(CORPUS_POSFREQUENCY_DIR)/on.txt: \
    $(CORPUS_BARETAGGED_FILE)

	cat $(CORPUS_BARETAGGED_FILE) \
		| sed -e 's/ /\n/g' \
		| grep '\$$ON\$$' \
		| sed -e '/^$$/d' \
		| awk 'BEGIN { FS="$$"; } { print $$1; }' \
		> ./$(CORPUS_POSFREQUENCY_DIR)/on.txt

./$(CORPUS_POSFREQUENCY_DIR)/on_frequency.txt: \
    ./$(CORPUS_POSFREQUENCY_DIR)/on.txt

	cat ./$(CORPUS_POSFREQUENCY_DIR)/on.txt \
		| sort | uniq -c | sort -rn \
		> ./$(CORPUS_POSFREQUENCY_DIR)/on_frequency.txt

	sort -k2.1 ./$(CORPUS_POSFREQUENCY_DIR)/on_frequency.txt \
		> ./$(CORPUS_POSFREQUENCY_DIR)/on_sorted.txt

# PN (personal name) frequency analysis.

./$(CORPUS_POSFREQUENCY_DIR)/pn.txt: \
    $(CORPUS_BARETAGGED_FILE)

	cat $(CORPUS_BARETAGGED_FILE) \
		| sed -e 's/ /\n/g' \
		| grep '\$$PN\$$' \
		| sed -e '/^$$/d' \
		| awk 'BEGIN { FS="$$"; } { print $$1; }' \
		> ./$(CORPUS_POSFREQUENCY_DIR)/pn.txt

./$(CORPUS_POSFREQUENCY_DIR)/pn_frequency.txt: \
    ./$(CORPUS_POSFREQUENCY_DIR)/pn.txt

	cat ./$(CORPUS_POSFREQUENCY_DIR)/pn.txt \
		| sort | uniq -c | sort -rn \
		> ./$(CORPUS_POSFREQUENCY_DIR)/pn_frequency.txt

	sort -k2.1 ./$(CORPUS_POSFREQUENCY_DIR)/pn_frequency.txt \
		> ./$(CORPUS_POSFREQUENCY_DIR)/pn_sorted.txt

# TN (temple name) frequency analysis.

./$(CORPUS_POSFREQUENCY_DIR)/tn.txt: \
    $(CORPUS_BARETAGGED_FILE)

	cat $(CORPUS_BARETAGGED_FILE) \
		| sed -e 's/ /\n/g' \
		| grep '\$$TN\$$' \
		| sed -e '/^$$/d' \
		| awk 'BEGIN { FS="$$"; } { print $$1; }' \
		> ./$(CORPUS_POSFREQUENCY_DIR)/tn.txt

./$(CORPUS_POSFREQUENCY_DIR)/tn_frequency.txt: \
    ./$(CORPUS_POSFREQUENCY_DIR)/tn.txt

	cat ./$(CORPUS_POSFREQUENCY_DIR)/tn.txt \
		| sort | uniq -c | sort -rn \
		> ./$(CORPUS_POSFREQUENCY_DIR)/tn_frequency.txt

	sort -k2.1 ./$(CORPUS_POSFREQUENCY_DIR)/tn_frequency.txt \
		> ./$(CORPUS_POSFREQUENCY_DIR)/tn_sorted.txt

# u (unlemmatizable) frequency analysis.

./$(CORPUS_POSFREQUENCY_DIR)/u.txt: \
    $(CORPUS_BARETAGGED_FILE)

	cat $(CORPUS_BARETAGGED_FILE) \
		| sed -e 's/ /\n/g' \
		| grep '\$$u\$$' \
		| sed -e '/^$$/d' \
		| awk 'BEGIN { FS="$$"; } { print $$1; }' \
		> ./$(CORPUS_POSFREQUENCY_DIR)/u.txt

./$(CORPUS_POSFREQUENCY_DIR)/u_frequency.txt: \
    ./$(CORPUS_POSFREQUENCY_DIR)/u.txt

	cat ./$(CORPUS_POSFREQUENCY_DIR)/u.txt \
		| sort | uniq -c | sort -rn \
		> ./$(CORPUS_POSFREQUENCY_DIR)/u_frequency.txt

	sort -k2.1 ./$(CORPUS_POSFREQUENCY_DIR)/u_frequency.txt \
		> ./$(CORPUS_POSFREQUENCY_DIR)/u_sorted.txt

# WN (watercourse name) frequency analysis.

./$(CORPUS_POSFREQUENCY_DIR)/wn.txt: \
    $(CORPUS_BARETAGGED_FILE)

	cat $(CORPUS_BARETAGGED_FILE) \
		| sed -e 's/ /\n/g' \
		| grep '\$$WN\$$' \
		| sed -e '/^$$/d' \
		| awk 'BEGIN { FS="$$"; } { print $$1; }' \
		> ./$(CORPUS_POSFREQUENCY_DIR)/wn.txt

./$(CORPUS_POSFREQUENCY_DIR)/wn_frequency.txt: \
    ./$(CORPUS_POSFREQUENCY_DIR)/wn.txt

	cat ./$(CORPUS_POSFREQUENCY_DIR)/wn.txt \
		| sort | uniq -c | sort -rn \
		> ./$(CORPUS_POSFREQUENCY_DIR)/wn_frequency.txt

	sort -k2.1 ./$(CORPUS_POSFREQUENCY_DIR)/wn_frequency.txt \
		> ./$(CORPUS_POSFREQUENCY_DIR)/wn_sorted.txt

# X (unknown) frequency analysis.

./$(CORPUS_POSFREQUENCY_DIR)/x.txt: \
    $(CORPUS_BARETAGGED_FILE)

	cat $(CORPUS_BARETAGGED_FILE) \
		| sed -e 's/ /\n/g' \
		| grep '\$$X\$$' \
		| sed -e '/^$$/d' \
		| awk 'BEGIN { FS="$$"; } { print $$1; }' \
		> ./$(CORPUS_POSFREQUENCY_DIR)/x.txt

./$(CORPUS_POSFREQUENCY_DIR)/x_frequency.txt: \
    ./$(CORPUS_POSFREQUENCY_DIR)/x.txt

	cat ./$(CORPUS_POSFREQUENCY_DIR)/x.txt \
		| sort | uniq -c | sort -rn \
		> ./$(CORPUS_POSFREQUENCY_DIR)/x_frequency.txt

	sort -k2.1 ./$(CORPUS_POSFREQUENCY_DIR)/x_frequency.txt \
		> ./$(CORPUS_POSFREQUENCY_DIR)/x_sorted.txt

# all words frequency analysis.

./$(CORPUS_POSFREQUENCY_DIR)/w.txt: \
    $(CORPUS_BARETAGGED_FILE)

	cat $(CORPUS_BARETAGGED_FILE) \
		| sed -e 's/ /\n/g' \
                | sed -e '/^$$/d' \
		> ./$(CORPUS_POSFREQUENCY_DIR)/w.txt

./$(CORPUS_POSFREQUENCY_DIR)/w_frequency.txt: \
    ./$(CORPUS_POSFREQUENCY_DIR)/w.txt

	cat ./$(CORPUS_POSFREQUENCY_DIR)/w.txt \
		| sort | uniq -c | sort -rn \
		> ./$(CORPUS_POSFREQUENCY_DIR)/w_frequency.txt

	sort -k2.1 ./$(CORPUS_POSFREQUENCY_DIR)/w_frequency.txt \
		> ./$(CORPUS_POSFREQUENCY_DIR)/w_sorted.txt


# Cleanup
# =======

clean:
	rm -f $(CORPUS_LEMMA_FILE)
	rm -f $(CORPUS_TAGGED_FILE)
	rm -f $(CORPUS_WORDTAGFREQ_FILE)
	rm -f $(CORPUS_BARETAGGED_FILE)
	rm -rf $(CORPUS_POSFREQUENCY_DIR)
