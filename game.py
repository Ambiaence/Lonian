import statistics 
import time
import copy
import pickle
import random
import numpy 
import sympy
import scipy
from scipy.integrate import quad

class proficiency:
    def __init__(self):
        self.avg = None # Average of last three times
        self.missed = 3 # The number of correct answers before question is considered known
        self.__lastThreeTimes = []

    def newTime(self, time):
        if len(self.__lastThreeTimes) != 0:
            self.__lastThreeTimes.pop(0) 

        self.__lastThreeTimes.append(time)
        if self.missed > 0:
            self.missed = self.missed-1;
            print("Missed", self.missed)
        self.__average(self.avg)

    def miss(self):
        self.missed = 3

    def __average(self, avg):
        self.avg = statistics.mean(self.__lastThreeTimes)
        
class integralMap:
    def __init__(self, numOfQuestions):
        self.__divisions = [] # list of points on the map
        self.__integralSliceLength = 1/numOfQuestions #Length of each sub interval
        print("test")
        f = lambda x: -numpy.log(x) # Function which detrmines the distrobution of weights
        for i in range(0, numOfQuestions-1):
            sliceProgress = self.__integralSliceLength * (i+1) 
            self.__divisions.append(quad(f, 0, sliceProgress)[0])

    def pickRandomIndex(self):
        index = 0
        value = random.uniform(0, 1)
        for x in self.__divisions:
            if value < x:
                return index
            index = index + 1
        return index

    def __function(x):
        return numpy.log(x) 

class pickleFriend:
    def __init__(self):
       print("PickleGuy created")         

    def open(self):
        print("Please enter quiz file name")
        name = input()
        try:
            pickle_in = open(name, "rb")
        except:
            print("Something is wrong")
            
        return pickle.load(pickle_in)
        
    def save(self, obj):
        print("What is the name of the file you want to save?")
        name = input()
        pickle_out = open(name, "wb")
        pickle.dump(obj, pickle_out)
        pickle_out.close()
        return 1

def sortParam(card):
    return card[1].avg
        

def sortByProficiency(cards):  
    numOfMissed = 0
    sortedCards = copy.copy(cards);

    for x in range(0, len(cards)):
        if cards[x][1].missed > 0:     
            numOfMissed = numOfMissed + 1
            sortedCards.insert(0, sortedCards.pop(x))

    sortedCards[numOfMissed:] = sorted(sortedCards[numOfMissed:],key = sortParam, reverse = True)
    return sortedCards

    
    

def newCards():
    cards = []
    for x in range(1,12):
        for y in range(x,12):
            cards.append([[x, y], proficiency()])
    return cards

pf = pickleFriend()

stageOne = True
while(stageOne):
    print("what do you want to do?")
    print("Open Quiz Object from file: 1")
    print("New Quiz Object: 2")
    answer = input()
    if answer == "1":
        cards = pf.open()
        stageOne = False
    if answer == "2":
        cards = newCards()
        stageOne = False 

distro = integralMap(len(cards))
stageTwo = True
while(stageTwo):
    cards = sortByProficiency(cards)
    for x in cards:
        print("[", x[1].missed, x[1].avg, "]", end =" ")

    pairNum = distro.pickRandomIndex()
    prof = cards[pairNum][1]
    pair = cards[pairNum][0]

    if random.uniform(0, 1) > .5: #50/50 for position
        numOne = pair[1]
        numTwo = pair[0]
    else:
        numOne = pair[0]
        numTwo = pair[1]

    print("\n\n",numTwo, "*", numOne)
    start = time.time()
    try:
        answer = int(input())
    except:
        pf.save(cards)

    if answer == numOne*numTwo:
        print("!!!GREAT!!!")
        elapse = time.time() - start 
        prof.newTime(elapse)
    else:
        print("???BOO???")
        print(numTwo, "*", numOne, "=", numOne*numTwo)
        answer = input()
        if answer == "save":
            pf.save(cards)
        else:
            prof.miss()

