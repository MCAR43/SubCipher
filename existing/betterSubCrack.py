#!/usr/bin/env python
#Mark Anderson
#CS3600
#Homework 1

#imports
from sys import argv
import re
import pprint
import time
import wordPatterns
import simpleSubCipher
#I/O#infile = open(argv[0], "r")
#outfile = open(argv[1], "w")


digraphs = ['th','er','on','an','re','he','in','ed','nd','ha','at','en','es','of','or','nt',
            'ea', 'ti', 'it', 'st','io','le','is','ou','ar','as','de','rt','ve']

trigraphs = ['the','and','tha','ent','ion','tio','for','nde','has','nce','edt','tis','oft']
doubles = ['s','e','t','f','l','m','o']
oneLetterWords = ['a','i']
twoLetterWords = ['of', 'to', 'in', 'it', 'is', 'be', 'as', 'at', 'so', 'we', 'he', 'by', 'or', 'on', 'do', 'if', 'me', 'my', 'up', 'an', 'go', 'no', 'us','am']



ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ .'
goalMap = {'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [], 'H': [], 'I': [], 'J': [], 'K': [], 'L': [],
            'M': [], 'N': [], 'O': [], 'P': [], 'Q': [], 'R': [], 'S': [], 'T': [], 'U': [], 'V': [], 'W': [], 'X': [],
            'Y': [], 'Z': [], ' ': [], '.': []}

englishLetterFreq = {' ': 30.0,'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33,
                     'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41,
                     'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29, 'V': 0.98,
                     'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07, '.': 0.14}
solvedword = 'keloirkobarosg'
#loirkobarots
def main():
    pp = pprint.PrettyPrinter(indent=4)
    inputtext = open("inputs/outfile.txt")
    message = inputtext.read()

    #give the program a head start with an initial decryption using message frequency
    messageFrequency = improvedLetterFreq(message)
    initialSolution = transposeAlphabets(messageFrequency)
    message = translateMessage(initialSolution, message)


    hackit(message)








def wordPattern(word):
    if len(word) > 2:
        index = 0
        pattern = ""
        letterMap = {}
        for letter in word:
            upper = letter.upper()
            if upper not in letterMap:
                letterMap[upper] = index
                pattern += str(letterMap[upper]) + "."
                index += 1
            else:
                pattern += str(letterMap[upper]) + "."
        return pattern[:-1]
    #unelegant way to remove the trailing "."


def createSolutionSet(cipherword):
    blankMap = alphabetMap()
    pattern = wordPattern(cipherword)
    potentialWords = wordPatterns.allPatterns[pattern]
    for word in potentialWords:
        index = 0
        for letter in word:
            if letter not in blankMap[cipherword[index].upper()]:
                blankMap[cipherword[index].upper()].append(letter)
            index+=1

    return blankMap


def removeSolved(currentKey):
    loopAgain = True
    while loopAgain:
        loopAgain = False
        solvedLetters = []
        for letter in ALPHABET:
            letter=letter.upper()
            print(currentKey[letter])
            if len(currentKey[letter] == 1):
                solvedLetters.append(currentKey[letter][0])

        for letter in ALPHABET:
            letter = letter.upper()
            for s in solvedLetters:
                if len(currentKey[letter]) != 1 and s in currentKey[letter]:
                    currentKey[letter].remove(s)
                    if len(currentKey[letter] == 1):
                        loopAgain = True

    return currentKey

def intersect(keyA, keyB):
    intersectedDict = alphabetMap()
    for letter in ALPHABET:
        upper = letter.upper()
        if keyA[upper] == []:
            intersectedDict[upper] = keyB[upper]
        elif keyB[upper] == []:
            intersectedDict[upper] = keyA[upper]
        else:
            for item in keyA[upper]:
                if item in keyB[upper]:
                    intersectedDict[upper].append(item)

    return intersectedDict

def improvedLetterFreq(message):
    tempDict = {}
    for letter in message:
        print(letter)
        key = letter.upper()
        if key in ALPHABET:
            try:
                tempDict[key] += 1
            except KeyError:
                tempDict[key] = 1

    for key in tempDict:
        tempDict[key] = (tempDict[key] / len(message))


    return sorted(tempDict, key=tempDict.get, reverse=True)


def freqMap():
    blankFreqMap = {'A': 0.0, 'B': 0.0, 'C': 0.0, 'D': 0.0, 'E': 0.0, 'F': 0.0, 'G': 0.0, 'H': 0.0, 'I': 0.0, 'J': 0.0,
                    'K': 0.0, 'L': 0.0,
                    'M': 0.0, 'N': 0.0, 'O': 0.0, 'P': 0.0, 'Q': 0.0, 'R': 0.0, 'S': 0.0, 'T': 0.0, 'U': 0.0, 'V': 0.0,
                    'W': 0.0, 'X': 0.0,
                    'Y': 0.0, 'Z': 0.0, ' ': 0.0, '.': 0.0}
    return blankFreqMap

def alphabetMap():
    map  = {'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [], 'H': [], 'I': [], 'J': [], 'K': [], 'L': [],
            'M': [], 'N': [], 'O': [], 'P': [], 'Q': [], 'R': [], 'S': [], 'T': [], 'U': [], 'V': [], 'W': [], 'X': [],
            'Y': [], 'Z': [], ' ': [], '.': []}

    return map


def transposeAlphabets(alphabet):
    counter = 0
    map = alphabetMap()
    for key in englishLetterFreq:
        map[key].append(alphabet[counter])
        counter += 1
    return map
    #return {v:k for k,v in goalMap.items()}


def translateMessage(key, ciphertext):
    generatedKey = ""
    for item in key:
        generatedKey += key[item][0]

    print(generatedKey)
    return simpleSubCipher.decryptMessage(generatedKey, ciphertext)

def hackit(message):
    intersectMap = alphabetMap()
    for word in message.split():
        map = alphabetMap()
        pattern = wordPattern(word)
        try:
            wordList = wordPatterns.allPatterns[pattern]
        except KeyError:
            wordList = None

        if wordList is not None:
            for decryption in wordList:
                print("Potential: " + decryption)
                index = 0
                for letter in decryption:
                    try:
                        if letter not in map[word[index].upper()]:
                            map[word[index].upper()].append(letter)
                        index += 1
                    except KeyError:
                        index +=1

        intersectMap = intersect(intersectMap, map)
        intersectMap = removeSolved(intersectMap)





if __name__ == '__main__':
    main()


    '''
        for word in message.split():
        if len(word) == 2:
            if word in twoLetter:
                twoLetter[word] += 1
            else:
                twoLetter[word] = 1
        elif len(word) == 3:
            if word in threeLetter:
                threeLetter[word] += 1
            else:
                threeLetter[word] = 1
    '''