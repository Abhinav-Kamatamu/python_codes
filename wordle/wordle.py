words = open('words.txt').read()

import random

def checkWord(word):

    boolean = False

    i = 0
    while not boolean:

        if words[i:i+5] == guess:
            boolean = True

        elif i > len(words):
            break

        else:
            i += 6

    return boolean

def pickWord(listOfWords):

    lenght = len(listOfWords)
    index = random.randint(0, int(((lenght + 1)/6) - 1)) * 6
    
    return listOfWords[index: index + 5]

mainWord = pickWord(words)
mainWordList = []

for letter in mainWord:
    mainWordList.append(letter)

print("type 'giveup' if you want to give up")
while True:

    guess = input("Enter your guess: ").lower()

    if guess == "giveup":
        print("the word was " + mainWord)
        break
    
    if not checkWord(guess):

        print("invalid guess")
        continue

    if guess == mainWord:

        print("you Win!")
        break

    else:

        i = 0
        while i <= 4:

            text = "GRAY"

            if guess[i] in mainWord:
                text = "YELLOW"
                if guess[i] == mainWord[i]:
                    text = "GREEN"

            print(guess[i] + " - " + text)
            
            i += 1
    

    


                
