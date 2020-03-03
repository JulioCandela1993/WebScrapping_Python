# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 08:49:46 2020

@author: juliochristian
"""
import json
import os
import re
from collections import Counter
import operator
import nltk
from nltk.corpus import stopwords
nltk.download("stopwords") # download the stopword corpus on our computer
import string

os.chdir("G:/Documentos/MasterDegree/BDMA/Classes/UPC/CloudComputing/Lab3")

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs

    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]

##Tokens to separate the text into elements
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
##Frequent words and punctuations
punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via', 'RT']
## New punctuation taken into account
new_punctuation = ["’","…","‘"]
new_stop = stop + new_punctuation

def tokenize(s):
    return tokens_re.findall(s)

def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens


with open('BrexitTweets.json','r') as json_file:
    count_all = Counter()
    count_hashtags = Counter()
    count_no_hashtags = Counter()
    for line in json_file:
        # The file generates some empty lines among tweets, so we need to skip them
        if line!='\n':
            tweet = json.loads(line)
            #print(tweet['text'])
            #Get tokens of the tweet text
            tokens = preprocess(tweet['text'], True)
            #print(tokens)
            # Create a list with all the terms 
            #terms_all = [term for term in tokens ]
            # Create a list with all the terms + non stop
            #terms_all = [term for term in tokens if term not in stop]
            # Create a list with all the terms + non stop + new punctuation
            terms_all = [term for term in tokens if term not in new_stop]
            # Create a list with only hashtags
            terms_hash = [term for term in tokens if term.startswith('#')]
            # Create a list with all preprocessed terms except hashtags nor mentions
            terms_only = [term for term in tokens if term not in new_stop and not term.startswith(('#', '@'))]
            # Update the counter
            count_all.update(terms_all)
            # Update the counter of hashtags
            count_hashtags.update(terms_hash)
            # Update the counter without hashtags or mentions
            count_no_hashtags.update(terms_only)
    # Most Common Tokens    
    print("\nTop 10 Tokens")    
    for word, index in count_all.most_common(10):
        print ('%s : %s' % (word, index))
    # Most Common Hashtags
    print("\nTop 10 Hashtags")
    for word, index in count_hashtags.most_common(10):
        print ('%s : %s' % (word, index))
    # Most Common Tokens without Hashtags or Mentions
    print("\nTop 10 No Hashtags nor mentions")
    for word, index in count_no_hashtags.most_common(10):
        print ('%s : %s' % (word, index))      
        
        
        
        
        
        