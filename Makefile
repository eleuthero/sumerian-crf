#!/bin/bash

# To do all of the above, type ``make all'.
# To remove all automatically-generated files, type ``make clean''.

SHELL=/bin/bash
WGET=/usr/bin/wget
UNZIP=/usr/bin/unzip

CORPUS_FILE_ZIP=./cdli_atffull.zip
CORPUS_FILE_URL= http://www.cdli.ucla.edu/tools/cdlifiles/$(CORPUS_FILE_ZIP)
CORPUS_FILE=./cdli_atffull.atf

CORPUS_LEMMA_FILE=./cdli_atffull_lemma.atf
CORPUS_LEMMA_TAGGED_FILE=./cdli_atffull_lemma_tagged.atf
CORPUS_LEMMA_CRF_FILE=./cdli_atffull_lemma_crf.csv
CORPUS_TRAINING_PERCENT=80
CORPUS_LEMMA_CRF_TRAIN_FILE=./cdli_atffull_train_crf.csv
CORPUS_LEMMA_CRF_TEST1_FILE=./cdli_atffull_lemma_test1_crf.csv
CORPUS_LEMMA_CRF_TEST2_FILE=./cdli_atffull_lemma_test2_crf.csv

CORPUS_NOLEMMA_FILE=./cdli_atffull_nolemma.atf
CORPUS_NOLEMMA_TAGGED_FILE=./cdli_atffull_nolemma_tagged.atf
CORPUS_NOLEMMA_CRF_FILE=./cdli_atffull_nolemma_crf.csv
CORPUS_NOLEMMA_CRF_TEST1_FILE=./cdli_atffull_nolemma_test1_crf.csv
CORPUS_NOLEMMA_CRF_TEST2_FILE=./cdli_atffull_nolemma_test2_crf.csv
SEGMENTATION_TABLET_COUNT=10
SEGMENTATION_PERMITDAMAGE_DIRNAME=./segment_permit_damage
SEGMENTATION_REMOVEDAMAGE_DIRNAME=./segment_remove_damage

CORPUS_WORDTAGFREQ_FILE=./cdli_atffull_wordtagfreq.txt
CORPUS_POSFREQUENCY_DIR=./pos_frequency
CORPUS_BARETAGGED_FILE=$(CORPUS_POSFREQUENCY_DIR)/cdli_atffull_bare.atf

# all: corpus tagfreq tagcrf baseline $(CORPUS_WORDTAGFREQ_FILE)
all: corpus tagfreq tagcrf $(CORPUS_WORDTAGFREQ_FILE)

# Generate corpus
# ===============

corpus:	\
    $(CORPUS_LEMMA_TAGGED_FILE) \
    $(CORPUS_NOLEMMA_TAGGED_FILE)

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

# Partition corpus into lemmatized and unlemmatized files.

$(CORPUS_LEMMA_FILE) $(CORPUS_NOLEMMA_FILE): \
    $(CORPUS_FILE)

	cat $(CORPUS_FILE) \
		| python ./generate_corpus.py \
			--lang sux \
            --lemmatizedfile $(CORPUS_LEMMA_FILE) \
            --unlemmatizedfile $(CORPUS_NOLEMMA_FILE)

# From the lemmatized corpus, generate a tagged corpus.

$(CORPUS_LEMMA_TAGGED_FILE): $(CORPUS_LEMMA_FILE)

	cat $(CORPUS_LEMMA_FILE) \
		| python ./tag_corpus.py \
			--nogloss --bestlemma --pf \
		> $(CORPUS_LEMMA_TAGGED_FILE)

# From the unlemmatized corpus, generate a tagged corpus.

$(CORPUS_NOLEMMA_TAGGED_FILE): $(CORPUS_NOLEMMA_FILE)

	cat $(CORPUS_NOLEMMA_FILE) \
		| python ./tag_corpus.py \
		> $(CORPUS_NOLEMMA_TAGGED_FILE)

# From the lemma file, generate a list of tagged words.

