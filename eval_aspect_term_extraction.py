# -*- coding: utf-8 -*-

'''
Run a task from the terminal::
>>> python eval_aspect_term_extraction.py predicted_aspect_terms_input_filename.txt correct_aspect_terms_csv_filename 
'''
import csv
import io
import json
import ast
import sys
import argparse

def aspect_extraction():
    
    b=1
    count = 0
    c=0
    common, relevant, retrieved = 0., 0., 0.
    for sid in pred_aspect_terms.keys(): 
        for index in range(len(corr_aspect_term)):
            if corr_aspect_term[index][0] == sid:
                pre = pred_aspect_terms[sid]
                if corr_aspect_term[index][5] !="": 
                    cor = [corr_aspect_term[index][5]]
                else:
                    cor = []    
                #print sid, pre, cor, len(pre), len(cor)
                #common += len([a for a in pre if a in cor])
                #common_list = []
                
                for a in pre: 
                    if len(cor)>0 and a==cor[0]:
                        c+=1
                        #common_list.append(a)
                        common+=len([a])              
                if pre == []:
                    retrieved+=0
                else:    
                    retrieved += len(pre)
                if cor==[]:
                    relevant += 0 
                else:
                    relevant+=len(cor)      
                #print sid, cor, pre, common, retrieved, relevant, len(cor), len(pre), count, c
    p = common / retrieved if retrieved > 0 else 0.
    r = common / relevant
    f1 = (1 + (b ** 2)) * p * r / ((p * b ** 2) + r) if p > 0 and r > 0 else 0.
    return p, r, f1, common, retrieved, relevant



with open(sys.argv[2], 'rb') as f:
    reader = csv.reader(f,delimiter ='#')
    corr_aspect_term = list(reader)

#print corr_aspect_term[1]

# Loads model from the model file
def load_output(file_path):
    with open(file_path) as output_file:
        output = json.load(output_file)
    output = ast.literal_eval(json.dumps(output, ensure_ascii=False, encoding='utf8'))
    return output
    
pred_aspect_terms = load_output(sys.argv[1])
#print pred_aspect_terms
print 'Precision = %f -- Recall = %f -- F1 = %f (#correct: %d, #retrieved: %d, #relevant: %d)' %aspect_extraction()
#print aspect_extraction()    
