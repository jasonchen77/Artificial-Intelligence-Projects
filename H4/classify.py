'''
Created on Oct 2, 2020

@author: Jason Chen
'''

from os import listdir
from os import path
import numpy as np

def create_bow(vocab, filepath):
    """ Create a single dictionary for the data
        Note: label may be None
    """
    bow = {}
    # TODO: add your code here
    readFile = open(filepath, "r")
    for rf in readFile:
        word = rf.strip()
        if word in vocab:
            if word not in bow:
                bow[word] = 1
            else:
                bow[word] += 1
        else:
            if None not in bow:
                bow[None] = 1
            else:
                bow[None] += 1
    readFile.close()

    return bow

def load_training_data(vocab, directory):
    """ Create the list of dictionaries """
    dataset = []
    # TODO: add your code here
    yearDir = listdir(directory)
    for yd in yearDir:
        filesSubDir = listdir(path.join(directory, yd))
        for fsd in filesSubDir:
            fileName = path.join(directory, yd, fsd)
            bagsOfWords = create_bow(vocab, fileName)
            dataset.append({"label": yd, "bow": bagsOfWords})


    return dataset

def create_vocabulary(directory, cutoff):
    """ Create a vocabulary from the training directory
        return a sorted vocabulary list
    """

    vocab = []
    # TODO: add your code here
    vocabUnsorted = []
    wordList = {}
    yearDir = listdir(directory)
    for yd in yearDir:
        filesSubDir = listdir(path.join(directory, yd))
        for fsd in filesSubDir:
            fileName = path.join(directory, yd, fsd)
            readFile = open(fileName, "r")
            for rf in readFile:
                word = rf.strip()
                if word not in wordList:
                    wordList[word] = 1
                else:
                    wordList[word] = wordList[word] + 1
            readFile.close()
            
    for wl in wordList:
        if wordList[wl] >= cutoff:
            vocabUnsorted.append(wl)
    
    vocab = sorted(vocabUnsorted)
    
    return vocab

def prior(training_data, label_list):
    """ return the prior probability of the label in the training set
        => frequency of DOCUMENTS
    """

    smooth = 1 # smoothing factor
    logprob = {}
    # TODO: add your code here
    fileCountByYear = {label_list[0]: 0, 
                       label_list[1]: 0}
    for td in training_data:
        if td["label"] == label_list[0]:
            fileCountByYear[label_list[0]] += 1
        if td["label"] == label_list[1]:
            fileCountByYear[label_list[1]] += 1
    pr0 = (fileCountByYear[label_list[0]] + smooth) / (len(training_data) + 2)
    pr1 = (fileCountByYear[label_list[1]] + smooth) / (len(training_data) + 2)
    pr0log = np.log(pr0)
    pr1log = np.log(pr1)
    logprob = {label_list[0]: pr0log, 
               label_list[1]: pr1log}


    return logprob

def p_word_given_label(vocab, training_data, label):
    """ return the class conditional probability of label over all words, with smoothing """
    
    smooth = 1 # smoothing factor
    word_prob = {}
    # TODO: add your code here
    vocabCopy = vocab.copy()
    vocabCopy.append(None)
    for v in vocabCopy:
        wordCount = 0
        allWordCount = 0
        for td in training_data:
            if td["label"] == label:
                for awid in td["bow"]:
                    allWordCount += td["bow"][awid]
                if v in td["bow"]:
                    wordCount += td["bow"][v]
        pWord = np.log((wordCount + smooth) / (allWordCount + len(vocabCopy)))
        word_prob[v] = pWord
    
    
    return word_prob

    
##################################################################################
def train(training_directory, cutoff):
    """ return a dictionary formatted as follows:
            {
             'vocabulary': <the training set vocabulary>,
             'log prior': <the output of prior()>,
             'log p(w|y=2016)': <the output of p_word_given_label() for 2016>,
             'log p(w|y=2020)': <the output of p_word_given_label() for 2020>
            }
    """
    retval = {}
    # TODO: add your code here
    vocabList = create_vocabulary(training_directory, cutoff)
    retval["vocabulary"] = vocabList
    trainingData = load_training_data(vocabList, training_directory)
    logPrior = prior(trainingData, ['2020', '2016'])
    retval["log prior"] = logPrior
    logP2016 = p_word_given_label(vocabList, trainingData, '2016')
    logP2020 = p_word_given_label(vocabList, trainingData, '2020')
    retval["log p(w|y=2016)"] = logP2016
    retval["log p(w|y=2020)"] = logP2020


    return retval


def classify(model, filepath):
    """ return a dictionary formatted as follows:
            {
             'predicted y': <'2016' or '2020'>, 
             'log p(y=2016|x)': <log probability of 2016 label for the document>, 
             'log p(y=2020|x)': <log probability of 2020 label for the document>
            }
    """
    retval = {}
    # TODO: add your code here
    vocabList = model["vocabulary"]
    inputBagOfWords = create_bow(vocabList, filepath)
    logXp2016 = 0
    logXp2020 = 0
    for ibow in inputBagOfWords:
        if ibow in model["log p(w|y=2016)"]:
            logXp2016 += (inputBagOfWords[ibow] * model["log p(w|y=2016)"][ibow])
        if ibow in model["log p(w|y=2020)"]:
            logXp2020 += (inputBagOfWords[ibow] * model["log p(w|y=2020)"][ibow])  
          
    logXp2016Final = logXp2016 + model["log prior"]["2016"]
    logXp2020Final = logXp2020 + model["log prior"]["2020"]
    
    if logXp2016Final > logXp2020Final:
        pY = '2016'
    else:
        pY = '2020'
    
    retval["predicted y"] = pY
    retval["log p(y=2016|x)"] = logXp2016Final
    retval["log p(y=2020|x)"] = logXp2020Final
           

    return retval

