# person.py

import numpy as np

class Person:
    def remove_dice(self, banned_numbers):
        self.diceBox = np.setdiff1d(self.diceBox, banned_numbers)
        
    def __init__(self, name, numDices, diceType):
        self.name = name
        self.diceBox = np.random.randint(1, diceType + 1, size=numDices)

    
