import pandas as pd
import numpy as np
import sklearn
from sklearn.model_selection import train_test_split

categoryDF=pd.read_csv("Z:/MSBooks/NLP/Project/aspectCategoryDetection.csv",delimiter='#')
del categoryDF['aspectTermPolarity']

domain=[]
for id in categoryDF.index:
    domain.append(categoryDF.iloc[id,0][:3])
categoryDF['domain'] = domain

categorySizeDF = pd.DataFrame({"count":categoryDF.groupby('domain').size()})
categorySizeDF = categorySizeDF.reset_index()



dfList=[]
currentIndex=0
for id in categorySizeDF.index:    
    if id == 0:
        currentIndex=categorySizeDF.iloc[id,1]
        dfList.append(categoryDF[:currentIndex])
        
    else:
        nextIndex= currentIndex  + categorySizeDF.iloc[id,1]
        dfList.append(categoryDF[currentIndex:nextIndex])
        currentIndex=nextIndex
        
def dataSetSplit(domainDF):
    train, rest = train_test_split(domainDF, test_size = 0.4)
    dev, test  = train_test_split(rest, test_size=0.5)
    finalDev = dev[[0,2,4]].copy()
    finalTest = test[[0,2,4]].copy()
    return train,finalDev,finalTest

appTrain,appDev,appTest = dataSetSplit(dfList[0])
camTrain,camDev,camTest = dataSetSplit(dfList[1])
heaTrain,heaDev,heaTest = dataSetSplit(dfList[2])
homTrain,homDev,homTest = dataSetSplit(dfList[3])
lapTrain,lapDev,lapTest = dataSetSplit(dfList[4])
mobTrain,mobDev,mobTest = dataSetSplit(dfList[5])
movTrain,movDev,movTest = dataSetSplit(dfList[6])
smaTrain,smaDev,smaTest = dataSetSplit(dfList[7])
speTrain,speDev,speTest = dataSetSplit(dfList[8])
tabTrain,tabDev,tabTest = dataSetSplit(dfList[9])
telTrain,telDev,telTest = dataSetSplit(dfList[10])
traTrain,traDev,traTest = dataSetSplit(dfList[11])




appTrain.to_csv("Z:/MSBooks/NLP/Project/categorysets/appTrain.csv",sep='#')
appDev.to_csv("Z:/MSBooks/NLP/Project/categorysets/appDev.csv",sep='#')
appTest.to_csv("Z:/MSBooks/NLP/Project/categorysets/appTest.csv",sep='#')

camTrain.to_csv("Z:/MSBooks/NLP/Project/categorysets/camTrain.csv",sep='#')
camDev.to_csv("Z:/MSBooks/NLP/Project/categorysets/appDev.csv",sep='#')
appTest.to_csv("Z:/MSBooks/NLP/Project/categorysets/appTest.csv",sep='#')


appTrain.to_csv("Z:/MSBooks/NLP/Project/categorysets/appTrain.csv",sep='#')
appDev.to_csv("Z:/MSBooks/NLP/Project/categorysets/appDev.csv",sep='#')
appTest.to_csv("Z:/MSBooks/NLP/Project/categorysets/appTest.csv",sep='#')

appTrain.to_csv("Z:/MSBooks/NLP/Project/categorysets/appTrain.csv",sep='#')
appDev.to_csv("Z:/MSBooks/NLP/Project/categorysets/appDev.csv",sep='#')
appTest.to_csv("Z:/MSBooks/NLP/Project/categorysets/appTest.csv",sep='#')

appTrain.to_csv("Z:/MSBooks/NLP/Project/categorysets/appTrain.csv",sep='#')
appDev.to_csv("Z:/MSBooks/NLP/Project/categorysets/appDev.csv",sep='#')
appTest.to_csv("Z:/MSBooks/NLP/Project/categorysets/appTest.csv",sep='#')

appTrain.to_csv("Z:/MSBooks/NLP/Project/categorysets/appTrain.csv",sep='#')
appDev.to_csv("Z:/MSBooks/NLP/Project/categorysets/appDev.csv",sep='#')
appTest.to_csv("Z:/MSBooks/NLP/Project/categorysets/appTest.csv",sep='#')

appTrain.to_csv("Z:/MSBooks/NLP/Project/categorysets/appTrain.csv",sep='#')
appDev.to_csv("Z:/MSBooks/NLP/Project/categorysets/appDev.csv",sep='#')
appTest.to_csv("Z:/MSBooks/NLP/Project/categorysets/appTest.csv",sep='#')

appTrain.to_csv("Z:/MSBooks/NLP/Project/categorysets/appTrain.csv",sep='#')
appDev.to_csv("Z:/MSBooks/NLP/Project/categorysets/appDev.csv",sep='#')
appTest.to_csv("Z:/MSBooks/NLP/Project/categorysets/appTest.csv",sep='#')

appTrain.to_csv("Z:/MSBooks/NLP/Project/categorysets/appTrain.csv",sep='#')
appDev.to_csv("Z:/MSBooks/NLP/Project/categorysets/appDev.csv",sep='#')
appTest.to_csv("Z:/MSBooks/NLP/Project/categorysets/appTest.csv",sep='#')

appTrain.to_csv("Z:/MSBooks/NLP/Project/categorysets/appTrain.csv",sep='#')
appDev.to_csv("Z:/MSBooks/NLP/Project/categorysets/appDev.csv",sep='#')
appTest.to_csv("Z:/MSBooks/NLP/Project/categorysets/appTest.csv",sep='#')
