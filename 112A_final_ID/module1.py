import pandas as pd



class Team:
    def __init__(self,team,year,dataPath):
        self.year = year
        __DataFrame = pd.read_excel(dataPath,sheet_name=year)
        self.table = __DataFrame.loc[ __DataFrame["Tm"] == team]  # type: ignore
        
class PlayerBattingData:
    def __init__(self,dataPath,name,team,year):
        self.name = name
        self.team = team
        self.year = year
        DataFrame = pd.read_excel(dataPath,sheet_name=year)
        table = DataFrame.loc[ DataFrame["Name"] == name]  # type: ignore
        self.__H : int = table["H"].values[0]
        self.__BB : int = table["BB"].values[0]
        self.__HBP : int = table["HBP"].values[0]
        self.__AB : int = table["AB"].values[0]
        self.__SF : int = table["SF"].values[0]
        self.__TWO_B : int = table["2B"].values[0]
        self.__THREE_B : int = table["3B"].values[0]
        self.__HR : int = table["HR"].values[0]
        self.__TB : int = self.__TWO_B* +self.__THREE_B*2 + self.__HR*3
        self.__OBP = (self.__H + self.__BB + self.__HBP)/(self.__AB + self.__BB + self.__SF + self.__HBP) if(self.__AB) else -1
        self.__SLG = self.__TB/self.__AB if(self.__AB) else -1
        self.OPS = self.__OBP + self.__SLG if (self.__AB) else "invalid"

def solution1(dataPath,constPath,year,minPA,team,saveFig=False):
    BOS = Team(team,year,dataPath)
    Ty_Adcock = PlayerBattingData(dataPath,"Ty\xa0Adcock",team,year)
    # print(BOS.table)
    print(Ty_Adcock.OPS)


# print(a.battingData["Name"])
# print(" ".join(a.battingData.values.tolist()[20][0].split()))
# print(a.index)
# print(a.loc[a.Name == "José Abreu"].G.values)
# print(a.battingData.loc[[,"PA"]])

# print(a.battingData['',''])


if __name__ == "__main__":
    solution1(dataPath="data/data_batting_2021-2023.xlsx",
              constPath="data/wOBA_FIP_constants.csv",
              year="2023",
              minPA=0,
              team="BOS")
