import json
import random
import pickle

# SaveData file being opened, and its data being extracted
with open("SaveData") as file:
    data = file.readlines()
    try:
        # Loads the words and their definitions
        wordsEnteredJson = json.loads(data[0])
        # Loads the indexes of each word which are to be used to access the answers for each word in the answers
        # text file.
        wordAnswersJson = json.loads(data[1])

        wordsEntered = dict(wordsEnteredJson)
        wordAnswers = dict(wordAnswersJson)
    except IndexError:
        # Contains the words and their definitions
        wordsEntered = dict()
        # Contains indexes of each word which are to be used to access the answers for each word in the answers
        # text file.
        wordAnswers = dict()

# The answers are loaded from the text file.
with open("Answers.txt", 'rb') as file:
    try:
        quizAnswers = pickle.load(file)
    except Exception:
        quizAnswers = list()
        print("Error at line 31")


# The data is saved and put into the text file
def saveData():
    # The wordsEntered and wordAnswers variables are converted to json format.
    wordsEnteredJson = json.dumps(wordsEntered)
    wordAnswersJson = json.dumps(wordAnswers)

    # The wordsEntered and wordAnswers variables are saved into the SaveData text file.
    with open("SaveData", 'r+') as file:
        file.truncate(0)
        file.write(wordsEnteredJson + "\n" + wordAnswersJson)

    # The answers for each word are saved into the Answers text file.
    with open("Answers.txt", 'wb') as file:
        file.truncate(0)
        pickle.dump(quizAnswers, file)


def enterWord():
    # The new word is being added to the dictionary.
    print("\n------------------------------------------------------------")
    newWord = input("Please enter the new word: ").lower()

    # If the user had already entered the same word before, he is given the choice of changing its definition or
    # canceling.
    if wordsEntered.__contains__(newWord):
        choice = None
        while True:
            error = False
            try:
                choice = int(input("\n> The word you entered has already been entered before."
                                   "\n\nEnter 1. = Change the definition of the currently existing word"
                                   "\nEnter 2. = Cancel"
                                   "\nPlease enter your choice (1 - 2): "))
            except ValueError:
                print("\nPlease enter a number between 1 - 2!")
                error = True

            #If an error doesn't happen, the menu isn't re-prompted to the user.
            if error == False:
                break

        isLoopStopped = False
        while isLoopStopped == False:
            if choice == 1:
                # The word chosen by the user, has its definition modified by the user
                wordsEntered.update({newWord: input("\nPlease enter the definition of the word '" + newWord + "': ")})

                # Since the word's definition has been modified, we give the user the option to clear or not clear the
                # word's previously saved answers, if there are any.

                # The program goes through each word in the wordAnswers variable, and when it finds the word which was
                # entered by the user it grabs its index, and clears the answers corresponding to the selected word.
                for word in wordAnswers:
                    if word == newWord:
                        # If the answers for the word are already empty, then the program doesn't have to clear it.
                        if len(quizAnswers[wordAnswers.get(newWord)]) > 0:
                            while True:
                                while True:
                                    error = False
                                    try:
                                        # The user chooses if he wants to clear the saved answers for his selected word
                                        # or not.
                                        choice = int(input("\n\nEnter 1. = Clear the answers for the selected word "
                                                           "whose definition was modified"
                                                           "\nEnter 2. = Dont clear the answers"
                                                           "\nPlease enter your choice (1 - 2): "))
                                    except ValueError:
                                        error = True
                                        print("\nPlease enter a number between 1 - 2!")

                                    # If an error happens, the program re - prompts the user to enter his menu choice.
                                    if error == False:
                                        break
                                if choice == 1:
                                    # If 1 is chosen, the answers for the selected word are cleared.
                                    quizAnswers[wordAnswers.get(newWord)] = list()
                                    break
                                elif choice == 2:
                                    # If 2 is cleared, the answers for the selected word aren't cleared.
                                    break

                isLoopStopped = True
            elif choice == 2:
                isLoopStopped = True
    else:
        # If the word entered has not been entered before in the program, the user is prompted to enter its definition.
        wordsEntered.update({newWord: input("Please enter the definition of the word '" + newWord + "': ").lower()})
        # The wordAnswers is updated since a new word has been added, and so a new index must be created to represent
        # the new word.
        wordAnswers.update({newWord: len(wordAnswers)})
        # The quizAnswers is appended with an empty list which can be later appended by multiple definitions.
        quizAnswers.append(list())


def lookUpWord():
    # Each currently existing word is displayed.
    print("\n-----------------------------------------------")
    for key in wordsEntered:
        print("> " + key)
    print("-----------------------------------------------")

    # The user enters his word of choice.
    wordChoice = input("\nPlease enter the word you want the definition/s for (from the list): ").lower()
    wordFound = False

    # The program goes through each already entered word, and if it finds the word the user typed in, the definition
    # menu is displayed.
    for key in wordsEntered:
        if wordChoice == key:

            wordFound = True
            definitionChoice = 0

            while True:
                error = False
                # The user chooses if he wants the original definition or all previous correct user answers
                try:
                    print("\n-------------------------------------------")
                    definitionChoice = int(input("Enter 1. = Get original definition"
                                                 "\nEnter 2. = Get all previous (correct) user answers"
                                                 "\nPlease enter your choice from the given menu: "))
                except ValueError:
                    print("\nPlease enter a number between 1 - 2!")
                    error = True

                # If the error is not true, then the menu is not re-prompted to the user.
                if error == False:
                    break

            #If the user chooses 1, the original definition of the chosen word is displayed.
            if definitionChoice == 1:
                print("\nDefinition of '" + key + "': " + wordsEntered.get(key))
                break

            #If the user chooses 2, all the previous (correct) answers of the user are displayed.
            if definitionChoice == 2:
                print("\n------------------------------------------------------------")
                for definition in quizAnswers[wordAnswers.get(wordChoice)]:
                    print("> " + definition)

    if wordFound == False:
        print("The word you entered wasn't found in the database!")


