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
        answers = self.listEnglishWords(answers)
        for i in answers:
            #print(i, self.isBoggleable(i))
            if self.isBoggleable(i):
                score += self.SCORING.get(len(i), 0)
                if len(i) >= max(self.SCORING, key=int):
                    score += self.SCORING[max(self.SCORING, key=int)]
        return score

    def isBoggleable(self, word, prevPos=None, depth=0):
        #Recursive function to check if a word can be made from the board
        def isAdjacent(c1, c2):
            if c2==None: return True
            if c1[0]-1 == c2[0] and c1[1] == c2[1]: return True
            elif c1[0] == c2[0] and c1[1]-1 == c2[1]: return True
            elif c1[0]-1 == c2[0] and c1[1]-1 == c2[1]: return True
            elif c1[0]+1 == c2[0] and c1[1] == c2[1]: return True
            elif c1[0] == c2[0] and c1[1]+1 == c2[1]: return True
            elif c1[0]+1 == c2[0] and c1[1]+1 == c2[1]: return True
            elif c1[0]+1 == c2[0] and c1[1]-1 == c2[1]: return True
            elif c1[0]-1 == c2[0] and c1[1]+1 == c2[1]: return True
            else: return False
        items = []
        for row, i in enumerate(self.board):
            try:
                columns = [n for n,val in enumerate(i) if val==word[depth].upper()]
            except:
                continue
            for column in columns:
                items.append([row, column])
        for i in items:
            if isAdjacent(i, prevPos):
                if self.isBoggleable(word, i, depth+1):
                    return True
                elif len(word)==depth+2:
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
