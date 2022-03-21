from flask import Flask, request, render_template, make_response
from flask_table import Table, Col
from flask import Markup


app = Flask(__name__)


@app.route('/')#initial GET route
def main():
    return render_template('index.html', title = "scrabble3000")#renders

def getWords(language, inputLetters, givenWord):#takes in full dictionary and user input to return a list of words that can be made.
    ogDictionary=createDict(language)#will only be used to make dictionary{}
    dictionary={}#made to only contain letters that are given--MORE EFFICIENT
    s=givenWord
    for l in inputLetters:
        s+=l
    for let in s:#Add latter given word in case there are words that start with those letters
        dictionary[let] = actualDictionary[let]

    result = []
    if(givenWord==""):#if there is no given woord
        for letter in dictionary:
            for dictWord in dictionary[letter]:
                #Loops through each word while it is using valid letters
                #Reset letters each time a new word is checked
                letters = inputLetters.copy()
                invalid = False
                j = 0

                while(not invalid and j < len(dictWord)):
                    if(dictWord[j] not in letters):
                #Checks if there is a wildcard left
                        if("*" in letters):
                            letters.remove("*")
                        else:
                            invalid = True
                    else:
                        letters.remove(dictWord[j])
                    j += 1

        #Adds the word to the list if it never used invalid characters
                if(not invalid):
                    result[dictWord]=sub

        valueDict={}
        lenDict={}
        for w in result:
            if len(w)>1:
                value=addLetters(w)-result[w]
                valueDict[w]=value
                length=len(w)
                lenDict[w]=length

        return valueDict, lenDict

    else:
        result={}
        # result = [givenWord]
        #Loops through the whole dictionary. 1 is the length of the dictionary
        for letter in dictionary:
            for dictWord in dictionary[letter]:
            #Loops through each word while it is using valid letters
            #Reset letters each time a new word is checked
                letters = inputLetters.copy()
                invalid = False
                j = 0

            #Finds the index of the given word of the current dictWord
                indexOfDictWord = dictWord.find(givenWord)
                if(indexOfDictWord == -1):
                    invalid = True

                while(not invalid and j < len(dictWord)):
                #If the next few letters of a word are the given word
                #Skip the next few letters
                    if(j == indexOfDictWord):
                        j += len(givenWord)
                    else:
                        if(dictWord[j] not in letters):
                        #Checks if there is a wildcard left
                            if("*" in letters):
                                letters.remove("*")
                            else:
                                invalid = True
                        else:
                            letters.remove(dictWord[j])
                        j += 1

            #Adds the word to the list if it never used invalid characters
                if(not invalid):
                    result += [dictWord]

        result.remove(givenWord)

    if(result == []):
        result = ["**Nothing Found**"]

        # words=""
    valueDict={}
    lenDict={}
    for word in result:
        # words=words+w+" "
        value=addLetterValues(word)
        valueDict[word]=value
        length=len(word)
        lenDict[word]=length


    return valueDict, lenDict


def createDictDict():
    dictDict={}
    letters="abcdefghijklmnopqrstuvwxyzåé"
    for let in letters:
        dictDict[let]=set()
    return dictDict


def createDict(language):
    dictDict=createDictDict()
    lines=""
    if language=="American":
        text_file = open("./dictionaries/american-english", "r")
        lines = text_file.readlines()
        text_file.close()
    elif language=="British":
        text_file = open("./dictionaries/british-english", "r")
        lines = text_file.readlines()
        text_file.close()
    for word in lines:
        word = word.strip('\n')
        word=word.lower()
        if "'s" in word:
            #no addo
            pass
        else:
            #add to dict
            firstlet=word[0:1]
            dictDict[firstlet].add(word)
    return dictDict


def addLetterValues(word):
    s = 0
    for i in word:
        s += letterValues[i]
    return s
    

def tableSorted(sortByDic):
    return sorted(sortByDic.items(), key=lambda kv:(kv[1], kv[0]), reverse=True)

def makeValueSortedTable(valueDic, lengthDic):
    master=""
    for i in tableSorted(valueDic):
        master+='''<tr>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
        </tr>'''.format(i[0], str(lengthDic[i[0]]), str(i[1]))#format(i, str(length), str(value))
    sortedTable=Markup(master)
    return sortedTable


def makeLengthSortedTable(valueDic, lengthDic):
    master=""
    for i in tableSorted(lengthDic):
        master+='''<tr>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
        </tr>'''.format(i[0], str(i[1]), str(valueDic[i[0]]))#format(i, str(length), str(value))
    sortedTable=Markup(master)
    return sortedTable



letterValues = {
    "a":1,
    "b":3,
    "c":3,
    "d":2,
    "e":1,
    "f":4,
    "g":2,
    "h":4,
    "i":1,
    "j":8,
    "k":5,
    "l":1,
    "m":3,
    "n":1,
    "o":1,
    "p":3,
    "q":10,
    "r":1,
    "s":1,
    "t":1,
    "u":1,
    "v":4,
    "w":4,
    "x":8,
    "y":4,
    "z":10,
    "*":0
    }
