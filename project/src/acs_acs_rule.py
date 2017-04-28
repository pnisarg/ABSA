import pandas as pd
from sklearn.model_selection import train_test_split
import codecs
from collections import OrderedDict
import pickle
import json,ast
import sys
from sklearn.metrics import f1_score

def loadCategoryData(categoryDataPath):
    """
    Module to load the aspect category dataset
    Args:
        categoryDataPath: aspect category data path
    Returns:
        train: training data frame
        test: testing data frame
    """
    categoryDF=pd.read_csv(categoryDataPath,delimiter='#',encoding = 'utf-8')
    del categoryDF['aspectTermPolarity']
    domain=[]
    for id in categoryDF.index:
        domain.append(categoryDF.iloc[id,0][:3])
    categoryDF['domain'] = domain
    train, test = train_test_split(categoryDF, test_size = 0.2)
    return train,test

def loadPOSTaggedReviewData(POSDataPath):
    """
    Module to load POS tagged review data
    Args:
        POSDataPath: POS tagged data path
    Returns:
        reviewList: list of pos tagged reviews
    """    
    reviewList=[]
    posReview = codecs.open(POSDataPath,encoding='utf-8')
    reviewList=[x.strip() for x in posReview.readlines()]
    return reviewList
    
def getAspectDefiningTerms(reviewList,train):
    """
    Module to extract aspect term defining words
    Args:
        reviewList: list of pos tagged reviews
        train: training data frame
    Returns:
        trainAdjectives = training data frame with aspect defining terms for each review
    """
    adjectives=OrderedDict()
    for item in reviewList:
        idAndTagged = item.split()
        id = idAndTagged[0]
        taggedSentence = idAndTagged[1:]
        domain = id.split("/")[0]
        definingTerms = [s for s in taggedSentence if "JJ" in s]
        adjTerms = []
        for items in definingTerms:
            word=items.split("/")[0]
            word = word.encode('utf-8')
            adjTerms.append(word)
            adjectives[domain]=adjTerms
    adjectiveDF = pd.DataFrame.from_dict(adjectives,orient='index')
    adjectiveDF = adjectiveDF.reset_index()
    adjectiveDF = adjectiveDF.rename(columns={"index":"reviewID"})
    domain=[]
    for id in adjectiveDF.index:
        domain.append(adjectiveDF.iloc[id,0][:3])
    adjectiveDF['domain'] = domain
    trainAdjectives = train.merge(adjectiveDF,how='inner',left_on='domainID',right_on='reviewID')
    trainAdjectives = trainAdjectives.drop(['domain_x','reviewID','domain_y'],axis=1)
    return trainAdjectives
    
def createTrainingLexicon(trainAdjectives):
    """
    Module to create a lexicon of aspect term defining words
    Args:
        trainAdjectives: training data frame with aspect defining terms for each review
    Returns:
        trainLexicon: Lexicon of defining terms under each category
    """
    trainLexicon={}
    for id in trainAdjectives.index:
        category = trainAdjectives.iloc[id,3]
        adjectives = trainAdjectives.iloc[id][4:]
        adjectives = adjectives.dropna()
        for items in adjectives:
            adjList=[]
            if category in trainLexicon.keys():
                trainLexicon[category].append(items)
            else:
                adjList.append(items)
                trainLexicon[category] = adjList
    word2Synset = pickle.load(open("WordSynsetDict.pk"))
    synonyms = pickle.load(open("SynsetWords.pk"))
    for key,item in trainLexicon.iteritems():
        for words in item:
            if isinstance(words,str):
                word = words.decode('utf-8','ignore')
                synList = getSynonyms(word,word2Synset,synonyms)
                if len(synList)>0:
                    for k,value in synList[0].iteritems():
                        for syns in value:
                            trainLexicon[key].append(syns)
    return trainLexicon
                            
def getSynonyms(word,word2Synset,synonyms):
    """
    Module to extract synonyms of a word using Hindi wordnet
    Args:
        word: the word of which synonyms has to be extracted
        word2Synset: dictionary of synset of the word
        synonyms: dictionary of synonyms of the word
    Returns:
        synList: list of synonyms of the word
    """
    synList=[]
    if word2Synset.has_key(word):
        synsets = word2Synset[word]
        for pos in synsets.keys():
            for synset in synsets[pos]:
                if synonyms.has_key(synset):
                    synDict = synonyms[synset]
                    synList.append(synDict)
    return synList
    
