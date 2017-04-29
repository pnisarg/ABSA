# -*- coding: utf-8 -*-
import io
import sys
import json
import ast
import operator
from itertools import islice
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm
from ate_rule_learn import write_json


CONST_SENTENCE = "SENTENCE"
CONST_ASPECT_TERMS = "ASPECT_TERMS"
CONST_ASPECT_TERMS_POLARITY = "ASPECT_TERMS_POLARITY"
CONST_CONTEXT_WINDOW_SIZE = 10


# Performs text formatting on sentence before training/classification.
def remove_unwanted_tokens(sentence):
    sentence = sentence.replace(",", " ")
    sentence = sentence.replace(u"।", "")
    sentence = sentence.replace("'", "")
    sentence = sentence.replace("-", " ")
    sentence = sentence.replace("(", " ")
    sentence = sentence.replace(")", " ")
    sentence = sentence.replace(".", "")
    sentence = sentence.replace(":", " ")
    sentence = sentence.strip()
    return sentence


# Returns the list of training sentences from the train file
# Returns sentence id, review, aspect terms and their associated polarity from
# each sentence.
def get_train_sentences(file_path):
    sentences = {}
    with io.open(file_path, 'r', encoding='utf8') as f:
        # skipping first line
        list(islice(f, 1))
        # reading from line 2
        for line in iter(f):
            line = line.rstrip()
            if line:
                sentence_data = line.split('#')

                # collecting aspect terms
                aspect_terms = []
                aspect_terms_str = sentence_data[5]
                aspect_terms_str = remove_unwanted_tokens(aspect_terms_str)
                aspect_terms_temp = aspect_terms_str.split('&')
                aspect_terms_temp = remove_blank_tokens(aspect_terms_temp)

                # skipping the line if no aspect terms found
                if len(aspect_terms_temp) == 0:
                    continue

                # sorting aspect terms based on their 'from' value
                aspect_terms_map ={}
                aspect_terms_from = sentence_data[2].split('&')
                for idx in range(len(aspect_terms_temp)):
                    aspect_term = aspect_terms_temp[idx]
                    aspect_term_from = aspect_terms_from[idx]
                    aspect_terms_map[aspect_term] = int(aspect_term_from)

                aspect_terms_seq_sorted = sorted(aspect_terms_map.items(), key=operator.itemgetter(1))
                for aspect_term in aspect_terms_seq_sorted:
                    aspect_terms.append(aspect_term[0])

                sentence_id = sentence_data[0]
                sentence = sentence_data[1]
                sentence = remove_unwanted_tokens(sentence)

                # collecting aspect terms polarity
                aspect_terms_polarity = []
                aspect_terms_polarity_temp = sentence_data[4].split('&')
                for aspect_term_polarity in aspect_terms_polarity_temp:
                    aspect_terms_polarity.append(aspect_term_polarity)


                sentence_map = {}
                sentence_map[CONST_SENTENCE] = sentence
                sentence_map[CONST_ASPECT_TERMS] = aspect_terms
                sentence_map[CONST_ASPECT_TERMS_POLARITY] = aspect_terms_polarity

                sentences[sentence_id] = sentence_map
    f.close()
    return sentences


# Removes blank tokens from the sentence
def remove_blank_tokens(sentence):
    updated_tokens = []
    for token in sentence:
        token = token.strip()
        if token:
            updated_tokens.append(token)
    return updated_tokens


# Reads the train sentences/reviews from the train file.
# Returns local context of aspect terms and its associated polarity
# for each sentence.
def get_train_lines(train_file_path):
    train_data = []

    sentences = get_train_sentences(train_file_path)
    for sent_id, sentence_map in sentences.iteritems():
        sentence = sentence_map[CONST_SENTENCE]
        sentence = sentence.split(" ")
        sentence = remove_blank_tokens(sentence)
        aspect_terms = sentence_map[CONST_ASPECT_TERMS]
        aspect_terms_polarity = sentence_map[CONST_ASPECT_TERMS_POLARITY]
        for idx in range(len(aspect_terms)):
            aspect_term = aspect_terms[idx]
            aspect_term_polarity = aspect_terms_polarity[idx]
            aspect_term_list = aspect_term.split(" ")
            context_sent = get_local_context(sentence, aspect_term_list)

            # updating sentence to remove processed tokens
            if aspect_term_list[0] in sentence:
                processed_idx = sentence.index(aspect_term_list[0])
            else:
                processed_idx = get_similar_index(sentence, aspect_term_list[0])
            sentence = sentence[processed_idx+1 : len(sentence)]

            train_data.append((aspect_term_polarity, context_sent))

    return train_data


