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

#CONSTANTS
MINIMUM_WORD_LENGTH = 2
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ .'
englishLetterFreq = {' ': 30.0,'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33,
                     'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41,
                     'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29, 'V': 0.98,
                     'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07, '.': 0.14}
pp = pprint.PrettyPrinter(indent=2)


def blankMap():
    map = {'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [], 'H': [], 'I': [], 'J': [], 'K': [], 'L': [],
           'M': [], 'N': [], 'O': [], 'P': [], 'Q': [], 'R': [], 'S': [], 'T': [], 'U': [], 'V': [], 'W': [], 'X': [],
           'Y': [], 'Z': [], ' ': [], '.': []}

    return map

def frequencyAnalysis(message):
    tempDict = {}
    tempKey = blankMap()
    counter = 0
    for letter in message:
        key = letter.upper()
        if key in ALPHABET:
            try:
                tempDict[key] += 1
            except KeyError:
                tempDict[key] = 1

    for key in tempDict:
        tempDict[key] = (tempDict[key] / len(message))

    for letter in ALPHABET:
        if letter not in tempDict.keys():
            tempDict[letter] = 0


    sortedList = sorted(tempDict, key=tempDict.get, reverse=True)

    for key in englishLetterFreq:
        tempKey[sortedList[counter]].append(key)
        counter+=1

    return translateText(message, tempKey), tempKey

def generateKey(key):
    generatedKey = ""
    for item in key:
        generatedKey += key[item][0]

    return generatedKey

def translateText(message, key):
    stringKey = generateKey(key)
    print(stringKey)
    return simpleSubCipher.decryptMessage(stringKey, message)

def wordPattern(word):
    index = 0
    pattern = ""
    letterMap = {}
    for letter in word:
        if letter.upper() in ALPHABET:
            upper = letter.upper()
            if upper not in letterMap:
                letterMap[upper] = index
                pattern += str(letterMap[upper]) + "."
                index += 1
            else:
                pattern += str(letterMap[upper]) + "."

        #unelegant way of slicing off trailing period
    return pattern[:-1]

def intersect(keyA, keyB):
    intersectedDict = blankMap()
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

def mappingFromPattern(pattern, cipherword):
    map = blankMap()
    try:
        potentialWords = wordPatterns.allPatterns[pattern]
    except KeyError:
        potentialWords = None

    if potentialWords is None:
        return map

    for word in potentialWords:
        map = createMap(map, cipherword, word)

    return map

def createMap(map, cipherword, potentialword):
    cipherword = cipherword.strip(',=-"\'!?:;')
    for i in range(0, len(cipherword)):
        cipherIndex = cipherword[i].upper()
        if potentialword[i] not in map[cipherIndex]:
            map[cipherIndex].append(potentialword[i])

    return map

def removeSolvedLetters(key):
    loopAgain = True
    while loopAgain:
        loopAgain = False
        singleMappedLetters = []
        for letter in ALPHABET:
            letter = letter.upper()
            if len(key[letter]) == 1:
                singleMappedLetters.append(key[letter][0])


        for cipherLetter in ALPHABET:
            for solved in singleMappedLetters:
                if len(key[cipherLetter]) != 1 and solved in key[cipherLetter]:
                    key[cipherLetter].remove(solved)
                    if len(key[cipherLetter]) == 1:
                        loopAgain = True

    return key

def checkIfSolved(solutionKey):
    for key in solutionKey:
        if solutionKey[key] == []:
            return False

    return True

def addToFinalKey(bestFit, mapping):
    for key in mapping:
        if len(mapping[key]) == 1:
            bestFit[key] = mapping[key]

    return bestFit




def main():
    counter = 0
    inputtext = open("inputs/testing.txt")
    message = inputtext.read()
    message, initKey = frequencyAnalysis(message)
    print(ALPHABET)
    print(generateKey(initKey))
    print(message)
    bestFit = blankMap()
    intMap = blankMap()
    for ciphWord in message.split():
        found = re.findall('^[A-Za-z0-9.]+$', ciphWord)
        validCipherWord = bool(found) and found[0] == ciphWord
        counter+=1
        if len(ciphWord) > 2 and validCipherWord:
            pattern = wordPattern(ciphWord)
            mapFromPattern = mappingFromPattern(pattern, ciphWord)
            intMap = intersect(intMap, mapFromPattern)
            bestFit = addToFinalKey(bestFit, intMap)
            print(bestFit)





if __name__ == '__main__':
    main()
