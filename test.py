import pandas as pd
data = pd.read_csv("data/wOBA_FIP_constants.csv")
data = data.loc[data["Season"] == 2023]
# print(data)
# print(data["wOBA"].values[0])
print(int("2023"))