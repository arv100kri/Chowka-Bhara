'''
Created on 27-Sep-2012

@author: Arvind Krishnaa Jagannathan
@author: Ramitha Chitloor
'''

class Position(object):
    '''
    Defines the (x,y) co-ordinates on the board
    '''

    x = 0
    y = 0

    def __init__(self,x,y):
        '''
        Constructor
        '''
        self.x = x
        self.y = y
        
    def setX(self,x):
        self.x = x
        
    def setY(self,y):
        self.y = y
      