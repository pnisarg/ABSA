python ate_crf_learn.py data/train/term_train.csv dependency_parse_train.txt output/ate_learn.txt
CRF++-0.58/crf_learn ate_crf_features.txt output/ate_learn.txt output/ate_crf_model
CRF++-0.58/crf_test -m output/ate_crf_model data/test/term_test.txt > output/ate_result_parse.txt
python ate_crf_detect.py data/term_test.csv output/ate_result_parse.txt output/ate_result_map.txt
python evaluate.py output/ate_result_map.txt data/raw/aspect_term.csv


