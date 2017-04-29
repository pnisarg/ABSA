# -*- coding: utf-8 -*-

'''
Run a task from the terminal::
>>> python Aspect_term_extraction_evaluation.py predicted_aspect_terms_input_filename correct_aspect_terms_csv_filename 
This program skips the blank entries.
'''
import csv
import json
import ast
import sys

def aspect_extraction(pred_aspect_terms,corr_aspect_terms):
    """
    Module to evaluate aspect term extraction
    Arguments:
        predicted aspect terms and correct aspect terms, both in list format
    Returns:
        Precision, Recall and F-score entire dataset
    """ 
    b=1.0
    common, relevant, retrieved = 0., 0., 0.
    for sid in pred_aspect_terms.keys():   
        for index in range(len(corr_aspect_terms)):   
            if corr_aspect_terms[index][0] == sid:
                pre = pred_aspect_terms[sid]
                if '&' in corr_aspect_terms[index][5]: 
                    cor = corr_aspect_terms[index][5].split('&')
                elif corr_aspect_terms[index][5] == '':
                    cor= []
                elif '&' not in corr_aspect_terms[index][5]:
                    cor = [corr_aspect_terms[index][5]]
                for a in pre: 
                    if len(cor)>0:
                        for c in cor:
                            if a==c:
                                common+=1  
                retrieved += (len(pre))
                relevant+=(len(cor))      
    p = common / retrieved if retrieved > 0 else 0.
    r = common / relevant
    f1 = (1 + (b ** 2)) * p * r / ((p * b ** 2) + r) if p > 0 and r > 0 else 0.
    return p, r, f1

def load_correct_aspect_term(file_path):
    """
    Module to load the original Aspect Term Dataset
    Arguments:
        file path for original dataset in csv format
    Returns:
        dataset in form of lists
    """         
    with open(file_path, 'rb') as f:
        reader = csv.reader(f,delimiter ='#')
        alist = list(reader)
    return alist     

def load_predicted_aspect_term(file_path):
    """
    Module to load the predicted Aspect Term Dataset 
    Arguments:
        file path for original dataset in txt format with mapping of { senetence id : [aspect term]}
    Returns:
        dataset in form of lists
    """         
    with open(file_path) as output_file:
        output = json.load(output_file)
    output = ast.literal_eval(json.dumps(output, ensure_ascii=False, encoding='utf8'))
    return output


def main(predAspectTermPath,correctAspectTermPath):
    """
    This Module takes input paths from user for predicted and correct aspect terms and prints precision, recall and F-score
    """
    pred_aspect_terms = load_predicted_aspect_term(predAspectTermPath)  
    corr_aspect_terms = load_correct_aspect_term(correctAspectTermPath) 
    print 'Precision = %f -- Recall = %f -- F1 = %f' %aspect_extraction(pred_aspect_terms,corr_aspect_terms)

main(sys.argv[1],sys.argv[2])