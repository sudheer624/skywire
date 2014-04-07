from __future__ import division
'''
Created on Jul 4, 2013

@author: swatha
'''
import nltk
from nltk.corpus import wordnet as wn
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import enchant
import nltk.metrics as metrics
from nltk.corpus import reuters
from nltk.corpus import brown
from nltk.corpus import PlaintextCorpusReader
from comprehend import Comprehend
from wikiMiner import WikiMiner
from spellCorrector import SpellCorrection
from wikiUtils import Utils
from nltk.stem.wordnet import WordNetLemmatizer
import sys

if __name__ == '__main__':
#    sentence = "i go the bill clinton"
#    tokens = nltk.word_tokenize(sentence)
#    print tokens
#    tagged = nltk.pos_tag(tokens)
#    print tagged
    #grammar = "NP: {<DT>?<JJ>*<NN>}"
    #cp = nltk.RegexpParser(grammar)
    #result = cp.parse(tagged)
    #wMiner = WikiMiner(False)
    '''
    print wMiner.getCorpus().fileids()
    words = wMiner.getCorpus().words()
    totalWordCount = len(words)
    print totalWordCount
    fdist = nltk.FreqDist(words)
    
    sc = SpellCorrection(fdist, totalWordCount)
    print sc.getCorrectWord('feelin')
    
    bigrams = nltk.bigrams(words)
    bigramFreq = nltk.FreqDist(bigrams)
    w = ('Baker', 'story')
    print w,bigramFreq.freq(w)
    print fdist.freq('story'), fdist['story']/totalWordCount
    print bigramFreq.items()
    '''
    #for k,v in bigramFreq.items():
    #    print k,v
    
    '''
    file_pattern = r".*/wiki_.*"
    corpus = PlaintextCorpusReader(corpus_root, file_pattern);
    print corpus.fileids()
    print len(corpus.words())
    '''
    
    
    '''
    print fdist['million']
    d = enchant.Dict("en_US")
    s = 'mllion'
    for w in d.suggest(s):
        print w.lower() + ' ' + str(fdist[w.lower()])
    '''
    
    '''
    depths = []
    test = Comprehend();
    sentences = test.readTweetFiles("/home/swatha/workspace-skywire/tweets/", "jesus");
    test.applyPOSTags(sentences)
    tokens = test.flatten(sentences)
    count = 0
    total = 0
    for t in tokens:
        total = total + 1
        synsets = wn.synsets(t)
        if len(synsets) == 0:
            print t
            count = count + 1
        else:
            for synset in synsets:
                depths.append(synset.min_depth())
    print (count*100)/total
    fdist = nltk.FreqDist(sorted(depths))
    fdist.plot()
    '''    
    
#    print nltk.corpus.stopwords.words('english')
#    utils = Utils()
#    utils.tokenizeSentence("i am a \"good\" boy")
    
    
#    cfdist = nltk.probability.ConditionalFreqDist()
#    cfdist['jesus']
#    for synset in wn.synsets('bill_clinton'):
#        print synset.lemma_names
#        for innerSynset in wn.synsets('president'):
#            print innerSynset.lemma_names
#            print synset.path_similarity(innerSynset)
    
#    fdist = nltk.FreqDist(tokens)
#    fdist.plot(50, cumulative=True)
#    print fdist.keys()
    str = "i am going to school"
    tokens = Utils().tokenizeSentence(str)
    tokens = nltk.pos_tag(tokens)
    print tokens
    for token in tokens:
        print WordNetLemmatizer().lemmatize(token[0], Utils().get_wordnet_pos(token[1]))
        
    print nltk.pos_tag('going')
    print sys.path
    print nltk.data.path