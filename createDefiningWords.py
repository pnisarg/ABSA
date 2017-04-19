reviewList=[]
posReview = codecs.open('Z:/MSBooks/NLP/Project/postaggedreviews.txt',encoding='utf-8')
reviewList=[x.strip() for x in posReview.readlines()]


from collections import OrderedDict
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
adjectiveDF.head()

domain=[]
for id in adjectiveDF.index:
    domain.append(categoryDF.iloc[id,0][:3])
adjectiveDF['domain'] = domain

