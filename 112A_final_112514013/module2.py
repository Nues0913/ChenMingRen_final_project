import pandas as pd
from mpl_toolkits.axes_grid1 import host_subplot
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random

class Team:
    
    def __init__(self, dataPath : str, constPath : str, year : str, team : str="none", minIP : float= 0.0):
        self.year = year
        self.team = team
        DataFrame = pd.read_excel(dataPath,sheet_name=year)
        constData = pd.read_csv(constPath)
        self.players = {}
        if(team != "none"):
            for i in list(DataFrame.loc[ (DataFrame["Tm"] == team) & (DataFrame["IP"] >= minIP)]["Name"]): # type: ignore
                self.players[i] = self.PlayerBattingData(DataFrame,constData,i,year,team)
        else:
            for i in list(DataFrame.loc[(DataFrame["IP"] >= minIP)]["Name"]): # type: ignore
                self.players[i] = self.PlayerBattingData(DataFrame,constData,i,year,team)
        self.LG_AVG_ERA_PLUS = self.players[list(self.players.keys())[0]].LG_AVG_ERA_PLUS
        self.LG_AVG_FIP = self.players[list(self.players.keys())[0]].LG_AVG_FIP
        
    class PlayerBattingData:
        def __init__(self, DataFrame : pd.DataFrame, constData : pd.DataFrame, name : str, year : str, team : str="none"):
            self.name = name
            table = DataFrame.loc[ DataFrame["Name"] == name]  # type: ignore
            lg_table = DataFrame.iloc[-1] # type: ignore
            const_table = constData.loc[constData["Season"] == int(year)]
            self.team = table["Tm"].values[0]
            LG_ERA = (lg_table["ER"] * 9 / lg_table["IP"])
            self.__ER : int = table["ER"].values[0]
            self.IP : float = table["IP"].values[0]
            self.__HR : int = table["HR"].values[0]
            self.__BB : int = table["BB"].values[0]
            self.__HBP : int = table["HBP"].values[0]
            self.__SO : int = table["SO"].values[0]
            self.__ERA = (self.__ER * 9 / self.IP) if(self.IP != 0.0) else "invalid"
            self.ERA_PLUS = LG_ERA / self.__ERA * 100 if(self.__ERA != 0.0) else "invalid"
            self.FIP = ((self.__HR * 13 + (self.__BB + self.__HBP) * 3 - self.__SO * 2) / self.IP) + const_table["cFIP"].values[0] if(self.IP != 0.0) else "invalid"
            self.LG_AVG_ERA_PLUS = LG_ERA / LG_ERA * 100
            self.LG_AVG_FIP = ((lg_table["HR"] * 13 + (lg_table["BB"] + lg_table["HBP"]) * 3 - lg_table["SO"] * 2) / lg_table["IP"]) + const_table["cFIP"].values[0]

    def getPlayersName(self) -> list[ str ]:
        data = list(self.players.keys())
        data.sort()
        return data
    
    def getPlayerInfo(self,playerName : str) -> PlayerBattingData: # type: ignore
        return self.players[playerName]

