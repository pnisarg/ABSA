python src/ate_crf_learn.py data/train/term_train.csv data/processed/dependency_parse_train.txt output/ate_learn.txt
tools/CRF++-0.58/crf_learn src/ate_crf_features.txt output/ate_learn.txt output/ate_crf_model
tools/CRF++-0.58/crf_test -m output/ate_crf_model data/test/term_test.txt > output/ate_result_parse.txt
python src/ate_crf_detect.py data/test/term_test.csv output/ate_result_parse.txt output/ate_result_map.txt
python src/ate_evaluation.py output/ate_result_map.txt data/raw/aspect_term.csv
