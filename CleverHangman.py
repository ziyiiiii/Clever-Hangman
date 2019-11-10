'''
@author: Ziyi Yan   zy81
'''

global DEBUG
DEBUG = True

def handleUserInputDifficulty():
    '''
    This function asks the user if they would like to play the game in (h)ard or (e)asy mode, then returns the
    corresponding number of misses allowed for the game.
    '''

    # Your Code Here
    print("you'll get 12 misses unless you enter 'h' for 'hard to guess'")
    print("How many misses do you want? Hard has 8 and Easy has 12")
    diff = input("(h)ard or (e)asy> ")
    if diff == "h":
        return 8
    else:
        return 12


def getWord(words, length):
    '''
    Selects the secret word that the user must guess.
    This is done by randomly selecting a word from words that is of length length.
    '''
    # Your Code Here
    import random
    z = []
    for wd in words:
        if len(wd) == length:
            z.append(wd)
    return random.choice(z)


def createDisplayString(lettersGuessed, missesLeft, hangmanWord):
    '''
    Creates the string that will be displayed to the user, using the information in the parameters.
    '''

    # Your Code Here
    y = lettersGuessed #lettersGuessed is a list of words that have been guessed
    w = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    for i in range(len(w)):
        if y.count(w[i]) == 1:
            w[i] = " "
    x = ' '.join(hangmanWord)
    return "letters not yet guessed: " + ''.join(w) + "\n" + "misses remaining = " + str(missesLeft) + "\n" + x


def handleUserInputLetterGuess(lettersGuessed, displayString):
    '''
    Prints displayString, then asks the user to input a letter to guess.
    This function handles the user input of the new letter guessed and checks if it is a repeated letter.
    '''

    # Your Code Here
    # while hangmanWord.find("_") != -1:
    guess = input("letter> ")
    while guess in lettersGuessed:
        print("you already guessed that")
        guess = input("letter> ")
        # else:
        #     lettersGuessed.append(guess)
    # print("letter> " + guess)
    return guess


def updateHangmanWord(guessedLetter, secretWord, hangmanWord):
    '''
    Updates hangmanWord according to whether guessedLetter is in secretWord and where in secretWord guessedLetter is in.
    '''

    # Your Code Here
    for i in range(len(secretWord)):
        if guessedLetter == secretWord[i]:
            hangmanWord[i] = guessedLetter
        # else:
        #     hangmanWord[i] = "_"
    return hangmanWord


def processUserGuess(guessedLetter, secretWord, hangmanWord, missesLeft):
    '''
    Uses the information in the parameters to update the user's progress in the hangman game.
    '''

    # Your Code Here

    hangmanWord = updateHangmanWord(guessedLetter, secretWord, hangmanWord)
    lst = []
    lst.append(hangmanWord)

    if guessedLetter not in secretWord:
        missesLeft -= 1
        bool = False
    if guessedLetter in secretWord:
        bool = True
    lst.append(missesLeft)
    lst.append(bool)
    return lst

def handleUserInputDebugMode():
    print("Which mode do you want: ")
    diff = input("(d)ebug or (p)lay: ")
    if diff == "d":
        return True
    else:
        return False

def handleUserInputWordLength():
    return int(input("How many letters in the word you'll guess: "))

def createTemplate(currentTemplate, letterGuess, word):
    for i in range(len(word)):
        lst2 = list(currentTemplate)
        if letterGuess == word[i]:
            lst2[i] = letterGuess
            currentTemplate = ''.join(lst2)
    return currentTemplate

def getNewWordList(currentTemplate, letterGuess, wordList):
    dic = {}
    for i in wordList:
        lst3 = list(currentTemplate)
        for idx in range(len(i)):
            if i[idx] == letterGuess:
                lst3[idx] = letterGuess
            if ''.join(lst3) not in dic:
                dic[''.join(lst3)] = []
        dic[''.join(lst3)].append(i)
    k = list(dic.keys())
    v = list(dic.values())
    maxitem = v[0]
    for i in range(len(v)):
        if len(v[i])>len(v[i-1]) and i > 0:
            maxitem = v[i]
    maxidx = v.index(maxitem)
    if DEBUG:
        # print("# possible words: " + str(len(wordList)))
        num = 0
        for key,value in sorted(dic.items()):
            if len(value) != 0:
                print(key+" : "+str(len(value)))
                num += 1
        print("# keys = " + str(num))
    return (k[maxidx], v[maxidx])


def runGame(filename):
    '''
    This function sets up the game, runs each round, and prints a final message on whether or not the user won.
    True is returned if the user won the game. If the user lost the game, False is returned.
    '''

    # Your Code Here
    global DEBUG
    f = open(filename)
    words = []
    for line in f.readlines():
        words.append(line.strip())
    # magic = getNewWordList(currentTemplate, letterGuess, wordList)

    DEBUG = handleUserInputDebugMode()

    length = handleUserInputWordLength()
    secretWord = getWord(words, int(length))

    wordList = [i for i in words if len(i) == len(secretWord)]

    hangmanWord = []
    for i in range(len(secretWord)):
        hangmanWord.append("_")

    lettersGuessed = []
    missesLeft = handleUserInputDifficulty()
    Left = missesLeft

    while missesLeft > 0 and "_" in hangmanWord:

        displayString = createDisplayString(lettersGuessed, missesLeft, hangmanWord)
        print(displayString)
        if DEBUG:
            print("(word is " + secretWord + ")")
            print("# possible words: " + str(len(wordList)))

        guessedLetter = handleUserInputLetterGuess(lettersGuessed, displayString)

        smart = getNewWordList(hangmanWord, guessedLetter, wordList)
        wordList = smart[1]
        secretWord = wordList[0]
        hangmanWord = list(smart[0])

        stupid = processUserGuess(guessedLetter, secretWord, hangmanWord, missesLeft)  # lst = stupid
        missesLeft = stupid[1]
        lettersGuessed.append(guessedLetter)

        if stupid[2] == False:
            print("you missed: " + guessedLetter + " not in word")

    if "_" not in hangmanWord:
        print("you guessed the word: " + secretWord + "\n" + "you made " + str(
            len(lettersGuessed)) + " guesses with " + str(Left - missesLeft) + " misses")
        return True

    print("you're hung!!" + "\n" + "word is " + secretWord + "\n" + "you made " + str(
        len(lettersGuessed)) + " guesses with " + str(Left - missesLeft) + " misses")
    return False


if __name__ == "__main__":
    '''
    Running Hangman.py should start the game, which is done by calling runGame, therefore, we have provided you this code below.
    '''
    runGame('lowerwords.txt')