$(CORPUS_WORDTAGFREQ_FILE): $(CORPUS_LEMMA_FILE)

	cat $(CORPUS_LEMMA_FILE) \
		| python ./tag_corpus.py \
			--nogloss --pf \
			--dumpindex $(CORPUS_WORDTAGFREQ_FILE) \
		> /dev/null

tagcrf: \
	$(CORPUS_LEMMA_CRF_TRAIN_FILE) \
	$(CORPUS_LEMMA_CRF_TEST1_FILE) \
	$(CORPUS_LEMMA_CRF_TEST2_FILE) \
	$(CORPUS_NOLEMMA_CRF_TEST1_FILE) \
	$(CORPUS_NOLEMMA_CRF_TEST2_FILE)

$(CORPUS_LEMMA_CRF_TRAIN_FILE) \
$(CORPUS_LEMMA_CRF_TEST1_FILE) \
$(CORPUS_LEMMA_CRF_TEST2_FILE): \
	$(CORPUS_LEMMA_CRF_FILE)

	cat $(CORPUS_LEMMA_CRF_FILE) \
		| python ./partition_corpus.py \
			--train $(CORPUS_LEMMA_CRF_TRAIN_FILE) \
			--test-remove-damage $(CORPUS_LEMMA_CRF_TEST1_FILE) \
			--test-permit-damage $(CORPUS_LEMMA_CRF_TEST2_FILE) \
			--percent $(CORPUS_TRAINING_PERCENT)

	# Done with this file; we just needed to split it up into a
	# training and a testing corpus.  Can remove it now, especially
	# since it's quite a sizable file.

	rm -f $(CORPUS_LEMMA_CRF_FILE)

$(CORPUS_NOLEMMA_CRF_TEST1_FILE) \
$(CORPUS_NOLEMMA_CRF_TEST2_FILE): \
	$(CORPUS_NOLEMMA_CRF_FILE)

	cat $(CORPUS_NOLEMMA_CRF_FILE) \
		| python ./partition_corpus.py \
			--train /dev/null \
			--test-remove-damage $(CORPUS_NOLEMMA_CRF_TEST1_FILE) \
			--test-permit-damage $(CORPUS_NOLEMMA_CRF_TEST2_FILE) \
			--percent 0

	mkdir $(SEGMENTATION_REMOVEDAMAGE_DIRNAME)
	cat $(CORPUS_NOLEMMA_CRF_TEST1_FILE) \
		| python ./segment.py \
			--count $(SEGMENTATION_TABLET_COUNT) \
			--directory $(SEGMENTATION_REMOVEDAMAGE_DIRNAME)

	mkdir $(SEGMENTATION_PERMITDAMAGE_DIRNAME)
	cat $(CORPUS_NOLEMMA_CRF_TEST2_FILE) \
		| python ./segment.py \
			--count $(SEGMENTATION_TABLET_COUNT) \
			--directory $(SEGMENTATION_PERMITDAMAGE_DIRNAME)

	# Done with this file; we just needed to split it up into chunks.
	# Can remove it now, especially since it's quite a sizable file.

	rm -f $(CORPUS_NOLEMMA_CRF_FILE)

$(CORPUS_LEMMA_CRF_FILE): $(CORPUS_LEMMA_FILE)

	cat $(CORPUS_LEMMA_FILE) \
		| python ./tag_corpus.py \
			--nogloss --bestlemma --crf \
		> $(CORPUS_LEMMA_CRF_FILE)

    # Add a blank line at the end of this file as a tablet delimiter.

	echo >> $(CORPUS_LEMMA_CRF_FILE)

$(CORPUS_NOLEMMA_CRF_FILE): $(CORPUS_NOLEMMA_FILE)

	cat $(CORPUS_NOLEMMA_FILE) \
		| python ./tag_corpus.py \
			--crf \
		> $(CORPUS_NOLEMMA_CRF_FILE)

    # Add a blank line at the end of this file as a tablet delimiter.

	echo >> $(CORPUS_NOLEMMA_CRF_FILE)

$(CORPUS_NOLEMMA_CRF_FILE): $(CORPUS_NOLEMMA_FILE)


