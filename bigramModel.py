import re
import numpy as np
import pandas

def readData(file):                     #fungsi untuk membuka/membaca file dari luar
    with open(file) as file:            #membuka file dan menamai file
        content = file.read()           #men-assign data yang ada di file ke variabel content
    return content                      #content sebagai return value

def cleanString(text):                  #fungsi untuk mengecilkan huruf dan memisahkan kata-katanya menjadi token-token
    data = []
    content_lower = text.lower()        #mengecilkan huruf pada teks
    for word in content_lower.split():  #perulangan sebanyak teks yang sudah dikecilkan dan di split menjadi token
        cleanContent = re.sub('["()&+,./;“”\"]', '', word)  #menghilangkan tanda baca dan tanda lainya yang tidak berkaitan menggunakan re
        data.append(cleanContent)       #menyimpan kata ke list data

    unqWord = sorted(set(data))         #mensorting data dan mengambil yang uniknya saja
    unqWord = list(unqWord)             #mengembalikan menjadi list kembali

    pandas.DataFrame(unqWord).to_csv('collectionWord.csv', index=False, header=False) #menyimpan ke dalam csv menggunakan pandas

    return data                         #variable data sebagai return value

def bigramModel(data):                  #fungsi bigram modelnya
    bigramList = []                     #bigramList merupakan list yang akan menyimpan kumpulan bigram
    bigramFreq = {}                     #bigramFreq dan ingramFreq, array yang menyimpan jumlah bigram dan unigram yang ada
    unigramFreq = {}

    for i in range(len(data)):
        if i < len(data) - 1:
            bigramList.append((data[i], data[i + 1]))       #menyimpan bigram(i, i+1) ke bigramList
            if (data[i], data[i + 1]) in bigramFreq:        #ketika bigram sudah ada di bigramFreq counting akan bertambah 1 (+1)
                bigramFreq[(data[i], data[i + 1])] += 1
            else:
                bigramFreq[(data[i], data[i + 1])] = 1      #ketika belum ada counting akan = 1
        if data[i] in unigramFreq:
            unigramFreq[data[i]] += 1                       #unigramFreq sama seperti bigramFreq
        else:                                               #fungsinya nanti dalam perhitungan probabilitas bigramnya
            unigramFreq[data[i]] = 1

    return bigramList, bigramFreq, unigramFreq

def probBigram(bigramList, bigramFreq, unigramFreq):
    probList = {}                                           #array untuk menyimpan bigram dan probabilitas masing masingnya
    for bigramNew in bigramList:
        word1 = bigramNew[0]                                #men-assign nilai Ci
        probList[bigramNew] = (bigramFreq.get(bigramNew) / (unigramFreq.get(word1)))    #P() = P(Ci,Ci+1)/P(Ci)

    pandas.Series(probList).to_csv('ProbBigram.csv', header=False)                      #menyimpan data probList ke csv

    return probList

def addOneSmothing(bigramList, bigramFreq, unigramFreq):
    ProbList = {}       #array menyimpan bigram dan probabilitas
    cStar = {}          #array untuk menyimpan perhitungan mencari count pada addOne Smothing

    for bigram in bigramList:
        word1 = bigram[0]
        ProbList[bigram] = (bigramFreq.get(bigram) + 1) / (unigramFreq.get(word1) + len(unigramFreq))           #perhitungan P = (Ci + 1)/N + V
        cStar[bigram] = (bigramFreq[bigram] + 1) * unigramFreq[word1] / (unigramFreq[word1] + len(unigramFreq)) #cStar = (Ci + 1)*(N/N+V)
                                                                                                                #N merupakan unigramFreq dan V merupakan vocab dari ungram
    pandas.Series(ProbList).to_csv('ProbBigramAddOneSmothing.csv', header=False)

    return ProbList, cStar

def inputTeks():

    word = pandas.read_csv('collectionWord.csv', names=['words'])['words'].tolist()             #membaca data dari csv
    probBigram = pandas.read_csv('ProbBigramAddOneSmothing.csv', header=None).values.tolist()   #membaca data dari csv

    kata = ''
    while (kata != '9999' or ''):
        print('Pengecekan Prediksi kemunculan kata selanjutnya')
        kata = input("Masukkan kata (9999 untuk selesai): ")     #untuk dapat menginputkan kata (ketik 9999 untuk selesai)
        kata = kata.lower()                 #mengecilkan kata yang di inputkan


        if (kata in word):

            r = []                              #variable untuk menyimpan list kata selanjutnya

            for row in probBigram:
                if kata == row[0]:              #ketika kata yang diinputkan sama dengan kata pada baris 1 di file csv
                    r.append((row[2], row[1]))  #memasukan nilai ke list r

            max_prob = max(r)                   #mencari probabilitas terbesarnya pada list r
            print('Kata Selanjutnya: ' + max_prob[1] + '\n')        #menampilkan kata selanjutnya
        else:
            print('kata tidak ada atau yang diinputkan bukan kata') #ketika kata tidak ada atau yang diinputkan bukan kata
            print('----------------------------------------------')

