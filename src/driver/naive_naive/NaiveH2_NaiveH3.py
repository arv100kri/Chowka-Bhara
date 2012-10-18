'''
Created on 27-Sep-2012

@author: Arvind Krishnaa Jagannathan
@author: Ramitha Chitloor

NaiveAgent1 Vs NaiveAgent2
N1 = H2
N2 = H3
'''

from core.game.model.Player import Player
from core.game.model.Board4 import Board
from core.game.timing import * 

if __name__ == '__main__': 
    f = open("NaiveH2_NaiveH3.txt", "w")
    for i in range(0,50):
        pathArrayA=[(0,2),(0,1),(0,0),(1,0),(2,0),(3,0),(4,0),(4,1),(4,2),(4,3),(4,4),(3,4),(2,4),(1,4),(0,4),(0,3),(1,3),(2,3),(3,3),(3,2),(3,1),(2,1),(1,1),(1,2),(2,2)]
        pathArrayB=[(4,2),(4,3),(4,4),(3,4),(2,4),(1,4),(0,4),(0,3),(0,2),(0,1),(0,0),(1,0),(2,0),(3,0),(4,0),(4,1),(3,1),(2,1),(1,1),(1,2),(1,3),(2,3),(3,3),(3,2),(2,2)]
        
        playerA = Player("NaiveAgent1", pathArrayA, 4, True)
        
        playerB = Player("NaiveAgent2", pathArrayB, 4, True)
        gameBoard = Board([playerA, playerB], 5)
        winner =""
        print "Initial State \n"
        playerA.printValue()
        playerB.printValue()
        print "*************************************************"
        count = 0
        while True:
            print "Chance of player: ", gameBoard.getCurrentPlayer().getPlayerName()
            gameBoard.setDiceValue()
            print "Dice Value is: ", gameBoard.getDiceValue()
            pawnChosen = gameBoard.choosePawnNaiveVsNaive(2,3)
            if pawnChosen is None:
                print "Player ", gameBoard.getCurrentPlayer().getPlayerName(), "does not have any pawns to move this turn"
            else:
                print "Player ", gameBoard.getCurrentPlayer().getPlayerName()," has chosen the pawn ", pawnChosen.printDetail()
            Tuple = gameBoard.movePawn(pawnChosen, gameBoard.getDiceValue())
            if Tuple[0]!=-1:
                print "Pawn ", Tuple[0], " is now at the position: ", Tuple[1].getPosition()
            print "======================================================================\n"
            print "State of the board \n"
            print "======================================================================\n"
            playerA.printValue()
            print "=======================================================================\n"
            playerB.printValue()
            print "=======================================================================\n"
            count+=1
            if gameBoard.hasTerminated() == True:
                winner = gameBoard.getWinner()
                break
        
        print "Game Over. The winner is ", winner
        print "Total number of moves ", count
        f.write(winner)
        f.write("\t")
        f.write(str(count))
        f.write("\n")
    f.close()