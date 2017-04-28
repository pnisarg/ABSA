import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.metrics import classification_report
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC
from sklearn.metrics import f1_score
from sklearn import tree
from collections import OrderedDict
from sklearn.ensemble import RandomForestClassifier

def loadCategoryDataFile(categoryDataPath):
    """
    Module to load aspect category dataset
    Args:
        categoryDataPath: aspect category data set
    Returns:
        train: training data
        test: testing data
    """
    categoryDF = pd.read_csv(categoryDataPath,delimiter='#',encoding = 'utf-8')
    train, test = train_test_split(categoryDF, test_size = 0.2)
    train = train.reset_index(drop='True')
    test = test.reset_index(drop='True')
    return train,test
    
def processCategoryData(train,test):
    """
    Module to create training and test data feature inputs and labels
    Args:
        train: training data
        test: testing data
    Returns:
        trainData: relevant training data
        trainLabels: train data labels
        testData: relevant test data
        testLabels: test data labels
        sentiTrainLabels: category sentiment training labels
        sentiTestLabels: category sentiment testing labels
    """
    trainData=[]
    testData = []
    trainLabels = []
    testLabels = []
    sentiTrainLabels=[]
    sentiTestLabels=[]
    for id in train.index:
        trainData.append(train.iloc[id,2])
        trainLabels.append(train.iloc[id,3])
        sentiTrainLabels.append(train.iloc[id,1])

    for id in test.index:
        testData.append(test.iloc[id,2])
        testLabels.append(test.iloc[id,3])
        sentiTestLabels.append(test.iloc[id,1])
        
    trainLabels = ['missing' if str(x)== 'nan' else x for x in trainLabels]
    testLabels = ['missing' if str(x) == 'nan' else x for x in testLabels]
    return trainData,trainLabels,testData,testLabels,sentiTrainLabels,sentiTestLabels
    
def loadHindiStopWords(stopWordsDataPath):
    """
    Module to load hindi stop words
    Args:
        stopWordsDataPath: hindi stop words dataset
    Returns:
        stopWords: stop word list
    """
    with open(stopWordsDataPath) as sw:
        stopWords=[x.strip("\n") for x in sw.readlines()]
    return stopWords
    
def createVectorizer(stopWords,trainData,testData):
    """
    Module to create tfidf feature vectors
    Args:
       stopWords: stop word list
       trainData: relevant training data
       testData: relevant test data
    Returns:
        train_vectors: training feature vector
        test_vectors: testing feature vector
    """ 
    vectorizer = TfidfVectorizer(stop_words=stopWords,min_df=5,max_df = 0.8,
                                 sublinear_tf=True,use_idf=True)
    train_vectors = vectorizer.fit_transform(trainData)
    test_vectors = vectorizer.transform(testData)
    return train_vectors,test_vectors
    
def loadSVMRbfClassifier(train_vectors,trainLabels,sentiTrainLabels,test_vectors):
    """
    RBF SVM Classifier module
    Args:
       train_vectors: training feature vector
       trainLabels: train data labels
       test_vectors: testing feature vector
       sentiTrainLabels: category sentiment training labels
    Returns:
        prediction_rbf: rbf predicted categories
        senti_prediction_rbf: rbf predicted sentiments
    """
    classifier_rbf = svm.SVC()
    classifier_rbf.fit(train_vectors, trainLabels)
    prediction_rbf = classifier_rbf.predict(test_vectors)
    senti_classifier_rbf=svm.SVC()
    senti_classifier_rbf.fit(train_vectors,sentiTrainLabels)
    senti_prediction_rbf = senti_classifier_rbf.predict(test_vectors)
    return prediction_rbf,senti_prediction_rbf
    
def loadSVMLinearClassifier(train_vectors,trainLabels,test_vectors,sentiTrainLabels):
    """
    Linear SVM Classifier module
    Args:
       train_vectors: training feature vector
       trainLabels: train data labels
       test_vectors: testing feature vector
       sentiTrainLabels: category sentiment training labels
    Returns:
        prediction_linear: linear predicted categories
        senti_prediction_linear: linear predicted sentiments
    """
    classifier_linear = OneVsRestClassifier(SVC(kernel='linear'))
    classifier_linear.fit(train_vectors, trainLabels)
    prediction_linear = classifier_linear.predict(test_vectors)

    senti_classifier_linear=svm.SVC(kernel='linear')
    senti_classifier_linear.fit(train_vectors,sentiTrainLabels)
    senti_prediction_linear = senti_classifier_linear.predict(test_vectors) 
    return prediction_linear,senti_prediction_linear   
    
def loadSVMLibLinearClassifier(train_vectors,trainLabels,test_vectors,sentiTrainLabels):
    """
    Lib Linear SVM Classifier module
    Args:
       train_vectors: training feature vector
       trainLabels: train data labels
       test_vectors: testing feature vector
       sentiTrainLabels: category sentiment training labels
    Returns:
        prediction_liblinear: lib linear predicted categories
        senti_prediction_liblinear: lib linear predicted sentiments
    """
    classifier_liblinear = svm.LinearSVC()
    classifier_liblinear.fit(train_vectors, trainLabels)
    prediction_liblinear = classifier_liblinear.predict(test_vectors)

    senti_classifier_liblinear=svm.LinearSVC()
    senti_classifier_liblinear.fit(train_vectors,sentiTrainLabels)
    senti_prediction_liblinear = senti_classifier_liblinear.predict(test_vectors)
    return prediction_liblinear,senti_prediction_liblinear
    
