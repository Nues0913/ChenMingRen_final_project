import pandas as pd

class Team:
    
    def __init__(self, dataPath : str, team : str, year : str, minPA : int= 0):
        self.year = year
        self.team = team
        DataFrame = pd.read_excel(dataPath,sheet_name=year)
        self.players = {}
        for i in list(DataFrame.loc[ (DataFrame["Tm"] == team) & (DataFrame["PA"] >= minPA)]["Name"]): # type: ignore
            self.players[i] = self.PlayerBattingData(dataPath,i,team,year)
        self.LG_AVG_OPS_PLUS = self.players[list(self.players.keys())[0]].LG_AVG_OPS_PLUS

        
    class PlayerBattingData:
        def __init__(self, dataPath : str, name : str, team : str, year : str):
            self.name = name
            DataFrame = pd.read_excel(dataPath,sheet_name=year)
            lg_table = DataFrame.iloc[-1] # type: ignore
            LG_SLG = (lg_table["H"] +
                    1*lg_table["2B"] +
                    2*lg_table["3B"] +
                    3*lg_table["HR"])/(lg_table["AB"])
            LG_OBP = (lg_table["H"] +
                    lg_table["BB"] +
                    lg_table["HBP"])/(lg_table["PA"])
            table = DataFrame.loc[ DataFrame["Name"] == name]  # type: ignore
            self.__H : int = table["H"].values[0]
            self.__BB : int = table["BB"].values[0]
            self.__HBP : int = table["HBP"].values[0]
            self.__AB : int = table["AB"].values[0]
            self.__TWO_B : int = table["2B"].values[0]
            self.__THREE_B : int = table["3B"].values[0]
            self.__HR : int = table["HR"].values[0]
            self.__PA : int = table["PA"].values[0]
            self.__TB : int = self.__H + self.__TWO_B + self.__THREE_B*2 + self.__HR*3
            self.__OBP = (self.__H + self.__BB + self.__HBP)/self.__PA if(self.__PA) else -1
            self.__SLG = self.__TB/self.__AB if(self.__AB) else -1
            self.OPS = self.__OBP + self.__SLG if (self.__AB) else "invalid"
            self.OPS_PLUS = 100*((self.__OBP/LG_OBP) + (self.__SLG/LG_SLG) - 1)
            self.LG_AVG_OPS_PLUS = 100*((LG_OBP/LG_OBP) + (LG_SLG/LG_SLG) - 1)

    def getPlayersName(self) -> list[ str ]:
        data = list(self.players.keys())
        data.sort()
        return data
    
    def getPlayerInfo(self,playerName : str) -> PlayerBattingData: # type: ignore
        return self.players[playerName]


def solution1(dataPath : str,constPath : str, year : str, minPA : int, team : str, saveFig : bool =False):
    LAA = Team(dataPath,team,year,minPA)
    requiredData = ["Shohei\xa0Ohtani*", "Brandon\xa0Drury", "Mickey\xa0Moniak*", "Luis\xa0Rengifo#", 
                    "Mike\xa0Trout", "Taylor\xa0Ward", "Zach\xa0Neto", "Gio\xa0Urshela", 
                    "Logan\xa0O'Hoppe", "Matt\xa0Thaiss*", "Chad\xa0Wallach", "Nolan\xa0Schanuel*", 
                    "Anthony\xa0Rendon", "Jared\xa0Walsh*"]
    print(LAA.team)
    print(LAA.year)
    data = []
    playersName = LAA.getPlayersName()
    AVG_OPS_PLUS = LAA.LG_AVG_OPS_PLUS
    print(f"AVG : {AVG_OPS_PLUS}")
    for i in playersName:
        print("{0} OPS+ : {1:0.0f}".format(i,LAA.getPlayerInfo(i).OPS_PLUS))



if __name__ == "__main__":
    solution1(dataPath="data/data_batting_2021-2023.xlsx",
              constPath="data/wOBA_FIP_constants.csv",
              year="2023",
              minPA=0,
              team="LAA")
