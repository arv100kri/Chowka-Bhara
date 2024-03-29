
'''
Created on 27-Sep-2012

@author: Arvind Krishnaa Jagannathan
@author: Ramitha Chitloor
'''
class Square(object):
    '''
    The square class models each square on the game board
    1. The (x,y) co-ordinate value of the square
    2. The list of pawns on that particular square --> Pawns will have identifying 
    information about which player it belongs to
    3. Indicates if this square is a safe square
    4. Indicates if this square is a goal square
    '''

    __position = (0,0)
    __pawnList = []
    __isSafeSquare = False
    __isGoalSquare = False
    
    def __init__(self, position, pawnList, isSafeSquare, isGoalSquare):
        '''
        Constructor
        '''
        self.__isSafeSquare = isSafeSquare
        self.__isGoalSquare = isGoalSquare
        self.__pawnList = pawnList
        self.__position = position
    
    '''
        This function will return a set of tuples (PlayerName, NumberOfPawns of PlayerName) 
    '''
    def getPlayersOnSquare(self):
        playerInformation = []
        for pawns in self.__pawnList:
            playerName = pawns.getName()[0]
            playerInformation.append(playerName)
        return playerInformation
    
    def getPawnsOnSquareForAPlayer(self, player):
        pawnList = []
        for pawn in self.__pawnList:
            playerName = pawn.getName()[0]
            if(playerName == player):
                pawnList.append(pawn)
        return pawnList
    
    def getPosition(self):
        return self.__position
    
    def isSafeSquare(self):
        return self.__isSafeSquare
    
    def isGoalSquare(self):
        return self.__isGoalSquare
    
    def addToPawnList(self, pawn):
        self.__pawnList.append(pawn)
    
    def deleteFromPawnList(self, pawn):
        self.__pawnList.remove(pawn)
        
    def addAllPawnsToList(self, listOfPawns):
        for pawn in listOfPawns:
            self.__pawnList.append(pawn)