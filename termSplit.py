import pandas as pd
import numpy as np
import sklearn
from sklearn.model_selection import train_test_split

termDF=pd.read_csv("aspectTerm.csv",delimiter='#')
termDF.columns=['domainID','review','termFrom','termTo','polarity','term']


termTrain, termRest = train_test_split(termDF, test_size = 0.4)
termDev, termTest = train_test_split(termRest,test_size=0.5)

finalTermDev = termDev[[0,1]].copy()
finalTermTest = termTest[[0,1]].copy()

termTrain.to_csv("termTrain.csv",sep='#')
finalTermDev.to_csv("termDev.csv",sep='#')
finalTermTest.to_csv("termTest.csv",sep='#')
