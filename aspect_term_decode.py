import sys
import os
import io
import json
import ast
from itertools import islice
from aspect_term_learn import write_sentences, write_json, read_parser_output, handle_special_cases


def get_two_levels_up_pids(asp_term_jj_data, relations):
	two_levels_up_pids = set()
	pid = asp_term_jj_data[0]
	two_levels_up_pids.add(pid)
	if pid != '0':
		ppid_relation = relations[int(pid) - 1]
		ppid = ppid_relation[4]
		two_levels_up_pids.add(ppid)
	return two_levels_up_pids


def detect_quality(aspect_terms_list, jj_list, relations):
	aspect_terms = {}
	for aspect_term in aspect_terms_list:
		aspect_term_val = aspect_term[1]
		asp_term_two_levels_up_pids = get_two_levels_up_pids(aspect_term, relations)
		quality_terms = []
		for jj in jj_list:
			jj_val = jj[1]
			#jj_two_levels_up_pids = get_two_levels_up_pids(jj, relations)
			jj_pid = jj[0]

			#if len(asp_term_two_levels_up_pids.intersection(jj_two_levels_up_pids)) != 0:
			if jj_pid in asp_term_two_levels_up_pids != 0:
				quality_terms.append(jj_val)

		# adding to aspect terms
		if aspect_term_val in aspect_terms:
			quality_terms.append(aspect_terms[aspect_term_val])

		aspect_terms[aspect_term_val] = quality_terms
	return aspect_terms


def get_vb_list(relations):
	vb_list = []
	for relation in relations:
		pos = relation[3]
		pid = relation[4]
		term = relation[1]
		if pos == 'VM' or pos == 'VGNN' or pos == 'VAUX':
			if term not in stop_words:
				vb_list.append((pid, term))
	return vb_list

def detect_terms(relations):
	aspect_terms = []
	for relation in relations:
		rel_name = relation[5]
		pos = relation[3]
		pid = relation[4]
		term = relation[1]
		if rel_name in aspect_term_rules and pos == 'NN':
			aspect_terms.append((pid, term))
	aspect_terms = list(set(aspect_terms))
	return aspect_terms

def get_jj_list(relations):
	jj_list = set()
	for relation in relations:
		if relation[3] == 'JJ':
			jj_list.add((relation[4], relation[1]))
	return jj_list

def load_stop_words(file_path):
	stop_words = {}
	with io.open(file_path, 'r', encoding='utf8') as f:
		for line in iter(f):
			line = line.rstrip()
			if line:
				stop_words[line] = 1
	f.close()
	return stop_words

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
				sentences.append((sentence_data[1], handle_special_cases(sentence_data[2])))
	f.close()
	return sentences

def load_rules(file_path):
    with open(file_path) as rules_file:
        rules = json.load(rules_file)
	rules = ast.literal_eval(json.dumps(rules))
	rules_file.close()
	return  rules


def apply_threshold(rules):
	aspect_term_rules = {}
	# calculating average
	values = rules.values()
	threshold = sum(values) / len(values)
	for rule, count in rules.iteritems():
		if count >= threshold:
			aspect_term_rules[rule] = count
	return aspect_term_rules

def main():
    aspect_terms = {}
    sentences = get_sentences(sys.argv[1])

    output_sentences = []
    for sentence_data in sentences:
        output_sentences.append(sentence_data[1])

    write_sentences(output_sentences, "./parser/hindi.input.txt")
    os.popen("make -C ./parser/ hindi.output")
    parser_output = read_parser_output("./parser/hindi.output")
    len_sent = len(sentences)
    len_parser = len(parser_output)
    for i in range(len_parser):
		relations = parser_output[i]
		sentence_id = sentences[i][0]
		sentence_aspect_terms_list = detect_terms(relations)
		jj_list = get_jj_list(relations)
		if len(jj_list) == 0:
			jj_list = get_vb_list(relations)
		sentence_aspect_terms = detect_quality(sentence_aspect_terms_list, jj_list, relations)
		aspect_terms[sentence_id] = sentence_aspect_terms

    return aspect_terms

if __name__ == '__main__':
	stop_words = load_stop_words("./hindi_stopwords.txt")
	initial_rules = load_rules("./aspect_term_rules.txt")
	aspect_term_rules = apply_threshold(initial_rules)
	aspect_terms = main()
	write_json(aspect_terms, "./aspect_terms_output.txt")
