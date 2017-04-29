# -*- coding: utf-8 -*-
import sys
import os
import io
import json
from itertools import islice


# Appends Hindi period '|' to the sentence if not already present.
# Also, removes all English periods '.'
def handle_special_cases(sentence):
    if sentence[-1] != u'।':
        sentence += u'।'
    return sentence.replace(".", "")


# Reads the training sentences from the training file
# Returns the sentence id, aspect terms and review in the following form:
# (sentence_id, (sentence, aspect_terms))
def get_sentences(file_path):
    sentences = []
    with io.open(file_path, 'r', encoding='utf8') as f:
        # skipping first line
        list(islice(f, 1))
        # reading from line 2
        for line in iter(f):
            line = line.rstrip()
            if line:
                sentence_data = line.split('#')
                sentence_id = sentence_data[0]
                sentence = sentence_data[1]
                sentence = handle_special_cases(sentence)
                aspect_terms = []
                aspect_terms_temp = sentence_data[5].split('&')
                for aspect_term in aspect_terms_temp:
                    aspect_terms.extend(aspect_term.split(' '))
                sentences.append((sentence_id, (sentence, aspect_terms)))
    f.close()
    return sentences


# Writes the list of sentences to the specified file in
# UTF-8 format.
def write_sentences(sentences, file_path):
    tot_sentences = len(sentences)
    idx = 1
    with io.open(file_path, 'w', encoding='utf8') as f:
        for sentence in sentences:
            if idx != tot_sentences:
                f.write(sentence + '\n')
            else:
                f.write(sentence)
            idx += 1
	f.close()


# Removes empty relations from the parser output resulting
# from empty blank lines in the output
def remove_empty_relations(parser_output):
    updated_parser_ouput = []
    for relations in parser_output:
        if len(relations) > 0:
            updated_parser_ouput.append(relations)
    return updated_parser_ouput


# Reads the dependecy parser output into a list
def read_parser_output(file_path):
    parser_output = []
    with io.open(file_path, 'r', encoding='utf8') as f:
        relations = []
        for line in iter(f):
            line = line.rstrip()
            if line:
                relations.append(line.split('\t'))
            else:
                parser_output.append(relations)
                relations = []
    f.close()
    return remove_empty_relations(parser_output)


# Extracts rules from the sentence dependency parse
# and the provided aspect terms
def learn_rules(relations, aspect_terms):
    rules = {}
    for relation in relations:
        term = relation[1]
        if term in aspect_terms:
            rule = relation[5]
            if rule in rules:
                rules[rule] += 1
            else:
                rules[rule] = 1
    return rules


# Updates learned rules count with the rules learned
# from the sentence.
def update_rules(aspect_term_rules, sentence_rules):
    for rule, count in sentence_rules.iteritems():
        if rule in aspect_term_rules:
            aspect_term_rules[rule] += count
        else:
            aspect_term_rules[rule] = count
    return aspect_term_rules


# Returns the words in the sentence as sentence signature.
def get_sentence_signature(sentence):
    return list(sentence.replace(" ", "")[:-1])


# Returns the words in the sentence' dependency parse as
# relation signature.
def get_relations_signature(relations):
    signature = ""
    for relation in relations:
        signature += relation[1]
    return list(signature[:-1])


# Writes the data map to file in UTF-8 format
def write_json(data_map, file_path):
    with io.open(file_path, 'w', encoding='utf8') as data_file:
        data_map = json.dumps(data_map, indent=4, ensure_ascii=False, encoding='utf8', sort_keys=True)
        data_file.write(data_map)
	data_file.close()


# Main function
def main():
    aspect_term_rules = {}

    # reading training sentences
    sentences = get_sentences(sys.argv[1])
    parser_file = sys.argv[2]
    parser_input_file = parser_file + "/hindi.input.txt"
    parser_output_file = "hindi.output"
    list_sentences = []
    for sentence_data in sentences:
        sentence = sentence_data[1][0]
        list_sentences.append(sentence)
    write_sentences(list_sentences, parser_input_file)

    # generating dependency parse structures for each sentence
    make_command = "make -C "+ parser_file + " " + parser_output_file
    os.popen(make_command)
    parser_output = read_parser_output(parser_file + "/" + parser_output_file)

    # learning rules
    len_sent = len(sentences)
    len_parser = len(parser_output)
    for idx in range(len_parser):
        relations = parser_output[idx]
        sentence_aspect_terms = sentences[idx][1][1]
        sentence_rules = learn_rules(relations, sentence_aspect_terms)
        aspect_term_rules = update_rules(aspect_term_rules, sentence_rules)

    return aspect_term_rules


'''
Run parameters:

python ate_rule_learn.py ./term_train.csv ./parser ./term_rules.txt
'''
if __name__ == '__main__':
    aspect_term_rules = main()
    # writing the learned rules to file
    write_json(aspect_term_rules, sys.argv[3])