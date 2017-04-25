import sys
import io
from itertools import islice
import codecs
import json

"""
    @var file_path: path to test csv file (UTF-8 encoded).
    Input file should be `#` separated and should have following columns in order
    => domainID # review
    
    @return: sentece_ids: list of sentence ids
    """
def get_sentence_ids(file_path):
    aspectTermsList = []
    with codecs.open(file_path, 'r', encoding='utf8') as f:
        # skipping first line
        list(islice(f, 1))
        sentence_ids = []
        # reading from line 2
        for line in iter(f):
            line = line.rstrip()
            if line:
                sentence_data = line.split('#')
                sentence_ids.append(sentence_data[0].strip())
        f.close()
    f.close()
    return sentence_ids

"""
    @var file_path: path to txt file containing generated dependency parse
    returns list of parser output.
    """
def read_parser_output(file_path):
    parser_output = []
    with codecs.open(file_path, 'r', encoding='utf8') as f:
        relations = []
        for line in iter(f):
            line = line.rstrip()
            if line:
                if "TRUE" in line:
                    relations.append(line)
            else:
                parser_output.append(relations)
                relations = []
    f.close()
    return parser_output

# Writes the aspect terms to file in Unicode format
def write_json(data, file_path):
    with io.open(file_path, 'w', encoding='utf8') as data_file:
        data = json.dumps(data, indent=4, ensure_ascii=False, encoding='utf8')
        data_file.write(data)
    data_file.close()

def mergeAspectTerm(list):
    result = []
    aspectTerm = list[0].strip().split("\t")[1]
    for i in range(1, len(list)):
        prevLine = list[i-1].strip().split("\t")
        currentLine = list[i].strip().split("\t")
        if(int(currentLine[0]) - int(prevLine[0]) == 1):
            aspectTerm = aspectTerm + " " + currentLine[1]
        else:
            result.append(aspectTerm)
            aspectTerm = currentLine[1]
    
    result.append(aspectTerm)
    return result


def write_sentences(sentenceIds, parser_output, file_path):
    result = {}
    i = 0
    for s in sentenceIds:
        lines = parser_output[i]
        aspectTerms = []
        if len(lines) > 1:
            result[s] = mergeAspectTerm(lines)
        else:
            for line in lines:
                aspectTerms.append(line.strip().split("\t")[1])
            result[s] = aspectTerms
        i = i + 1

    write_json(result, file_path)

"""
    This function reads from termTest.csv & result.txt file and generates evaluation.txt
    file in CoNLL format. The evaluation.txt file will be used for evaluating F-score for .
    
    Run: python aspectTermEvaluation.py termTest.csv result.txt evaluation.txt
    """
def main():
    senteceIds = get_sentence_ids(sys.argv[1]) #read test file
    parser_output = read_parser_output(sys.argv[2])
    write_sentences(senteceIds, parser_output, sys.argv[3])

if __name__ == '__main__':
    main()

