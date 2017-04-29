'''
Run on terminal
>>>python Aspect_term_polarity_evaluation.py predAspectTermPolarityPath correctAspectTermPolarityPath
'''
import csv
import json
import ast
import sys

def aspect_polarity_estimation(pred_aspect_polarity,correct_aspect_polarity):
        """
        Module to evaluate aspect term polarities
        Arguments:
            predicted aspect term polarities and correct aspect term polarities, both in list format
        Returns:
            Accuracy for entire dataset
        """ 
        common, relevant, retrieved = 0., 0., 0.
        for sid in pred_aspect_polarity: 
            for index in range(len(correct_aspect_polarity)):
                if correct_aspect_polarity[index][0] == sid:
                    pre = pred_aspect_polarity[sid].keys()
                    if correct_aspect_polarity[index][4] !="": 
                        cor4 = correct_aspect_polarity[index][4].split('&')
                    else:
                        cor4 = 'None' 
                    if correct_aspect_polarity[index][5] !="": 
                        cor5 = correct_aspect_polarity[index][5].split('&')
                    else:
                        cor5 = 'None'       
                    retrieved+=len(pred_aspect_polarity[sid].keys())           
                    for k in pre: 
                        if cor5!='None':
                            for ind in range(len(cor5)):
                                if k == cor5[ind]:
                                    if pred_aspect_polarity[sid][k] == cor4[ind]:
                                        common+=1           
        acc = common / retrieved
        return acc
        
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


def load_predicted_aspect_term_polarity(file_path):
    """
    Module to load the predicted Aspect Term Polarity Dataset 
    Arguments:
        file path for original dataset in txt format with mapping of { senetence id : {aspect term :polarity}}
    Returns:
        dataset in form of lists
    """         
    with open(file_path) as output_file:
        output = json.load(output_file)
    output = ast.literal_eval(json.dumps(output, ensure_ascii=False, encoding='utf8'))
    return output
    
def main(predAspectTermPolarityPath,correctAspectTermPolarityPath):
    """
    This Module takes input paths from user for predicted and correct aspect term polarities and prints accuracy
    """
    pred_aspect_term_polarities = load_predicted_aspect_term_polarity(predAspectTermPolarityPath)  
    corr_aspect_term_polarities = load_correct_aspect_term(correctAspectTermPolarityPath) 
    print 'Accuracy = %f'%aspect_polarity_estimation(pred_aspect_term_polarities,corr_aspect_term_polarities)

main(sys.argv[1],sys.argv[2])

