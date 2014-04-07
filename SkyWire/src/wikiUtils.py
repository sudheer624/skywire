'''
Created on Aug 31, 2013

@author: swatha
'''
import nltk
import nltk.corpus.reader.wordnet as wordnet

class Utils(object):
    
    def __init__(self):
        self.stopwords = set(nltk.corpus.stopwords.words('english'))
        
    def tokenizeSentence( self, sentence ):
        words = []
        sentence = sentence.replace('\"', '')\
                           .replace('.', '')\
                           .replace(',', '')\
                           .replace(':', '')\
                           .replace('!', '')\
                           .replace('\'', '')
        for w in nltk.word_tokenize(sentence):
            if w not in self.stopwords:
                words.append(w)
        return words
    
    def get_wordnet_pos(self, treebank_tag):
        if treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('N'):
            return wordnet.NOUN
        elif treebank_tag.startswith('R'):
            return wordnet.ADV
        else:
            return ''