baseline: tagcrf

	python ./baseline.py \
		--train $(CORPUS_LEMMA_CRF_TRAIN_FILE) \
		--test $(CORPUS_LEMMA_CRF_TEST1_FILE)

	python ./baseline.py \
		--train $(CORPUS_LEMMA_CRF_TRAIN_FILE) \
		--test $(CORPUS_LEMMA_CRF_TEST2_FILE)

# Corpus statistics by part of speech.
# ====================================

# Generate a bare tagged file containing only the words in the lemmatized
# corpus and their associated parts of speech.

tagfreq: \
    $(CORPUS_POSFREQUENCY_DIR) \
    $(CORPUS_POSFREQUENCY_DIR)/fn_frequency.txt \
    $(CORPUS_POSFREQUENCY_DIR)/gn_frequency.txt \
    $(CORPUS_POSFREQUENCY_DIR)/mn_frequency.txt \
    $(CORPUS_POSFREQUENCY_DIR)/n_frequency.txt \
    $(CORPUS_POSFREQUENCY_DIR)/on_frequency.txt \
    $(CORPUS_POSFREQUENCY_DIR)/pn_frequency.txt \
    $(CORPUS_POSFREQUENCY_DIR)/tn_frequency.txt \
    $(CORPUS_POSFREQUENCY_DIR)/u_frequency.txt \
    $(CORPUS_POSFREQUENCY_DIR)/wn_frequency.txt \
    $(CORPUS_POSFREQUENCY_DIR)/w_frequency.txt \
    $(CORPUS_POSFREQUENCY_DIR)/x_frequency.txt \
    $(CORPUS_POSFREQUENCY_DIR)/notpn_frequency.txt \
    $(CORPUS_POSFREQUENCY_DIR)/determinatives.txt \

$(CORPUS_POSFREQUENCY_DIR):

	mkdir --parents $(CORPUS_POSFREQUENCY_DIR)

$(CORPUS_BARETAGGED_FILE): $(CORPUS_LEMMA_FILE)

	cat $(CORPUS_LEMMA_FILE) \
		| python ./tag_corpus.py \
			--nogloss --bestlemma --pf --bare \
		> $(CORPUS_BARETAGGED_FILE)

# FN (field name) frequency analysis.

$(CORPUS_POSFREQUENCY_DIR)/fn.txt: \
    $(CORPUS_BARETAGGED_FILE)

	cat $(CORPUS_BARETAGGED_FILE) \
		| grep '\sFN$$' \
		| awk 'BEGIN { FS="\t"; } { print $$1; }' \
		> $(CORPUS_POSFREQUENCY_DIR)/fn.txt

$(CORPUS_POSFREQUENCY_DIR)/fn_frequency.txt: \
    $(CORPUS_POSFREQUENCY_DIR)/fn.txt

	cat $(CORPUS_POSFREQUENCY_DIR)/fn.txt \
		| grep -v "x" \
		| sort | uniq -c | sort -rn \
		> $(CORPUS_POSFREQUENCY_DIR)/fn_frequency.txt

	sort -k2.1 $(CORPUS_POSFREQUENCY_DIR)/fn_frequency.txt \
		> $(CORPUS_POSFREQUENCY_DIR)/fn_sorted.txt

# GN (geographical name) frequency analysis.

$(CORPUS_POSFREQUENCY_DIR)/gn.txt: \
    $(CORPUS_BARETAGGED_FILE)

	cat $(CORPUS_BARETAGGED_FILE) \
		| grep '\sGN$$' \
		| awk 'BEGIN { FS="\t"; } { print $$1; }' \
		> $(CORPUS_POSFREQUENCY_DIR)/gn.txt

$(CORPUS_POSFREQUENCY_DIR)/gn_frequency.txt: \
    $(CORPUS_POSFREQUENCY_DIR)/gn.txt

	cat $(CORPUS_POSFREQUENCY_DIR)/gn.txt \
		| sort | uniq -c | sort -rn \
		> $(CORPUS_POSFREQUENCY_DIR)/gn_frequency.txt

	sort -k2.1 $(CORPUS_POSFREQUENCY_DIR)/gn_frequency.txt \
		> $(CORPUS_POSFREQUENCY_DIR)/gn_sorted.txt

