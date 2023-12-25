import random
import numpy as np
import matplotlib.pyplot as plt

class Person:
    def __init__(self, name, numDices, diceType):
        self.name = name
        self.numDices = numDices
        self.diceBox = np.random.randint(1, diceType + 1, size=numDices)

    def remove_dice(self, banned_numbers):
        self.diceBox = np.setdiff1d(self.diceBox, banned_numbers)

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

    return result, rounds



def gameStats(player1, player2, numDices=10, diceType=12, ban=None, numGames=100, plot_result=True):
    results = {'Player1 Wins': 0, 'Player2 Wins': 0, 'Ties': 0, 'Average Rounds': 0}

    game_rounds = []
    win_rates_player1 = []
    win_rates_player2 = []
    tie_rates = []

    for _ in range(numGames):
        winner, rounds_played = oneGame(player1, player2, numDices, diceType, ban)

        if winner == player1:
            results['Player1 Wins'] += 1
        elif winner == player2:
            results['Player2 Wins'] += 1
        else:
            results['Ties'] += 1

        results['Average Rounds'] += rounds_played

        game_rounds.append(rounds_played)
        win_rates_player1.append(results['Player1 Wins'] / (results['Player1 Wins'] + results['Player2 Wins'] + results['Ties']))
        win_rates_player2.append(results['Player2 Wins'] / (results['Player1 Wins'] + results['Player2 Wins'] + results['Ties']))
        tie_rates.append(results['Ties'] / (results['Player1 Wins'] + results['Player2 Wins'] + results['Ties']))

    if plot_result:
        game_numbers = np.arange(1, numGames+1)

        plt.plot(game_numbers, game_rounds, alpha=0.5, label='Game Rounds')
        plt.title('Game Rounds')
        plt.xlabel('Game Number')
        plt.ylabel('Rounds Played')
        plt.legend()
        plt.show()

        plt.plot(game_numbers, win_rates_player1, label='Player1 Win Rate', alpha=0.5)
        plt.plot(game_numbers, win_rates_player2, label='Player2 Win Rate', alpha=0.5)
        plt.plot(game_numbers, tie_rates, label='Tie Rate', alpha=0.5)

        plt.title('Win Rates and Tie Rates')
        plt.xlabel('Game Number')
        plt.ylabel('Rate')
        plt.legend()
        plt.show()

    print(f"Player1 Wins: {results['Player1 Wins']} ({results['Player1 Wins'] / numGames * 100:.2f}%)")
    print(f"Player2 Wins: {results['Player2 Wins']} ({results['Player2 Wins'] / numGames * 100:.2f}%)")
    print(f"Ties: {results['Ties']} ({results['Ties'] / numGames * 100:.2f}%)")
    print(f"Average Rounds: {results['Average Rounds'] / numGames}")

# test
if __name__ == "__main__":
    player1 = "Alice"
    player2 = "Bob"
    numDices = 10
    diceType = 12
    ban = [3, 7, 11]
    numGames = 100
    plot_result = True

    gameStats(player1, player2, numDices, diceType, ban, numGames, plot_result)
