import sys
import io
from itertools import islice
import codecs

def get_sentences(file_path):
    aspectTermsList = []
    with codecs.open(file_path, 'r', encoding='utf8') as f:
        # skipping first line
        list(islice(f, 1))
        # reading from line 2
        for line in iter(f):
            line = line.rstrip()
            if line:
                sentence_data = line.split('#')
                aspectTerms = []
                aspect_terms_temp = sentence_data[6].split(',') 
                for aspect_term in aspect_terms_temp:
                    for x in aspect_term.strip().split():
                        aspectTerms.append(x)
                aspectTermsList.append(aspectTerms)
        f.close()
    f.close()
    return aspectTermsList


def read_parser_output(file_path):
    parser_output = []
    with codecs.open(file_path, 'r', encoding='utf8') as f:
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

def write_sentences(aspectTerms, parser_output, file_path):
    i = 0
    with codecs.open(file_path, 'w', encoding='utf8') as f:
        for sentence in parser_output:
            aspect_term_words = aspectTerms[i]
            for word in sentence:
                if word.strip().split("\t")[1] in aspect_term_words:
                    f.write(word +"\tTRUE") 
                else:
                    f.write(word + "\tFALSE")
                f.write("\n")
            f.write("\n")
            i = i + 1
        f.close()


def main():
    aspectTerms = get_sentences(sys.argv[1]) #[['abc'],['dvs adf']]
    parser_output = read_parser_output(sys.argv[2])
    write_sentences(aspectTerms, parser_output, sys.argv[3]) 

if __name__ == '__main__':
    aspect_term_rules = main()
    #write_json(aspect_term_rules, "./aspect_term_rules.txt")

