# -*- coding: utf-8 -*-

"""
Demo program of Hindi WordNet in Python. 

Here I demonstrate all the functionalities of the libraries, but note you can load only the pickle files which are necessary for your task rather than loading every pickle file. Loading of pickle files takes time and memory. But once loaded, all your WordNet operations are just O(1) which means your WordNet lookup is no longer a bottleneck.

Developer: Siva Reddy <siva@sivareddy.in>
Please point http://sivareddy.in/downloads for others to find these python libraries.

"""

import pickle

word2Synset = pickle.load(open("WordSynsetDict.pk"))
synset2Onto = pickle.load(open("SynsetOnto.pk"))
synonyms = pickle.load(open("SynsetWords.pk"))
synset2Gloss = pickle.load(open("SynsetGloss.pk"))
synset2Hypernyms = pickle.load(open("SynsetHypernym.pk"))
synset2Hyponyms = pickle.load(open("SynsetHyponym.pk"))
synset2Hypernyms = pickle.load(open("SynsetHypernym.pk"))

word = "खाना".decode('utf-8', 'ignore')
while True:
    if word2Synset.has_key(word):
        synsets = word2Synset[word]
        print "Word -->", "खाना "
        for pos in synsets.keys():
            print "POS Category -->", pos
            for synset in synsets[pos]:
                print "\t\tSynset -->", synset
                if synonyms.has_key(synset):
                    print "\t\t\t Synonyms -->", synonyms[synset]
                if synset2Gloss.has_key(synset):
                    print "\t\t\t Synset Gloss", synset2Gloss[synset]
                if synset2Onto.has_key(synset):
                    print "\t\t\t Ontological Categories", synset2Onto[synset]
                if synset2Hypernyms.has_key(synset):
                    print "\t\t\t Hypernym Synsets", synset2Hypernyms[synset]
                if synset2Hyponyms.has_key(synset):
                    print "\t\t\t Hyponym Synsets", synset2Hyponyms[synset]
    word = raw_input("Enter a word: ").decode("utf-8", "ignore")
