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

    # print(f"year : {opt.year} {opt.dir}")
    
    # write a program that calculates the advanced batting statistics
    # solution1(
    # dataPath=???,
    # constPath=???,
    # year=???,
    # minPA=???,
    # team=???,
    # saveFig=???,
    # )
    # solution2(
    # dataPath=???,
    # constPath=???,
    # year=???,
    # minIP=???,
    # team=???,
    # saveFig=???,
    # )