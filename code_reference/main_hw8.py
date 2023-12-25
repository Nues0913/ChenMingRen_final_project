import argparse
from game import oneGame
from test import gameStats


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="2023 NYCUDOPCS Homework #8")
    parser.add_argument("--name1", default="player1", type=str, help="player1 (default: player1)")
    parser.add_argument("--name2", default="player2", type=str, help="player2 (default: player2)")
    parser.add_argument("--games", default=100, type=int, help="Number of games (default: 100)")
    parser.add_argument("--num", default=10, type=int, help="Number of dices (default: 10)")
    parser.add_argument("--ban", default=[2, 4, 6], type=int, nargs='+', help="ban (default: [2, 4, 6])")
    parser.add_argument("--plot", default=True, help="Whether to plot results")
    parser.add_argument("--dtype", default=12, type=int, help="Dice type (default: 12)")

    opt = parser.parse_args()

    print("Problem 1:")
    oneGame(player1=opt.name1, player2=opt.name2, numDices=opt.num, diceType=opt.dtype, ban=opt.ban)

    print("==" * 60)
    print("Problem 2 & 3")
    gameStats(numGames=opt.games, player1=opt.name1, player2=opt.name2, numDices=opt.num, diceType=opt.dtype, ban=opt.ban, plot_result=opt.plot)

"""
Created on Thu Dec 7 20:46:23 2023
@author: Hsieh Ming Ren,112514013
@collaborators: Lin Way Tang,112514016
"""