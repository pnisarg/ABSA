import sys
import io
from itertools import islice
import codecs

"""
@var file_path: path to input csv file (UTF-8 encoded). Given file would be used for training.
Input file should be `#` separated and should have following columns in order
=> domainID # review # terms from # terms to # polarity # terms

@return: aspectTermsList: list of aspect terms for corresponding sentence
"""
def getSentences(file_path):
    aspectTermsList = []
    with codecs.open(file_path, 'r', encoding='utf8') as f:
        list(islice(f, 1)) # skipping first line
        # reading from line 2
        for line in iter(f):
            line = line.rstrip()
            if line:
                sentence_data = line.split('#') #using '#' as delimiter
                aspectTerms = []
                aspect_terms_temp = sentence_data[5].split('&')  
                for aspect_term in aspect_terms_temp:
                    for x in aspect_term.strip().split():
                        aspectTerms.append(x)
                aspectTermsList.append(aspectTerms)
        f.close()
    f.close()
    return aspectTermsList

"""
@var file_path: path to txt file containing generated dependency parse
returns list of parser output. 
"""
def readParserOutput(file_path):
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


def writeSentences(aspectTerms, parser_output, file_path):
    i = 0
    print len(aspectTerms)
    print len(parser_output)
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

"""
This function reads from termTrain.csv & termTrain.txt file and generates output.txt
file in CoNLL format. The output.txt file will be used by CRF++ to train out model

Run >>>: python aspectTermMarking.py termTrain.csv termTrain.txt output.txt
"""
def main():
    aspectTerms = getSentences(sys.argv[1]) #[['abc'],['dvs adf']]
    parser_output = readParserOutput(sys.argv[2])
    writeSentences(aspectTerms, parser_output, sys.argv[3]) 

if __name__ == '__main__':
    main()
