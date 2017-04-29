# -*- coding: utf-8 -*-
import sys
import pickle
import json
import ast
import io
from ate_rule_learn import write_json

CONST_POS_SCORE = "POS_SCORE"
CONST_NEG_SCORE = "NEG_SCORE"

hindi_word_net = sys.argv[3]
word2Synset = pickle.load(open( hindi_word_net + "/WordSynsetDict.pk"))
synonyms = pickle.load(open(hindi_word_net + "/SynsetWords.pk"))


# Returns the synonyms of the word from Hindi SWN
def get_synonyms(word):
    output = []
    syn_map_list = []
    if word2Synset.has_key(word):
        synsets = word2Synset[word]
        for pos in synsets.keys():
            for synset in synsets[pos]:
                if synonyms.has_key(synset):
                    synDict = synonyms[synset]
                    syn_map_list.append(synDict)

    for syn_map in syn_map_list:
        for word_synoyms_list in syn_map.values():
            output.extend(word_synoyms_list)

    return output


# Loads model from the model file
def load_terms_output(file_path):
    with open(file_path) as terms_output_file:
        terms_otuput = json.load(terms_output_file)
    terms_otuput = ast.literal_eval(json.dumps(terms_otuput, ensure_ascii=False, encoding='utf8'))
    terms_output_file.close()
    return terms_otuput


# Creates a lexicon of words from the Hindi SWN.
# This includes the positive and negative polarity scores for each word
# from the SWN
def generate_lexicon(hindi_swn_dir):
    lexicon = {}
    swn_file = hindi_swn_dir + "/HSWN_WN.txt"
    with io.open(swn_file, 'r', encoding='utf8') as f:
        for line in iter(f):
            line = line.rstrip()
            if line:
                data = line.split()
                pos_score = float(data[2])
                neg_score = float(data[3])
                words = data[4]
                words = words.split(',')
                for word in words:
                    word_map = {}
                    word_map[CONST_POS_SCORE] = pos_score
                    word_map[CONST_NEG_SCORE] = neg_score
                    lexicon[word] = word_map
    return lexicon


# Return the effective score of a word or its synonym from lexicon.
# Effective score is the difference between its positive polarity and
# negative polarity.
def get_score(word, swn_lexicon):
    score = 0
    word_synoyms = []
    word = word.decode("utf-8")
    if word not in swn_lexicon:
        word_synoyms = get_synonyms(word)
    else:
        word_synoyms.append(word)

    for word in word_synoyms:
        if word in swn_lexicon:
            pos_score = swn_lexicon[word][CONST_POS_SCORE]
            neg_score = swn_lexicon[word][CONST_NEG_SCORE]
            score = pos_score - neg_score
            break

    return score


# Detects polarity of aspect terms from Hindi SWN Lexicon
def detect_polarity(terms_output, swn_lexicon):
    terms_polarity_output = {}
    for sent_id, sent_map in terms_output.iteritems():
        sent_polarity = {}
        for aspect_term, quality_words in sent_map.iteritems():
            polarity = "neu"
            score = 0
            for quality_word in quality_words:
                score += get_score(quality_word, swn_lexicon)
            if score > 0:
                polarity = "pos"
            elif score < 0:
                polarity = "neg"
            sent_polarity[aspect_term] = polarity
        terms_polarity_output[sent_id] = sent_polarity
    return terms_polarity_output


# Main function
if __name__ == '__main__':

    # loading aspect terms rule based output
    terms_output = load_terms_output(sys.argv[1])

    # generating Hindi Sentiwordnet lexicon
    hindi_swn_dir = sys.argv[2]
    swn_lexicon = generate_lexicon(hindi_swn_dir)

    # detecting polarity
    terms_polarity_output = detect_polarity(terms_output, swn_lexicon)

    # writing output to file
    write_json(terms_polarity_output, sys.argv[4])