from django.shortcuts import render
from django.http import HttpResponse

from .forms import *

import re
import numpy as np
import pandas
import os

def readData(file):
    with open(file) as file:
        content = file.read()
    return content

def cleanString(text):
    data = []
    content_lower = text.lower()
    for word in content_lower.split():
        cleanContent = re.sub('["()&+,./;“”\"]', '', word)
        data.append(cleanContent)

    unqWord = sorted(set(data))
    unqWord = list(unqWord)

    pandas.DataFrame(unqWord).to_csv('collectionWord.csv', index=False, header=False)

    return data

def bigramModel(data):
    bigramList = []
    bigramFreq = {}
    unigramFreq = {}

    for i in range(len(data)):
        if i < len(data) - 1:
            bigramList.append((data[i], data[i + 1]))
            if (data[i], data[i + 1]) in bigramFreq:
                bigramFreq[(data[i], data[i + 1])] += 1
            else:
                bigramFreq[(data[i], data[i + 1])] = 1
        if data[i] in unigramFreq:
            unigramFreq[data[i]] += 1
        else:
            unigramFreq[data[i]] = 1

    return bigramList, bigramFreq, unigramFreq

def probBigram(bigramList, bigramFreq, unigramFreq):
    probList = {}
    for bigramNew in bigramList:
        word1 = bigramNew[0]
        probList[bigramNew] = (bigramFreq.get(bigramNew) / (unigramFreq.get(word1)))

    pandas.Series(probList).to_csv('ProbBigram.csv', header=False)

    return probList

def addOneSmothing(bigramList, bigramFreq, unigramFreq):
    ProbList = {}
    cStar = {}

    for bigram in bigramList:
        word1 = bigram[0]
        ProbList[bigram] = (bigramFreq.get(bigram) + 1) / (unigramFreq.get(word1) + len(unigramFreq))
        cStar[bigram] = (bigramFreq[bigram] + 1) * unigramFreq[word1] / (unigramFreq[word1] + len(unigramFreq))
    pandas.Series(ProbList).to_csv('ProbBigramAddOneSmothing.csv', header=False)

    return ProbList, cStar

def inputTeks(kata):

    word = pandas.read_csv('collectionWord.csv', names=['words'])['words'].tolist()
    probBigram = pandas.read_csv('ProbBigramAddOneSmothing.csv', header=None).values.tolist()
    
    kata = kata.lower()


    if (kata in word):

        r = []

        for row in probBigram:
            if kata == row[0]:
                r.append((row[2], row[1]))

        max_prob = max(r)
        return max_prob[1]
    else:
        return ('kata tidak ada atau yang diinputkan bukan kata')

def inputKalimat(kalimat):
    inp = kalimat
    inp = inp.lower()

    inputList = []
    outputProb1 = 1
    outputProb2 = 1

    for i in range(len(inp.split()) - 1):
        inputList.append((inp.split()[i], inp.split()[i + 1]))

    # Model Bigram

    for i in range(len(inputList)):
        if inputList[i] in bigramProb:
            outputProb1 *= bigramProb[inputList[i]]
        else:
            outputProb1 *= 0

    # Add One Smoothing

    for i in range(len(inputList)):
        if inputList[i] in bigramAddOne:
            outputProb2 *= bigramAddOne[inputList[i]]
        else:
            if inputList[i][0] not in unigramFreq:
                unigramFreq[inputList[i][0]] = 1
            prob = (1) / (unigramFreq[inputList[i][0]] + len(unigramFreq))
            addOneCStar = 1 * unigramFreq[inputList[i][0]] / (
                    unigramFreq[inputList[i][0]] + len(unigramFreq))
            outputProb2 *= prob

    # Perplexity
    if len(inputList) == 0:
        perplexity = 'error'
    else:
        perplexity = (1 / outputProb2)**(1 / len(inputList))
        
    return [inputList, perplexity]

module_dir = os.path.dirname(__file__)
file_path = os.path.join(module_dir, 'Artikel.txt')
text_file = open(file_path , 'r')
text = text_file.read()
text = cleanString(text)
bigramList, bigramFreq, unigramFreq = bigramModel(text)
bigramProb = probBigram(bigramList, bigramFreq, unigramFreq)
bigramAddOne, addOneCstar = addOneSmothing(bigramList,bigramFreq,unigramFreq)

# Create your views here.
def Home(request):
    return render(request, 'lm/home.html')

def Perplex(request):
    if request.method == 'POST':
        form = KalimatForm(request.POST)
        if form.is_valid():
            bigram = inputKalimat(form.cleaned_data.get('kalimat'))
            return render(request, 'lm/perplex.html', {'form': form, 'bigram': bigram[0], 'perplex': bigram[1]})
    else:
        form = KalimatForm(request.POST)
        return render(request, 'lm/perplex.html', {'form': form})

def Word(request):
    if request.method == 'POST':
        form = KataForm(request.POST)
        if form.is_valid():
            prediksi = inputTeks(form.cleaned_data.get('kata'))
            return render(request, 'lm/word_predict.html', {'form': form, 'prediksi': prediksi})
    else:
        form = KataForm(request.POST)
        return render(request, 'lm/word_predict.html', {'form': form})