# The user chooses whether he will be given the word, or the definition in the quiz.
def quizMenu():
    choice = 0
    error = False

    while error == True:
        try:
            # The user chooses whether he will be given the word, or the definition in the quiz.
            choice = int(input("\nEnter 1. = Word based quiz"
                               "\nEnter 2. = Definition based quiz"
                               "\nPlease enter your choice: (1 - 2): "))
            error = False
        except ValueError:
            error = True
            print("Please enter a number between 1 - 2!")

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

    # This variable is used to calculate how much of the questions the user gotten correct.
    score = 0
    # This variable is used to calculate how many questions the user answers.
    questionsAnswered = 0

    print("\nENTER QUIT AT ANYTIME IF YOU WANT TO CANCEL THE QUIZ")

    # The questions are asked (for all the already entered words in the program) - depending on the user's chosen
    # quiz mode.

    if isWord:
        # For each word in the database the question will be asked
        for index, key in enumerate(shuffledWords):
            print("--------------------------------------------------")
            answer = input(f"({index}/{len(shuffledWords)}) - What is the definition of the word: {key}?: ").lower()
            if answer == "quit":
                break

            # Each time a questions is asked in the quiz, this variable is incremented by one.
            questionsAnswered += 1

            # The answer is initially set to incorrect.
            answerCorrect = False

            # The program goes through each word in wordAnswers.
            for word in wordAnswers:
                # if the word matches the current word in the quiz...
                if word == key:
                    # the program gets the index of the word and uses the index to check the existing definitions /
                    # answers for the current word.
                    for definition in quizAnswers[wordAnswers.get(key)]:
                        # If the user's answer matches any of the previously entered answers for the current word, his
                        # answer is instantly / automatically set to correct.
                        if answer == definition:
                            answerCorrect = True
                        else:
                            pass

            # If the program finds the answer to be correct from previously answered (correct) answers, the score is
            # incremented by one and the user is displayed a correct answer message.
            if answerCorrect:
                score += 1
                print("\nYour answer is correct!")
            else:
                # if the program doesn't find the answer, it asks the user if he thinks that his answer is correct.
                print("\nYour answer: " + answer)
                print("Correct answer: " + shuffledWords.get(key))

                while True:
                    isCorrect = input("\n(If yes, your answer will be saved in the program's database and when you "
                                      "enter the same answer in the future it will immediately mark your answer as"
                                      " correct)\nThe answer you entered wasn't found in any of the program's saved "
                                      "(correct) answers. Do you think your answer is correct? (yes : no): ").lower()
                    if isCorrect == "yes":
                        # If the user marks his answer as correct, the score is incremented by 1 and his answer is saved
                        score += 1
                        quizAnswers[wordAnswers.get(key)].append(answer)
                        break
                    elif isCorrect == "no":
                        # If the user marks his answer as incorrect, the program moves on to the next question
                        break

    elif not isWord:
        # For each word in the database the question will be asked
        for index, key in enumerate(shuffledWords):
            # The user is prompted to answer the question
            print("--------------------------------------------------")
            answer = input(f"({index}/{len(shuffledWords)}) - What is the word coming from the definition:"
                           f"\n> {shuffledWords.get(key)}"
                           f"\nEnter your answer (word): ").lower()
            if answer == "quit":
                # If the user enters quit the quiz will immediately stop and display the score the user achieved
                # depending on the amount of questions he had been prompted so far.
                break

            # The amount of questions prompted / asked to the user is incremented by 1
            questionsAnswered += 1

            print("\nYour answer: " + answer)
            print("Correct answer: " + key)

            # If the user's answer matches to the word corresponding to the given definition, the user gains score.
            if answer == key:
                print("Result: Correct!")
                score += 1
            elif not answer == key:
                print("Result: Incorrect!")

    # Total score is displayed
    print("------------------------------------------------")
    print("\nYour total score was: {0:.2f}%".format((score / questionsAnswered) * 100))


def menu():
    while (True):

        # Menu is displayed and the user makes his choice.
        print("\n-----------------------------------------------")
        print("Enter 1. = Enter new word and its definition")
        print("Enter 2. = Look up word for its definition")
        print("Enter 3. = Play quiz")
        print("Enter 4. = Quit")
        print("-----------------------------------------------")

        try:
            choice = int(input("Enter your choice (1 - 4): "))
        except ValueError:
            print("\nPlease enter a number between 1 - 4!")
            continue
        if (choice == 1):
            # The user enters a new word into the program's database.
            enterWord()
        elif (choice == 2):
            # If at least 1 word has been entered before in the program, the method lookUpWord() is called.
            if len(wordsEntered) > 0:
                lookUpWord()
            else:
                print("A word hasn't been entered into the database yet!")
        elif (choice == 3):
            # If at least 1 word has been entered before in the program, the method quizMenu() is called.
            if len(wordsEntered) > 0:
                quizMenu()
            else:
                print("A word hasn't been entered into the database yet!")
        elif (choice == 4):
            # The program is closed after all data is saved.
            saveData()
            break
        else:
            print("\nInvalid input! please enter a number between 1 and 3")

menu()