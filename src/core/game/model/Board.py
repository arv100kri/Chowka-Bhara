'''
Created on 02-Oct-2012

@author: Arvind Krishnaa Jagannathan
@author: Ramitha Chitloor
'''
from core.game.model.Dice import Dice
from core.game.model.Player import Player
from core.game.model.Square import Square
from sets import Set
from core.game.utility import SimpleMath
import random
import sys

class Board(object):
    '''
    Board Class
    1. Dimensions of the board
    2. List of squares -- instantiated by the board class
    3. List of players -- instantiated by the board class, identify the computer player
            -- Once a player has finished the game, delete the player from this list and add it to the "WinnerQueue"
            -- Head of the WinnerQueue is the 1st winner
    4. Turn -- determines who is the current player an integer
    5. DiceValue - the value of the 4 dices
    6. ChoosePawn(Player, diceValue) -- > Returns a pawn
            if computer: AI - Instantiates one object for the game and calls the function
            else if Human: WaitForHumanInput()
    7. isHit(Square, Pawn) -- If Pawn goes to Square, is there a hit.
                                if there is a hit, then reset the position of the pawn which got hit (!SafeSquare)
    8. isCanPawnMove()
                    -- Updates the status of each pawn of the current player to whether
                    it can be moved from its current location to a location indicated by diceValue
    
    --> Turn switch
    '''
    __playersList = []
    __currentPlayer = Player("None",[],0,False)
    __otherPlayer = Player("None", [], 0, False)
    __squaresDictionary = {}
    __dice = 0
    __dimension = 5
    __winner = Player("None",[],0,False)
    __isTerminated = False
    
    infinity = 9999999999999
    
    def __init__(self, playersList, d):
        '''
        Constructor
        '''
        if len(playersList)!=0:
            self.__playersList = playersList
            self.__dimension = d
            self.__currentPlayer = self.__playersList[0]
            self.__otherPlayer = self.__playersList[1]
            for i in range(0, self.__dimension):
                for j in range(0, self.__dimension):
                    ''' Goal Square '''
                    dimension = self.__dimension-1
                    if i == dimension/2 and j == dimension/2:                
                        self.__squaresDictionary[(i,j)] = Square((i,j), [], True, True)
                    #For dimension = 5X5 Safe Squares
                    elif (i==dimension/2 and j==0) or (i==0 and j==dimension/2) or (i==dimension and j==dimension/2) or (i==dimension/2 and j==dimension):
                        self.__squaresDictionary[(i,j)] = Square((i,j), [], True, False)
                    else:
                        self.__squaresDictionary[(i,j)] = Square((i,j), [], False, False)
    
    def isTerminated(self):
        return self.__isTerminated
    
    def getDiceValue(self):
        return self.__dice
    
    def setDiceValue(self):
        self.__dice = Dice.generateRandom()
            
    def copy(self):
        return Board(self.__playersList, self.__dimension)
    
    def setCurrentPlayer(self, player):
        self.__currentPlayer = player

    def setOtherPlayer(self, player):
        self.__otherPlayer = player
        
    def getCurrentPlayer(self):
        return self.__currentPlayer
    
    def getOtherPlayer(self):
        return self.__otherPlayer
        
    def isHit(self, squareToCheck, pawnMoved):
        if(squareToCheck.isSafeSquare() == False):
            playerName = pawnMoved.getName()[0]
            playerSet = []
            playersOnSquare = squareToCheck.getPlayersOnSquare(playerSet)
            for player in playersOnSquare:
                if(player.getPlayerName() != playerName):
                    return True
        return False
                    
    def choosePawn(self):
        movablePawnsList = self.getMovablePawns(self.__dice)
        pawnId = random.randint(0, len(movablePawnsList))
        while pawnId >= len(movablePawnsList):
            pawnId = random.randint(0, len(movablePawnsList))
        chosenPawn = movablePawnsList[pawnId]
        return chosenPawn
    
    def movePawn(self, pawn, diceValue):
        tuplePawnIdPosition = (-1,(0,0))
        if pawn is not None:
            pawn.setCumulativeDiceValue(diceValue, False)
            if pawn.getCumulativeDiceValue() >= 25:
                pawn.forceSet(24)
            newPawnPosition = self.__currentPlayer.getPathArray()[pawn.getCumulativeDiceValue()]
            pawn.setPosition(newPawnPosition)
            newPawnSquare = self.__squaresDictionary[newPawnPosition]
            if(newPawnSquare.isGoalSquare() == True):
                pawn.setIsActive(False)
                self.__currentPlayer.getPawnList().remove(pawn)
                if(len(self.__currentPlayer.getPawnList()) ==0):
                    self.__winner = self.__currentPlayer
                    self.terminate()
            if self.isHit(newPawnSquare, pawn):
                playerName = self.__currentPlayer.getPlayerName()
                playersOnSquare = newPawnSquare.getPlayersOnSquare()
                for player in playersOnSquare:
                    if(player.getPlayerName() != playerName):
                        pawnsHit = newPawnSquare.getPawnsOnSquareForAPlayer(player)
                        for pawn in pawnsHit:
                            pawn.setCumulativeDiceValue(0, True)
                            pawn.setPosition(player.getPathArray([0]))    
            tuplePawnIdPosition = (pawn.getName()[1], newPawnPosition)
            tempPlayer = self.__currentPlayer
            self.setCurrentPlayer(self.__otherPlayer)
            self.setOtherPlayer(tempPlayer)
        return tuplePawnIdPosition
        
        
    def getMovablePawns(self, diceValue):
        pawnListOfCurrentPlayer = self.__currentPlayer.getPawnList()
        movablePawnsList = []
        for pawn in pawnListOfCurrentPlayer:
            j = pawn.getCumulativeDiceValue()
            # print "CHECKING: ", j+diceValue
            for i in range(1,diceValue):
                position = self.__currentPlayer.getPathArray()[(j+i)%25]
                checkingSquare = self.__squaresDictionary[position]
                otherPlayerPawns = checkingSquare.getPawnsOnSquareForAPlayer(self.__otherPlayer)
                if len(otherPlayerPawns) >= 2:
                    #Check for the destination square
                    if i==diceValue:
                        pawn.setIsMovable(False)
                        pawn.getHasBeenBlocked(True)
                        break
                    #Check for intermediate squares
                    else:
                        if pawn.getHasBeenBlocked() == True:
                            pawn.setIsMovable(True)
                            break
                        else:
                            pawn.getIsMovable(False)
                            pawn.setHasBeenBlocked(True)
                            break                   
            if pawn.getIsMovable() == True:
                movablePawnsList.append(pawn)    
        #Return those pawns which has the isMovable property as true
        return movablePawnsList
    
    def getDistanceOfClosestOpponent(self, positionInPathArray): #positionInPathArray = cumulativeDiceValue
        i = 1
        broken = False
        if positionInPathArray-1>=0:
            for j in (positionInPathArray-1, -1,-1):
                if j<len(self.__currentPlayer.getPathArray()):
                    positionTuple = self.__currentPlayer.getPathArray()[j]
                    # print "J: ", j
                    squareToCheck = self.__squaresDictionary[positionTuple]
                    players = Set()
                    squareToCheck.getPlayersOnSquare(players);
                    if self.__otherPlayer.getPlayerName() in players:
                        broken = True
                        break
                    i+=1
                if broken!=True:
                    lengthEnd = len(self.__currentPlayer.getPathArray())
                    for j in (lengthEnd -1, positionInPathArray, -1):
                        if j<len(self.__currentPlayer.getPathArray()):
                            positionTuple = self.__currentPlayer.getPathArray()[j]
                            squareToCheck = self.__squaresDictionary[positionTuple]
                            players = Set()
                            squareToCheck.getPlayersOnSquare(players);
                            if self.__otherPlayer.getPlayerName() in players:
                                break;
                            i+=1
        return i
            
    
    #The pawn to be evaluated will only be a pawn which can be moved
    def naiveEvaluationFunction(self, pawnToBeEvaluated, diceValue):
        # print "FINAL POSITION INDEX: ", pawnToBeEvaluated.getCumulativeDiceValue()+ diceValue
        finalPawnPosition = self.__currentPlayer.getPathArray()[(pawnToBeEvaluated.getCumulativeDiceValue()+ diceValue)%25]
        squareToCheck = self.__squaresDictionary[finalPawnPosition]
        #Distance from the goal
        distanceToGoalSquare = len(self.__currentPlayer.getPathArray()) - (pawnToBeEvaluated.getCumulativeDiceValue()+ diceValue)
        if distanceToGoalSquare == 0:
            return self.infinity
        evaluatedValue = 1;
        #Check for an opponent pawn being hit
        if(self.isHit(squareToCheck, pawnToBeEvaluated)):
            evaluatedValue+=10
        #Check for double+ formation
        if(len(squareToCheck.getPawnsOnSquareForAPlayer(self.__currentPlayer))>=1):
            evaluatedValue+=7
        #Check for safe square
        if(squareToCheck.isSafeSquare() == True):
            evaluatedValue+=8
        #Check for the reachability
        distanceToClosestOpponentPawn = self.getDistanceOfClosestOpponent(pawnToBeEvaluated.getCumulativeDiceValue() + diceValue)
        if distanceToClosestOpponentPawn > 8:
            evaluatedValue+=6
        elif distanceToClosestOpponentPawn > 4:
            evaluatedValue+=5
        elif distanceToClosestOpponentPawn > 3:
            evaluatedValue+=4
        elif distanceToClosestOpponentPawn > 2:
            evaluatedValue+=3
        elif distanceToClosestOpponentPawn > 1:
            evaluatedValue+=2
        else:
            evaluatedValue+=1
        return evaluatedValue/float(distanceToGoalSquare)    
     
    def printList(self,pawnsList):
        for pawn in pawnsList:
            print pawn.getName()[1]," " 
    
    def getPawnIdOfPawnToMoveNaively(self, diceValue):
        #Assume player is A
        movablePawnsList = self.getMovablePawns(self.__dice)
        Eval = 0
        pawnId = -1
        #first level
        for pawn in movablePawnsList:
            evaluationValue = self.naiveEvaluationFunction(pawn, self.__dice)
            print "Evaluation Function for the pawn ", pawn.getName()[1]," being chosen is: ", evaluationValue
            if evaluationValue > Eval:
                Eval = evaluationValue
                pawnId = pawn.getName()[1]
        return pawnId
                
    def getPawnIdOfPawnToMoveThroughAI(self, diceValue):
        #Assume player is A
        movablePawnsList = self.getMovablePawns(self.__dice)
        print "Number of pawns available: ", len(movablePawnsList)
        print "Available pawns to move for player: ", self.printList(movablePawnsList)
        print "\n=======================================================================\n"
        pawnIdValueDictionary = {}
        pawnIdPotentialDicePawnIdTupleList = []
        evaluationValuesToBeConsideredList = []
        #first level
        for pawn in movablePawnsList:
            print "Pawn under consideration", pawn.getName(), "\n"
            evaluationValue = self.naiveEvaluationFunction(pawn, self.__dice)
            print "Naive Level 1 evaluation: ", evaluationValue
            pawnIdValueDictionary[pawn.getName()[1]] = evaluationValue
            assumedBoardPosition = self.copy()
            assumedBoardPosition.movePawn(pawn, diceValue)
            #Now player becomes B
            potentialPawnIdValueTupleList = []
            potentialEvaluationList = []
            pawnIdPotentialDicePawnIdTupleList = []
            for otherPlayerDiceValue in (1,2,3,4,8):
                potEvaluation = 0
                for otherPlayerPawn in assumedBoardPosition.getMovablePawns(otherPlayerDiceValue):
                    potentialEvaluation = assumedBoardPosition.naiveEvaluationFunction(otherPlayerPawn, otherPlayerDiceValue)
                    potentialPawnIdValueTuple = (otherPlayerPawn.getName()[1], potentialEvaluation)
                    if(len(potentialPawnIdValueTupleList) == 0):
                        potentialPawnIdValueTupleList.insert(0, potentialPawnIdValueTuple)
                        potEvaluation = potentialEvaluation
                    else:
                        potEval = potentialPawnIdValueTupleList[0][1]
                        if potentialEvaluation > potEval:
                            potentialPawnIdValueTupleList.insert(0, potentialPawnIdValueTuple)
                            potEvaluation = potentialEvaluation
                #Have a tuple of the form (Di,P)
                #Form a ordered tuple (FirstLevelPawn, (Di,P))
                orderedTuple = (pawn.getName()[1], (otherPlayerDiceValue, potentialPawnIdValueTupleList[0][0]))
                pawnIdPotentialDicePawnIdTupleList.append(orderedTuple)
                #Add the evaluation function of this pawn to the list#
                potentialEvaluationList.append(potEvaluation)
            #    pawnIdValueDictionary    #
            #----------(P1 => V1)------------------#
            #    pawnIdPotentialDicePawnIdTupleList    #    #    potentialEvaluationList    #
            #----------(P1,(D1,q))-------------------#        # Evaluation(D1,q)    #
            #----------(P1,(D2,q))-------------------#        # Evaluation(D1,q)    #
            #----------(P1,(D3,q))-------------------#        # Evaluation(D1,q)    #
            #----------(P1,(D4,q))-------------------#        # Evaluation(D1,q)    #
            #----------(P1,(D8,q))-------------------#        # Evaluation(D1,q)    #
            counterForPotentialEvaluationList = 0
            #print potentialEvaluationList, "LENGTHLIST: ", len(pawnIdPotentialDicePawnIdTupleList)
            for pawnIdPotentialDicePawnIdTuple in pawnIdPotentialDicePawnIdTupleList:
                potentialDiceValue = pawnIdPotentialDicePawnIdTuple[1][0]
                potentialPawnMovedId = pawnIdPotentialDicePawnIdTuple[1][1]
                pawn2 = assumedBoardPosition.getCurrentPlayer().getPawnWithPawnName(potentialPawnMovedId)
                assumedBoardPosition.movePawn(pawn2, potentialDiceValue)
                #Player is now A
                overallEvaluation = pawnIdValueDictionary[pawn.getName()[1]] 
                #if counterForPotentialEvaluationList == len(potentialEvaluationList):
                #    counterForPotentialEvaluationList%= len(potentialEvaluationList)
                #print "LENGTH: ", len(potentialEvaluationList), "COUNTER: ", counterForPotentialEvaluationList
                overallEvaluation-= potentialEvaluationList[counterForPotentialEvaluationList]  #V1 - Ei
                counterForPotentialEvaluationList+=1
                
                #Updated the value from choice of player B                
                # Now pawns P1,q have been moved. Perform a naive evaluation for each of pawns P1,P2,P3,P4
                #Second Level
                for secondLevelDiceValue in (1,2,3,4,8):
                    evaluationValueLevel2 = 0    
                    for pawn3 in assumedBoardPosition.getMovablePawns(secondLevelDiceValue):
                        evaluationLevel2 = assumedBoardPosition.naiveEvaluationFunction(pawn3, secondLevelDiceValue)
                        if evaluationLevel2 > evaluationValueLevel2:
                            evaluationValueLevel2 = evaluationLevel2
                    overAllEvaluationLevel2 = overallEvaluation + evaluationValueLevel2     #V1-E1+Fi
                    evaluationValuesToBeConsideredList.append(overAllEvaluationLevel2)
            
            finalEvaluator = SimpleMath.find_average(evaluationValuesToBeConsideredList)
            pawnIdValueDictionary[pawn.getName()[1]] = finalEvaluator
            print "Evaluation value of ", pawn.getName(), " is: ", finalEvaluator
        #Every pawn's heuristic value has been found out
        
        Max = 0
        chosenOne = -1
        for PawnName,EvaluationValue in pawnIdValueDictionary.iteritems():
            if Max < EvaluationValue:
                chosenOne = PawnName
                Max = EvaluationValue
        
        return chosenOne
    
    def terminate(self):
        print "Game Over", self.__currentPlayer.getPlayerName(), " wins the game"
        sys.exit()