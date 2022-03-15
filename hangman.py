import json
import random
import turtle
from pathlib import Path

### Find Path of Hangman ###
source_path = Path(__file__).resolve()
source_dir = source_path.parent

### Global Variables ###
wordsPath = str(source_dir) + "/words/"
jsonWords = ""
word = ""
wordlist = []
paQuestion = 'Do you want to play again?'
used_Letters = []
numguesses = 8
correctletters = []
gameIsDone = False

### Setup Turtle ###
t = turtle.Turtle(visible=False)
t.hideturtle()
t.speed(50)
t.pensize(5)
t.penup()

### Start Word Writing Turtle ###
w = turtle.Turtle(visible=False)
w.hideturtle()
align = "left"
font=("Arial", 36, "bold")
w.penup()
w.goto(-300,-300)

### Start Used Letter Writing Turtle ###
ul = turtle.Turtle(visible=False)
ul.hideturtle()
ulfont=("Arial", 24, "bold")
ul.penup()
ul.goto(-375,300)

### Function Get List of Words ###
def getWordList(listFileName):
    global words
    with open(wordsPath + listFileName) as f:
        words = json.load(f)

### Function Choose Word List ###
def chooseWordList():
    global jsonWords
    print("Type a number to choose a word list:")
    print("1. Kindergarten Sight Words")
    print("2. 3rd Grade Words")
    menuChoice = input()
    match menuChoice:
        case "1":
            return "k-sight-words.json"
        case "2":
            return "3rd-grade.json"
        case _:
            getWordList(chooseWordList())

### Function Setup Game ###
def setupGame():
    ### Setup Globals ###
    global used_Letters
    global numguesses
    global correctletters
    global gameIsDone
    global word
    global words
    global wordlist

    used_Letters = []
    numguesses = 8
    correctletters = []

    t.clear()
    t.reset()
    t.hideturtle()
    t.speed(50)
    t.pensize(5)
    w.clear()
    w.reset()
    w.hideturtle()
    w.speed(50)
    ul.clear()
    ul.reset()
    ul.hideturtle()
    ul.speed(50)
    gameIsDone = False
        
    ### Randomly select word from list ###
    word = random.choice(words).lower()

    ### Create list from word ###
    wordlist = list(word)

    ### Check for apostrophe ###
    if "'" in wordlist:
        correctletters.append("'")

    return

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

### Build Second Part of Hangman Stand ###
def buildSecondStand():
    t.penup()
    t.goto(350,350)
    t.pendown()
    t.goto(200,350)
    t.goto(200,300)
    t.penup()

### Build Head ###
def buildHead():
    t.penup()
    t.goto(200,200)
    t.pendown()
    t.circle(50)
    t.penup()

### Build Body ###
def  buildBody():
    t.penup()
    t.goto(200,200)
    t.pendown()
    t.goto(200,-50)
    t.penup()

### Build Left Arm ###
def buildLeftArm():
    t.penup()
    t.goto(200,100)
    t.pendown()
    t.setheading(180-45)
    t.forward(100)
    t.penup()

### Build Right Arm ###
def buildRightArm():
    t.penup()
    t.goto(200,100)
    t.pendown()
    t.setheading(45)
    t.forward(100)
    t.penup()

### Build Left Leg ###
def buildLeftLeg():
    t.penup()
    t.goto(200,-50)
    t.setheading(270-45)
    t.pendown()
    t.forward(150)
    t.penup()

### Build Right Leg ###
def buildRightLeg():
    t.penup()
    t.goto(200,-50)
    t.setheading(270+45)
    t.pendown()
    t.forward(150)
    t.penup()

### Build Board ###
def buildWord(correctletters, secretWord):
    usedLetters()
    writeWord = ""
    blanks = '_' * len(secretWord)
    
    for i in range(len(secretWord)):
        if secretWord[i] in correctletters:
            blanks = blanks[:i] + secretWord[i] + blanks[i+1:]

    for letter in blanks:
        writeWord += letter + " "

    w.clear()
    w.penup()
    w.goto(-300,-300)
    w.write(writeWord, font=font, align=align)
    w.penup()
    
def usedLetters():
    writeUsedLetters = ""
    
    if len(used_Letters) > 0:
        for letter in used_Letters:
            writeUsedLetters += letter + " "
    
    ul.clear()
    ul.penup()
    ul.goto(-375,300)
    ul.write("Used Letters:", font=ulfont, align=align)
    ul.goto(-375, 250)
    ul.write(writeUsedLetters, font=ulfont, align=align)
    ul.penup()

def playAgain(question):
    reply = str(raw_input(question+' (y/n): ').lower().strip())
    if reply != '':
        if reply[0] == 'y':
            return True
        elif reply[0] == 'n':
            return False
        else:
            return playAgain(paQuestion)
    else:
        return playAgain(paQuestion)

def buildHangman(numguesses):
    match numguesses:
        case 7:
            buildFirstStand()
            return
        case 6:
            buildSecondStand()
            return
        case 5:
            buildHead()
            return
        case 4:
            buildBody()
            return
        case 3:
            buildLeftArm()
            return
        case 2:
            buildRightArm()
            return
        case 1:
            buildLeftLeg()
            return
        case 0:
            buildRightLeg()
            return
    
### Setup Game ###
getWordList(chooseWordList())
setupGame()

while True:
    buildWord(correctletters, word)
    letterguess = enter_letter(used_Letters)
    used_Letters.append(letterguess)
    if letterguess in wordlist :
        correctletters.append(letterguess)
        ### Check for Win ###
        foundAllLetters = True
        for i in range(len(wordlist)):
            if wordlist[i] not in correctletters:
                foundAllLetters = False
                break
        if foundAllLetters:
            buildWord(correctletters, word)
            print("You've won the game! The word was " + word +".")
            gameIsDone = True
    else:
        numguesses = numguesses - 1
        buildHangman(numguesses)
        if numguesses == 0:
            print("You have run out of guesses. The word was " + word + ".")
            gameIsDone = True

    ### End Game ###
    if gameIsDone:
        if playAgain(paQuestion):
            setupGame()
        else:
            break
