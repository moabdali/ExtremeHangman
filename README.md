# ExtremeHangman
 Hangman but with some twists to make it challenging

v 0.1: 
	- console based Hangman
	Working:
	- parsing any text document, drops words that use anything but the 52 English letters (26 upper case, 26 lower case)
	- has a feature where the length is hidden; if you guess a letter, it acts as though the word length is equal to the spot of the word.  In other words, if the word is Github, and you guess "t", then you see:  _ _ t.   If you later guess "u", then you see:  _ _ t _ u  And so on. 
	- shows a life counter instead of a hangman.  This is partially due to showing a hanging person being offensive to many people, but also due to laziness.  A life bar may be implemented eventually.
	- shows a score, but doesn't do anything yet
	- you can guess the word, but wrong guesses will cost two lives.

	
	Potential Ideas:
	- endless mode where you guess as many words as you can until you lose.  Guessing a word correctly/solving it will give you more lives
	- multiple puzzles mode where you can attempt guesses toward more than one word.  Lose more points for each error.  Good way to gain faster scores, but you need to die faster to make it balanced
	- option to where if a word has duplicates, you have to reguess the same letter.  So for Reddit, if you guess d, you only see "_ _ d" and have to guess d again to see "_ _ d d"
	- point system can be set to where you have to pay out points each time you guess a letter, more common letters are worth more.  That is, if you guess e, you may have to pay 10 points.  If you guess z, only 1 point.  If you're wrong, maybe double the point penalty
	- level up system where guessing more and more words raises your level, which unlocks perks like "see word length" or "destroy an invalid letter" or even "regenerate a life".  Achievements can exist for guessing letters correctly in a row, or guessing letters in alphabetical order.  Stuff like that. 

v 0.2:
	- now allows you to use multiple words at the same time
	- fixed a bunch of logic errors having to do with displaying used letters
	- fixed errors with formatting (such as trying to print lists instead of words)
	- fixed errors regarding checks to see if you won

v 0.3 - has a GUI now
      - you can play by just pressing letters; no need to hit enter
      - need to figure out why the game doesn't update the "remaining letters" immediately; otherwise working without issue
	  - renamed to .pyw type in order to avoid dealing with a console window (as it's no longer needed)
	  - added the PySimpleGUI.py file to the folder to avoid issues with having to download it
	  
	  
v 0.3.1
	  - corrected the remaining letters issue from v .3; it was a logic error that needed a duplicate print and a refresh window call

v 0.4
	 - added balance to the lives; more words = fewer lives (trust me, it makes sense - more words increases the likelihood of a letter being correct, and they more letters you get correct, the more likely you are to solve words)
       - corrected a formatting issue where the solutions on death were shown as a list of characters instead of a single string for each word

v 0.4.1
        - doesn't display errors for using shift, as well as potential accident input (such as mouse wheel or capslock)
        - punishes player for trying to be funny (takes away a life if you input an illegal button on purpose such as + or ] and so on)
        - formatting changes to pop ups and solution screen