from bs4 import BeautifulSoup
import requests
import pandas as pnd
from requests_html import HTMLSession 
from requests_html import AsyncHTMLSession 
import sys 


# Today
class Parser:

    def __init__(self):
        self.url = 'https://www.myscore.ru'
        self.session = HTMLSession()
        self.urls = {
            "Хоккей":"/hockey","Теннис":"/tennis","Баскетбол":"/basketball",
            "Волейбол":"/volleyball","Гандбол":"/handball","Футзал":"/futsal",
            "Бейсбол":"/baseball"}

    def GetUrl(self,sport):
        if sport == "Футбол":
            res = self.session.get(self.url)
            return res
        else:
            try:
                    sportUrl = self.urls[sport]
            except KeyError:
                    print("Not at dict")
                    return
            fullUrl = self.url + self.urls[sport]
            res = self.session.get(fullUrl)
            return res

    def SportToday(self,sport):
        teams_home_array = []
        teams_away_array = []
        teams_home_scores = []
        teams_away_scores = []
        games_statuses_array = []
        games_start_times_array = []

        if sport == "Футбол":
            self.Today()
            return
        res = self.GetUrl(sport)
        res.html.render(sleep=1)
        teams_home = res.html.find('.padl')
        i = 0
        while i<len(teams_home):
            teams_home_array += [teams_home[i].text]
            teams_away_array += [teams_home[i+1].text]
            i+=2
        # print(len(teams_away_array)>0)
        # print(len(teams_away_array)==len(teams_home_array))
        # print(teams_away_array)

        if len(teams_away_array)==len(teams_home_array) and len(teams_away_array)>0:
            games_scores_home = res.html.find('.cell_sc.score-home')
            games_scores_away = res.html.find('.cell_ta.score-away')
            games_statuses = res.html.find('.cell_aa.timer')
            games_start_times = res.html.find('.cell_ad.time')

            for score in games_scores_home:
                teams_home_scores.append(score.text.replace('\xa0', ''))
            for score in games_scores_away:
                teams_away_scores.append(score.text.replace('\xa0', ''))
            for game in games_statuses:
                games_statuses_array.append(game.text)
            for time in games_start_times:
                games_start_times_array.append(time.text)
        
            d = {'start_time': games_start_times_array, 'game_status': games_statuses_array, 'home_team': teams_home_array,
               'score_home': teams_home_scores,'score_away':teams_away_scores, 'away_team': teams_away_array }
            todayDataFrame = pnd.DataFrame(data = d)
            print(todayDataFrame)
            # return todayDataFrame
        else:
            # print("Bad")
            return "Bad"

    def GetLeagues(self,sport,res):
        leagueArray = []
        if sport == "Футбол":
            units = res.html.find('.soccer')
            for i in units:
                matchesCount = i.find('tbody')
                print(matchesCount)
                country = i.find('.country_part')[0]
                tournament = i.find('.tournament_part')[0]
                print(country.text,tournament.text)
        else:
            pass

    def Today(self): # Footbal
        teams_home_array = []
        teams_away_array = []
        all_games_scores_array = []
        # live_games_scores_array = []
        games_statuses_array = []
        games_start_times_array = []


        # soup = BeautifulSoup(page,"html.parser")
        # check = soup.find("div",{"id":"fscon"})
        res = self.GetUrl("Футбол")  # == res.text
        res.html.render(sleep=1)
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
        # return todayDataFrame.size
        self.GetLeagues("Футбол",res)


if __name__ == "__main__":
    full = Parser()
    test = input("Введите название спорта:")
    # test = sys.argv[1]
    full.SportToday(test)
    # full.GetLeagues()
# else:
#     full = Parser()
#     test = sys.argv[1]
#     full.SportToday(test)
