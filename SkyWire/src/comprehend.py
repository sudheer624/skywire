'''
Created on Jul 23, 2013

@author: swatha
'''

import os
import json
import nltk
import enchant
import nltk.metrics as metrics

class Comprehend(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.wordNetFilterTags = ['NN', 'NNS', 'NNP', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
        self.dictionary = enchant.Dict("en_US")
    
    def test(self):
        print "this is my first class in python"
    
    def readTweetFiles(self, path, filterStr):
        sentences = []
        for dirname, dirnames, filenames in os.walk(path):
            for filename in filenames:
                filePath = os.path.join(dirname, filename)
                line = open(filePath).readline()
                tweetContent = json.loads(line)
                for tweetInfo in tweetContent['statuses'] :
                    tweetText = self.__normalize(json.dumps(tweetInfo['text']).lower())
                    if filterStr.lower() in tweetText :
                        address = json.dumps(tweetInfo['user']['location'])
                        address = address.replace("\"", "")
                        if len(address) > 0 :
                            obj = {}
                            obj['raw_text'] = tweetText
                            sentences.append(obj)
        return sentences
    
    def preprocessTweets(self, sentences):
#        sentenceTokens = []
#        stemmer = nltk.LancasterStemmer()
#        for sentence in sentences :
#            tokens = []
#            for t in nltk.word_tokenize(sentence):
#                #tokens.append(stemmer.stem(t))
#                tokens.append(t)
#            sentenceTokens.append(tokens)
#            print sentence
        return sentences
    
    def __normalize(self, sentence):
        sentence = sentence.replace('\"', '')\
                           .replace('.', '')\
                           .replace(',', '')\
                           .replace(':', '')\
                           .replace('!', '')\
                           .replace('\'', '')
        return sentence
    
    def flatten(self, sentences):
        allTokens = []
        wnFilter = set(self.wordNetFilterTags)
        for sentence in sentences:
            tokens = sentence['pos_tags']
            for t in tokens:
                if t[1] in wnFilter:
                    allTokens.append(t[0])
        return set(allTokens)
    
    def applyPOSTags(self, sentences):
        for sentence in sentences:
            tokens = nltk.word_tokenize(sentence['raw_text'])
            tagged = nltk.pos_tag(tokens)
            sentence['pos_tags'] = tagged
            
    def correctTypo(self, word):
        dist = []
        for sWord in self.dictionary.suggest(word):
            dist.append(metrics.edit_distance(sWord, word))
        return dist