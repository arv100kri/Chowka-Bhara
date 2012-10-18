'''
Created on 02-Oct-2012

@author: Arvind Krishnaa Jagannathan
@author: Ramitha Chitloor
The heuristic function is H4
w1*f1+w2*f2+w3*f3+w4*f4/(w5*f5+w6*f6)
f1: Hitting opponent pawn
f2: Moving to safe square
f3: Out-of-reach --> Distance from the closest opponent pawn behind the curent pawn
f4: Formation of double on outer square
f5: Distance from goal square

w1: 10
w2: 8
w3: [6 for distance>8 .... 1]
w4: 7
w5: distance from the goal square
'''
from core.game.model.Dice import Dice
from core.game.model.Player import Player
from core.game.model.Square import Square
from sets import Set
from core.game.utility import SimpleMath
import random
import sys
import copy

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
    
    def __init__(self, playersList, d, squares= None):
        '''
        Constructor
        '''
        if len(playersList)!=0:
            self.__playersList = playersList
            self.__dimension = d
            self.__currentPlayer = self.__playersList[0]
            self.__otherPlayer = self.__playersList[1]
            if squares is not None:
                self.__squaresDictionary = squares
            else:
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
                self.__squaresDictionary[(0,2)].addAllPawnsToList(self.__currentPlayer.getPawnList())
                self.__squaresDictionary[(4,2)].addAllPawnsToList(self.__otherPlayer.getPawnList())
    
    @staticmethod
    def newcopy(board):
        #playerName, pathArray, numberOfPawns, isComputerPlayer):
        player1 = copy.deepcopy(board.getCurrentPlayer())
        player2 = copy.deepcopy(board.getOtherPlayer())
        player1List = []
        player2List = []
        for pawn in player1.getPawnList():
            player1List.append(copy.deepcopy(pawn))
        for pawn2 in player2.getPawnList():
            player2List.append(copy.deepcopy(pawn2))
        
        player1.setPawnList(player1List)
        player2.setPawnList(player2List)
        newDictionary = {}
        for pos,square in board.getSquaresDictionary().items():
            newDictionary[pos] = copy.deepcopy(square)
                
        return Board([player1, player2], board.__dimension, newDictionary) 
    
    def __deepcopy__(self, memo):
        return self
    
    def isTerminated(self):
        return self.__isTerminated
    
    def getDiceValue(self):
        return self.__dice
    
    def setDiceValue(self):
        self.__dice = Dice.generateRandom()
    
    def getPlayerList(self):
        return self.__playersList
    
    def setCurrentPlayer(self, player):
        self.__currentPlayer = player

    def setOtherPlayer(self, player):
        self.__otherPlayer = player
        
    def getCurrentPlayer(self):
        return self.__currentPlayer
    
    def getOtherPlayer(self):
        return self.__otherPlayer
     
    def getSquaresDictionary(self):
        return self.__squaresDictionary
         
    def index_id(self, pawnlist, pawn):
        i = 0
        for p in pawnlist:
            if p.getName()[1] == pawn:
                break
            i+=1
        return i

        
    def isHit(self, squareToCheck, pawnMoved):
        if(squareToCheck.isSafeSquare() == False):
            playerName = pawnMoved.getName()[0]
            playersOnSquare = squareToCheck.getPlayersOnSquare()
            for player in playersOnSquare:
                if(player != playerName):
                    return True
        return False
                    
    def choosePawnIntelligentVsRandom(self):
        if(self.__currentPlayer.getIsSmartComputerPlayer()):
            pawnId = self.getPawnIdOfPawnToMoveThroughAI(self.__dice) #Here is the AI function
            if pawnId is not None:
                chosenPawn = self.__currentPlayer.getPawnList()[self.index_id(self.__currentPlayer.getPawnList(), pawnId)]
            else:
                return None
            #chosenPawn.setCumulativeDiceValue(chosenPawn.getCumulativeDiceValue() - self.__dice, False)'''
            '''movablePawnsList = self.getMovablePawns(self.__dice)
            if len(movablePawnsList) == 0:
                return None
            randompawnId = random.randint(0, len(movablePawnsList)-1)
            print len(movablePawnsList), " ", randompawnId
            chosenPawn = movablePawnsList[randompawnId]'''
        else:
            movablePawnsList = self.getMovablePawns(self.__dice)
            if len(movablePawnsList) == 0:
                return None
            randompawnId = random.randint(0, len(movablePawnsList)-1)
            print len(movablePawnsList), " ", randompawnId
            chosenPawn = movablePawnsList[randompawnId]
        #self.movePawn(chosenPawn, self.__dice)    
        #MOVE THE CHOSEN PAWN. Let this function not return anything
        return chosenPawn
    
    def choosePawnNaiveVsRandom(self):
        if(self.__currentPlayer.getIsSmartComputerPlayer()):
            pawnId = self.getPawnIdOfPawnToMoveNaively(self.__dice) #Here is the AI function
            if pawnId is not None:
                chosenPawn = self.__currentPlayer.getPawnList()[self.index_id(self.__currentPlayer.getPawnList(), pawnId)]
            else:
                return None
            #chosenPawn.setCumulativeDiceValue(chosenPawn.getCumulativeDiceValue() - self.__dice, False)'''
            '''movablePawnsList = self.getMovablePawns(self.__dice)
            if len(movablePawnsList) == 0:
                return None
            randompawnId = random.randint(0, len(movablePawnsList)-1)
            print len(movablePawnsList), " ", randompawnId
            chosenPawn = movablePawnsList[randompawnId]'''
        else:
            movablePawnsList = self.getMovablePawns(self.__dice)
            if len(movablePawnsList) == 0:
                return None
            randompawnId = random.randint(0, len(movablePawnsList)-1)
            print len(movablePawnsList), " ", randompawnId
            chosenPawn = movablePawnsList[randompawnId]
        #self.movePawn(chosenPawn, self.__dice)    
        #MOVE THE CHOSEN PAWN. Let this function not return anything
        return chosenPawn
    
    def choosePawnIntelligentVsNaive(self):
        if(self.__currentPlayer.getIsSmartComputerPlayer()):
            pawnId = self.getPawnIdOfPawnToMoveThroughAI(self.__dice) #Here is the AI function
            if pawnId is not None:
                chosenPawn = self.__currentPlayer.getPawnList()[self.index_id(self.__currentPlayer.getPawnList(), pawnId)]
            else:
                return None
            #chosenPawn.setCumulativeDiceValue(chosenPawn.getCumulativeDiceValue() - self.__dice, False)'''
            '''movablePawnsList = self.getMovablePawns(self.__dice)
            if len(movablePawnsList) == 0:
                return None
            randompawnId = random.randint(0, len(movablePawnsList)-1)
            print len(movablePawnsList), " ", randompawnId
            chosenPawn = movablePawnsList[randompawnId]'''
        else:
            '''
            movablePawnsList = self.getMovablePawns(self.__dice)
            if len(movablePawnsList) == 0:
                return None
            randompawnId = random.randint(0, len(movablePawnsList)-1)
            print len(movablePawnsList), " ", randompawnId
            chosenPawn = movablePawnsList[randompawnId]
            '''
            pawnId = self.getPawnIdOfPawnToMoveNaively(self.__dice) #Naive Evaluation
            if pawnId is not None:
                chosenPawn = self.__currentPlayer.getPawnList()[self.index_id(self.__currentPlayer.getPawnList(), pawnId)]
            else:
                return None
        #MOVE THE CHOSEN PAWN. Let this function not return anything
        return chosenPawn
    
    def choosePawnIntelligentVsIntelligent(self, h1, h2):
        if self.getCurrentPlayer().getPlayerName()== "IntelligentAgent1":
            pawnId = self.getPawnIdOfPawnToMoveThroughAI(self.__dice, h1) #Here is the AI function
            if pawnId is not None:
                chosenPawn = self.__currentPlayer.getPawnList()[self.index_id(self.__currentPlayer.getPawnList(), pawnId)]
                return chosenPawn
            else:
                return None
        else:
            pawnId = self.getPawnIdOfPawnToMoveThroughAI(self.__dice, h2) #Here is the AI function
            if pawnId is not None:
                chosenPawn = self.__currentPlayer.getPawnList()[self.index_id(self.__currentPlayer.getPawnList(), pawnId)]
                return chosenPawn
            else:
                return None

    def choosePawnNaiveVsNaive(self, h1, h2):
        if self.getCurrentPlayer().getPlayerName()== "NaiveAgent1":
            pawnId = self.getPawnIdOfPawnToMoveNaively(self.__dice, h1) #Here is the AI function
            if pawnId is not None:
                chosenPawn = self.__currentPlayer.getPawnList()[self.index_id(self.__currentPlayer.getPawnList(), pawnId)]
                return chosenPawn
            else:
                return None
        else:
            pawnId = self.getPawnIdOfPawnToMoveNaively(self.__dice, h2) #Here is the AI function
            if pawnId is not None:
                chosenPawn = self.__currentPlayer.getPawnList()[self.index_id(self.__currentPlayer.getPawnList(), pawnId)]
                return chosenPawn
            else:
                return None

    def movePawn(self, pawn, diceValue):
        tuplePawnIdPosition = (-1,(0,0))
        
        if pawn is not None:
            print "The pawn to be moved is ", pawn.getName()," whose Cumulative Dice Value is: ", pawn.getCumulativeDiceValue()
            '''
                Wasteful checking
            '''
            if pawn.getCumulativeDiceValue()+diceValue <25:
                oldPosition = pawn.getPosition()
                pawn.setCumulativeDiceValue(diceValue, False)
                newPawnPosition = self.__currentPlayer.getPathArray()[pawn.getCumulativeDiceValue()]
                pawn.setPosition(newPawnPosition)
                newPawnSquare = self.__squaresDictionary[newPawnPosition]
                tuplePawnIdPosition = (pawn.getName()[1], pawn)
                self.__currentPlayer.getPawnList()[self.index_id(self.__currentPlayer.getPawnList(), tuplePawnIdPosition[0])] = pawn
                if(newPawnSquare.isGoalSquare() == True):
                    pawn.setIsActive(False)
                    self.__currentPlayer.getPawnList().remove(pawn)
                    print pawn.getName()," has reached the goal square"
                    print "The remaining pawns are "
                    for p in self.__currentPlayer.getPawnList():
                        print p.getName()
                    
                if self.isHit(newPawnSquare, pawn):
                    print "Hit detected"
                    playerName = self.__currentPlayer.getPlayerName()
                    playersOnSquare = newPawnSquare.getPlayersOnSquare()
                    for player in playersOnSquare:
                        if(player != playerName):
                            pawnsHit = newPawnSquare.getPawnsOnSquareForAPlayer(player)
                            for pawn1 in pawnsHit:
                                newPawnSquare.deleteFromPawnList(pawn1)
                                pawn1.setCumulativeDiceValue(0, True)
                                pawn1.setPosition(self.__otherPlayer.getPathArray()[0])
                                self.__otherPlayer.getPawnList()[self.index_id(self.__otherPlayer.getPawnList(), pawn1.getName()[1])] = pawn1
                                self.__squaresDictionary[self.__otherPlayer.getPathArray()[0]].addToPawnList(pawn1)
                                print pawn1.getName()," is sent back home"
                
                self.__squaresDictionary[newPawnPosition].addToPawnList(pawn)
                self.__squaresDictionary[oldPosition].deleteFromPawnList(pawn)  
              
        tempPlayer = self.__currentPlayer
        self.setCurrentPlayer(self.__otherPlayer)
        self.setOtherPlayer(tempPlayer)
        return tuplePawnIdPosition
        
        
    def getMovablePawns(self, diceValue):
        pawnListOfCurrentPlayer = self.__currentPlayer.getPawnList()
        movablePawnsList = []
        for pawn in pawnListOfCurrentPlayer:
            print "Checking if the player ", self.__currentPlayer.getPlayerName()," can move the pawn ", pawn.getName()
            if pawn.getCumulativeDiceValue()+diceValue >= 25:
                continue
            j = pawn.getCumulativeDiceValue()
            if j>15:
                movablePawnsList.append(pawn)
            else: #Only on the outer square
                print "Has the pawn ", pawn.getName()," been blocked before: ", pawn.getHasBeenBlocked()      
                for i in range(1,diceValue+1):
                    position = self.__currentPlayer.getPathArray()[j+i]
                    checkingSquare = self.__squaresDictionary[position]
                    otherPlayerPawns = checkingSquare.getPawnsOnSquareForAPlayer(self.__otherPlayer.getPlayerName())
                    if len(otherPlayerPawns) >= 2:
                        #Check for the destination square
                        #Check for intermediate squares
                        if i!=diceValue:
                            if pawn.getHasBeenBlocked() == True: #If it has already been blocked it can move
                                pawn.setIsMovable(True)
                                print "The pawn ", pawn.getName(), " can move"
                                break
                            else:
                                pawn.setIsMovable(False)    #Else this pawn cannot move
                                pawn.setHasBeenBlocked(True)
                                print "There is an opponent double blocking ", pawn.getName()
                                break
                        else:
                            #If its a safe square its ok
                            if checkingSquare.isSafeSquare() ==False:
                                print "There is an opponent double on the destination square for ", pawn.getName()
                                pawn.setIsMovable(False)
                                pawn.setHasBeenBlocked(True)
                            else:
                                pawn.setIsMovable(True)
                            break
                    else:
                        pawn.setIsMovable(True)                   
            if pawn.getIsMovable() == True:
                movablePawnsList.append(pawn)    
        #Return those pawns which has the isMovable property as true
        print "The pawns which can be moved"
        for pawn in movablePawnsList:
            print pawn.getName()
        return movablePawnsList
    
    
    def getDistanceOfClosestOpponent(self, pawn, diceValue): 
        pawnDistanceToGoal = len(self.__currentPlayer.getPathArray()) - (pawn.getCumulativeDiceValue()+ diceValue)
        distance = 8
        for opponentPawn in self.__otherPlayer.getPawnList():
            opponentPawnDistanceToGoal = len(self.__otherPlayer.getPathArray()) - opponentPawn.getCumulativeDiceValue()
            if opponentPawnDistanceToGoal != pawnDistanceToGoal:
                newDistance = 8 - (pawnDistanceToGoal - opponentPawnDistanceToGoal)
                if newDistance < distance and newDistance > 0:
                    distance = newDistance
        return distance
            
    
    #The pawn to be evaluated will only be a pawn which can be moved
    def naiveEvaluationFunction(self, pawnToBeEvaluated, diceValue, heuristic):
        # print "FINAL POSITION INDEX: ", pawnToBeEvaluated.getCumulativeDiceValue()+ diceValue
        finalPawnPosition = self.__currentPlayer.getPathArray()[(pawnToBeEvaluated.getCumulativeDiceValue()+ diceValue)%25]
        squareToCheck = self.__squaresDictionary[finalPawnPosition]
        #Distance from the goal
        distanceToGoalSquare = len(self.__currentPlayer.getPathArray()) - (pawnToBeEvaluated.getCumulativeDiceValue()+ diceValue)
        evaluatedValue = 1;
        
        if heuristic == 1:
            if(self.isHit(squareToCheck, pawnToBeEvaluated)):
                evaluatedValue+=10
            if(squareToCheck.isSafeSquare() == True):
                evaluatedValue+=8
            #return evaluatedValue
        
        elif heuristic == 4:
            if distanceToGoalSquare == 0:
                return self.infinity
            #Check for an opponent pawn being hit
            if(self.isHit(squareToCheck, pawnToBeEvaluated)):
                evaluatedValue+=10
            #Check for double+ formation on the outer square
            if(len(squareToCheck.getPawnsOnSquareForAPlayer(self.__currentPlayer.getPlayerName()))>=1 and pawnToBeEvaluated.getCumulativeDiceValue()+diceValue<=15):
                evaluatedValue+=7
            #Check for safe square
            if(squareToCheck.isSafeSquare() == True):
                evaluatedValue+=8
            #Check for the reachability
            distanceToClosestOpponentPawn = self.getDistanceOfClosestOpponent(pawnToBeEvaluated, diceValue)
            #print "DISTANCE: ", distanceToClosestOpponentPawn
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
            #Distance to safe square
            if ((pawnToBeEvaluated.getCumulativeDiceValue()+ diceValue)<4):
                distanceToSafeSquare = 4 - (pawnToBeEvaluated.getCumulativeDiceValue()+ diceValue)
            elif ((pawnToBeEvaluated.getCumulativeDiceValue()+ diceValue)<8):
                distanceToSafeSquare = 8 - (pawnToBeEvaluated.getCumulativeDiceValue()+ diceValue)
            elif ((pawnToBeEvaluated.getCumulativeDiceValue()+ diceValue)<12):
                distanceToSafeSquare = 12 - (pawnToBeEvaluated.getCumulativeDiceValue()+ diceValue)
            else:
                distanceToSafeSquare = 25 - (pawnToBeEvaluated.getCumulativeDiceValue()+ diceValue)
            if distanceToSafeSquare == 0:
                return self.infinity
            evaluatedValue = evaluatedValue/float(distanceToGoalSquare+distanceToSafeSquare)
        
        elif heuristic == 3:
            if(self.isHit(squareToCheck, pawnToBeEvaluated)):
                evaluatedValue+=10
            #Distance to safe square
            if ((pawnToBeEvaluated.getCumulativeDiceValue()+ diceValue)<4):
                distanceToSafeSquare = 4 - (pawnToBeEvaluated.getCumulativeDiceValue()+ diceValue)
            elif ((pawnToBeEvaluated.getCumulativeDiceValue()+ diceValue)<8):
                distanceToSafeSquare = 8 - (pawnToBeEvaluated.getCumulativeDiceValue()+ diceValue)
            elif ((pawnToBeEvaluated.getCumulativeDiceValue()+ diceValue)<12):
                distanceToSafeSquare = 12 - (pawnToBeEvaluated.getCumulativeDiceValue()+ diceValue)
            else:
                distanceToSafeSquare = 25 - (pawnToBeEvaluated.getCumulativeDiceValue()+ diceValue)
            if distanceToSafeSquare == 0:
                return self.infinity
            else:
                evaluatedValue = evaluatedValue/float(distanceToSafeSquare)
        
        elif heuristic == 2:
            if distanceToGoalSquare == 0:
                return self.infinity
            if(self.isHit(squareToCheck, pawnToBeEvaluated)):
                evaluatedValue+=10
            distanceToClosestOpponentPawn = self.getDistanceOfClosestOpponent(pawnToBeEvaluated, diceValue)
            #print "DISTANCE: ", distanceToClosestOpponentPawn
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
            evaluatedValue*= len(self.__currentPlayer.getPawnList())
            evaluatedValue/= float(distanceToGoalSquare)
            
        print "Naive Level 1 evaluation for pawn", pawnToBeEvaluated.getName()[1],"of player: ", self.__currentPlayer.getPlayerName()," when the dice value is: ", diceValue,": ", str(evaluatedValue)
        return evaluatedValue
    
     
    def printList(self,pawnsList):
        for pawn in pawnsList:
            print pawn.getName()[1]
    
    def getPawnIdOfPawnToMoveNaively(self, diceValue, heuristic):
        #Assume player is A
        movablePawnsList = self.getMovablePawns(diceValue)
        if len(movablePawnsList)==0:
            print "There is no pawn for ", self.__currentPlayer.getPlayerName(),""
            return None
        Eval = 0
        pawnId = -1
        #first level
        for pawn in movablePawnsList:
            evaluationValue = self.naiveEvaluationFunction(pawn, self.__dice, heuristic)
            print "Evaluation Function for the pawn ", pawn.getName()[1]," being chosen is: ", evaluationValue
            if evaluationValue > Eval:
                Eval = evaluationValue
                pawnId = pawn.getName()[1]
        return pawnId
                
    def getPawnIdOfPawnToMoveThroughAI(self, diceValue, heuristic):
        #Assume player is A
        #movablePawnsList = self.getMovablePawns(self.__dice)
        print "\n======================AI Simulation=====================================\n"
        movablePawnsList = self.getMovablePawns(diceValue)
        if len(movablePawnsList)==0:
            print "There is no pawn for ", self.__currentPlayer.getPlayerName(),""
            return None
        print "Number of pawns available: ", len(movablePawnsList)
        print "Available pawns to move for player: ", self.printList(movablePawnsList)
        print "\n=======================================================================\n"
        pawnIdValueDictionary = {}
        pawnIdPotentialDicePawnIdTupleList = []
        #first level
        for pawn in movablePawnsList:
            print "Pawn under consideration", pawn.getName(), "\n"
            evaluationValuesToBeConsideredList = []
            evaluationValue = self.naiveEvaluationFunction(pawn, self.__dice, heuristic)
            pawnIdValueDictionary[pawn.getName()[1]] = evaluationValue
            assumedBoardPosition = Board.newcopy(self)
            
            print "The pawn moved is ", pawn.getName()
            mytuple = assumedBoardPosition.movePawn(copy.deepcopy(pawn), diceValue)
            #assumedBoardPosition.__otherPlayer.getPawnList()[int(mytuple[0])] = copy.deepcopy(mytuple[1])
            #Now player becomes B
            potentialPawnIdValueTupleList = []
            potentialEvaluationList = []
            pawnIdPotentialDicePawnIdTupleList = []
            for otherPlayerDiceValue in (1,2,3,4,8):
                potEvaluation = 0
                secondMovablePawns = assumedBoardPosition.getMovablePawns(otherPlayerDiceValue)
                if len(secondMovablePawns) ==0:
                    continue
                for otherPlayerPawn in secondMovablePawns:
                    potentialEvaluation = assumedBoardPosition.naiveEvaluationFunction(otherPlayerPawn, otherPlayerDiceValue, heuristic)
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
                if pawn2 is None:
                    continue
                print "The pawn moved is ", pawn2.getName()
                mysecondtuple = assumedBoardPosition.movePawn(copy.deepcopy(pawn2), potentialDiceValue)
                #assumedBoardPosition.__otherPlayer.getPawnList()[int(mysecondtuple[0])] = copy.deepcopy(mysecondtuple[1])
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
                    depth2List = assumedBoardPosition.getMovablePawns(secondLevelDiceValue)
                    if len(depth2List) == 0:
                        continue    
                    for pawn3 in depth2List:
                        evaluationLevel2 = assumedBoardPosition.naiveEvaluationFunction(pawn3, secondLevelDiceValue, heuristic)
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
        print "\n======================AI Simulation Ends. Chosen Pawn is: ", chosenOne
        if chosenOne == -1:
            if len(movablePawnsList)==0:
                return None
            else:
                chosenPawn = movablePawnsList[random.randint(0, len(movablePawnsList)-1)]
                return chosenPawn.getName()[1]
        return chosenOne
    
    def hasTerminated(self):
        if len(self.__currentPlayer.getPawnList()) == 0 or len(self.__otherPlayer.getPawnList()) ==0:
            return True
        return False
    
    def getWinner(self):
        if len(self.__currentPlayer.getPawnList()) == 0:
            return self.__currentPlayer.getPlayerName()
        elif len(self.__otherPlayer.getPawnList()) ==0:
            return self.__otherPlayer.getPlayerName()
        else:
            return "None"  
        