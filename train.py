#!/usr/bin/env python

import sys
import os
import os.path
import re
import nltk
import math
import string
import csv
import pickle

training_set = sys.argv[1] #file name of training set
model_file = sys.argv[2] #file namel of model_file
porter = nltk.PorterStemmer() #Porter stemmer from nltk module
#lancaster = nltk.LancasterStemmer() #Porter stemmer from nltk module
##############################################################################################################################
#SUB FUNCTION
##############################################################################################################################

#tokenlize and filter the empty string ''
def split_words(input):
    return filter(filter_white_space,re.split('[^A-Za-z]|;|\s+|\#|\.|\*|/\|/|W+|!|:|^|%|\)|\(',input)) #',|;| *|\.|\*|/|;'

#to filter '' empty string
def filter_white_space(x):
    return x !=''

#to lowercase
def lc_word(input):
    return input.lower()

def filter_white_space(x):
        return x !='' #to filter '' empty string

#tokenlize and filter the empty string ''
def split_words(input):
        return filter(filter_white_space,re.split('[^A-Za-z]|;|\s+|\#|\.|\*|/\|/|W+|!|:|^|%|\)|\(',input))

#to remove punctuation
#deal with ',' later
puncts='.?!";-\'[]()'
def r_punctuation(input):
    data = ''
    for sym in puncts:
        data = data.replace(sym,' ')
    return data

#to remove stopwords or "too common" words
#could be addeed from chi-squared test(ones with low independency)
#stemming
stops={'d':0,'i':0,'of':0,'a':0,'an':0,'is':0,'was':0,'been':0,'are':0,'were':0,'it':0,'its':0,'they':0,'them':0,'this':0,'that':0,'the':0,'these':0,'those':0,'there':0,'here':0,'while':0,'when':0,'has':0,'had':0,'have':0,'s':0,'st':0,'to':0,'or':0,'and':0}
def r_word(input):
    corpus = []
    for item in input:
        if not stops.has_key(item):
            corpus.append(porter.stem(item)) #stem the word
    return corpus

##############################################################################################################################
#MAIN
##############################################################################################################################
#read training_set
file = open(training_set,'r')
#file = open('train.csv','r')
data = file.read()      #raw_data:whole training_set's text

data_set = re.split('\n',data.strip('\n'))

#number of document
N = len(data_set)-1 #6351
#print N
N_p = float(0)
N_n = float(0)

#########################################################################################
#PREPROCESSING
#########################################################################################
document = [] #index starts from 0,document[0] = document_1:[calss,tokenized_list[text]]
for i in range(N):

    temp_str = re.sub(',\"','@\"',data_set[i+1])
    temp_str = re.sub(',\"','@\"',data_set[i+1])
    temp_list = re.split('@',temp_str)

    if temp_list[0] == '0':
        N_n += 1
    else:
        N_p += 1

    temp_token_set = split_words(temp_list[1])
    temp_corpus = r_word(temp_token_set)

    document.append([string.atof(temp_list[0]),temp_corpus])

P_p = math.log(N_p/N)
P_n = math.log(N_n/N)

model = {}
#########################################################################################
#TRAINING
#########################################################################################
for info in document:
    for word in info[1]:
        if model.has_key(word):
            if info[0] == 0:
                model[word][0] += 1
            else:
                model[word][1] += 1
        else: #word is not included in model
            model[word] = [0,0] #[0]: nunber in class 0, [1]: number in class 1.
            if info[0] == 0:
                model[word][0] += 1
            else:
                model[word][1] += 1

#########################################################################################
#FEATURE SELECTION
#########################################################################################
fs_table = {}
for word in model.keys():
    #N_xy: if the documant contains term t x = 1, or x = 0
    #      if the document is in class c y = 1, or y = 0
    N_11 = model[word][1]
    N_10 = model[word][0]
    N_01 = N_p - model[word][1]
    N_00 = N_n - model[word][0]

    x_square =( (N_11 + N_10 + N_01 + N_00) * (N_11*N_00 - N_10*N_01)**2 )/( (N_11 + N_01) * (N_11 + N_10) * (N_10 + N_00) * (N_01 + N_00) )
    fs_table[word] = x_square

#sort the fs_table by value
fs_selection = sorted(fs_table.items(), key=lambda x: x[1] , reverse=True)


for item in fs_selection:
    if len(item[0]) < 2:#modify the parameter to find good features
        #print 'word: %s, score: %f\n' %(item[0], item[1])
        if not stops.has_key(item[0]) and item[1] < 10:
            stops[item[0]] = 0
            del model[item[0]]
            #print 'word: %s, score: %f\n' %(item[0], item[1])
    if item[1] <= 0.0005:#modify the parameter to find good features
        #print 'word: %s, score: %f\n' %(item[0], item[1])
        if not stops.has_key(item[0]):
            stops[item[0]] = 0
            del model[item[0]]

# for item in model.keys():
#     if len(item) <3:
#         print 'word: %s\n' %(item)

#use pickle to save the infomation needed for model
model_package = [model,P_n,P_p]
package = model_package
fn = model_file
#fn = 'model.pkl'
with open(fn, 'w') as f:
        picklestring = pickle.dump(package, f)
print 'training done'
file.close()


