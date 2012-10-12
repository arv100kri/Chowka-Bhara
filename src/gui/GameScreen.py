'''
Created on Oct 6, 2012

@author: Arvind Krishnaa Jagannathan
@author: Ramitha Chitloor
'''

import pygtk
pygtk.require('2.0')
import gtk

class GameScreen(gtk.Window):
    
    def destroy(self, widget, data = None):
        print "you have closed the game window"
        gtk.main_quit() 
    
    def resetTextBox(self,widget):
        #Call this function when the player has moved the position to indicate change of turn
        self.statusTextBox.set_text("Player 2's turn, roll dice")
    
    def computerPlayerMove(self, pawnName, pawnId, currentPos, newPos):
        #pass tuples for the currentPos and newPos
        currentIndex = currentPos[0] + 5*currentPos[1]
        newIndex = newPos[0] + 5*newPos[1]
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
        
    def start(self):
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

        '''
        #Testing square. To comment out later
        self.button1 = gtk.Button()
        self.image1=gtk.image_new_from_pixbuf(self.pix_pawnblue)
        self.button1.add(self.image1)
        self.button1.connect("clicked",self.changePawnPosition)
        self.button1.set_tooltip_text("pawn button is here")
        self.pawnHbox[0].pack_start(self.button1, False)
        self.button2 = gtk.Button()
        self.image2=gtk.image_new_from_pixbuf(self.pix_pawnblue)
        self.button2.add(self.image1)
        self.button2.connect("clicked",self.changePawnPosition)
        self.button2.set_tooltip_text("pawn button is here")
        self.pawnHbox[0].pack_start(self.button2, False)
        '''
        
        
        self.statusTextBox = gtk.Entry()
        self.statusTextBox.set_text("Player 1's turn, roll dice")
        
        self.buttonDice = gtk.Button("Roll Dice")
        #Insert the randomly generated dice value here
        self.labelDice = gtk.Label("5")
        
        self.box2 = gtk.HBox()
        self.box2.pack_start(self.buttonDice)
        self.box2.pack_start(self.labelDice)
        
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