# MN (month name) frequency analysis.

$(CORPUS_POSFREQUENCY_DIR)/mn.txt: \
    $(CORPUS_BARETAGGED_FILE)

	cat $(CORPUS_BARETAGGED_FILE) \
		| grep '\sMN$$' \
		| awk 'BEGIN { FS="\t"; } { print $$1; }' \
		> $(CORPUS_POSFREQUENCY_DIR)/mn.txt

$(CORPUS_POSFREQUENCY_DIR)/mn_frequency.txt: \
    $(CORPUS_POSFREQUENCY_DIR)/mn.txt

	cat $(CORPUS_POSFREQUENCY_DIR)/mn.txt \
		| sort | uniq -c | sort -rn \
		> $(CORPUS_POSFREQUENCY_DIR)/mn_frequency.txt

	sort -k2.1 $(CORPUS_POSFREQUENCY_DIR)/mn_frequency.txt \
		> $(CORPUS_POSFREQUENCY_DIR)/mn_sorted.txt

# n (number) frequency analysis.

$(CORPUS_POSFREQUENCY_DIR)/n.txt: \
    $(CORPUS_BARETAGGED_FILE)

	cat $(CORPUS_BARETAGGED_FILE) \
		| grep '\sn$$' \
		| awk 'BEGIN { FS="\t"; } { print $$1; }' \
		> $(CORPUS_POSFREQUENCY_DIR)/n.txt

$(CORPUS_POSFREQUENCY_DIR)/n_frequency.txt: \
    $(CORPUS_POSFREQUENCY_DIR)/n.txt

	cat $(CORPUS_POSFREQUENCY_DIR)/n.txt \
		| sort | uniq -c | sort -rn \
		> $(CORPUS_POSFREQUENCY_DIR)/n_frequency.txt

	sort -k2.1 $(CORPUS_POSFREQUENCY_DIR)/n_frequency.txt \
		> $(CORPUS_POSFREQUENCY_DIR)/n_sorted.txt

# ON (object name) frequency analysis.

$(CORPUS_POSFREQUENCY_DIR)/on.txt: \
    $(CORPUS_BARETAGGED_FILE)

	cat $(CORPUS_BARETAGGED_FILE) \
		| grep '\sON$$' \
		| awk 'BEGIN { FS="\t"; } { print $$1; }' \
		> $(CORPUS_POSFREQUENCY_DIR)/on.txt

$(CORPUS_POSFREQUENCY_DIR)/on_frequency.txt: \
    $(CORPUS_POSFREQUENCY_DIR)/on.txt

	cat $(CORPUS_POSFREQUENCY_DIR)/on.txt \
		| sort | uniq -c | sort -rn \
		> $(CORPUS_POSFREQUENCY_DIR)/on_frequency.txt

	sort -k2.1 $(CORPUS_POSFREQUENCY_DIR)/on_frequency.txt \
		> $(CORPUS_POSFREQUENCY_DIR)/on_sorted.txt

# PN (personal name) frequency analysis.

$(CORPUS_POSFREQUENCY_DIR)/pn.txt: \
    $(CORPUS_BARETAGGED_FILE)

	cat $(CORPUS_BARETAGGED_FILE) \
		| grep '\sPN$$' \
		| awk 'BEGIN { FS="\t"; } { print $$1; }' \
		> $(CORPUS_POSFREQUENCY_DIR)/pn.txt

$(CORPUS_POSFREQUENCY_DIR)/pn_frequency.txt: \
    $(CORPUS_POSFREQUENCY_DIR)/pn.txt

	cat $(CORPUS_POSFREQUENCY_DIR)/pn.txt \
		| sort | uniq -c | sort -rn \
		> $(CORPUS_POSFREQUENCY_DIR)/pn_frequency.txt

	sort -k2.1 $(CORPUS_POSFREQUENCY_DIR)/pn_frequency.txt \
		> $(CORPUS_POSFREQUENCY_DIR)/pn_sorted.txt

