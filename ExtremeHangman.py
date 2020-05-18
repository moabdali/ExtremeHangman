import string
import random
from time import sleep
from os import system, name
import copy


#stock code for clearing the screen
def screen_clear():
   if name == 'nt':
      _ = system('cls')
   # for mac and linux(here, os.name is 'posix')
   else:
      _ = system('clear')
    #screen_clear()
#end stock code for clearing screen


maxWords = 10

def guessWord(hangWords,solveList):
    a = input(f'Guess a word. >>')
    success = False
    for i in range(len(hangWords)):
        if hangWords[i] == a:
            solveList[i] = a
            success = True
    #win a word    
    if success:
        return 0
    else:
        #lose lives
        return 1


def isItANumber(questionString):
    while True:
        myNum = input(questionString)
        try:
            myNum = int(myNum)
            return myNum
        except ValueError:
            print(f"That's not an integer.  Try again.")

def generateWordList(wordList,letters):
    try:
        file = open("words.txt","r")
    except IOError:
        print("File not found.  You must have a words.txt file in the same directory.")
        quit()
        
    for i in file:
        i = i.rstrip()
        skipFlag = 0
        for checkLetters in i:
            if checkLetters not in letters:
                skipFlag = 1
                break
        if skipFlag == 0:
            wordList.append(i)
    print("All done!")
    print("There are "+str(len(wordList))+" words available!")
    sleep(1)    

def blankOutSolveList(solveList):
    for i in range(len(solveList)):
        for j in range(len(solveList[i])):
            solveList[i][j] = "?"
                   
def split(word):
    return [char for char in word]
    
def intro(wordList,hangWords):

    solveList = []
    #contains the 52 valid letters (26 upper, 26 lower)
    letters = list(string.ascii_letters)
    

    
    #introduction
    print(f"Welcome to Extreme Hangman.")
    #sleep(1)
    #end introduction


    #how many words will the player use?
    while True:
        questionString = (f"How many words would you like to attempt simultaneously?  You may do up to {maxWords}.\n>> ")
        a = isItANumber(questionString)
        if a > 0 and a <= maxWords:
            numOfWords = a
            break
        else:
            print(f"Number must be between 1 and {maxWords}")
        
    #loading words into memory and filtering
    print(f"Loading the word list to memory and deleting invalid words.  This may take a few seconds...")
    generateWordList(wordList,letters)
    random.seed()

    # generate the to-solve word list
    for i in range(numOfWords):
        word = wordList[random.randint(0,len(wordList))]
        word = split(word)
        hangWords.append(word)

    # make a true copy of the puzzle words
    solveList = copy.deepcopy(hangWords)

    # set the slots in solveList to ? to show they're not solved
    blankOutSolveList(solveList)
    return solveList
    
    
