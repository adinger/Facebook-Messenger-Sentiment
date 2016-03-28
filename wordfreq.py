#! /usr/bin/env python
# wordcount.py: parse & return word frequency
import sys, nltk

def get_word_frequency(filename):

    f = open(filename, 'rU')
    txt = f.read()
    f.close()

    tokens = nltk.word_tokenize(txt) # tokenize text
    clean_tokens = []

    for word in tokens:
        word = word.lower()
        if word.isalpha(): # drop all non-words
            clean_tokens.append(word)

    # make frequency distribution of words
    fd = nltk.FreqDist(clean_tokens)
    for token in fd:
        print(token, ':', fd[token])

get_word_frequency("data/words_test.txt")