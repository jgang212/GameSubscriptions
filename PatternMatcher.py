import pandas as pd
from fuzzywuzzy import fuzz

gameRankingsDF = pd.read_csv("gameRankings.csv")
findGamesDF = pd.read_csv("PSNow_Games.csv", encoding='latin1')

findGames = []
reviewGames = []
matchScores = []
scores = []
reviews = []
for i, gameRow in findGamesDF.iterrows():
    bestRatio = 0
    bestMatch = ""
    bestMatchScore = 0
    bestMatchReviews = 0
    for j, reviewRow in gameRankingsDF.iterrows():
        currentRatio = fuzz.ratio(gameRow['title'].lower(), reviewRow['Title'].lower())
        if currentRatio > bestRatio:
            bestRatio = currentRatio
            bestMatch = reviewRow['Title']
            bestMatchScore = reviewRow['Score']
            bestMatchReviews = reviewRow['Review']
    #     if currentRatio == 100:
    #         print("Found perfect match", reviewRow['Title'])
    print(gameRow['title'], bestRatio, bestMatch)
    findGames.append(gameRow['title'])
    reviewGames.append(bestMatch)
    matchScores.append(bestRatio)
    scores.append(bestMatchScore)
    reviews.append(bestMatchReviews)

gameMatchDF = pd.DataFrame({'Looked': findGames, 'Found': reviewGames, 'Match': matchScores, 'Score': scores, 'Reviews': reviews})

# export to CSV
gameMatchDF.to_csv("PSNow_gameMatches.csv", index=False)