def loadAspectTermData(aspectTermDataPath):
    """
    Module to load aspect term data obtained from Aspect Term Extraction Module
    Args:
        aspectTermDataPath: aspect term data path from Aspect Term Extraction Module
    Returns:
        termData: list of aspect term data from Aspect Term Extraction Module
    """    
    with open(aspectTermDataPath) as termFile:
        termData = json.load(termFile)
    termData = ast.literal_eval(json.dumps(termData, ensure_ascii=False, encoding='utf8'))
    return termData
        
def getCategoryPrediction(termData,trainLexicon,test):
    """
    Module to get category predictions
    Args:
        termData: list of aspect term data from Aspect Term Extraction Module
        trainLexicon: Lexicon of defining terms under each category
        test: testing data frame
    Returns:
        finalDF: data frame with predicted and true category labels
    """
    categoryDict=OrderedDict()
    for key,items in termData.iteritems():
        for k,v in items.iteritems():
            if len(v)>0:
                for items in v:
                    for lexKey,lexItems in trainLexicon.iteritems():
                        if items.decode('utf-8','ignore') in lexItems:
                            categoryDict[key] = lexKey
    predictedCategoryDF = pd.DataFrame(categoryDict.items(), columns=['reviewID', 'predictedCategory'])
    finalDF = test.merge(predictedCategoryDF,left_on="domainID",right_on="reviewID")
    finalDF = finalDF.dropna()
    finalDF.reset_index(drop='True')
    return finalDF
    
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
    
def loadAspectTermSentimentData(termSentimentDataPath):
    """
    Module to load aspect term sentiment data from Aspect Term Sentiment Extraction Module
    Args:
       termSentimentDataPath: aspect term sentiment data path 
    Returns:
        termSentiData: dictionary of aspect terms and its sentiment
    """    
    with open(termSentimentDataPath) as termSentiFile:
        termSentiData = json.load(termSentiFile)
    termSentiData = ast.literal_eval(json.dumps(termSentiData, ensure_ascii=False, encoding='utf8'))
    return termSentiData

def getCategorySentiments(termSentiData,trainLexicon,finalDF):
    """
    Module to extract category-wise sentiment scores and
    generate final dataframe with predicted and true sentiment
    Args:
        termSentiData: dictionary of aspect terms and its sentiment
        trainLexicon: Lexicon of defining terms under each category
        finalDF: data frame with predicted and true category labels
    Returns:
        finaDF: data frame with predicted and true category sentiment labels
    """
    categorySentiScore={}
    for key,values in termSentiData.iteritems():
        if len(values)>0:
            for k,v in values.iteritems():
                for entKey,entVal in trainLexicon.iteritems():
                    if k in entVal:
                        if entKey in categorySentiScore:
                            categorySentiScore[entKey] += v
                        else:
                            categorySentiScore[entKey] = v
    predictedCategory = finalDF['predictedCategory']
    predictedCategorySentiment=[]
    for category in predictedCategory:
        if category in categorySentiScore.keys():
            if categorySentiScore[category] > 0:
                predictedCategorySentiment.append('pos')
            elif categorySentiScore[category] == 0:
                predictedCategorySentiment.append('neu')
            elif categorySentiScore[category] < 0:
                predictedCategorySentiment.append('neg')
        else:
            predictedCategorySentiment.append('neu')
    finalDF['predictedCategorySentiment'] = predictedCategorySentiment
    return finalDF
                            
def main(categoryDataPath,POSDataPath,aspectTermDataPath,termSentimentDataPath):
    """
    Module to perform Aspect Category Detection based on 
    Aspect Terms and Aspect Defining Terms extracted from Aspect Term Extraction module
    using Rule based and CRF techniques
    Args:
       categoryDataPath: aspect category data path
       POSDataPath: POS tagged data path
       aspectTermDataPath: aspect term data path from Aspect Term Extraction Module
       termSentimentDataPath: aspect term sentiment data path 
    Returns:
        None
    """
    train,test = loadCategoryData(categoryDataPath)
    reviewList = loadPOSTaggedReviewData(POSDataPath)
    trainAdjectives = getAspectDefiningTerms(reviewList,train)
    trainLexicon = createTrainingLexicon(trainAdjectives)
    termData = loadAspectTermData(aspectTermDataPath)
    finalDF = getCategoryPrediction(termData,trainLexicon,test)
    getFScores(finalDF['aspectCategory'], finalDF['predictedCategory'])
    termSentiData = loadAspectTermSentimentData(termSentimentDataPath)
    finalDF = getCategorySentiments(termSentiData,trainLexicon,finalDF)
    getFScores(finalDF['categoryPolarity'], finalDF['predictedCategorySentiment'])
    
main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])