# TN (temple name) frequency analysis.

./$(CORPUS_POSFREQUENCY_DIR)/tn.txt: \
    $(CORPUS_BARETAGGED_FILE)

	cat $(CORPUS_BARETAGGED_FILE) \
		| grep '\sTN$$' \
		| awk 'BEGIN { FS="\t"; } { print $$1; }' \
		> $(CORPUS_POSFREQUENCY_DIR)/tn.txt

$(CORPUS_POSFREQUENCY_DIR)/tn_frequency.txt: \
    $(CORPUS_POSFREQUENCY_DIR)/tn.txt

	cat $(CORPUS_POSFREQUENCY_DIR)/tn.txt \
		| sort | uniq -c | sort -rn \
		> $(CORPUS_POSFREQUENCY_DIR)/tn_frequency.txt

	sort -k2.1 $(CORPUS_POSFREQUENCY_DIR)/tn_frequency.txt \
		> $(CORPUS_POSFREQUENCY_DIR)/tn_sorted.txt

# u (unlemmatizable) frequency analysis.

./$(CORPUS_POSFREQUENCY_DIR)/u.txt: \
    $(CORPUS_BARETAGGED_FILE)

	cat $(CORPUS_BARETAGGED_FILE) \
		| grep '\su$$' \
		| awk 'BEGIN { FS="\t"; } { print $$1; }' \
		> $(CORPUS_POSFREQUENCY_DIR)/u.txt

$(CORPUS_POSFREQUENCY_DIR)/u_frequency.txt: \
    $(CORPUS_POSFREQUENCY_DIR)/u.txt

	cat $(CORPUS_POSFREQUENCY_DIR)/u.txt \
		| sort | uniq -c | sort -rn \
		> $(CORPUS_POSFREQUENCY_DIR)/u_frequency.txt

	sort -k2.1 $(CORPUS_POSFREQUENCY_DIR)/u_frequency.txt \
		> $(CORPUS_POSFREQUENCY_DIR)/u_sorted.txt

# WN (watercourse name) frequency analysis.

$(CORPUS_POSFREQUENCY_DIR)/wn.txt: \
    $(CORPUS_BARETAGGED_FILE)

	cat $(CORPUS_BARETAGGED_FILE) \
		| grep '\sWN$$' \
		| awk 'BEGIN { FS="\t"; } { print $$1; }' \
		> $(CORPUS_POSFREQUENCY_DIR)/wn.txt

$(CORPUS_POSFREQUENCY_DIR)/wn_frequency.txt: \
    $(CORPUS_POSFREQUENCY_DIR)/wn.txt

	cat $(CORPUS_POSFREQUENCY_DIR)/wn.txt \
		| sort | uniq -c | sort -rn \
		> $(CORPUS_POSFREQUENCY_DIR)/wn_frequency.txt

	sort -k2.1 $(CORPUS_POSFREQUENCY_DIR)/wn_frequency.txt \
		> $(CORPUS_POSFREQUENCY_DIR)/wn_sorted.txt

# X (unknown) frequency analysis.

$(CORPUS_POSFREQUENCY_DIR)/x.txt: \
    $(CORPUS_BARETAGGED_FILE)

	cat $(CORPUS_BARETAGGED_FILE) \
		| grep '\sX$$' \
		| awk 'BEGIN { FS="\t"; } { print $$1; }' \
		> $(CORPUS_POSFREQUENCY_DIR)/x.txt

$(CORPUS_POSFREQUENCY_DIR)/x_frequency.txt: \
    $(CORPUS_POSFREQUENCY_DIR)/x.txt

	cat $(CORPUS_POSFREQUENCY_DIR)/x.txt \
		| sort | uniq -c | sort -rn \
		> $(CORPUS_POSFREQUENCY_DIR)/x_frequency.txt

	sort -k2.1 $(CORPUS_POSFREQUENCY_DIR)/x_frequency.txt \
		> $(CORPUS_POSFREQUENCY_DIR)/x_sorted.txt

