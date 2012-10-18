'''
Created on Oct 6, 2012

@author: Arvind Krishnaa Jagannathan
@author: Ramitha Chitloor
'''

import pygtk
pygtk.require('2.0')
import gtk

from core.game.model.Player import Player
#from core.game.model.Board import Board
from core.game.model.Board2 import Board
from core.game.timing import * 

class GameScreen(gtk.Window):

    def destroy(self, widget, data = None):
        print "you have closed the game window"
        gtk.main_quit() 
    
    def resetTextBox(self,widget):
        #Call this function when the player has moved the position to indicate change of turn
        self.statusTextBox.set_text("Player 2's turn, roll dice")
    
    def computerPlayerMove(self, pawnName, pawnId, currentPos, newPos):
        #pass tuples for the currentPos and newPos
        currentIndex = 5*currentPos[0] + currentPos[1]
        newIndex = 5*newPos[0] + newPos[1]
        print "current pos =", currentPos, "index +", currentIndex
        if pawnName == "blue":
            self.pawnHbox[currentIndex].remove(self.pawnblueButton[pawnId])
            self.pawnHbox[newIndex].pack_start(self.pawnblueButton[pawnId], False)
        if pawnName == "red":
            self.pawnHbox[currentIndex].remove(self.pawnredButton[pawnId])
            self.pawnHbox[newIndex].pack_start(self.pawnredButton[pawnId], False)
        print ("computer player ",pawnName, "changed pos from", currentIndex, "to", newIndex)
        
    def changePawnPosition(self,widget, pawnName, pawnId):
        #Get the next position from the code and use it to change the value here. The index for Hbox is calculated as x*5+y
        #modify this function to get the current position and  next position from the game and add them in place of 0 and 12 here 
        self.pawnHbox[2].remove(widget)
        self.pawnHbox[12].pack_start(widget, False)
        print ("pawn clicked",pawnName,pawnId)
    
    def addImage(self, widget, img):
        widget.add(img)
    
    def start(self, playA, playB):
        self.setDice = 1
        pathArrayA=[(0,2),(0,1),(0,0),(1,0),(2,0),(3,0),(4,0),(4,1),(4,2),(4,3),(4,4),(3,4),(2,4),(1,4),(0,4),(0,3),(1,3),(2,3),(3,3),(3,2),(3,1),(2,1),(1,1),(1,2),(2,2)]
        pathArrayB=[(4,2),(4,3),(4,4),(3,4),(2,4),(1,4),(0,4),(0,3),(0,2),(0,1),(0,0),(1,0),(2,0),(3,0),(4,0),(4,1),(3,1),(2,1),(1,1),(1,2),(1,3),(2,3),(3,3),(3,2),(2,2)]
        self.playerA = Player(playA, pathArrayA, 4, True)
        self.playerB = Player(playB, pathArrayB, 4, False)
        self.gameBoard = Board([self.playerA, self.playerB], 5)
        self.winner =""
        print "Initial State \n"
        self.playerA.printValue()
        self.playerB.printValue()
        print "*************************************************"
        
        self.gamewindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.gamewindow.set_size_request(380,440)
        self.gamewindow.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.gamewindow.set_title("Chowka-Bhara")
        self.gamewindow.show_all()
        
        #getting the images for the squares
        self.pix_safesquare = gtk.gdk.pixbuf_new_from_file("square_safe.png")
        self.pix_safesquare = self.pix_safesquare.scale_simple(75, 75, gtk.gdk.INTERP_BILINEAR)
        self.pix_goalsquare = gtk.gdk.pixbuf_new_from_file("square_goal.png")
        self.pix_goalsquare = self.pix_goalsquare.scale_simple(75, 75, gtk.gdk.INTERP_BILINEAR)
        self.pix_whitesquare = gtk.gdk.pixbuf_new_from_file("square_white.png")
        self.pix_whitesquare = self.pix_whitesquare.scale_simple(75, 75, gtk.gdk.INTERP_BILINEAR)
        
        #getting the images for the pawns
        self.pix_pawnblue = gtk.gdk.pixbuf_new_from_file("pawn_blue.png")
        self.pix_pawnblue = self.pix_pawnblue.scale_simple(10, 10, gtk.gdk.INTERP_BILINEAR)
        self.image_pawnblue = gtk.image_new_from_pixbuf(self.pix_pawnblue)
        self.pix_pawnred = gtk.gdk.pixbuf_new_from_file("pawn_red.png")
        self.pix_pawnred = self.pix_pawnred.scale_simple(10, 10, gtk.gdk.INTERP_BILINEAR)
        self.image_pawnred = gtk.image_new_from_pixbuf(self.pix_pawnred)
        
        #building the board
        self.table = gtk.Table(rows=5, columns=5, homogeneous=False)
        self.table.show()
        self.__dimension = 5
        dimension = self.__dimension-1
        self.images = [5*[None], 5*[None], 5*[None], 5*[None], 5*[None]]
        # building the array of horizontal box containers, one for each cell in the table
        self.pawnHbox = map(lambda i:gtk.HBox(), range(5*5))
        for i in range(5*5):
            y,x = divmod(i, 5)
            self.table.attach(self.pawnHbox[i], x,x+1, y,y+1)
            self.pawnHbox[i].show()
        #Assigning background images for each cell in the table
        for i in range(0, self.__dimension):
            for j in range(0, self.__dimension):
                print ('i=',i,'j=',j)
                if i == dimension/2 and j == dimension/2:                
                    self.images[i][j] = gtk.image_new_from_pixbuf(self.pix_goalsquare)
                elif (i==dimension/2 and j==0) or (i==0 and j==dimension/2) or (i==dimension and j==dimension/2) or (i==dimension/2 and j==dimension):
                    self.images[i][j] = gtk.image_new_from_pixbuf(self.pix_safesquare)
                else:
                    self.images[i][j] = gtk.image_new_from_pixbuf(self.pix_whitesquare)
                self.table.attach(self.images[i][j], i, i+1, j, j+1, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL, xpadding=0, ypadding=0)
                self.images[i][j].show()
        
        #creating 4 pawns for player 1 
        self.pawnblueButton = map (lambda i:gtk.Button(), range(4))
        self.image_pawnblue = map (lambda i:gtk.image_new_from_pixbuf(self.pix_pawnblue), range(4))
        for i in range(4):
            #self.image_pawnblue[i]=gtk.image_new_from_pixbuf(self.pix_pawnblue)
            self.pawnNameId = 'blue'+i.__str__()
            print self.pawnNameId
            self.pawnblueButton[i].add(self.image_pawnblue[i])
            self.pawnblueButton[i].connect("clicked",self.changePawnPosition,"blue",i)
            self.pawnHbox[2].pack_start(self.pawnblueButton[i],False)
        
        #creating 4 pawns for player 2
        self.pawnredButton = map (lambda i:gtk.Button(), range(4))
        self.image_pawnred = map (lambda i:gtk.image_new_from_pixbuf(self.pix_pawnred), range(4))
        for i in range(4):
            #self.image_pawnred[i]=gtk.image_new_from_pixbuf(self.pix_pawnred)
            self.pawnNameId = 'red'+i.__str__()
            print self.pawnNameId
            self.pawnredButton[i].add(self.image_pawnred[i])
            self.pawnredButton[i].connect("clicked",self.changePawnPosition,"red",i)
            self.pawnHbox[22].pack_start(self.pawnredButton[i],False)

        self.labelDice = gtk.Label("")
        
        self.statusTextBox = gtk.Entry()
        self.statusTextBox.set_text("Turn of "+self.gameBoard.getCurrentPlayer().getPlayerName()+" Roll dice")
        
        self.buttonMakeMove = gtk.Button("Make Move")
        self.buttonMakeMove.connect("clicked",self.makeNextMove)
        
        self.buttonRollDice = gtk.Button("Roll Dice")
        self.buttonRollDice.connect("clicked",self.rollDice)
        
        self.box2 = gtk.HBox()
        self.box2.pack_start(self.buttonRollDice)
        self.box2.pack_start(self.labelDice)
        self.box2.pack_start(self.buttonMakeMove)
        
        #Testing image. Can be commented later
        #self.image2=gtk.image_new_from_pixbuf(self.pix_safesquare)
        
        #Vertical containers to hold game and dice buttons
        self.box1 = gtk.VBox()
        self.box1.pack_start(self.table)
        self.box1.pack_start(self.statusTextBox)
        self.box1.pack_start(self.box2)
        self.box1.show()
       

        self.gamewindow.add(self.box1)
        self.gamewindow.show_all()
        self.gamewindow.connect("destroy",self.destroy)
        
        #Dialog boxes for alerts
        self.dialog1 = gtk.MessageDialog(
            parent         = None,
            flags          = gtk.DIALOG_DESTROY_WITH_PARENT,
            type           = gtk.MESSAGE_INFO,
            buttons        = gtk.BUTTONS_OK,
            message_format = "Thank you for playing")
        self.dialog1.set_title('Game Over!')
        self.dialog1.connect('response', lambda dialog1, response: self.dialog1.destroy())
        
        self.dialogRollDice = gtk.MessageDialog(
            parent         = None,
            flags          = gtk.DIALOG_DESTROY_WITH_PARENT,
            type           = gtk.MESSAGE_INFO,
            buttons        = gtk.BUTTONS_OK,
            message_format = "Roll Dice First!")
        self.dialogRollDice.set_title('Alert!')
        self.dialogRollDice.connect('response', lambda dialogRollDice, response: self.dialogRollDice.destroy())

        self.dialogMakeMove = gtk.MessageDialog(
            parent         = None,
            flags          = gtk.DIALOG_DESTROY_WITH_PARENT,
            type           = gtk.MESSAGE_INFO,
            buttons        = gtk.BUTTONS_OK,
            message_format = "Make Move First!")
        self.dialogMakeMove.set_title('Alert!')
        self.dialogMakeMove.connect('response', lambda dialogMakeMove, response: self.dialogMakeMove.destroy())

        
    def rollDice(self,widget):
        if (self.setDice == 1):
            self.setDice = 0
            self.gameBoard.setDiceValue()
            self.labelDice.set_text(str(self.gameBoard.getDiceValue()))
            self.statusTextBox.set_text("Turn of "+self.gameBoard.getCurrentPlayer().getPlayerName()+" Make move")
        else:
            self.dialogMakeMove.show()
            
        
    def makeNextMove(self,widget):
        if (self.setDice == 0):
            self.setDice = 1
            print "Chance of player: ", self.gameBoard.getCurrentPlayer().getPlayerName()
            self.pawnChosen = self.gameBoard.choosePawnIntelligentVsRandom()
            self.currentPlayer = self.gameBoard.getCurrentPlayer().getPlayerName()
            if self.pawnChosen is None:
                print "Player ", self.gameBoard.getCurrentPlayer().getPlayerName(), "does not have any pawns to move this turn"
            else:
                print "Player ", self.gameBoard.getCurrentPlayer().getPlayerName()," has chosen the pawn ", self.pawnChosen.printDetail()
                self.currentPosition = self.pawnChosen.getPosition()
                print "Current pawn position = ", self.currentPosition
            print "dice value = ", self.gameBoard.getDiceValue()              
            Tuple = self.gameBoard.movePawn(self.pawnChosen, self.gameBoard.getDiceValue())
            if Tuple[0]!=-1:
                print "Pawn ", Tuple[0], " is now at the position: ", Tuple[1].getPosition()
            self.newPosition = Tuple[1].getPosition()
            print "self.currentPlayer  ", self.currentPlayer  ,"self.playerA.getPlayerName()", self.playerA.getPlayerName()
            if (self.currentPlayer == self.playerA.getPlayerName()):
                    self.computerPlayerMove("blue", Tuple[0], self.currentPosition, self.newPosition)
            else:
                    self.computerPlayerMove("red", Tuple[0], self.currentPosition, self.newPosition)
            self.statusTextBox.set_text("Turn of "+self.gameBoard.getCurrentPlayer().getPlayerName()+" Roll dice")
            print "======================================================================\n"
            print "State of the board \n"
            print "======================================================================\n"
            self.playerA.printValue()
            print "=======================================================================\n"
            self.playerB.printValue()
            print "=======================================================================\n"
            if self.gameBoard.hasTerminated() == True:
                self.winner = self.gameBoard.getWinner()
                print self.dialog1.show()
        else:
            self.dialogRollDice.show()
            
        
