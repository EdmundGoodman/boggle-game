#Edmund Goodman - Creative Commons Attribution-NonCommercial-ShareAlike 2.5
#Boggle Game
from random import choice
import os, time

class boggle:
    def __init__(self):
        #Initialise variables
        self.SCORING = { 3:1, 4:1, 5:2, 6:3, 7:4, 8:11 }
        #The actual boggle dice values are used to most accurately simulate the game
        self.BOGGLEDICE = ['AACIOT','ABILTY','ABJMOQ','ACDEMP','ACELRS','ADENVZ','AHMORS',
        'BIFORX','DENOSW','DKNOTU','EEFHIY','EGKLUY','EGINTV','EHINPS','ELPSTU','GILRUW']
        self.size = 4
        self.board = ['Qu' if x=='Q' else x for x in [choice(i) for i in self.BOGGLEDICE]]
        self.board = [self.board[i:i+self.size] for i in range(0,len(self.board),self.size)]

    def displayBoard(self):
        #Print the board
        for y in self.board:
            print(y)

    def getAnswers(self):
        #Get the answers from the user input
        answers, score = set([i for i in input("Words: ").split()]), 0
        answers = self.onlyEnglishWords(answers)
        for i in answers:
            if self.isBoggleable(i):
                score += self.SCORING.get(len(i), 0)
                if len(i) >= max(self.SCORING, key=int):
                    score += self.SCORING[max(self.SCORING, key=int)]
                print("{} is correct, scoring: {}".format(i, self.SCORING.get(len(i), 0)))
            else:
                print("{} is incorrect".format(i))
        return score


    def isBoggleable(self, word, depth=0):
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
                    letter = self.board[y][x]
                    if letter in adj:
                        adj[letter].append((x,y))
                    else:
                        adj[letter] = [(x,y)]
            return adj

        letter = word[depth]
        items = []
        for row, i in enumerate(self.board):
            try:
                columns = [n for n,val in enumerate(i) if val==word[depth].upper()]
            except:
                continue
            for column in columns:
                items.append([column, row])

        try:
            nextLetter = word[depth+1].upper()
        except IndexError:
            return True

        for item in items:
            adj = getAdjacent(item)
            if nextLetter in adj:
                for nextPos in adj[nextLetter]:
                    if self.isBoggleable(word, depth+1):
                        return True
        return False

    def listEnglishWords(self, words):
        #Return all the words in the input list which are in the dictionary 'wordList' file
        with open("wordList.txt") as wordFile:
            englishWords = set(word.strip().lower() for word in wordFile)
        return [word for word in words if word in englishWords]

    def play(self):
        #Play the game
        os.system('clear')
        self.displayBoard()
        score = self.getAnswers()
        print("You scored: ", score)

game = boggle()
game.play()
