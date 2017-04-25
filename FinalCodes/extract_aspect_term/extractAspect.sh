python aspectTermMarking.py termTrain.csv termTrain.txt output.txt
CRF++-0.58/crf_learn template_1.txt output.txt model
CRF++-0.58/crf_test -m model termTest.txt > result.txt
python aspectTermEvaluation.py termTest.csv result.txt evaluation.txt
python evaluate.py evaluation.txt aspectTerm.csv 