def solution2(dataPath : str,constPath : str, year : str, minIP : float, team : str="none", saveFig : bool =False):
        
    # specified team
    if(team != "none"):

        # initial data
        theTeam = Team(dataPath,constPath,year,team,minIP)
        data = []
        playersName = theTeam.getPlayersName()
        LG_AVG_ERA_PLUS = theTeam.LG_AVG_ERA_PLUS
        LG_AVG_FIP = theTeam.LG_AVG_FIP
        for i in playersName:
            data.append(theTeam.getPlayerInfo(i))

        # choose top 13 players or less by ERA_PLUS
        data = list(filter(lambda x: x.ERA_PLUS != "invalid", data))
        data.sort(key=lambda x: x.ERA_PLUS,reverse=True)
        # for i in range(len(data)):
        #     print(f"{data[i].name}  ERA+ : {data[i].ERA_PLUS}  IP : {data[i].IP}")
        if(len(data) >= 13):
            data = data[0:13]
        else: data = data[0:len(data)]

        # draw figure
        fig2 = plt.figure(2, figsize=(12,4), dpi=100, facecolor="w")
        host = host_subplot(111)
        par = host.twinx()
        host.scatter(range(len(data)), list(map(lambda x: x.ERA_PLUS, data)), c="r")
        par.scatter(range(len(data)), list(map(lambda x: x.FIP, data)), c="b")
        data1, = host.plot(
            range(len(data)), 
            np.ones((len(data),))*100, 
            'r--', 
            label=r"League average ERA$^+$",    # LaTeX syntax
        )
        data2, = par.plot(
            range(len(data)), 
            np.ones((len(data),))*LG_AVG_FIP, 
            'b--', 
            label="Average FIP = {:.03f}".format(LG_AVG_FIP),
        )
        host.set_ylabel(r"ERA$^+$", color='r')
        host.set_xticks(range(len(data)))
        host.set_xticklabels(list(map(lambda x: x.name, data)), fontsize=8)
        for label in host.get_xticklabels():
            label.set_rotation(40)
            label.set_horizontalalignment('center')
        host.tick_params(axis='x', which='both', direction='inout')
        host.tick_params(axis='y', labelcolor='r')
        host.legend(labelcolor="linecolor")
        par.set_ylabel("FIP", color='b')
        par.tick_params(axis='y', labelcolor='b')
        fig2.suptitle(r"ERA$^+$ & FIP of Team {0}, Season {1}".format(team,year))
        if saveFig == True:
            fig2.savefig(f"fig/ERA+ & FIP of Team {team}, Season {year}", bbox_inches='tight', facecolor='white')
        plt.show()
    
    # no specified team
    else:

        # initial data
        AllTeam = Team(dataPath,constPath,year,team,minIP)
        data = []
        data_with_invalid = []
        playersName = AllTeam.getPlayersName()
        LG_AVG_ERA_PLUS = AllTeam.LG_AVG_ERA_PLUS
        LG_AVG_FIP = AllTeam.LG_AVG_FIP

        # choose top 5 players by ERA_PLUS and 15 random players
        for i in playersName:
            data.append(AllTeam.getPlayerInfo(i))
        data_with_invalid = list(filter(lambda x: x.ERA_PLUS == "invalid", data))
        data = list(filter(lambda x: x.ERA_PLUS != "invalid", data))
        data.sort(key=lambda x: x.ERA_PLUS,reverse=True)
        # for i in range(5):
        #     print(f"name : {data[i].name}  team : {data[i].team}  ERA_PLUS : {data[i].ERA_PLUS}")
        newdata = data[0:5]
        newdata.extend(random.sample(data[5:len(data)],k = 15))

        # for i in data:
        #     if (i.name == "Tony\u00A0Gonsolin" or i.name == "Julio\u00A0Urías*" or i.name == "Dylan\u00A0Cease" or i.name == "Alek\u00A0Manoah" or i.name == "Justin\u00A0Verlander"):
        #         print(f"name : {i.name}  team : {i.team}  ERA_PLUS : {i.ERA_PLUS}  IP : {i.IP}")

        #draw figure
        fig2 = plt.figure(2, figsize=(12,4), dpi=100, facecolor="w")
        host = host_subplot(111)
        par = host.twinx()
        host.scatter(range(len(newdata)), list(map(lambda x: x.ERA_PLUS, newdata)), c="r")
        par.scatter(range(len(newdata)), list(map(lambda x: x.FIP, newdata)), c="b")
        data1, = host.plot(
            range(len(newdata)), 
            np.ones((len(newdata),))*100, 
            'r--', 
            label=r"League average ERA$^+$",    # LaTeX syntax
        )
        data2, = par.plot(
            range(len(newdata)), 
            np.ones((len(newdata),))*LG_AVG_FIP, 
            'b--', 
            label="Average FIP = {:.03f}".format(LG_AVG_FIP),
        )
        host.set_ylabel(r"ERA$^+$", color='r')
        host.set_xticks(range(len(newdata)))
        host.set_xticklabels(list(map(lambda x: x.name, newdata)), fontsize=8)
        for label in host.get_xticklabels():
            label.set_rotation(40)
            label.set_horizontalalignment('center')
        host.tick_params(axis='x', which='both', direction='inout')
        host.tick_params(axis='y', labelcolor='r')
        host.legend(labelcolor="linecolor")
        par.set_ylabel("FIP", color='b')
        par.tick_params(axis='y', labelcolor='b')
        fig2.suptitle(r"ERA$^+$ & FIP of players, Season {0}".format(year))
        if saveFig == True:
            fig2.savefig(f"fig/ERA+ & FIP of players, Season {year}", bbox_inches='tight', facecolor='white')
        plt.show()

# for testing
if __name__ == "__main__":
    solution2(
    dataPath="data/data_pitching_2021-2023.xlsx",
    constPath="data/wOBA_FIP_constants.csv",
    year="2022",
    minIP=25.2, # minIP = 25.2 if want to fit the PDF's figure in problem2,team specified, and minIP = 130.0 for figure in problem2,team specified,
    team="LAA",
    saveFig=True
    )
