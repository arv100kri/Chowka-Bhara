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
        
    def comboText(self,widget):
        print widget.get_active_text()
        if (widget.get_active_text()=="computer"):
            return 1
        else:
            return 0
     
    def textChange(self,widget):
        print widget.get_text()
        return widget.get_text()
    
    def openGame(self,widget):
        game = GameScreen()
        game.start()
        #gtk.main_quit()
            
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_size_request(200,150)
        self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.window.set_title("Chowka-Bhara")
        self.window.set_tooltip_text("Game of dice!")
        
        self.button1 = gtk.Button("EXIT")
        self.button1.connect("clicked",self.destroy)
        self.button1.set_tooltip_text("Click to exit")
        
        self.button2 = gtk.Button("Play")
        self.button2.connect("clicked",self.openGame)
        self.button2.set_tooltip_text("Click to start game")
                
        self.label1 = gtk.Label("Choose player type")
        self.combo = gtk.combo_box_entry_new_text()
        self.combo.connect("changed", self.comboText)
        self.combo.append_text("Human")
        self.combo.append_text("Computer")
        
        self.label2 = gtk.Label("Enter the name of the player")
        self.textbox1 = gtk.Entry()
        self.textbox1.connect("changed", self.textChange)
       
        #Packing to the box containers
        self.box2 = gtk.HBox()
        self.box2.pack_start(self.button1,False,False,25)
        self.box2.pack_start(self.button2,False,False,50)
        
        self.box1 = gtk.VBox()
        self.box1.pack_start(self.label1,False)
        self.box1.pack_start(self.combo,False)
        self.box1.pack_start(self.label2,False)
        self.box1.pack_start(self.textbox1,False)
        self.box1.pack_start(self.box2,False)
               
        self.window.add(self.box1)
        self.window.show_all()
        self.window.connect("destroy",self.destroy)
        
    def main(self):
        gtk.main()

if __name__ == '__main__':
    base = Base()
    base.main()