def inputKalimat():
    try:
        inp = ''
        while (inp != '9999'):
            print('pengecekan probabilitas dan perplexity')
            inp = input('Masukan Kalimat (9999 untuk selesai): ')        #untuk dapat menginputkan kalimat (ketik 9999 untuk selesai)
            inp = inp.lower()                       #mengecilkan kalimat yang di inputkan

            inputList = []                          #list untuk menyimpan bigram yang diinputkan
            outputProb1 = 1                         #outProb merupakan inisiasi awal diisi 1.0
            outputProb2 = 1

            if (inp == '9999' or inp == ''):
                break

            for i in range(len(inp.split()) - 1):
                inputList.append((inp.split()[i], inp.split()[i + 1]))      #memasukan bigram dari input ke dalam inputList
            print(inputList)

            # Model Bigrma

            print('Bigram\t\t\t\t' + 'Count\t\t\t\t' + 'Probability\n')
            for i in range(len(inputList)):                                 #perulangan sebanyak banyak data pada inputList
                if inputList[i] in bigramProb:                              #jika inputList ada di bigram maka
                    print(str(inputList[i]) + '\t\t' + str(bigramFreq[inputList[i]]) + '\t\t' + str(
                        bigramProb[inputList[i]]))                                                      #menampilkan bigram, count, dan probabilitas
                    outputProb1 *= bigramProb[inputList[i]]                                             #pada bigram model dan outputProb1 = probabiliti(1) * ....* probabiliti(n)
                else:
                    print(str(inputList[i]) + '\t\t\t' + str(0) + '\t\t\t' + str(0))
                    outputProb1 *= 0                                                                    #akan menghasilkan probabilitas 0 ketika tidak ada bigram yang di corpus/csv

            print('\n' + 'Bigram Probability Probablility = ' + str(outputProb1) + '\n')                #menapilkna output bigram model

            # Add One Smoothing

            print('Bigram\t\t\t\t' + 'Count\t\t\t\t' + 'Probability\n')
            for i in range(len(inputList)):
                if inputList[i] in bigramAddOne:                                                        #jika inputList ada di bigram maka
                    print(str(inputList[i]) + '\t\t' + str(addOneCstar[inputList[i]]) + '\t\t' + str(
                        bigramAddOne[inputList[i]]))                                                    #menampilkan bigram, count, dan probabilitas pada AddOne Smoothing
                    outputProb2 *= bigramAddOne[inputList[i]]                                           #outputProb2 = probabiliti(1) * ....* probabiliti(n)
                else:
                    if inputList[i][0] not in unigramFreq:                                              #jika inputList tidak ada unigram/tidak memiliki bigram maka akan melakukan perhitungan
                        unigramFreq[inputList[i][0]] = 1
                    prob = (1) / (unigramFreq[inputList[i][0]] + len(unigramFreq))                      #perhitungan prob = (1/N+V)
                    addOneCStar = 1 * unigramFreq[inputList[i][0]] / (
                            unigramFreq[inputList[i][0]] + len(unigramFreq))                            #perhitungan Count pada AddOne = (1 * N)/(N + V)
                    outputProb2 *= prob                                                                 #outputProb2 = probabiliti(1) * ....* probabiliti(n)
                    print(str(inputList[i]) + '\t' + str(addOneCStar) + '\t' + str(prob))               #menapilkna output bigram AddOne

            print('\n' + 'Add One Probablility = ' + str(outputProb2) + '\n')

            # Perplexity
            perplexity = (1 / outputProb2)**(1 / len(inputList))                                        #perhitungan perplexity = (1/P)pangkat(1/n) = (akar n dari 1/n)
            print('Perplexity : ' + str(perplexity))
            print('----------------------------------------------')

    except ZeroDivisionError as detail:
        print('Handling run-time error:', detail)                                                       #melakukan handling error apabila menemukan error tidak bissa dibagi 0
    except:
        print(' ')


if __name__ == '__main__':                                                                              #main programnya
    text = readData("Artikel.txt")                                                                      #memanggil fungsi readData dan memasukan file .txt
    text = cleanString(text)                                                                            #melakukan pengecilan huruf dan memisahkan menjadi token
    bigramList, bigramFreq, unigramFreq = bigramModel(text)                                             #melakukan assign value yang didapat dari fungsi bigramModel dengan parameter text
    bigramProb = probBigram(bigramList, bigramFreq, unigramFreq)                                        #melakukan assign value yang didapat dari fungsi probBigram dengan parameter variable sebelumnya
    bigramAddOne, addOneCstar = addOneSmothing(bigramList,bigramFreq,unigramFreq)                       #melakukan assign value yang didapat dari fungsi AddOneSmothing dengan parameter variable sebelumnya

    i = ''
    while(i != '0'):
        print('---------------------')
        print('1. Prediksi kata')
        print('2. Kalimat')
        print('0. keluar')
        print('---------------------')
        i = input('Masukan Pilihan: ')
        if(i == '1'):
            inputTeks()                                             #fungsi inputTeks untuk pengecekan kata selanjutnya dari input kata
        if(i == '2'):
            inputKalimat()                                          #fungis inputKalimat untukpengecekan probabilitas dan perplexity dari input kalimat




