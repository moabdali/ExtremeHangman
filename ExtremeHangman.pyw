#!/usr/bin/python3
import string
import random
from time import sleep
from os import system, name
import copy #for copying arrays
import PySimpleGUI as sg #for making a gui


#stock code for clearing the screen
def screen_clear():
   if name == 'nt':
      _ = system('cls')
   # for mac and linux(here, os.name is 'posix')
   else:
      _ = system('clear')
    #screen_clear()
#end stock code for clearing screen

# most words on screen at a time; need play testing to see if I should lower it
maxWords = 10


# not used right now; allow player to guess the whole word
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


# input validation for ints
def isItANumber(numOfWords):
    while True:
      try:
            numOfWords = int(numOfWords)
            return 1
      except ValueError:
            return 0
            #print(f"That's not an integer.  Try again.")
            



# makes the words
def generateWordList(wordList,letters):
    try:
        file = open("words.txt","r")
    except IOError:
        sg.popup("File not found.  You must have a words.txt file in the same directory.")
        quit()
        
    for i in file:
        i = i.rstrip()
        skipFlag = 0
        for checkLetters in i:
           #makes sure that any words that don't use only letters, get rejected
            if checkLetters not in letters:
                skipFlag = 1
                break
        if skipFlag == 0:
            wordList.append(i)
    sleep(1)    


# the solveArray is currently a duplicate of the answers, so we want to make the arrays reset to all "???" while maintaining the same length per word
def blankOutSolveList(solveList):
    for i in range(len(solveList)):
        for j in range(len(solveList[i])):
            solveList[i][j] = "?"

# break up a string into chars                   
def split(word):
    return [char for char in word]


