python aspectTermMarking.py termTrain.csv termTrain.txt output/output.txt
CRF++-0.58/crf_learn template.txt output/output.txt output/model
CRF++-0.58/crf_test -m output/model termTest.txt > output/result.txt
python aspectTermEvaluation.py termTest.csv output/result.txt output/evaluation.txt
python evaluate.py output/evaluation.txt aspectTerm.csv 


