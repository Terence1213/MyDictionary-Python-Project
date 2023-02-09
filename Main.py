import ast
import random

# SaveData file being opened, and its data being extracted
with open("SaveData") as file:
    data = file.read()

wordsEntered = dict()

# The string variable data obtained from the text file is converted to a dictionary
if data != "":
    wordsEntered = ast.literal_eval(data)


# The data is saved and put into the text file
def saveData():
    with open("SaveData", 'r+') as file:
        file.truncate(0)
        file.write(str(wordsEntered))


def enterWord():
    # The new word is being added to the dictionary.
    print("\n------------------------------------------------------------")
    newWord = input("Please enter the new word: ").lower()
    if wordsEntered.__contains__(newWord):
        choice = int(input("> The word you entered has already been entered before."
                           "\n\nEnter 1. = Change the definition of the currently existing word"
                           "\nEnter 2. = Cancel"))

        isLoopStopped = False
        while isLoopStopped == False:
            if choice == 1:
                wordsEntered.update({newWord: input("\nPlease enter the definition of the word '" + newWord + "': ")})
                isLoopStopped = True
            elif choice == 2:
                isLoopStopped = True
    else:
        wordsEntered.update({newWord: input("Please enter the definition of the word '" + newWord + "': ")})


def lookUpWord():
    # Each currently existing word is displayed.
    print("\n-----------------------------------------------")
    for key in wordsEntered:
        print("> " + key)
    print("-----------------------------------------------")

    # The user enters the word of choice, and gets its definition
    wordChoice = input("\nPlease enter the word you want the definition for (from the list): ").lower()
    wordFound = False
    for key in wordsEntered:
        if wordChoice == key:
            print("\nDefinition of '" + key + "': " + wordsEntered.get(key))
            wordFound = True

    if wordFound == False:
        print("The word you entered wasn't found in the database!")

#The user chooses whether he will be given the word, or the definition in the quiz.
def quizMenu():

    choice = int(input("\nEnter 1. = Word based quiz"
                       "\nEnter 2. = Definition based quiz"
                       "\nPlease enter your choice: (1 - 2): "))

    while True:
        if choice == 1:
            isWordQuiz = True
            break
        elif choice == 2:
            isWordQuiz = False
            break

    quiz(isWordQuiz)

# A quiz consisting of each word already entered into the program. - The questions are always in a randomised order.
def quiz(isWord):
    # Typecasts the dictionary's keys into a list, so that they can be shuffled
    keys = list(wordsEntered.keys())
    random.shuffle(keys)

    shuffledWords = dict()

    # The shuffled keys are entered into a new dictionary, with their old values (from the old dictionary).
    for key in keys:
        shuffledWords.update({key: wordsEntered.get(key)})

    score = 0

    print("\nENTER QUIT AT ANYTIME IF YOU WANT TO CANCEL THE QUIZ")

    # The questions are asked (for all the already entered words in the program) - depending on the user's chosen
    # quiz mode.

    if isWord:
        #For each word in the database the question will be asked
        for key in shuffledWords:
            print("--------------------------------------------------")
            answer = input("What is the definition of the word: " + key + "?: ").lower()
            if answer == "quit":
                break

            print("\nYour answer: " + answer)
            print("Correct answer: " + shuffledWords.get(key))

            while True:
                isCorrect = input("Do you think your answer is correct? (yes : no): ").lower()
                if isCorrect == "yes":
                    score += 1
                    break
                elif isCorrect == "no":
                    break

    elif not isWord:
        #For each word in the database the question will be asked
        for key in shuffledWords:
            print("--------------------------------------------------")
            answer = input("What is word coming from the definition:\n> " + shuffledWords.get(key) +
                           "\nEnter your answer (word): ").lower()
            if answer == "quit":
                break

            print("\nYour answer: " + answer)
            print("Correct answer: " + key)

            if answer == key:
                print("Result: Correct!")
                score += 1
            elif not answer == key:
                print("Result: Incorrect!")



    # Total score is displayed
    print("------------------------------------------------")
    print("Your total score was: {0:.2f}%".format((score / len(wordsEntered) * 100)))


def menu():
    while (True):

        # Menu is displayed and the user makes his choice.
        print("\n-----------------------------------------------")
        print("Enter 1. = Enter new word and its definition")
        print("Enter 2. = Look up word for its definition")
        print("Enter 3. = Play quiz")
        print("Enter 4. = Quit")
        print("-----------------------------------------------")

        choice = int(input("Enter your choice (1 - 4): "))
        if (choice == 1):
            enterWord()
        elif (choice == 2):
            if len(wordsEntered) > 0:
                lookUpWord()
            else:
                print("A word hasn't been entered into the database yet!")
        elif (choice == 3):
            if len(wordsEntered) > 0:
                quizMenu()
            else:
                print("A word hasn't been entered into the database yet!")
        elif (choice == 4):
            saveData()
            break
        else:
            print("\nInvalid input! please enter a number between 1 and 3")

menu()