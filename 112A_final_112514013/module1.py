import pandas as pd
from mpl_toolkits.axes_grid1 import host_subplot
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random

class Team:
    
    def __init__(self, dataPath : str, constPath : str, year : str, team : str="none", minPA : int= 0):
        self.year = year
        self.team = team
        DataFrame = pd.read_excel(dataPath,sheet_name=year)
        constData = pd.read_csv(constPath)
        self.players = {}
        if(team != "none"):
            for i in list(DataFrame.loc[ (DataFrame["Tm"] == team) & (DataFrame["PA"] >= minPA)]["Name"]): # type: ignore
                self.players[i] = self.PlayerBattingData(DataFrame,constData,i,year,team)
        else:
            for i in list(DataFrame.loc[(DataFrame["PA"] >= minPA)]["Name"]): # type: ignore
                self.players[i] = self.PlayerBattingData(DataFrame,constData,i,year,team)
        self.LG_AVG_OPS_PLUS = self.players[list(self.players.keys())[0]].LG_AVG_OPS_PLUS
        self.LG_AVG_wRC = self.players[list(self.players.keys())[0]].LG_AVG_wRC
        
    class PlayerBattingData:
        def __init__(self, DataFrame : pd.DataFrame, constData : pd.DataFrame, name : str, year : str, team : str="none"):
            self.name = name
            table = DataFrame.loc[ DataFrame["Name"] == name]  # type: ignore
            lg_table = DataFrame.iloc[-1] # type: ignore
            const_table = constData.loc[constData["Season"] == int(year)]
            self.team = table["Tm"].values[0]
            LG_SLG = (lg_table["H"] +
                    1*lg_table["2B"] +
                    2*lg_table["3B"] +
                    3*lg_table["HR"])/(lg_table["AB"])
            LG_OBP = (lg_table["H"] +
                    lg_table["BB"] +
                    lg_table["HBP"])/(lg_table["PA"])
            LG_wOBA = const_table["wOBA"].values[0]
            LG_wOBAScale = const_table["wOBAScale"].values[0]
            LG_R_PA = const_table["R/PA"].values[0]
            self.__AB : int = table["AB"].values[0]
            self.__BB : int = table["BB"].values[0]
            self.__TWO_B : int = table["2B"].values[0]
            self.__THREE_B : int = table["3B"].values[0]
            self.__H : int = table["H"].values[0]
            self.__HBP : int = table["HBP"].values[0]
            self.__HR : int = table["HR"].values[0]
            self.__IBB : int = table["IBB"].values[0]
            self.__PA : int = table["PA"].values[0]
            self.__SF : int = table["SF"].values[0]
            self.__TB : int = self.__H + self.__TWO_B + self.__THREE_B*2 + self.__HR*3
            self.__OBP = (self.__H + self.__BB + self.__HBP)/self.__PA if(self.__PA) else "invalid"
            self.__SLG = self.__TB/self.__AB if(self.__AB) else "invalid"
            self.OPS = self.__OBP + self.__SLG if (self.__AB) else "invalid" # type: ignore
            self.OPS_PLUS = 100*((self.__OBP/LG_OBP) + (self.__SLG/LG_SLG) - 1) if(self.__AB) else "invalid"
            self.wOBA = (
                0.696*(self.__BB - self.__IBB) +
                0.726*(self.__HBP) +
                0.883*(self.__H - self.__TWO_B - self.__THREE_B - self.__HR) +
                1.244*(self.__TWO_B) +
                1.569*(self.__THREE_B) +
                2.004*(self.__HR)) / (self.__AB + self.__BB + self.__SF + self.__HBP - self.__IBB) if(self.__AB + self.__BB + self.__SF + self.__HBP - self.__IBB) else "invalid"
            self.wRC = (((self.wOBA - LG_wOBA) / LG_wOBAScale) + LG_R_PA) * self.__PA if(self.wOBA != "invalid") else "invalid"
            self.LG_AVG_OPS_PLUS = 100*((LG_OBP/LG_OBP) + (LG_SLG/LG_SLG) - 1)
            self.LG_AVG_wRC = ((LG_wOBA - LG_wOBA) / LG_wOBAScale + LG_R_PA) * lg_table["PA"]

    def getPlayersName(self) -> list[ str ]:
        data = list(self.players.keys())
        data.sort()
        return data
    
    def getPlayerInfo(self,playerName : str) -> PlayerBattingData: # type: ignore
        return self.players[playerName]


