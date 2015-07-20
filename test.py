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

model_file = sys.argv[1] #file namel of model_file
test_set = sys.argv[2] #file name of test set
prediction_file = sys.argv[3] #file name of prediction_file
porter = nltk.PorterStemmer() #Porter stemmer from nltk module
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

#use pickle to save the infomation needed for model
fn = model_file
#fn = 'model.pkl'
with open(fn, 'r') as f:
        model_package = pickle.load(f)

P_p = model_package[2]
P_n = model_package[1]
model = model_package[0]

B = len(model) #number of term in the vocabulary
sum_Tn = float(0) #sum of the number of occurrences of term in the tranning documnet from class 0
sum_Tp = float(0) #sum of the number of occurrences of term in the tranning documnet from class 1

for word in model:
    sum_Tn += model[word][0]
    sum_Tp += model[word][1]

P_Cn = float(0)
P_Cp = float(0)

#read training_set
file = open(test_set,'r')
#file = open('test.csv','r')
data = file.read()      #raw_data:whole training_set's text

data_set = re.split('\n',data.strip('\n'))

document = [] #index starts from 0,document[0] = document_1:[calss,tokenized_list[text]]

for i in range(len(data_set)-1):

    temp_token_set = split_words(data_set[i+1])
    temp_corpus = r_word(temp_token_set)

    #could stem the set here
    document.append(temp_corpus)

write_data = [['Id','Category']]

for i in range(len(document)):

    P_Cn = P_n
    p_Cp = P_p

    for word in document[i]: #tokenized corpus
        if model.has_key(word):
            P_Cn += math.log((model[word][0] + 1)/(sum_Tn + B))
            p_Cp += math.log((model[word][1] + 1)/(sum_Tp + B))
        else:
            P_Cn += math.log(1/(sum_Tn + B))
            p_Cp += math.log(1/(sum_Tp + B))

    if P_Cn > p_Cp: #predict 0
        write_temp = [i+1,0]

    else: #predict 1

        write_temp = [i+1,1]

    write_data.append(write_temp)

file = open(prediction_file,"w")
#file = open('prediction_file.csv',"w")
write = csv.writer(file)
write.writerows(write_data)
file.close()
print 'prediction done'
