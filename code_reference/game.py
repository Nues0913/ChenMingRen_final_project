import random
import numpy as np
from person import Person
def eliminated(person):
    return len(person.diceBox) == 0

def oneGame(player1, player2, numDices, diceType, ban):
    p1 = Person(player1, numDices=numDices, diceType=diceType)
    p2 = Person(player2, numDices=numDices, diceType=diceType)

    rounds = 0

    while True:
        rounds += 1

        if ban:
            p1.remove_dice(ban)
            p2.remove_dice(ban)

        p1.diceBox = np.random.randint(1, diceType + 1, size=len(p1.diceBox))
        p2.diceBox = np.random.randint(1, diceType + 1, size=len(p2.diceBox))

        if eliminated(p1) and eliminated(p2):
            result = "Tie"
            break
        elif eliminated(p1):
            result = p2.name
            break
        elif eliminated(p2):
            result = p1.name
            break

    print(f"{result} wins ")
    print(f"{player1}的最终骰子数字: {p1.diceBox}")
    print(f"{player2}的最终骰子数字: {p2.diceBox}")
    return result, rounds

