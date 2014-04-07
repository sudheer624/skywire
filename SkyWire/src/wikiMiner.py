'''
Created on Aug 3, 2013

@author: swatha
'''

import os
import random
import datetime
import shutil
from nltk.corpus import PlaintextCorpusReader

class WikiMiner(object):
    '''
    classdocs
    '''


    def __init__(self, fullDistribution):
        '''
        Constructor
        '''
        self.sample_sub_dir = "samples"
        corpus_root = '/workspace-memorymap/wikipedia/text-format'
        file_pattern = r".*/wiki_.*"
        if fullDistribution:
            self.corpus = PlaintextCorpusReader(corpus_root, file_pattern);
        else:
            self.corpus = PlaintextCorpusReader(self.__generateRandomSample(corpus_root, 17000), r'.*');
        
    def __generateRandomSample(self, corpus_root, num_samples):
        allFiles = []
        for dirname, dirnames, filenames in os.walk(corpus_root):        
            # print path to all filenames.
            for filename in filenames:
                allFiles.append(os.path.join(dirname, filename))
        sample_sub_dir_path = os.path.join(corpus_root, self.sample_sub_dir)
        if os.path.exists(sample_sub_dir_path):
            shutil.rmtree(sample_sub_dir_path)
        os.makedirs(sample_sub_dir_path)
        random.seed(datetime.datetime.now())
        sampleFiles = random.sample(allFiles, num_samples)
        for samplefile in sampleFiles:
            prefixes = samplefile.split('/')
            symFile = os.path.join(sample_sub_dir_path, prefixes[len(prefixes)-2] + '_' + prefixes[len(prefixes)-1])
            os.symlink(samplefile, symFile) 
        return sample_sub_dir_path
    
    def getCorpus(self):
        return self.corpus

if __name__ == '__main__':
    miner = WikiMiner(False)
    