def getFScores(y_true,y_pred):
    """
    Module to find the f_score of predicted results
    Args:
        y_true: true labels
        y_pred: predicted labels
    Returns:
        None
    """
    print f1_score(y_true, y_pred, average='micro')
    
def getClassificationReport(y_train,y_true,y_pred):
    """
    Module to find class-wise classification report
    Args:
        y_train: training data labels
        y_true: true labels
        y_pred: predicted labels
    Returns:
        None
    """
    target_names = set(y_train)
    target_list = list(target_names)
    print(classification_report(y_true, y_pred, target_names=target_list))
    
def loadDecisionTree(trainLabels,train_vectors,test_vectors):
    """
    Decision Tree classification module
    Args:
       trainLabels: training data labels
       train_vectors: training feature vectors
       test_vectors: testing feature vectors
    Returns:
        resultData: Decision Tree classifier prediction
        trainMacros: Decision Tree label to integer map
        reverseMap: Decision Tree integer to label map
    """
    trainSet = set(trainLabels)
    i=0
    macros=OrderedDict()
    reverseMap=OrderedDict()
    for item in trainSet:
        macros[item]=i
        reverseMap[i]=item
        i  += 1
    trainMacros=[]
    for item in trainLabels:
        trainMacros.append(macros[item])    
    clf = OneVsRestClassifier(tree.DecisionTreeClassifier())
    clf = clf.fit(train_vectors, trainMacros)
    result = clf.predict(test_vectors)  
    resultList= result.tolist()
    resultData=[]
    for item in resultList:
        resultData.append(reverseMap[item]) 
    return resultData,trainMacros,reverseMap

def loadRandomForest(train_vectors,trainMacros,test_vectors,reverseMap):
    """
    Random Forest classifier module
    Args:
       train_vectors: training feature vectors
       trainMacros: label to integer map
       test_vectors: testing feature vectors
       reverseMap: integer to label map
    Returns:
        rfresultData: Random Forest prediction results
    """
    rfClf = OneVsRestClassifier(RandomForestClassifier())
    rfClf.fit(train_vectors,trainMacros)
    rfresult = rfClf.predict(test_vectors)
    rfresultList = rfresult.tolist()
    rfresultData=[]
    for item in rfresultList:
        rfresultData.append(reverseMap[item])
    return rfresultData
    
def main(categoryDataPath,stopWordsDataPath):
    """
    This module performs Aspect Category Detection and
    Aspect Category Sentiment Analysis based on Multi-Label Machine Learning models.
    Have used RBFSVM, LinearSVM, LibLinearSVM, DecisionTrees and RandomForest Classifiers
    for Aspect Category Detection and the results are compared
    
    Args:
        categoryDataPath: aspect category dataset
        stopWordsDataPath: stop words dataset
    Returns:
        None
    """
    train,test = loadCategoryDataFile(categoryDataPath)
    trainData,trainLabels,testData,testLabels,sentiTrainLabels,sentiTestLabels = processCategoryData(train,test)
    stopWords = loadHindiStopWords(stopWordsDataPath)
    train_vectors,test_vectors = createVectorizer(stopWords,trainData,testData)
    prediction_rbf,senti_prediction_rbf = loadSVMRbfClassifier(train_vectors,trainLabels,sentiTrainLabels,test_vectors)
    prediction_linear,senti_prediction_linear = loadSVMLinearClassifier(train_vectors,trainLabels,test_vectors,sentiTrainLabels)
    prediction_liblinear,senti_prediction_liblinear = loadSVMLibLinearClassifier(train_vectors,trainLabels,test_vectors,sentiTrainLabels)
    getFScores(testLabels, prediction_rbf)
    getFScores(testLabels, prediction_linear)
    getFScores(testLabels, prediction_liblinear) 
    getFScores(sentiTestLabels, senti_prediction_rbf)   
    getFScores(sentiTestLabels, senti_prediction_linear)   
    getFScores(sentiTestLabels, senti_prediction_liblinear)
    getClassificationReport(testLabels, prediction_rbf)
    getClassificationReport(testLabels, prediction_linear)
    getClassificationReport(testLabels, prediction_liblinear)
    getClassificationReport(sentiTestLabels, prediction_rbf)
    getClassificationReport(sentiTestLabels, prediction_linear)
    getClassificationReport(sentiTestLabels, prediction_liblinear)
    resultData,trainMacros,reverseMap = loadDecisionTree(trainLabels,train_vectors,test_vectors)
    getFScores(testLabels, resultData)
    rfresultData = loadRandomForest(train_vectors,trainMacros,test_vectors,reverseMap)
    getFScores(testLabels, rfresultData)
    
main(sys.argv[1],sys.argv[2])