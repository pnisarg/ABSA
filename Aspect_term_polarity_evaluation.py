'''
Run on terminal
>>>python Aspect_term_polarity_evaluation.py predicted_ATS original_AT.csv
'''

import csv
import json
import ast
import sys
def aspect_polarity_estimation():
        i=0
        common, relevant, retrieved = 0., 0., 0.
        for sid in pred_aspect_sent: 
            '''if i==50:
                break
            i+=1 '''
            for index in range(len(corr_aspect_sent)):
                if corr_aspect_sent[index][0] == sid:
                    pre = pred_aspect_sent[sid].keys()
                    if corr_aspect_sent[index][4] !="": 
                        cor4 = corr_aspect_sent[index][4].split('&')
                    else:
                        cor4 = 'None' 
                    if corr_aspect_sent[index][5] !="": 
                        cor5 = corr_aspect_sent[index][5].split('&')
                    else:
                        cor5 = 'None'       
                    '''if pred_aspect_sent[sid] == {}:
                        if len(cor4)>0 and cor4!='None':
                            for ind in range(len(cor5)): 
                                #final_list.append([sid,'None','None',cor5[ind],cor4[ind]])
                                c+=1  
                                print "pred empty but corr exists"
                                print sid, retrieved, len(pred_aspect_sent[sid].keys()), pre, cor5[ind]    
                        else:
                            print "Both Empty"'''
                    retrieved+=len(pred_aspect_sent[sid].keys()) 
                    #print sid, retrieved            
                    for k in pre:
                        #pred_sent=''
                        #print sid, k,  pred_aspect_sent[sid],cor5, cor4
                        '''if pred_aspect_sent[sid][k] == 1:
                            pred_sent = 'pos'
                        elif pred_aspect_sent[sid][k] == 0:
                            pred_sent = 'neu'
                        elif pred_aspect_sent[sid][k] == -1:
                            pred_sent = 'neg' '''  
                        #print sid, retrieved, len(pred_aspect_sent[sid].keys()), pre, cor5    
                        if cor5!='None':
                            for ind in range(len(cor5)):
                                if k == cor5[ind]:
                                    if pred_aspect_sent[sid][k] == cor4[ind]:
                                        common+=1
                                        #print "Match"
                                        #print sid,k,pred_aspect_sent[sid][k],cor5[ind],cor4[ind],common, retrieved
                                    '''else:
                                        print "Sent Not match"
                                        if sid == "tab_763":
                                            print sid, pred_aspect_sent[sid][k], cor4[ind]
                                        print sid,k,pred_aspect_sent[sid][k],cor5[ind],cor4[ind],common, retrieved
                                else:
                                    print "Aspect Term Not Match"
                                    print sid,k,pred_aspect_sent[sid][k],cor5[ind],cor4[ind],common, retrieved 
                        if cor4 == "None":
                            print "Pred exists corr empty"
                            print sid, retrieved, len(pred_aspect_sent[sid].keys()), k, cor5'''               
        acc = common / retrieved
        #return acc, common, retrieved
        #print c, count, cnt
        return acc
with open(sys.argv[2], 'rb') as f:
    reader = csv.reader(f,delimiter ='#')
    corr_aspect_sent = list(reader)

#print corr_aspect_term[1]

# Loads model from the model file
def load_output(file_path):
    with open(file_path) as output_file:
        output = json.load(output_file)
    output = ast.literal_eval(json.dumps(output, ensure_ascii=False, encoding='utf8'))
    return output
    
pred_aspect_sent = load_output(sys.argv[1])

print 'Accuracy = %f'%aspect_polarity_estimation()