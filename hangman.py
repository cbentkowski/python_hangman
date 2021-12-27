import json
import random
import turtle

### Setup Turtle ###
t = turtle.Turtle(visible=False)
t.speed(50)
t.pensize(5)
t.penup()

### Start Writing Turtle ###
w = turtle.Turtle(visible=False)
align = "left"
font=("Arial", 36, "bold")
w.penup()
w.goto(-300,-300)

### Function Enter a Letter ###
from pip._vendor.distlib.compat import raw_input
def enter_letter(used):
    while True:
        print("Guess a letter: ")
        guess = input()
        guess = guess.lower()
        if len(guess) != 1:
            print('Please enter a single letter')
        elif guess in used:
            print("You've already used this letter. Guess again.")
        elif not guess.isalpha():
            print("Please enter letters only.")
        else:
            return guess

### Build First Part of Hangman Stand ###
def buildFirstStand():
    t.penup()
    t.goto(300,-200)
    t.pendown()
    t.goto(400,-200)
    t.penup()
    t.goto(350,-200)
    t.pendown()
    t.goto(350,350)
    t.penup()

### Build Board ###
def build_board(correctletters, secretWord):
    used_letters()
    blanks = '_' * len(secretWord)
    
    for i in range(len(secretWord)):
        if secretWord[i] in correctletters:
            blanks = blanks[:i] + secretWord[i] + blanks[i+1:]
    
    for letter in blanks:
        print(letter, end=' ')
    
    print()
    
def used_letters():
    print("Used Letters: ", end='')
    for letter in usedLetters:
        print(letter, end=' ')
    print()

def playAgain(question):
    reply = str(raw_input(question+' (y/n): ').lower().strip())
    if reply[0] == 'y':
        return True
    elif reply[0] == 'n':
        return False
    else:
        return playAgain(paQuestion)
    

### Load list of words ###
with open('words.json') as f:
    words = json.load(f)
    
### Randomly select word from list ###
word = random.choice(words).lower()
### Create list from word ###
wordlist = list(word)

### Setup Game ###
paQuestion = 'Do you want to play again?'
usedLetters = []
numguesses = 6
correctletters = []
gameIsDone = False

while True:
    build_board(correctletters, word)
    letterguess = enter_letter(usedLetters)
    usedLetters.append(letterguess)
    if letterguess in wordlist :
        correctletters.append(letterguess)
        ### Check for Win ###
        foundAllLetters = True
        for i in range(len(wordlist)):
            if wordlist[i] not in correctletters:
                foundAllLetters = False
                break
        if foundAllLetters:
            print("You've won the game! The word was " + word +".")
            gameIsDone = True
    else:
        numguesses = numguesses - 1
        if numguesses == 0:
            print("You have run out of guesses. The word was " + word + ".")
            gameIsDone = True

    ### End Game ###
    if gameIsDone:
        if playAgain(paQuestion):
            usedLetters = []
            numguesses = 6
            correctletters = []
            gameIsDone = False
            word = random.choice(words).lower()
            wordlist = list(word)
        else:
            break