# all words frequency analysis.

$(CORPUS_POSFREQUENCY_DIR)/w.txt: \
    $(CORPUS_BARETAGGED_FILE)

	cat $(CORPUS_BARETAGGED_FILE) \
		| awk 'BEGIN { FS="\t"; } { print $$1; }' \
		> $(CORPUS_POSFREQUENCY_DIR)/w.txt

$(CORPUS_POSFREQUENCY_DIR)/w_frequency.txt: \
    $(CORPUS_POSFREQUENCY_DIR)/w.txt

	cat $(CORPUS_POSFREQUENCY_DIR)/w.txt \
		| sort | uniq -c | sort -rn \
		> $(CORPUS_POSFREQUENCY_DIR)/w_frequency.txt

	sort -k2.1 $(CORPUS_POSFREQUENCY_DIR)/w_frequency.txt \
		> $(CORPUS_POSFREQUENCY_DIR)/w_sorted.txt

# Not-PN frequency analysis.

$(CORPUS_POSFREQUENCY_DIR)/notpn.txt: \
	$(CORPUS_BARETAGGED_FILE)

	cat $(CORPUS_POSFREQUENCY_DIR)/fn.txt \
		$(CORPUS_POSFREQUENCY_DIR)/gn.txt \
		$(CORPUS_POSFREQUENCY_DIR)/n.txt \
		$(CORPUS_POSFREQUENCY_DIR)/on.txt \
		$(CORPUS_POSFREQUENCY_DIR)/tn.txt \
		$(CORPUS_POSFREQUENCY_DIR)/wn.txt \
		> $(CORPUS_POSFREQUENCY_DIR)/notpn.txt

$(CORPUS_POSFREQUENCY_DIR)/notpn_frequency.txt: \
	$(CORPUS_POSFREQUENCY_DIR)/notpn.txt
 
	cat $(CORPUS_POSFREQUENCY_DIR)/notpn.txt \
		| sort | uniq -c | sort -rn \
		> $(CORPUS_POSFREQUENCY_DIR)/notpn_frequency.txt
 
	sort -k2.1 $(CORPUS_POSFREQUENCY_DIR)/notpn_frequency.txt \
		> $(CORPUS_POSFREQUENCY_DIR)/notpn_sorted.txt

# Determinative frequency analysis.

$(CORPUS_POSFREQUENCY_DIR)/determinatives.txt: \
	$(CORPUS_BARETAGGED_FILE)

	cat $(CORPUS_BARETAGGED_FILE) \
		| sed -e 's/{/\n{/g' \
		| sed -e 's/}/}\n/g' \
		| grep '[{}]' | sort | uniq -c | sort -rn \
		> $(CORPUS_POSFREQUENCY_DIR)/determinatives.txt

# Cleanup
# =======

clean:
	rm -f $(CORPUS_LEMMA_FILE)
	rm -f $(CORPUS_LEMMA_TAGGED_FILE)
	rm -f $(CORPUS_NOLEMMA_FILE)
	rm -f $(CORPUS_NOLEMMA_TAGGED_FILE)
	rm -f $(CORPUS_LEMMA_CRF_FILE)
	rm -f $(CORPUS_LEMMA_CRF_TRAIN_FILE)
	rm -f $(CORPUS_LEMMA_CRF_TEST1_FILE)
	rm -f $(CORPUS_LEMMA_CRF_TEST2_FILE)
	rm -f $(CORPUS_NOLEMMA_CRF_FILE)
	rm -f $(CORPUS_NOLEMMA_CRF_TEST1_FILE)
	rm -f $(CORPUS_NOLEMMA_CRF_TEST2_FILE)
	rm -f $(CORPUS_WORDTAGFREQ_FILE)
	rm -f $(CORPUS_BARETAGGED_FILE)
	rm -rf $(CORPUS_POSFREQUENCY_DIR)
	rm -rf $(SEGMENTATION_PERMITDAMAGE_DIRNAME)
	rm -rf $(SEGMENTATION_REMOVEDAMAGE_DIRNAME)
