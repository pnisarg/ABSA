import pandas as pd
import numpy as np
import sklearn
from sklearn.model_selection import train_test_split

categoryDF=pd.read_csv("Z:/MSBooks/NLP/Project/aspectCategoryDetection.csv",delimiter='#',encoding = 'utf-8')
del categoryDF['aspectTermPolarity']

domain=[]
for id in categoryDF.index:
    domain.append(categoryDF.iloc[id,0][:3])
categoryDF['domain'] = domain

categorySizeDF = pd.DataFrame({"count":categoryDF.groupby('domain',sort='False').size()})
categorySizeDF = categorySizeDF.reset_index()

temp = categorySizeDF.ix[10]
categorySizeDF.ix[10] = categorySizeDF.ix[11]
categorySizeDF.ix[11]= temp

dfList=[]
currentIndex= 0 
for id in categorySizeDF.index:    
    if id == 0:
        currentIndex=categorySizeDF.iloc[id,1]
        dfList.append(categoryDF[:currentIndex])
        
    else:
        nextIndex= currentIndex  + categorySizeDF.iloc[id,1]
        dfList.append(categoryDF[currentIndex:nextIndex])
        currentIndex=nextIndex
		
		
entertainmentDF = dfList[6].append(dfList[10])
electronicDF = dfList[1]
for i in range(len(dfList)):
    if i>1 and i!=6 and i!=10:
        electronicDF = electronicDF.append(dfList[i])

entertainmentDF = entertainmentDF.dropna(axis=0,how='any')
electronicDF = electronicDF.dropna(axis=0,how='any')