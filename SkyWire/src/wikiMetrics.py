'''
Created on Aug 17, 2013

@author: swatha
'''

from disco import util
from disco import core
import sys
import nltk
import nltk.corpus.reader.wordnet as wordnet

def map(line, params):
    for w in line.split():
        yield w, 1

def reduce(iterator, params):
    freqCounts = dict()  
    for w, count in iterator:
        if freqCounts.get(w) == None:
            freqCounts[w] = count
        else:
            freqCounts[w] = freqCounts[w] + count
    for w, counts in freqCounts.items():
        yield w, counts


class WikiMetrics(core.Job):
    partitions = 16
    merge_partitions = False
    sort = False
    
    def setLineParser(self):
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
            w = w.lower()
            if w not in self.stopwords:
                words.append(w)
        
        #lemmatizations
        tokens = nltk.pos_tag(words)
        nWords = []
        for token in tokens:
            pos = self.get_wordnet_pos(token[0], token[1])
            if len(pos) > 0 :
                nWords.append(nltk.stem.wordnet.WordNetLemmatizer().lemmatize(token[0], pos))
            else :
                nWords.append(token);
        return nWords
    
    def get_wordnet_pos(self, token, tag):
        if tag.startswith('J'):
            return wordnet.ADJ
        elif tag.startswith('V'):
            return wordnet.VERB
        elif tag.startswith('N'):
            return wordnet.NOUN
        elif tag.startswith('R'):
            return wordnet.ADV
        else:
            return ''

    def map(self, line, params):
        for w in self.tokenizeSentence(line):
            yield w, 1

    def reduce(self, iterator, out, params):
        freqCounts = dict()  
        for w, count in iterator:
            if freqCounts.get(w) == None:
                freqCounts[w] = count
            else:
                freqCounts[w] = freqCounts[w] + count
        for w, counts in freqCounts.items():
            out.add(w, counts)
                
if __name__ == '__main__':
    from wikiMetrics import WikiMetrics
    wikiMetrics = WikiMetrics()
    wikiMetrics.setLineParser()
    job = wikiMetrics.run(input=["data:wiki_sample"])
    metricsFile = open("wiki-metrics-sample", "w")
    for word, count in core.result_iterator(job.wait(show=True)):
        metricsFile.write(word + "\t" + str(count) + "\n")
    metricsFile.close()