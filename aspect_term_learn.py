import sys
import os
import io
import json
from itertools import islice


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


def read_parser_output(file_path):
    parser_output = []
    with io.open(file_path, 'r', encoding='utf8') as f:
        relations = []
        for line in iter(f):
            line = line.rstrip()
            if line:
                relations.append(line)
            else:
                parser_output.append(relations)
                relations = []
    f.close()
    return parser_output

def learn_rules(relations, aspect_terms):
    rules = {}
    for relation in relations:
        relation_data = relation.split('\t')
        term = relation_data[1]
        if term in aspect_terms:
            rule = relation_data[5]
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
    for i in range(len(parser_output)):
        sentence_relations = parser_output[i]
        if len(sentence_relations) > 0 :
            sentence_aspect_terms = sentences[i][1][1]
            sentence_rules = learn_rules(sentence_relations, sentence_aspect_terms)
            aspect_term_rules = update_rules(aspect_term_rules, sentence_rules)
    return aspect_term_rules


# Writes the aspect terms to file in Unicode format
def write_json(data, file_path):
    with io.open(file_path, 'w', encoding='utf8') as data_file:
        data = json.dumps(data, indent=4, ensure_ascii=False, encoding='utf8')
        data_file.write(data)
	data_file.close()

if __name__ == '__main__':
    aspect_term_rules = main()
    write_json(aspect_term_rules, "./aspect_term_rules.txt")