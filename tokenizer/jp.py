#!/usr/bin/env python
# -*- : coding: utf-8 -*-

import nltk
from nltk.corpus.reader import *
from nltk.corpus.reader.util import *
from nltk.tokenize.api import *

stopwords = nltk.corpus.stopwords.words('japanese')
jp_sent_tokenizer = nltk.RegexpTokenizer(u'[^　「」！？。]*[！？。]')

class JPMeCabTokenizer(TokenizerI):

    def __init__(self) :
        import MeCab
        self.mecab = MeCab.Tagger('-Ochasen')

    def tekens(self) :
        return self.tokens

    def tokenize(self, text):
        node = self.mecab.parseToNode(text.encode('utf-8'))
        results = []
        while node is not None :
        	if ( node.posid >= 36 and node.posid <= 67 ) or \
        		( node.posid >= 31 and node.posid <= 33 ) :
        		word = node.feature.split(',')[6].decode('utf-8')
        		word = word == '*' and node.surface or word
        		if word not in stopwords :
        			results.append(word)
        	node = node.next
        self.tokens = results
        return results

def JapaneseCorpusReader(root, fieldsids, encoding='utf-8') :
    corpus = PlaintextCorpusReader( root, fieldsids,
                encoding = encoding,
                para_block_reader = read_line_block,
                sent_tokenizer = jp_sent_tokenizer,
                word_tokenizer = JPMeCabTokenizer())
    return corpus


if __name__ == '__main__' :
	reader = JapaneseCorpusReader("data", "index")
	print '/'.join(reader.words())
