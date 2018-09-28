#!/usr/bin/python3
from bs4 import BeautifulSoup
import requests
import pandas as pnd
from requests_html import HTMLSession


# Today
class Parser:

    def __init__(self):
        self.url = 'https://www.myscore.ru/'
        self.session = HTMLSession()

    def GetUrl(self, url=0):
        if url == 0:
            res = self.session.get(self.url)
            res.html.render()
            return res
        else:
            # if /hockey in url -> do something
            # to get teams in hockey use .padl
            res = requests.get(url)
            return res.text

    # Friday Task
    def Today(self):
        teams_home_array = []
        teams_away_array = []
        all_games_scores_array = []
        # live_games_scores_array = []
        games_statuses_array = []
        games_start_times_array = []

        # soup = BeautifulSoup(page,"html.parser")
        # check = soup.find("div",{"id":"fscon"})
        res = self.GetUrl()  # == res.text

        teams_home = res.html.find('.padr')
        teams_away = res.html.find('.padl')
        all_games_scores = res.html.find('.cell_sa.score')
        # live_games_scores = res.html.find('.cell_sa.score.bold.playing')
        games_statuses = res.html.find('.cell_aa.timer')
        games_start_times = res.html.find('.cell_ad.time')

        for team in teams_home:
            teams_home_array.append(team.text)
        for team in teams_away:
            teams_away_array.append(team.text)
        for score in all_games_scores:
            all_games_scores_array.append(score.text.replace('\xa0', ''))
        # for score in live_games_scores:
        #     live_games_scores_array.append(score.text.replace('\xa0', ''))
        for game in games_statuses:
            games_statuses_array.append(game.text)
        for time in games_start_times:
            games_start_times_array.append(time.text)

        d = {'start_time': games_start_times_array, 'game_status': games_statuses_array, 'home_team': teams_home_array,
             'score': all_games_scores_array, 'away_team': teams_away_array }
        todayDataFrame = pnd.DataFrame(data = d)
        print(todayDataFrame)


if __name__ == "__main__":
    full = Parser()
    full.Today()
