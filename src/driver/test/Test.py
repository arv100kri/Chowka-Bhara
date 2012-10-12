'''
Created on 27-Sep-2012

@author: Arvind Krishnaa Jagannathan
@author: Ramitha Chitloor
'''

from core.game.model.Player import Player
#from core.game.model.Board import Board
from core.game.model.Board1 import Board
from core.game.timing import * 

if __name__ == '__main__': 
    pathArrayA=[(0,2),(0,1),(0,0),(1,0),(2,0),(3,0),(4,0),(4,1),(4,2),(4,3),(4,4),(3,4),(2,4),(1,4),(0,4),(0,3),(1,3),(2,3),(3,3),(3,2),(3,1),(2,1),(1,1),(1,2),(2,2)]
    pathArrayB=[(4,2),(4,3),(4,4),(3,4),(2,4),(1,4),(0,4),(0,3),(0,2),(0,1),(0,0),(1,0),(2,0),(3,0),(4,0),(4,1),(3,1),(2,1),(1,1),(1,2),(1,3),(2,3),(3,3),(3,2),(2,2)]
    
    playerA = Player("IntelligentAgent1", pathArrayA, 4, True)
    
    playerB = Player("RandomAgent1", pathArrayB, 4, False)
    gameBoard = Board([playerA, playerB], 5)
    print "Initial State \n"
    playerA.printValue()
    playerB.printValue()
    print "*************************************************"
    while gameBoard.isTerminated()!=True:
        print "Chance of player: ", gameBoard.getCurrentPlayer().getPlayerName()
        gameBoard.setDiceValue()
        print "Dice Value is: ", gameBoard.getDiceValue()
        pawnChosen = gameBoard.choosePawn()
        print "Player ", gameBoard.getCurrentPlayer().getPlayerName()," has chosen the pawn ", pawnChosen.printDetail()
        Tuple = gameBoard.movePawn(pawnChosen, gameBoard.getDiceValue())
        print "Pawn ", Tuple[0], " is now at the position: ", Tuple[1]
        print "======================================================================\n"
        print "State of the board \n"
        print "======================================================================\n"
        playerA.printValue()
        print "=======================================================================\n"
        playerB.printValue()
        print "=======================================================================\n"        