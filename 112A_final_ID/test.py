import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

batting2023 = pd.read_excel("./data/data_batting_2021-2023.xlsx", "2023")

# PA >= 100
batting2023 = batting2023[batting2023["PA"] >= 100]

# wOBA
batting2023["wOBA"] = (
    0.696 * (batting2023["BB"] - batting2023["IBB"]) + \
    0.726 * batting2023["HBP"] + \
    0.883 * (batting2023["H"]-batting2023["2B"]-batting2023["3B"]-batting2023["HR"]) + \
    1.244 * batting2023["2B"] + \
    1.569 * batting2023["3B"] + \
    2.004 * batting2023["HR"]
) / (batting2023["AB"] + batting2023["BB"] + batting2023["SF"] + batting2023["HBP"] - batting2023["IBB"])

# wRC
batting2023["wRC"] = (
    (batting2023["wOBA"] - 0.318)/1.204 + 0.122
) * batting2023["PA"]

# Extract data
df = batting2023.sort_values(by="wRC", ascending=False)

requiredData = ["Shohei\xa0Ohtani*", "Brandon\xa0Drury", "Mickey\xa0Moniak*", "Luis\xa0Rengifo#", 
                "Mike\xa0Trout", "Taylor\xa0Ward", "Zach\xa0Neto", "Gio\xa0Urshela", 
                "Logan\xa0O'Hoppe", "Matt\xa0Thaiss*", "Chad\xa0Wallach", "Nolan\xa0Schanuel*", 
                "Anthony\xa0Rendon", "Jared\xa0Walsh*"]

for i in requiredData:
    print(batting2023.loc[batting2023["Name"] == i])

print(batting2023.iloc[-1])