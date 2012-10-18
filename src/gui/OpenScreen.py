'''
Created on Oct 6, 2012

@author: Arvind Krishnaa Jagannathan
@author: Ramitha Chitloor
'''
import pygtk
pygtk.require('2.0')
import gtk
from GameScreen import GameScreen

class Base:
    def destroy(self, widget, data = None):
        print "you have closed the window"
        gtk.main_quit() 
        
    def setPlayerA(self,widget):
        print widget.get_active_text()
        self.playerA = widget.get_active_text()
        
    def setPlayerB(self,widget):
        print widget.get_active_text()
        self.playerB = widget.get_active_text()
        
    def getPlayerA (self):
        return self.playerA
    
    def getPlayerB(self):
        return self.playerB      
     
    def textChange(self,widget):
        print widget.get_text()
        return widget.get_text()
    
    def openGame(self,widget):
        game = GameScreen()
        print self.getPlayerA()
        print self.getPlayerB()
        game.start(self.getPlayerA(),self.getPlayerB())
        #gtk.main_quit()
            
    def __init__(self):
        self.playerA = "RandomAgent"
        self.playerB = "RandomAgent"
        
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_size_request(200,150)
        self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.window.set_title("Chowka-Bhara")
        self.window.set_tooltip_text("Game of dice!")
        
        self.buttonExit = gtk.Button("EXIT")
        self.buttonExit.connect("clicked",self.destroy)
        self.buttonExit.set_tooltip_text("Click to exit")
        
        self.buttonPlay = gtk.Button("Play")
        self.buttonPlay.connect("clicked",self.openGame)
        self.buttonPlay.set_tooltip_text("Click to start game")
                
        self.labelPlayerA = gtk.Label("Choose Player A")
        self.comboPlayerA = gtk.combo_box_entry_new_text()
        self.comboPlayerA.connect("changed", self.setPlayerA)
        self.comboPlayerA.append_text("NaiveAgent")
        self.comboPlayerA.append_text("RandomAgent")
        self.comboPlayerA.append_text("IntelligentAgent")
        
        self.labelPlayerB = gtk.Label("Choose Player B")
        self.comboPlayerB = gtk.combo_box_entry_new_text()
        self.comboPlayerB.connect("changed", self.setPlayerB)
        self.comboPlayerB.append_text("NaiveAgent")
        self.comboPlayerB.append_text("RandomAgent")
        self.comboPlayerB.append_text("IntelligentAgent")
       
        #Packing to the box containers
        self.box2 = gtk.HBox()
        self.box2.pack_start(self.buttonExit,False,False,25)
        self.box2.pack_start(self.buttonPlay,False,False,50)
        
        self.box1 = gtk.VBox()
        self.box1.pack_start(self.labelPlayerA,False)
        self.box1.pack_start(self.comboPlayerA,False)
        self.box1.pack_start(self.labelPlayerB,False)
        self.box1.pack_start(self.comboPlayerB,False)
        self.box1.pack_start(self.box2,False)
               
        self.window.add(self.box1)
        self.window.show_all()
        self.window.connect("destroy",self.destroy)
        
    def main(self):
        gtk.main()

if __name__ == '__main__':
    base = Base()
    base.main()