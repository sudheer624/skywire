from __future__ import division
'''
Created on Aug 4, 2013

@author: swatha
'''

'''
Spell corrector uses generative bayesian model for identifying the correct spelling
Misspelling can happen due to following any number of times
    -character deletion
    -character replacement (deletion + addition)
    -character addition
    -combining multiple words together

MW - denotes random variable to identify misspelt word
W - denotes random variable to identify correct word

P(W/MW) = ( P(MW/W) * P(W) )/P(MW)
P(MW/W) - captures generative process
P(W) - prior probability (correction process). Using wikipeidia documents for word prior probabilities
P(MW) - this is very hard to compute. We can avoid this as a normalizing constant.

we can simply  ( P(MW/W) * P(W) )/P(MW) using loglikelihood.

Algorithm:
1) Using english dictionary (enchant) generate all possible meaningful words (w1,w2,w3....wn) from mw

             n
2) compute argmax( log p(MW/Wi) + log p(Wi) )
            i=1
'''

import math
import enchant
import nltk.metrics as metrics

class SpellCorrection(object):
    '''
    classdocs
    '''


    def __init__(self, freqDist, totalWordCount):
        '''
        Constructor
        '''
        self.dictionary = enchant.Dict("en_US")
        self.freqDist = freqDist
        self.totalWordCount = totalWordCount
        
    def getCorrectWord(self, typo):
        suggestedWords = self.dictionary.suggest(typo)
        maxlikelihood = float('-inf')
        correctedWord = ''
        for sWord in suggestedWords:
            words = sWord.split(' ')
            if len(words) > 0:
                prior = 0
                for w in words:
                    prior = prior + (self.freqDist[w] + 1)/self.totalWordCount
                priorProbability = prior/len(words)
            else:
                priorProbability = (self.freqDist[sWord] + 1)/self.totalWordCount
            
            edist = metrics.edit_distance(typo.lower(), sWord.lower())
            nDeletions = 0
            nReplacements = 0
            nAdditions = 0
            if len(sWord) > len(typo):
                nDeletions = len(sWord) - len(typo)
                nReplacements = edist - nDeletions
            elif len(sWord) < len(typo):
                nAdditions = len(typo) - len(sWord)
                nReplacements = edist - nAdditions
            elif len(sWord) == len(typo):
                nReplacements = edist
            
            generativeCount = self.__getGenerativeCountForAddition(sWord, nAdditions) * self.__getGenerativeCountForDeletion(sWord, nDeletions) * self.__getGenerativeCountForReplacement(sWord, nReplacements)
            likelihood = (math.log(1/generativeCount) + math.log(priorProbability))
            
            #Since we are using log probabilities which will be negative value
            if maxlikelihood < likelihood:
                maxlikelihood = likelihood
                correctedWord = sWord
            
            print sWord + ' ' + str(priorProbability) + ' ' + str(nDeletions) + ' ' + str(nReplacements) + ' ' + str(nAdditions) + ' ' + str(likelihood)
            
        return correctedWord
            
    def __getGenerativeCountForDeletion(self, sWord, nDeletions):
        base = len(sWord)
        total = 1
        for i in range(nDeletions):
            total = total * (base - i)
        return total
    
    def __getGenerativeCountForAddition(self, sWord, nAdditions):
        base = len(sWord) + 1
        total = 1
        for i in range(nAdditions):
            total = total * (base + i) * 26
        return total
    
    def __getGenerativeCountForReplacement(self, sWord, nReplacements):
        base = len(sWord)
        total = 1
        for i in range(nReplacements):
            total = total * (base - i) * 25
        return total