#introductory stuff    
def intro(wordList,hangWords):

   #contains the blanks you've successfully solved so far   
   solveList = []
   
   #contains the 52 valid letters (26 upper, 26 lower)
   letters = list(string.ascii_letters)

   #creates a PySimpleGui window requesting number of words the player wants to guess (tentatively at a max of 10 words
   questionString = (f"How many words would you like to attempt simultaneously?  You may do up to {maxWords}. ")
   sg.theme('DarkAmber')   # Add a little color to the window
   numOfWordsLayout = [[sg.Text(questionString)]]
   numOfWordsLayout.append( [sg.T("Number of words: "), sg.InputText()])
   numOfWordsLayout.append( [sg.Button('Submit')] )
   numOfWordsWindow = sg.Window('Number of words',numOfWordsLayout )
    
   #test to make sure the player picks between 1 and max words (10)
   while True:
      event,values = numOfWordsWindow.read(timeout=10)
      if event == 'Submit':
        numOfWords = values[0]
        result = isItANumber(numOfWords)
        if result == 0:
           sg.popup('Enter a number!')
           continue
        else:
           numOfWords = int(numOfWords)
           if numOfWords > 0 and numOfWords <= maxWords:
              
              numOfWordsWindow.close()
              break
           else:
              sg.popup('Enter a number between 1 and 10!')
              continue

       
    
   #loading words into memory and filtering
   sg.popup_timed(f"Loading the word list to memory and deleting invalid words. This window will close automatically when ready.")
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
    #the answers
    hangWords = []
    #guesses before you die
    hp = 8
    #points are not implemented yet; more of a placeholder for future things
    points = 100
    #how many words the player wants to guess at a time
    numOfWords = 0
    #a flag to make sure we don't reveal the length of unsolved words
    foundAtLeastOneLetter = []
    lengthFoundLetter = []
    #longest length of any given puzzle that was found so far
    maxWordFound = []
    #used for cocatenating what used to be a multiline print statement into a single string 
    printString = []
    #flag to make sure I don't open up duplicate windows all day; the window only initilializes once
    firstTimeWindow = True
    #letters the player got wrong
    failList = []
    #contains the 52 valid letters (26 upper, 26 lower)
    letters = list(string.ascii_letters)
    letters.sort()
    #iterates through each puzzle, looking for a match with the guessed letter
    distanceMoved = []
    #if no letter was found, the player loses a life
    foundALetterThisTime=False
    #valid letters the players can guess at (they might be incorrect, but they're still valid)
    remainingLetters = []

    #copy all the letters (uppercase and lowercase) into the remaining letters
    for i in range(len(letters)):
       remainingLetters.append(letters[i])

    #play the intro sequence, including initializing words.  Returns the solveList blanked out list
    solveList = intro(wordList,hangWords)


    #set all the puzzles to assume no letters have been found (needed to make sure the length is hidden)
    #also set the length of the word found so far to 0 (since we didn't find a word yet)
    numOfWords = len(hangWords)
    for i in range (numOfWords):
        foundAtLeastOneLetter.append(False)
        distanceMoved.append(0)
        maxWordFound.append(0)
        lengthFoundLetter.append(0)
        printString.append("")
        
    
    while True:
        #assume player is a winner until an unsolved puzzle is found; easier to do it this way than to assume they're losing and checking to see that each puzzle was won.
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
                sg.popup("WINNER")
                quit()
            break
       
        
        #display each puzzle as it currently appears
        for i in range (numOfWords):

            if foundAtLeastOneLetter[i] == False:
                myString = (f"Word {i+1}:  ")
                printString[i]= myString
                continue
            elif "?" not in solveList[i]:
                myString = (f"Word {i+1}: ")
                for j in solveList[i]:
                   myString += (f" {j} ")
                myString+=(f" <SOLVED!>")
                printString[i] = myString
                continue
            elif foundAtLeastOneLetter[i] == True:
                myString =(f"Word {i+1}: ")
                for j in range (maxWordFound[i]+1):
                    if solveList[i][j] == "?":
                        myString+=(" _ ")
                    else:
                        myString+=(f" {solveList[i][j]} ")
                printString[i]=myString
        
        lettersString = ""
        # print remaining letters
        for i in range(0,len(letters)):
            
            if letters[i] not in failList and letters[i] in remainingLetters:
                lettersString+=("["+letters[i]+"]")
                if letters[i] == "Z":
                    lettersString+=("\n")
            else:
                if letters[i] not in remainingLetters:
                    lettersString+=("[#]")
                elif letters[i] in failList:
                    lettersString+=("[#]")


        if firstTimeWindow == True:
          layout = []
          layout.append( [ sg.Text("EXTREME HANGMAN", size = (30,None), font="Courier 40", text_color = 'red', justification = "center")])
          for i in range(0,numOfWords):
             layout += [sg.Text("",font = "courier 25", size=(100,None),key = i)],
          
          layout.append( [ sg.Text(" Missed Letters ",font = "courier 25", size=(100,None), key = 'reserved1')])
          layout.append( [ sg.Text(" Remaining Letters:",font = "courier 25", size=(100,None),key = 'reserved2')])
          layout.append( [ sg.Text(" letters",font = "courier 25", size=(100,None), key = 'reserved3')])
          #layout.append( [ sg.Button( lettersString[i],i in range(0,52), key = i, size = (100,None))])
          layout.append( [ sg.Text(" ",font = "courier 25", size=(100,None), key = 'reserved5')])
          layout.append( [ sg.Text(" Lives Remaining ",font = "courier 25", size=(100,None), key = 'livesRemaining')])
          layout.append( [ sg.Text(" ",font = "courier 25", size=(100,None), key = 'messageToUser')])
          layout.append( [ sg.Text("",key = 'guessme',font = "courier 25", size=(100,None), justification = "center")] )
          window = sg.Window('Extreme Hangman',layout, finalize = True,  return_keyboard_events=True,)
          window.TKroot.focus_force()
          firstTimeWindow = False
          
        #update the current status of the words solved
        for i in range (numOfWords):
           window[i](printString[i])

        #sets letters that you have used to "#" symbols so that you don't reuse them
        for i in range(len(remainingLetters)):
           for j in range(len(solveList)):
              if remainingLetters[i] in solveList[j]:
                 remainingLetters[i] = "#"

        
        #incorrect letters (letters that you guessed that aren't in the puzzle)
        failList.sort()
        window['reserved1'](f"Incorrect letters: {failList}")
        window['reserved2']("Remaining letters: ")


       
        window['reserved3'](lettersString)
        
        window['reserved5']("*"*78)
        hpbar = "Lifepoints left: " + ("[*]"*(hp))
        window['livesRemaining'](hpbar)
        

        event, values = window.read()




        #points will be used in the future... but not yet
        #print("Points: "+str(points))


        #make a more dramatic death thing   
        if hp == 0:
            sg.popup("You dead")
            sg.popup(f"Solution: {hangWords}")
            sleep(10)
            quit()

        #debug for seeing the answers
        # print(f"[[[Words are {hangWords}]]]")
        #debug 


        

        
        window['guessme']("What letter would you like to guess?")


        #old method for getting inputs.  Keep here just in case...
        #letterGuess = sg.popup_get_text('Guess a letter', 'Enter a letter')


        #the main aspect of the game is this one simple equation.  It gets the input from the player's keyboard
        letterGuess = event



    #future feature for guessing the whole word at one time
    #print("Enter 1 if you want to guess the word (costs 2 lives if you're wrong)")
    ##    if letterGuess == "1":
    ##       a = guessWord(hangWords)
    ##       if a == 0:
    ##          hp -= 2
    ##          continue
    ##       elif a == 1:
    ##          print("WINNER")
    ##          sleep(3)
    ##          quit()



        #the following checks are self explanatory
        dupCheck = False
        for i in solveList:
           for j in i:
              if letterGuess == j:
                 dupCheck = True
                 break
               
        if dupCheck == True:
           window['messageToUser']("You fool!  You already got this correct!")
           continue

        if letterGuess not in letters:
            window['messageToUser'](f"(You fool, that's not a valid letter. Try again)")
            sleep(3)
        if letterGuess in failList:
            window['messageToUser']("You fool!  You already guessed that.")
            continue

        for i in range(numOfWords):
            distanceMoved[i] = 0


        #the main meat of the processing.  Basically it takes the letter and goes from left to right to set if the letter
        #exists in a given word.  If it does, it notes the last occurrence of the letter and appends the location in the
        #corresponding solve list, and then continues on with the next word.  If no words have that letter, then the flags
        #remain false and the next section punishes the player with hp loss. 
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

        # updates the window with messages    
        if foundALetterThisTime == False and letterGuess in letters:   
            hp -=1
            window['messageToUser']("Ouch, you guessed wrong!  That'll cost a life.")
            failList.append(letterGuess)
            failList.sort()
        else:
            window['messageToUser']("You found a letter!",text_color = "green")
            
        
        
gameLoop()
