# A web scraper that creates a CSV file of all games with >= 5 reviews
# on gamerankings.com so we can easily search through the data later

from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import pandas as pd

# web scraping functions
def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)

def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

# main
gameList = []
scoreReviewList = []
gameRankings = {}

# go through all games with >= 5 reviews and store them in lists
for i in range(0, 411):
    raw_html = simple_get('https://www.gamerankings.com/browse.html?page=' + str(i) + '&numrev=4')

    if raw_html is not None:
        html = BeautifulSoup(raw_html, 'html.parser')

        for td in html.find_all('td'):
            if td.a:
                if td.a['href'].count("/") == 3 and "//" not in td.a['href']:
                    #print(td.a.text)
                    gameList.append(td.a.text)
            if td.span:
                if td.span['style']:
                    #print(td.span.text)
                    #print(td.text.split("%")[1][0])
                    scoreReviewList.append((float(td.span.text.split("%")[0]), int(td.text.split("%")[1].split(" ")[0])))

titleList = []
scoreList = []
reviewList = []
if len(gameList) == len(scoreReviewList):
    for i in range(0, len(gameList)):
        if gameList[i] not in gameRankings:
            gameRankings[gameList[i]] = scoreReviewList[i]
        # combine reviews (weighted average) for games on multiple platforms
        else:
            #print(gameList[i])
            existingScore = gameRankings[gameList[i]][0]
            existingReviews = gameRankings[gameList[i]][1]
            newReviews = existingReviews + scoreReviewList[i][1]
            newScore = (existingScore * existingReviews + scoreReviewList[i][0] * scoreReviewList[i][1]) / newReviews
            gameRankings[gameList[i]] = (newScore, newReviews)
else:
    print("Mistmatched game and score lists")

# put into dataframe for export and future analysis
for game in gameRankings:    
    titleList.append(game)
    scoreList.append(gameRankings[game][0])
    reviewList.append(gameRankings[game][1])

gameRankingsDF = pd.DataFrame({'Title': titleList, 'Score': scoreList, 'Review': reviewList})

#print(gameRankingsDF)
print(len(gameRankingsDF))

# export to CSV
gameRankingsDF.to_csv("gameRankings.csv", index=False)
