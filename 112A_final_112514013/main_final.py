import argparse
from module1 import solution1
from module2 import solution2

if __name__ == "__main__":
    # describe about the program
    parser = argparse.ArgumentParser(description="2023 NYCUDOPCS FinalProject")
    # add two optional argument
    parser.add_argument("--dir", default="", type=str, help="Directoryof data")
    parser.add_argument("--year", default=2023, type=int, help="Whichyear? (default: 2023)")
    opt = parser.parse_args()
    
    # calculate the advanced statistics
    solution1(
    dataPath="data/data_batting_2021-2023.xlsx",
    constPath="data/wOBA_FIP_constants.csv",
    year="2023",
    minPA=0,
    team="LAA", # disabled this for no specified team
    saveFig=False # create a 'fig' folder in the same directory as the python file, or change the save location of savefig() in each moudle for the images
    )
    solution2(
    dataPath="data/data_pitching_2021-2023.xlsx",
    constPath="data/wOBA_FIP_constants.csv",
    year="2022",
    minIP=25.2, # minIP = 25.2 if want to fit the PDF's figure in problem2,team specified, and minIP = 130.0 for figure in problem2,team specified,
    team="LAA", # disabled this for no specified team
    saveFig=False # create a 'fig' folder in the same directory as the python file, or change the save location of savefig() in each moudle for the images
    )

"""
Created on Sun Jan 7 00:49:45 2024
@author: Hsieh Ming Ren, 112514013
@collaborators: 
"""