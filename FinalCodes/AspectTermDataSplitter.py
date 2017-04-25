import pandas as pd
from sklearn.model_selection import train_test_split
import sys

def main(aspectTermDataPath):
    """
    Module to load aspect terms data
    Args:
        aspectTermDataPath: data path to aspect terms data set
    Returns:
        None
    """
    termDF=pd.read_csv(aspectTermDataPath,delimiter='#')
    termDF.columns=['domainID','review','termsFrom','termsTo','polarity','terms']
    termTrain, termTest = train_test_split(termDF, test_size = 0.2)
    finalTermTest = termTest[[0,1]].copy()
    termTrain.to_csv("termTrain.csv",index=False,sep="#")
    finalTermTest.to_csv("termTest.csv",index=False,sep='#')

main(sys.argv[1])