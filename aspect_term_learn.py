# -*- coding: utf-8 -*-
import sys
import os
import io
import json
from itertools import islice


def handle_special_cases(sentence):
    if sentence[-1] != u'।':
        sentence += u'।'
    return sentence.replace(".", "")

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
                sentence_id = sentence_data[1]
                sentence = sentence_data[2]
                sentence = handle_special_cases(sentence)
                aspect_terms = []
                aspect_terms_temp = sentence_data[6].split(',')
                for aspect_term in aspect_terms_temp:
                    aspect_terms.extend(aspect_term.split(' '))
                sentences.append((sentence_id, (sentence, aspect_terms)))
    f.close()
    return sentences

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

def remove_empty_relations(parser_output):
    updated_parser_ouput = []
    for relations in parser_output:
        if len(relations) > 0:
            updated_parser_ouput.append(relations)
    return updated_parser_ouput

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


def update_rules(aspect_term_rules, sentence_rules):
    for rule, count in sentence_rules.iteritems():
        if rule in aspect_term_rules:
            aspect_term_rules[rule] += count
        else:
            aspect_term_rules[rule] = count
    return aspect_term_rules


def get_sentence_signature(sentence):
    return list(sentence.replace(" ", "")[:-1])


def get_relations_signature(relations):
    signature = ""
    for relation in relations:
        signature += relation[1]
    return list(signature[:-1])


def is_similar(sentence_signature, relations_signature):
    set_chars_sent_sig = set(sentence_signature)
    set_chars_rel_sig = set(relations_signature)
    union = set_chars_sent_sig.union(set_chars_rel_sig)
    intersection = set_chars_sent_sig.intersection(set_chars_rel_sig)
    cnt_union = len(union)
    cnt_intersection = len(intersection)

    if float(cnt_intersection) / cnt_union > 0.7:
        return True
    else:
        return False

# Writes the aspect terms to file in Unicode format
def write_json(data, file_path):
    with io.open(file_path, 'w', encoding='utf8') as data_file:
        data = json.dumps(data, indent=4, ensure_ascii=False, encoding='utf8')
        data_file.write(data)
	data_file.close()


def main():
    aspect_term_rules = {}
    sentences = get_sentences(sys.argv[1])
    list_sentences = []
    for sentence_data in sentences:
        sentence = sentence_data[1][0]
        list_sentences.append(sentence)
    write_sentences(list_sentences, "./parser/hindi.input.txt")
    os.popen("make -C ./parser/ hindi.output")
    parser_output = read_parser_output("./parser/hindi.output")

    len_sent = len(sentences)
    len_parser = len(parser_output)
    for idx in range(len_parser):
        relations = parser_output[idx]
        sentence_aspect_terms = sentences[idx][1][1]
        sentence_rules = learn_rules(relations, sentence_aspect_terms)
        aspect_term_rules = update_rules(aspect_term_rules, sentence_rules)

    return aspect_term_rules


if __name__ == '__main__':
    aspect_term_rules = main()
    write_json(aspect_term_rules, "./aspect_term_rules.txt")