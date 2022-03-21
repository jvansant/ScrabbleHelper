from __future__ import unicode_literals
from flask import Flask, request, render_template, make_response
from flask import Markup


app = Flask(__name__)
    

@app.route('/', methods=['GET','POST'])
def make_sheet():
    if request.method=="GET":
        return render_template('scrabble_input.html')
    else:
        letters=[]
        letters.append(request.form['let'])
        letters.append(request.form['let1'])
        letters.append(request.form['let2'])
        letters.append(request.form['let3'])
        letters.append(request.form['let4'])
        letters.append(request.form['let5'])
        letters.append(request.form['let6'])

        if letters.count("*")>1:
            return render_template('scrabble_input.html', jerrormsg="**Cannot use wild-card * more than once**")#all=words)
        
        checked=request.form.get('checked')
        exist=request.form.get('prior')
        language=request.form.get('lang')
        if not checked:
            exist=""

        
        try:
            valueDict, lenDict = getWords(language, letters, exist)
        except KeyError:
            return render_template('scrabble_input.html', jerrormsg="**Only letters a-z allowed**")#all=words)

        
        if len(valueDict)<1:
            return render_template('scrabble_input.html', jletters=letters, jgiven=exist, jlanguage=language, jerrormsg="**Nothing Found**")#all=words)
        
        table=makeTable(valueDict, lenDict)
        

        return render_template('table.html', jletters=letters, jgiven=exist, jlanguage=language, tinside=table)#all=words)


    


def getWords(language, inputLetters, givenWord):#takes in full dictionary and user input to return a list of words that can be made.
    ogDictionary=createDict(language)#will only be used to make dictionary{}
    dictionary={}#made to only contain letters that are given--MORE EFFICIENT
    s=givenWord
    for l in inputLetters:
        s+=l
    if "*" in s:
        dictionary=ogDictionary
    else:        
        for let in s:#ADD LATTER GIVEN WORD IN CASE THERE ARE WORDS THAT START WITH THOSE LETTERS
            dictionary[let] = ogDictionary[let]

    if(not givenWord):
        result = {}
        for letter in dictionary:
            for dictWord in dictionary[letter]:
                sub=0
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
                            sub=addLetters(dictWord[j])
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
                sub=0

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
                                sub=addLetters(dictWord[j])
                            else:
                                invalid = True
                        else:
                            letters.remove(dictWord[j])
                        j += 1

            #Adds the word to the list if it never used invalid characters
                if(not invalid):
                    result[dictWord]=sub

        try:
            del result[givenWord]
        except:
            print("nogiven")

        # if(result == []):
        #     result = ["**Nothing Found**"]

            # words=""
        valueDict={}
        lenDict={}
        for w in result:
            if len(w)>1:
            # words=words+w+" "
                value=addLetters(w)-result[w]
                valueDict[w]=value
                length=len(w)
                lenDict[w]=length

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


def addLetters(word):
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
        "\'":0,
        "*":0,
        "å":1,
        "é":1,
        "ñ":1,
        "ö":1,
        "ê":1,
        "ô":1,
        "ü":1,
        "è":1,
        "â":1,
        "ó":1,
        }
    s = 0
    for i in word:
        s += letterValues[i]
    return s
    

# def sortDic(sortByDic):
#     return sorted(sortByDic.items(), key=lambda kv:(kv[1], kv[0]), reverse=True)


def makeTable(valueDic, lengthDic):
    master=""
    for i in valueDic:
        master+='''<tr>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
        </tr>'''.format(i, lengthDic[i], valueDic[i])#format(i, str(length), str(value))
    table=Markup(master)
    return table


