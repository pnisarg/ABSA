import sys
import os
import io
import json
import ast
import operator
from itertools import islice
from ate_rule_learn import write_sentences, write_json, read_parser_output, handle_special_cases


# Returns the parent id and grand-parent id for the specified word
# from the dependency parse tree
def get_two_levels_up_pids(asp_term_jj_data, relations):
	two_levels_up_pids = set()
	pid = asp_term_jj_data[0]
	two_levels_up_pids.add(pid)
	if pid != '0':
		ppid_relation = relations[int(pid) - 1]
		ppid = ppid_relation[4]
		two_levels_up_pids.add(ppid)
	return two_levels_up_pids


# Returns the quality defining words for the extracted aspect terms
def detect_quality(aspect_terms_list, jj_list, relations):
	aspect_terms = {}
	for aspect_term in aspect_terms_list:
		aspect_term_val = aspect_term[1]
		asp_term_two_levels_up_pids = get_two_levels_up_pids(aspect_term, relations)
		quality_terms = []
		for jj in jj_list:
			jj_val = jj[1]
			jj_two_levels_up_pids = get_two_levels_up_pids(jj, relations)
			jj_pid = jj[0]

			# if jj_pid in asp_term_two_levels_up_pids :
			if len(asp_term_two_levels_up_pids.intersection(jj_two_levels_up_pids)) != 0:
				quality_terms.append(jj_val)

		# adding to aspect terms
		if aspect_term_val in aspect_terms:
			quality_terms.extend(aspect_terms[aspect_term_val])

		aspect_terms[aspect_term_val] = quality_terms
	return aspect_terms


# Retunrns verbs and adverbs from the sentence's dependency parse
def get_vb_list(relations):
	vb_list = []
	for relation in relations:
		pos = relation[3]
		pid = relation[4]
		term = relation[2]
		if pos == 'VM' or pos == 'VGNN' or pos == 'VAUX':
			if term not in stop_words:
				vb_list.append((pid, term))
	return vb_list


# Detects aspect terms from the sentence's dependency parse
def detect_terms(relations):
	aspect_terms = []
	for rule in rules_list:
		for relation in relations:
			rel_name = relation[5]
			pos = relation[3]
			pid = relation[4]
			term = relation[1]
			if rel_name == rule[0] and pos == 'NN':
				aspect_terms.append((pid, term))
		if len(aspect_terms) > 0:
			break;
	aspect_terms = list(set(aspect_terms))
	return aspect_terms


# Returns all adjectives from the sentence' dependency parse
def get_jj_list(relations):
	jj_list = set()
	for relation in relations:
		if relation[3] == 'JJ':
			jj_list.add((relation[4], relation[2]))
	return jj_list


# Loads Hindi stopwords from file
def load_stop_words(file_path):
	stop_words = {}
	with io.open(file_path, 'r', encoding='utf8') as f:
		for line in iter(f):
			line = line.rstrip()
			if line:
				stop_words[line] = 1
	f.close()
	return stop_words


# Reads the test sentences from the test file
# Returns the sentence id and review in the following form:
# (sentence_id, sentence)
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
				sentences.append((sentence_data[0], handle_special_cases(sentence_data[1])))
	f.close()
	return sentences


# Loads rules from file
def load_rules(file_path):
    with open(file_path) as rules_file:
        rules = json.load(rules_file)
	rules = ast.literal_eval(json.dumps(rules))
	rules_file.close()
	return rules


# Applies threshold to the dependency labels count to
# extract rules
def apply_threshold(rules):
	aspect_term_rules = {}
	# calculating average
	values = rules.values()
	threshold = sum(values) / len(values)
	threshold += int(0.3 * threshold)
	for rule, count in rules.iteritems():
		if count >= threshold:
			aspect_term_rules[rule] = count
	return aspect_term_rules


# Main function
def main():
    aspect_terms = {}

	# reading test sentences
    sentences = get_sentences(sys.argv[1])
    parser_file = sys.argv[4]
    parser_input_file = parser_file + "/hindi.input.txt"
    parser_output_file = "hindi.output"

    output_sentences = []
    for sentence_data in sentences:
        output_sentences.append(sentence_data[1])
    write_sentences(output_sentences, parser_input_file)

	# generating dependency parse structures for each sentence
    make_command = "make -C " + parser_file + " " + parser_output_file
    os.popen(make_command)
    parser_output = read_parser_output(parser_file + "/" + parser_output_file)

	# detecting terms
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


'''
Run parameters:

python ate_rule_detect.py ./term_test.csv ./term_rules.txt ./terms_output.txt ./parser ./hindi_stopwords.txt
'''
if __name__ == '__main__':

	# loading Hindi stopwords
	stop_words = load_stop_words(sys.argv[5])

	# generating rules
	initial_rules = load_rules(sys.argv[2])
	aspect_term_rules = apply_threshold(initial_rules)
	rules_list = sorted(aspect_term_rules.items(), key=operator.itemgetter(1), reverse=True)

	# detecting aspect terms from rules
	aspect_terms = main()

	# writing the output to file
	write_json(aspect_terms, sys.argv[3])
