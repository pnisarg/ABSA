import sys
import io
import os
from itertools import islice
from ate_rule_learn import handle_special_cases, write_sentences


# Reads the input sentences from the specified file.
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
                sentence = sentence_data[1]
                sentence = handle_special_cases(sentence)
                sentences.append(sentence)
    f.close()
    return sentences


# Main function
def main():
    parser_file = sys.argv[1]

    # reading sentences
    sentences = get_sentences(sys.argv[2])
    parser_input_file = parser_file + "/hindi.input.txt"
    parser_output_file = "hindi.output"
    write_sentences(sentences, parser_input_file)

    # generating dependency parse
    make_command = "make -C " + parser_file + " " + parser_output_file
    os.popen(make_command)
    os.rename(parser_file + "/" + parser_output_file, sys.argv[3])

'''
Run parameters:

python generate_dependency_parse.py ./parser ./term_train.csv ./dependency_parse_train.txt
'''
if __name__ == '__main__':
    main()