# Returns local context sentence to the aspect term to be used for training
# the classifier.
def get_local_context(sentence, aspect_term):
    aspect_term_size = len(aspect_term)
    window_size = CONST_CONTEXT_WINDOW_SIZE

    if aspect_term_size >= window_size:
        return ' '.join(aspect_term)

    remaining_size = window_size - aspect_term_size
    left_size = remaining_size / 2
    left_tokens = get_preceding_tokens(sentence, aspect_term, left_size)
    right_size = remaining_size - len(left_tokens)
    right_tokens = get_succeeding_tokens(sentence, aspect_term, right_size)
    train_sentence = get_train_sentence(left_tokens, aspect_term, right_tokens)
    return train_sentence


# Returns the concatenated string of left tokens, aspect terms and right tokens
# to be used as the training sentence
def get_train_sentence(left_tokens, aspect_term, right_tokens):
    left = ' '.join(left_tokens)
    term = ' '.join(aspect_term)
    right = ' '.join(right_tokens)
    return left + " " + term + " " + right


# Returns list of preceding tokens to the aspect term of the
# specified size.
def get_preceding_tokens(sentence, aspect_term, size):
    tokens = []
    first_aspect_term = aspect_term[0]
    if first_aspect_term in sentence:
        start_idx = sentence.index(first_aspect_term)
    else:
        start_idx = get_similar_index(sentence, first_aspect_term)
    if size >= start_idx:
        tokens = sentence[0: start_idx]
    else:
        tokens = sentence[start_idx - size: start_idx]
    return tokens


# Returns the index of a similar sounding word (only different in some chars)
# to the aspect term in the sentence.
def get_similar_index(sentence, aspect_term):
    idx = 0;
    for word in sentence:
        if aspect_term in word:
            return idx
        else:
            idx += 1
    return idx


# Returns list of succeeding tokens to the aspect term of the
# specified size.
def get_succeeding_tokens(sentence, aspect_term, size):
    tokens = []
    last_aspect_term = aspect_term[-1]
    if last_aspect_term in sentence:
        start_idx = last_index(last_aspect_term, sentence)
    else:
        start_idx = len(sentence) - 1 - get_similar_index(sentence[::-1], last_aspect_term)

    remaining = len(sentence) - start_idx - 1
    if size >= remaining:
        tokens = sentence[start_idx + 1 : len(sentence)]
    else:
        tokens = sentence[start_idx + 1: start_idx + size + 1]
    return tokens


# Returns the last index of the item in the specified list
def last_index(item, list):
    return len(list) - 1 - list[::-1].index(item)


# Returns training data for the vectorizer from train lines
def get_train_data(train_lines):
    train_data = []
    train_labels = []
    for train_line in train_lines:
        train_labels.append(train_line[0])
        train_data.append(train_line[1])
    return train_data, train_labels


# Loads aspect terms' output from file
def load_aspect_terms(file_path):
    with open(file_path) as output_file:
        aspect_terms = json.load(output_file)
    aspect_terms = ast.literal_eval(json.dumps(aspect_terms, ensure_ascii=False, encoding='utf8'))
    return aspect_terms


