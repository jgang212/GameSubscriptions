import pandas as pd

PSNow_DF = pd.read_csv("PSNow_gameMatches.csv", encoding='latin1')
XboxGP_DF = pd.read_csv("XboxGP_gameMatches.csv", encoding='latin1')

overlaps = []
scoreSum = 0
for i, gameRow in PSNow_DF.iterrows():
    if gameRow['Found'] in XboxGP_DF['Found'].tolist():
        overlaps.append(gameRow['Found'])
        scoreSum += gameRow['Score']
        print(gameRow['Found'] + "," + str(gameRow['Score']))

print(len(overlaps))
print(scoreSum)