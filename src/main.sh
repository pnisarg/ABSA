trainPath='./../data/train'
testPath='./../data/test'
pdataPath='./../data/processed'
outputPath='./../output'
toolsPath='./../tools'
rawData='./../data/raw'

python ate_crf_learn.py $trainPath/term_train.csv $pdataPath/dependency_parse_train.txt $outputPath/ate_learn.txt
$toolsPath/CRF++-0.58/crf_learn ate_crf_features.txt $outputPath/ate_learn.txt  $outputPath/ate_crf_model
$toolsPath/CRF++-0.58/crf_test -m  $outputPath/ate_crf_model $pdataPath/dependency_parse_test.txt >  $outputPath/ate_result_parse.txt
python ate_crf_detect.py $testPath/term_test.csv  $outputPath/ate_result_parse.txt  $outputPath/ate_result_map.txt
python evaluation/ate_evaluation.py  $outputPath/ate_result_map.txt $rawData/aspect_term.csv
