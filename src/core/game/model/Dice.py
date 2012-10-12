'''
Created on 27-Sep-2012

@author: Arvind Krishnaa Jagannathan
@author: Ramitha Chitloor
'''
import random
class Dice(object):
    '''
    Class that simulates the rolling of 4 special dice = shells
    Generate either 0 or 1 for each dice. Final value is the sum of these dice values
    If all the dice values are 0, then final value = 8
    '''


    def __init__(self):
        '''
        Constructor
        '''
    @staticmethod   
    def generateRandom():
        diceValue1 = random.randint(0,1)
        diceValue2 = random.randint(0,1)
        diceValue3 = random.randint(0,1)
        diceValue4 = random.randint(0,1)
        cumulativeDiceValue = diceValue1 + diceValue2 + diceValue3 + diceValue4
        if cumulativeDiceValue == 0:
            cumulativeDiceValue = 8
        return cumulativeDiceValue