'''
Created on Apr 22, 2014

@author: sramoji
'''
import logging
from nltk.corpus import stopwords
from gensim import corpora, models, similarities

class DocumentSummerizer(object):
    '''
    classdocs
    '''


    def __init__(self, documents, query):
        '''
        Constructor
        '''
        self.documents = documents
        self.query = query
        self.stopwords = stopwords.words('english')
        #logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    
    def getSummary(self):
        try:
            texts = [[word for word in document.lower().split() if word not in self.stopwords] for document in self.documents]
            allTokens = sum(texts, [])
            tokensOnce = set(word for word in set(allTokens) if allTokens.count(word) == 1)
            texts = [[word for word in text if word not in tokensOnce] for text in texts]
            dictionary = corpora.Dictionary(texts)
            corpus = [dictionary.doc2bow(text) for text in texts]
            tfidf = models.TfidfModel(corpus)
            corpusTfidf = tfidf[corpus]
            lsi = models.LsiModel(corpusTfidf, id2word=dictionary, num_topics=2)
            corpusLsi = lsi[corpusTfidf]
            querybow = dictionary.doc2bow(self.query.lower().split())
            queryTfidf = tfidf[querybow]
            queryVec = lsi[queryTfidf]
            index = similarities.MatrixSimilarity(corpusLsi)
            sims = index[queryVec]
            sims = sorted(enumerate(sims), key=lambda item: -item[1])
            documentScores = dict()
            for i,score in sims:
                documentScores[i] = score
            filteredDocuments = []
            for i, document in enumerate(self.documents):
                if documentScores[i] > 0.0:
                    filteredDocuments.append(document)
            return "".join(filteredDocuments)
        except:
            return "".join(self.documents)