def solution1(dataPath : str,constPath : str, year : str, minPA : int, team : str="none", saveFig : bool =False):
    
    # specified team
    if(team != "none"):

        # initial data
        theTeam = Team(dataPath,constPath,year,team,minPA)
        data = []
        playersName = theTeam.getPlayersName()
        AVG_OPS_PLUS = theTeam.LG_AVG_OPS_PLUS
        LG_AVG_wRC = theTeam.LG_AVG_wRC
        for i in playersName:
            data.append(theTeam.getPlayerInfo(i))

        # choose top 14 players or less by wRC
        data = list(filter(lambda x: x.wRC != "invalid", data))
        data.sort(key=lambda x: x.wRC,reverse=True)
        # for i in range(len(data)):
        #     print(f"{data[i].name}  ERA+ : {data[i].ERA_PLUS}  IP : {data[i].IP}")
        if(len(data) >= 14):
            data = data[0:14]
        else: data = data[0:len(data)]

        # draw figure
        fig2 = plt.figure(2, figsize=(12,4), dpi=100, facecolor="w")
        host = host_subplot(111)
        par = host.twinx()
        host.scatter(range(len(data)), list(map(lambda x: x.OPS_PLUS, data)), c="r")
        par.scatter(range(len(data)), list(map(lambda x: x.wRC, data)), c="b")
        data1, = host.plot(
            range(len(data)), 
            np.ones((len(data),))*100, 
            'r--', 
            label=r"League average OPS$^+$",    # LaTeX syntax
        )
        data2, = par.plot(
            range(len(data)), 
            np.ones((len(data),))*LG_AVG_wRC, 
            'b--', 
            label="Average wRC = {:.03f}".format(LG_AVG_wRC),
        )
        host.set_ylabel(r"OPS$^+$", color='r')
        host.set_xticks(range(len(data)))
        host.set_xticklabels(list(map(lambda x: x.name, data)), fontsize=8)
        for label in host.get_xticklabels():
            label.set_rotation(40)
            label.set_horizontalalignment('center')
        host.tick_params(axis='x', which='both', direction='inout')
        host.tick_params(axis='y', labelcolor='r')
        host.legend(labelcolor="linecolor")
        par.set_ylabel("wRC", color='b')
        par.tick_params(axis='y', labelcolor='b')
        fig2.suptitle(r"OPS$^+$ & wRC of Team {0}, Season {1}".format(team,year))
        if saveFig == True:
            fig2.savefig(f"fig/OPS+ & wRC of Team {team}, Season {year}", bbox_inches='tight', facecolor='white')
        plt.show()

    # no specified team
    else:

        # initial data
        AllTeam = Team(dataPath,constPath,year,team,minPA)
        data = []
        data_with_invalid = []
        playersName = AllTeam.getPlayersName()
        AVG_OPS_PLUS = AllTeam.LG_AVG_OPS_PLUS
        LG_AVG_wRC = AllTeam.LG_AVG_wRC

        # choose top 5 players by wRC and 15 random players
        for i in playersName:
            data.append(AllTeam.getPlayerInfo(i))
        data_with_invalid = list(filter(lambda x: x.wRC == "invalid", data))
        data = list(filter(lambda x: x.wRC != "invalid", data))
        data.sort(key=lambda x: x.wRC,reverse=True)
        # for i in range(5):
        #     print(f"name : {data[i].name}  team : {data[i].team}  wRC : {data[i].wRC}")
        newdata = data[0:5]
        newdata.extend(random.sample(data[5:len(data)],k = 15))

        #draw figure
        fig2 = plt.figure(2, figsize=(12,4), dpi=100, facecolor="w")
        host = host_subplot(111)
        par = host.twinx()
        host.scatter(range(len(newdata)), list(map(lambda x: x.OPS_PLUS, newdata)), c="r")
        par.scatter(range(len(newdata)), list(map(lambda x: x.wRC, newdata)), c="b")
        data1, = host.plot(
            range(len(newdata)), 
            np.ones((len(newdata),))*100, 
            'r--', 
            label=r"League average OPS$^+$",    # LaTeX syntax
        )
        data2, = par.plot(
            range(len(newdata)), 
            np.ones((len(newdata),))*LG_AVG_wRC, 
            'b--', 
            label="Average wRC = {:.03f}".format(LG_AVG_wRC),
        )
        host.set_ylabel(r"OPS$^+$", color='r')
        host.set_xticks(range(len(newdata)))
        host.set_xticklabels(list(map(lambda x: x.name, newdata)), fontsize=8)
        for label in host.get_xticklabels():
            label.set_rotation(40)
            label.set_horizontalalignment('center')
        host.tick_params(axis='x', which='both', direction='inout')
        host.tick_params(axis='y', labelcolor='r')
        host.legend(labelcolor="linecolor")
        par.set_ylabel("wRC", color='b')
        par.tick_params(axis='y', labelcolor='b')
        fig2.suptitle(r"OPS$^+$ & wRC of players, Season {0}".format(year))
        if saveFig == True:
            fig2.savefig(f"fig/OPS+ & wRC of players, Season {year}", bbox_inches='tight', facecolor='white')
        plt.show()

# for testing
if __name__ == "__main__":
    solution1(
    dataPath="data/data_batting_2021-2023.xlsx",
    constPath="data/wOBA_FIP_constants.csv",
    year="2023",
    minPA=0,
    team="LAA",
    saveFig=False
    )