def gameLoop():
    #will contain the entire valid wordlist
    wordList = []
    hangWords = []
    hp = 8
    points = 100
    numOfWords = 0
    foundAtLeastOneLetter = []
    lengthFoundLetter = []
    maxWordFound = []
    
    failList = []
    #contains the 52 valid letters (26 upper, 26 lower)
    letters = list(string.ascii_letters)
    letters.sort()
    distanceMoved = []
    foundALetterThisTime=False
    remainingLetters = []

    for i in range(len(letters)):
       remainingLetters.append(letters[i])

    
    #play the intro sequence, including initializing words.  Returns the solveList blanked out list
    solveList = intro(wordList,hangWords)


    #set all the puzzles to assume no letters have been found (needed to make sure the length is hidden)
    #also set the length of the word found so far to -1 (since we didn't find a word yet)
    numOfWords = len(hangWords)
    for i in range (numOfWords):
        foundAtLeastOneLetter.append(False)
        distanceMoved.append(0)
        maxWordFound.append(0)
        lengthFoundLetter.append(0)
    #debug false check
    #print(foundAtLeastOneLetter)
    while True:
        winner = True
        foundALetterThisTime = False
        
        #winner check
        while True:
            #if any unsolved letters exist, program assumes you haven't won yet
            for i in range (numOfWords):
                if "?" in solveList[i]:
                    winner = False
                    break
            
            #debug make a fancier win thing here
            if winner == True:
                print("WINNER")
                quit()
            break

        screen_clear()
        
        #display each puzzle as it currently appears
        for i in range (numOfWords):
            
            if foundAtLeastOneLetter[i] == False:
                print(f"Word {i+1}:  ")
                continue
            elif "?" not in solveList[i]:
                print(f"Word {i+1}: ", end = "")
                for j in solveList[i]:
                   print(f" {j} ",end="")
                print(" <SOLVED!>")
                continue
            elif foundAtLeastOneLetter[i] == True:
                print(f"Word {i+1}: ",end="")
                for j in range (maxWordFound[i]+1):
                    if solveList[i][j] == "?":
                        print(" _ ", end="")
                    else:
                        print(f" {solveList[i][j]} ", end="")
                        
            print("\n",end="")

        for i in range(len(remainingLetters)):
           for j in range(len(solveList)):
              if remainingLetters[i] in solveList[j]:
                 remainingLetters[i] = "#"

        
        #incorrect letters
        failList.sort()
        print(f"\nIncorrect letters: {failList}\n")
        print("*"*78)
        print("Remaining letters: ")
        for i in range(0,len(letters)):
            if letters[i] not in failList and letters[i] in remainingLetters:
                print("["+letters[i]+"]",end="")
                if letters[i] == "Z":
                    print("\n")
            else:
                if letters[i] not in remainingLetters:
                    print("[#]",end="")
                elif letters[i] in failList:
                    print("[#]", end="")
        print("\n")
        print("*"*78)
        
        print("Lifepoints left: "+"[*]"*(hp))
        print("Points: "+str(points))
            
        if hp == 0:
            print("You dead")
            print(f"Solution: {hangWords}")
            sleep(10)
            quit()

        #debug
        # print(f"[[[Words are {hangWords}]]]")
        #debug

        #print("Enter 1 if you want to guess the word (costs 2 lives if you're wrong)")
        
        print("What letter would you like to guess?")
        letterGuess = input(" >>")

    ##    if letterGuess == "1":
    ##       a = guessWord(hangWords)
    ##       if a == 0:
    ##          hp -= 2
    ##          continue
    ##       elif a == 1:
    ##          print("WINNER")
    ##          sleep(3)
    ##          quit()

        dupCheck = False
        for i in solveList:
           for j in i:
              if letterGuess == j:
                 dupCheck = True
                 break
               
        if dupCheck == True:
           print("You fool!  You already got this correct!")
           continue

        
        if letterGuess not in letters:
            print(f"(You fool, that's not a valid letter. Try again)")
            sleep(3)
            continue
        if letterGuess in failList:
            print("You fool!  You already guessed that.")
            sleep(3)
            continue

        for i in range(numOfWords):
            
            distanceMoved[i] = 0
        
        for wordScan in range(numOfWords):
            for letterScan in range (len(hangWords[wordScan])):
                if letterGuess == hangWords[wordScan][letterScan]:
                    foundAtLeastOneLetter[wordScan] = True
                    foundALetterThisTime = True
                    lengthFoundLetter[wordScan] = distanceMoved[wordScan]
                    if lengthFoundLetter[wordScan] > maxWordFound[wordScan]:
                        maxWordFound[wordScan] = lengthFoundLetter[wordScan]
                    solveList[wordScan][lengthFoundLetter[wordScan]] = letterGuess
                distanceMoved[wordScan] += 1

            
        if foundALetterThisTime == False:   
            hp -=1
            print("Ouch, you guessed wrong!  That'll cost a life.")
            sleep(2)
            failList.append(letterGuess)
            failList.sort()
        else:
            print("You found a letter.")
            sleep(.75)
            
gameLoop()
