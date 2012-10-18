'''
Created on 27-Sep-2012

@author: Arvind Krishnaa Jagannathan
@author: Ramitha Chitloor
'''

class Pawn(object):
    '''
    Class to define the attributes and properties of a pawn
    1. Name of the pawn in the format (PlayerName, i)
    2. The cumulative dice value
    3. Position the pawn is on (x,y)
    '''
    
    @classmethod
    def empty(self):
        '''
            Empty constructor
        '''
        return Pawn("",(0,0))
        
    def __init__(self, name, position, isActive):
        '''
        Initializes the starting position of the pawn for a given player
        position = player.path[0]
        '''
        self.__position = position
        self.__name = name
        self.__cumulativeDiceValue = 0
        self.__isActive = isActive
    
    def __eq__(self, other):
        return self.getName() == other.getName()
    
    def setName(self, name):
        self.name = name
    
    def getName(self):
        return self.__name
    
    def printDetail(self):
        return self.__name[1], "at ", self.__position
    
    def forceSet(self, value):
        self.__cumulativeDiceValue = value
    
    def setCumulativeDiceValue(self,diceValue,isHit):
        if isHit:
            self.__cumulativeDiceValue = 0
        else:
            self.__cumulativeDiceValue+= diceValue 

    def getCumulativeDiceValue(self):
        return self.__cumulativeDiceValue

    def setPosition(self, position):
        self.__position = position
    
    def getPosition(self):
        return self.__position
    
    def getIsActive(self):
        return self.__isActive
    
    def setIsActive(self, isActive):
        self.__isActive = isActive
    
    def setIsMovable(self, isMovable):
        self.__isMovable = isMovable
    
    def setHasBeenBlocked(self, hasBeenBlocked):
        self.__hasBeenBlocked = hasBeenBlocked
        
    def getIsMovable(self):
        return self.__isMovable
    
    def getHasBeenBlocked(self):
        return self.__hasBeenBlocked
    
    __name = ("", 0)
    __cumulativeDiceValue = 0
    __position = (0,0)
    __isActive = True
    __isMovable = True
    __hasBeenBlocked = False