# Reads the test sentences/reviews from the test file.
# Returns sentence id, review and aspect terms for each sentence.
def get_test_sentences(test_file_path):
    sentences = {}
    with io.open(test_file_path, 'r', encoding='utf8') as f:
        # skipping first line
        list(islice(f, 1))
        # reading from line 2
        for line in iter(f):
            line = line.rstrip()
            if line:
                sentence_data = line.split('#')

                # collecting aspect terms
                aspect_terms = []
                aspect_terms_str = sentence_data[4]
                aspect_terms_str = remove_unwanted_tokens(aspect_terms_str)
                aspect_terms_temp = aspect_terms_str.split('&')
                aspect_terms_temp = remove_blank_tokens(aspect_terms_temp)

                # sorting aspect terms based on their 'from' location
                aspect_terms_map = {}
                aspect_terms_from = sentence_data[2].split('&')
                for idx in range(len(aspect_terms_temp)):
                    aspect_term = aspect_terms_temp[idx]
                    aspect_term_from = aspect_terms_from[idx]
                    aspect_terms_map[aspect_term] = int(aspect_term_from)

                aspect_terms_seq_sorted = sorted(aspect_terms_map.items(), key=operator.itemgetter(1))
                for aspect_term in aspect_terms_seq_sorted:
                    aspect_terms.append(aspect_term[0])

                sentence_id = sentence_data[0]
                sentence = sentence_data[1]
                sentence = remove_unwanted_tokens(sentence)

                sentence_map = {}
                sentence_map[CONST_SENTENCE] = sentence
                sentence_map[CONST_ASPECT_TERMS] = aspect_terms

                sentences[sentence_id] = sentence_map
    f.close()
    return sentences


# Returns the list of test data for each sentence from the test file
# If the sentence does not have any aspect terms, then also such a
# sentence is included here. It is discarded while creating test data
# from test lines.
def get_test_lines(term_polarity_test_file):
    test_lines = []
    test_sentences = get_test_sentences(term_polarity_test_file)

    for sent_id, sentence_data in test_sentences.iteritems():
        aspect_terms = sentence_data[CONST_ASPECT_TERMS]
        sentence = sentence_data[CONST_SENTENCE]
        sentence = sentence.split(" ")
        sentence = remove_blank_tokens(sentence)
        sent_test_list = []
        for idx in range(len(aspect_terms)):
            aspect_term = aspect_terms[idx]
            aspect_term = remove_unwanted_tokens(aspect_term)
            aspect_term_list = aspect_term.split(" ")

            context_sent = get_local_context(sentence, aspect_term_list)

            # updating sentence to remove processed tokens
            if aspect_term_list[0] in sentence:
                processed_idx = sentence.index(aspect_term_list[0])
            else:
                processed_idx = get_similar_index(sentence, aspect_term_list[0])
            sentence = sentence[processed_idx + 1: len(sentence)]

            sent_test_list.append((aspect_term, context_sent))

        test_lines.append((sent_id, sent_test_list))

    return test_lines


# Returns the test data for the classifier
def get_test_data(test_lines):
    test_data = []
    for test_line in test_lines:
        sent_data = test_line[1]
        if len(sent_data) > 0:
            for aspect_term_data in sent_data:
                test_data.append(aspect_term_data[1])
    return test_data


# Returns the output map from the classifiers output for each
# test sentence
def generate_output(prediction, test_lines):
    aspect_terms_polarity = {}
    prediction_idx = 0
    for test_line in test_lines:
        sentence_id = test_line[0]
        sentence_map = {}
        for aspect_terms in test_line[1]:
            aspect_term = aspect_terms[0]
            polarity = prediction[prediction_idx]
            prediction_idx += 1
            sentence_map[aspect_term] = polarity
        aspect_terms_polarity[sentence_id] = sentence_map
    return aspect_terms_polarity


'''
Run parameters:

python ats_svm_detect.py ./term_polarity_train.csv ./term_polarity_test.csv ./term_polarity_output.txt
'''
if __name__ == '__main__':
    # fetching training lines
    train_lines = get_train_lines(sys.argv[1])

    # computing training data
    train_data, train_labels = get_train_data(train_lines)

    # fetching test data
    test_lines = get_test_lines(sys.argv[2])
    test_data = get_test_data(test_lines)

    # training SVM
    vectorizer = CountVectorizer(min_df=0.002, ngram_range=(1, 2), encoding="utf-8")
    train_vectors = vectorizer.fit_transform(train_data)

    # performing classification with SVM, kernel=linear
    classifier_linear = svm.SVC(kernel='linear')
    classifier_linear.fit(train_vectors, train_labels)
    test_vectors = vectorizer.transform(test_data)
    prediction = classifier_linear.predict(test_vectors)

    # generating output
    aspect_terms_polarity = generate_output(prediction, test_lines)
    write_json(aspect_terms_polarity, sys.argv[3])