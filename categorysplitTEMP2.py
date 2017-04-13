import pandas as pd
import numpy as np
import sklearn
from sklearn.model_selection import train_test_split

categoryDF=pd.read_csv("Z:/MSBooks/NLP/Project/aspectCategoryDetection.csv",delimiter='#')
del categoryDF['aspectTermPolarity']
categoryDF.head()

categoryTrain, categoryRest = train_test_split(categoryDF, test_size = 0.4)
categoryDev, categoryTest = train_test_split(categoryRest,test_size=0.5)

finalCategoryDev = categoryDev[[0,2]].copy()
finalCategoryTest = categoryTest[[0,2]].copy()

categoryTrain.to_csv("Z:/MSBooks/NLP/Project/categorysets/categoryTrain.csv",sep='#')
finalCategoryDev.to_csv("Z:/MSBooks/NLP/Project/categorysets/categoryDev.csv",sep='#')
finalCategoryTest.to_csv("Z:/MSBooks/NLP/Project/categorysets/categoryTest.csv",sep='#')