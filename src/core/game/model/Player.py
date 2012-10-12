'''
Created on 27-Sep-2012

@author: Arvind Krishnaa Jagannathan
@author: Ramitha Chitloor
'''
from core.game.model.Pawn import Pawn
class Player(object):
    '''
    Defines the class player which will have
    1. The list of pawns belonging to the player
    2. The name of the player
    3. Path array indicating
        path[x] = the position of a pawn of the player after x moves
    4. Indicates if the player is a computer or a human
    '''
    
    __pawnLists = []
    __pathArray = []
    __playerName = ""
    __numberOfPawns = 4
    __isSmartComputerPlayer = True
    
    def __init__(self, playerName, pathArray, numberOfPawns, isComputerPlayer):
        '''
        Constructor
        '''
        self.__playerName = playerName
        self.__pathArray = pathArray
        self.__numberOfPawns = numberOfPawns
        self.__isSmartComputerPlayer = isComputerPlayer
        self.__pawnLists = []
        for i in range(0,numberOfPawns):
            pawnName = (self.__playerName, i)
            self.__pawnLists.insert(i,Pawn(pawnName, self.__pathArray[0],True))

    def getIsSmartComputerPlayer(self):
        return self.__isSmartComputerPlayer

    def printValue(self):
        print "Player Name is: ", self.__playerName
        print "Path Array is: ", self.__pathArray
        print "Number of pawns are: ", len(self.__pawnLists)
        for i in range(0,len(self.__pawnLists)):
            pawn = self.__pawnLists[i]
            print "Details of the pawn "+ str(pawn.getName()) + "\n Initial Position: "+ str(pawn.getPosition()) + "\n Cumulative Dice Value: " + str(pawn.getCumulativeDiceValue())            
    
    def getPlayerName(self):
        return self.__playerName

    def getPawnList(self):
        return self.__pawnLists
    
    def getPathArray(self):
        return self.__pathArray
    
    def getPawnWithPawnName(self, pawnName):
        for pawn in self.__pawnLists:
            if pawn.getName()[1] == pawnName:
                return pawn