import random
import time # time.sleep(n) wait n seconds

#== Generate random number of length n ==
def genNDigits(n):
    res = ""
    number = 0
    lst = []

    firstFlag = True
    
    for i in range(n):

        if firstFlag:
            randomDigit = random.randint(1,9)
            firstFlag = False
        else:
            randomDigit = random.randint(0,9)
            while randomDigit in lst:
                randomDigit = random.randint(0,9)

        lst.append(randomDigit)
        res += str(randomDigit)
        
    return res    

#== Standard game ==
def game():

    print("A random", 4, "digit number is generated... Good luck guessing!")
    answer = genNDigits(4)
    tries = 0
    
    while True:
        tries += 1
        
        guess = input("Guess?: ")
        while not validateGuess(guess, 4):
            guess = input("Guess again: ")
        
        print("You guess " + str(guess))
        res = takeAGuess(guess, answer)
        if res == "44":
            break

    print("\nYou guessed it! The answer is", str(answer), "| Total tries:", str(tries))

    getInput = input(seeAwesomeBot)
    while not validateInput(getInput, ['y','n']):
        print("")
        getInput = input(seeAwesomeBot)

    if getInput == 'y':
        engageCompetitionMode()
        bottedGame(answer, tries)

#==== Game input functions/checks ====

def takeAGuess(guess, answer):
        bulls = 0
        cows = 0
        answerCopy = list(answer)
        for i in range(4):
            if guess[i] in answerCopy:
                cows += 1
                answerCopy.remove(guess[i])
            if guess[i] == answer[i]:
                bulls += 1
        print("Cows:", str(cows), "Bulls:", str(bulls))       
        return str(cows) + str(bulls)


def validateGuess(string, length):
    if not string.isdigit():
        print("Input must only contain digits. Try again.")
        return False
    elif len(string) != length:
        print("Input must contain exactly", length, "digits. Try again.")
        return False
    else:
        return True


#== Botted game ==
## High Level Strategy ##
# Algorithm runs in 2 stages
# 1. Figure out all numbers in the answer
# 2. Figure out position of numbers in the answer
# state and dic used to store current gameboard information
def bottedGame(gameState, yourTries = 0):

    # Bot variables and state    
    dic = {"Exist":[],"DoesNotExist":"9","Answers":[],"Counter":0}
    stage = 0
    state = 0
    tries = 0

    if gameState == "Random":
        answer = genNDigits(4)
        print("Random 4 digit number generated. (Pss. It's " + answer + ")")
    else:
        answer = gameState
        print("Let's see how many tries it takes to generate", answer)
    time.sleep(2)
          
    while True:
        time.sleep(0.5)
        
        tries += 1
        guess = cowbot(stage, state, dic)
        print("Try " + str(tries) + " | Bot guesses " + str(guess))
        res = takeAGuess(guess, answer)
        if res == "44":
            break

        elif stage == 0:        
            if res == "11":
                dic["Exist"].append(guess[0])
                if len(dic["Exist"]) == 4:
                    print("\nI got the list yo:", dic["Exist"],"\n")
                    time.sleep(1)
                    stage += 1
                    state = 0
                    continue
                
            elif res == "00":
                dic["DoesNotExist"] = guess[0]
            else:
                print("Unexpected output for game: " + res)
            state += 1
            
        elif stage == 1:
            if res == "11":
                dic["Answers"].append(guess[state])
                del dic["Exist"][dic["Counter"]] 
                print("\nDigit", state + 1, "confirmed. Next!\n")
                time.sleep(1)
                    
                state += 1
                dic["Counter"] = 0
                if state == 3:
                    stage += 1
                    state = 0
                    
            elif res == "10":
                dic["Counter"] += 1

                if dic["Counter"] == 3 - state:

                    print("\n### Run hyper optimisation! ###")
                    time.sleep(0.5)
                    
                    resCount = dic["Counter"]
                    dic["Answers"].append(dic["Exist"][resCount])
                    del dic["Exist"][resCount]
                    print("\nDigit", state + 1, "confirmed. Next!\n")
                    time.sleep(1)

                    dic["Counter"] = 0
                    state += 1
                    if state == 3:
                        stage += 1
                        state = 0
                
            else:
                print("Unexpected output for game: " + res)
    
    print("\nBot finished guessing! The answer is", str(answer), "| Total tries:", str(tries))

    if yourTries > 0:
        print("\nYour tries:", yourTries)
        if yourTries > tries:
            print("Meh, tighten up your strategy and try harder next time.")
        elif yourTries == tries:
            print("Not bad at all. You matched my bot.")
        else:
            print("Well done. As you realised sometimes a little bit of guessing can outmatch a bot. This is the beauty of human sentience. You are awarded with... Nothing.")

    backToMenu()

# Generates guess based on state and gameboard information        
def cowbot(stage, state, dic):
    if stage == 0:
        return 4 * str(state)

    elif stage == 1:
        tempList = list(4 * str(dic["DoesNotExist"]))

        while dic["Exist"][dic["Counter"]] == "-1":
            dic["Counter"] += 1
            
        tempList[state] = dic["Exist"][dic["Counter"]]
        return "".join(tempList)

    elif stage == 2:

        print("... I have everything I need now >:)\n")
        time.sleep(1.5)

        counter = 0
        while dic["Exist"][counter] == "-1":
            counter += 1
        
        return "".join(dic["Answers"]) + (dic["Exist"][counter])

    else:
        print("Unexpected output for cowbot")

#==== User interface functions ====

def backToMenu():
    input("\nPress ENTER to go back.\n")    
    print("I'm taking you back to the main menu... \n")
    time.sleep(0.5)

def validateInput(string, lst):
    if string.lower() not in lst:
        print("Read instructions properly leh.. Try again.")
        return False
    else:
        return True

def engageCompetitionMode():
    print("\n...")
    time.sleep(1)
    print("\n...")
    time.sleep(1)
    print("\nCompetition mode.. engaged.\n")
    time.sleep(1)

mainMenu = "Welcome to Cows and Bulls.\nEnter 'i' to read instructions\nEnter 'p' to play a game\nEnter 'b' to run a botted game\nPress 'q' to quit\nInput: "
instructions = "Here are the rules of this game:\n\nI will generate a random 4 digit number (with no duplicates). And your job is to guess this number. For each number you guessed" + \
               " correctly in the right position, I will award you with a Bull, otherwise you get a Cow instead. Getting 4 Bulls mean you guessed the number correctly. And hey you can try competing with my bot. He is " + \
               "hard to beat though. >:)\nTurns out my bot currently has a bug for some numbers with a certain condition (I don't even know which). Power to anyone if you can spot/fix that bug.\n"
seeAwesomeBot = "Want to see how many tries my bot can do this in? (y/n)\nCompete with the bot: "
    
# User interface
def init():
    while True:
        getInput = input(mainMenu)
        while not validateInput(getInput,['p','b','q','i']):
            print("")
            getInput = input(mainMenu)
        print("")
        getInput = getInput.lower()
        if getInput == 'i':
            print(instructions)
            backToMenu()
        elif getInput == 'p':
            game()
        elif getInput == 'b':
            bottedGame("Random") 
        elif getInput == 'q':
            break

    print("Bye. Enter 'init()' to start me again.")

init()
    


















