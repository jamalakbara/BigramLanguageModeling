import re
import numpy as np
import pandas

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

def inputTeks():

    word = pandas.read_csv('collectionWord.csv', names=['words'])['words'].tolist()
    probBigram = pandas.read_csv('ProbBigramAddOneSmothing.csv', header=None).values.tolist()

    kata = ''
    while (kata != '9999' or ''):
        kata = input("Masukkan kata: ")
        kata = kata.lower()


        if (kata in word):

            r = []
            for row in probBigram:
                if kata == row[0]:
                    r.append((row[2], row[1]))
            max_prob = max(r)
            print('Kata Selanjutnya: ' + max_prob[1] + '\n')
        else:
            print('kata tidak ada')

def inputKalimat():
    try:
        inp = ''
        while (inp != '9999'):
            inp = input('Masukan Kalimat: ')
            inp = inp.lower()

            inputList = []
            outputProb1 = 1
            outputProb2 = 1

            if (inp == '9999' or inp == ''):
                break

            for i in range(len(inp.split()) - 1):
                inputList.append((inp.split()[i], inp.split()[i + 1]))
            print(inputList) 

            # ------------------------------ Bigram Model -------------------------------------

            print('Bigram\t\t\t\t' + 'Count\t\t\t\t' + 'Probability\n')
            for i in range(len(inputList)):
                if inputList[i] in bigramProb:
                    print(str(inputList[i]) + '\t\t' + str(bigramFreq[inputList[i]]) + '\t\t' + str(
                        bigramProb[inputList[i]]))
                    outputProb1 *= bigramProb[inputList[i]]
                else:
                    print(str(inputList[i]) + '\t\t\t' + str(0) + '\t\t\t' + str(0))
                    outputProb1 *= 0

            print('\n' + 'Bigram Probability Probablility = ' + str(outputProb1) + '\n')

            # ------------------------------- Add One Smoothing ---------------------------------

            print('Bigram\t\t\t\t' + 'Probability\n')
            for i in range(len(inputList)):
                if inputList[i] in bigramAddOne:
                    print(str(inputList[i]) + '\t\t' + str(addOneCstar[inputList[i]]) + '\t\t' + str(
                        bigramAddOne[inputList[i]]))
                    outputProb2 *= bigramAddOne[inputList[i]]
                else:
                    if inputList[i][0] not in unigramFreq:
                        unigramFreq[inputList[i][0]] = 1
                    prob = (1) / (unigramFreq[inputList[i][0]] + len(unigramFreq))
                    addOneCStar = 1 * unigramFreq[inputList[i][0]] / (
                            unigramFreq[inputList[i][0]] + len(unigramFreq))
                    outputProb2 *= prob
                    print(str(inputList[i]) + '\t' + str(addOneCStar) + '\t' + str(prob))

            print('\n' + 'Add One Probablility = ' + str(outputProb2) + '\n')

            # ------------------------------- Perplexity -------------------------------------------
            perplexity = (1 / outputProb2)**(1 / len(inputList))
            print('Perplexity : ' + str(perplexity))

    except ZeroDivisionError as detail:
        print('Handling run-time error:', detail)
    except:
        print(' ')


if __name__ == '__main__':
    text = readData("Artikel.txt")
    text = cleanString(text)
    bigramList, bigramFreq, unigramFreq = bigramModel(text)
    bigramProb = probBigram(bigramList, bigramFreq, unigramFreq)
    bigramAddOne, addOneCstar = addOneSmothing(bigramList,bigramFreq,unigramFreq)

    inputTeks()
    inputKalimat()

