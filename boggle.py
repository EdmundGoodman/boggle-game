#Edmund Goodman - Creative Commons Attribution-NonCommercial-ShareAlike 2.5
from random import choice
import os, time, re

class boggle:
    def __init__(self):
        #Initialise variables
        self.SCORING = { 3:1, 4:1, 5:2, 6:3, 7:4, 8:11 }
        #The actual boggle dice values are used to most accurately simulate the game
        self.BOGGLEDICE = ['AACIOT','ABILTY','ABJMOQ','ACDEMP','ACELRS','ADENVZ','AHMORS',
        'BIFORX','DENOSW','DKNOTU','EEFHIY','EGKLUY','EGINTV','EHINPS','ELPSTU','GILRUW']
        self.size = 4

    def generateRandomBoard(self):
        #Randomly generate the board, via the dice, then arrange it into a square
        self.board = ['Qu' if x=='Q' else x for x in [choice(i) for i in self.BOGGLEDICE]]
        self.board = [self.board[i:i+self.size] for i in range(0,len(self.board),self.size)]

    def inputBoard(self):
        self.board = [[input("Letter: ")[0].upper() for _ in range(self.size)] for _ in range(self.size)]
        self.board = ['Qu' if x=='Q' else x for x in self.board]

    def displayBoard(self):
        #Print the board
        for y in self.board:
            print(y)

    def scoreAnswers(self, answers, verbose=True):
        #Get the answers from the user input
        score = 0
        answers = self.onlyEnglishWords( set([i for i in answers.split()]) )
        for i in answers:
            if self.isBoggleable(i):
                if len(i) <= max(self.SCORING, key=int):
                    wordScore = self.SCORING.get(len(i), 0)
                else:
                    wordScore = self.SCORING[max(self.SCORING, key=int)]
                score += wordScore
                if verbose:
                    print("{} is correct, scoring: {}".format(i, wordScore))
            else:
                if verbose:
                    print("{} is incorrect".format(i))
        return score

    def onlyEnglishWords(self, words):
        #Return all the words in the input list which are in the dictionary 'wordList' file
        with open("../gameWinners/wordList.txt") as wordFile:
            englishWords = set(word.strip().lower() for word in wordFile)
        return [word for word in words if word in englishWords]

    def isBoggleable(self, word, prevPos=[], depth=0):
        #A function to check if a word can be made on a boggle board

        def getAdjacent(pos):
            #A helper function that given a position on the board, returns a
            #dictionary with a key of adjacent letters, and a value of a list
            #of adjacent positions
            adj = {}
            for dx, dy in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
                if (pos[0]+dx<0 or pos[0]+dx>=self.size) or (pos[1]+dy<0 or pos[1]+dy>=self.size):
                    continue
                else:
                    x = pos[0]+dx
                    y = pos[1]+dy
                    letter = self.board[y][x][0]
                    if letter in adj:
                        adj[letter].append((x,y))
                    else:
                        adj[letter] = [(x,y)]
            return adj

        #Get the every position of the current letter on the board
        letter = word[depth]
        items = []
        for row, i in enumerate(self.board):
            try:
                columns = [n for n,val in enumerate(i) if val[0]==letter.upper()]
            except:
                continue
            for column in columns:
                items.append([column, row])

        #At the end of the word, exit
        if len(word) == depth+1:
            return True

        #If the letter is a q, skip the following 'u', as the dice is 'Qu'
        if letter == "q":
            depth += 1
        nextLetter = word[depth+1].upper()

        #For each possible next letter, create a branch of the search tree
        for item in items:
            adj = getAdjacent(item)
            if nextLetter in adj:
                for nextPos in adj[nextLetter]:
                    if self.isBoggleable(word, prevPos+[nextPos], depth+1):
                        #print(prevPos, depth)
                        return True

        #If the next letter isn't found, the word is invalid
        return False

    def play(self):
        #Play the game
        os.system('clear')
        self.generateRandomBoard()
        self.displayBoard()
        answers = input("Words: ")
        score = self.scoreAnswers(answers)
        print("You scored: ", score)

    def win(self):
        #Win at boggle, by finding every possible valid word on the grid
        os.system('clear')
        self.inputBoard()
        self.displayBoard()

        #Read in all the allowed words
        with open("../gameWinners/wordList.txt") as wordFile:
            possibleWords = [x.strip().lower() for x in wordFile if len(x)>3]

        #Flatten the board
        validLetters = sum(self.board, [])
        regex = "^[" + "".join(validLetters).lower() + "]*$"
        pattern = re.compile(regex)
        possibleWords = [x for x in possibleWords if bool(pattern.match(x))]

        validWords = []
        for word in possibleWords:
            if self.isBoggleable(word):
                validWords.append(word)

        validWordsString = " ".join(validWords)
        print("Words: ", validWordsString)

        score = self.scoreAnswers(validWordsString, False)
        print("You scored: ", score)

    def menu(self):
        os.system('clear')
        print("Do you want to:")
        print("\t1) Play a round")
        print("\t2) Find all valid words on a board")
        option = input("Enter an option number: ")
        if option == "1":
            self.play()
        elif option == "2":
            self.win()
        else:
            print("Invalid option")


game = boggle()
game.menu()
