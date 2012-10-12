'''
Created on Oct 6, 2012

@author: Arvind Krishnaa Jagannathan
@author: Ramitha Chitloor
'''

class SimpleMath(object):
    
    def __init__(self):
        '''
        Constructor
        '''
    
    @staticmethod
    def find_average(List):    #finds the average of the numbers in this list
        Sum = 0
        length = len(List)
        if(length == 0):
            return 0
        for x in List:
            Sum+=x
        return Sum/length
        