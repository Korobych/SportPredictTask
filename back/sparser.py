from bs4 import BeautifulSoup
import requests
import pandas as pnd
from requests_html import HTMLSession 
import sys
from selenium import webdriver 
import selenium
import numpy as np
import time

# Today
class Parser:

    def __init__(self):
        self.url = 'https://www.myscore.ru'
        self.urls = {
            "Хоккей":"/hockey","Теннис":"/tennis","Баскетбол":"/basketball",
            "Волейбол":"/volleyball","Гандбол":"/handball","Футзал":"/futsal",
            "Бейсбол":"/baseball","Футбол":"/"}
        self.team_urls = {}
        self.docker = '/app/back/chromedriver'

    def SportToday(self,sport):
        teams_home_array = []
        teams_away_array = []
        teams_home_scores = []
        teams_away_scores = []
        games_statuses_array = []
        games_start_times_array = []

        if sport == "Футбол":
            t = self.FootBall()
            return t

        # driver = webdriver.Chrome('/home/prazd/selenium/chromedriver')
        driver = webdriver.Chrome('/Users/Koroba/Downloads/chromedriver')
        url = self.url + self.urls[sport]
        driver.get(url)
        teams_home = driver.find_elements_by_class_name("padl")
        i = 0
        while i<len(teams_home):
            teams_home_array += [teams_home[i].text]
            teams_away_array += [teams_home[i+1].text]
            i+=2
    
        if len(teams_away_array)==len(teams_home_array) and len(teams_away_array)>0:
            games_scores_home = driver.find_elements_by_class_name("cell_sc")
            games_scores_away = driver.find_elements_by_class_name("cell_ta")
            games_statuses = driver.find_elements_by_class_name("cell_aa")
            games_start_times = driver.find_elements_by_class_name("cell_ad")

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
            # todayDataFrame = pnd.DataFrame(data = d)
            # print(todayDataFrame)
        else:
            return "Bad"

    def GetLeagues(self,sport,driver):
        if sport == "Футбол":
            check = driver.find_elements_by_class_name("expand-league")
            i = 0
            while i < len(check):
                try:
                    check[i].click()
                    i+=1
                except selenium.common.exceptions.WebDriverException:
                    i+1
            print("end")
        else:
            pass

    def get_two_teams_url(self, team1, team2, sport, driver):
        window_before = driver.window_handles[0]
        if sport == "Футбол":
            soccer_bloсks = driver.find_elements_by_class_name("soccer")
            for block in soccer_bloсks[1:]:
                tbody = block.find_element_by_tag_name("tbody")
                trs = tbody.find_elements_by_tag_name("tr")
                print(len(trs), '- количество игр в лиге')
                for el in trs:
                    padr = el.find_element_by_class_name("padr")
                    padl = el.find_element_by_class_name("padl")
                    if padr.text == team1 and padl.text == team2 or padr.text == team2 and padl.text == team1:
                        el.click()
                        window_after = driver.window_handles[1]
                        driver.switch_to.window(window_after)
                        teams_url_data = driver.find_elements_by_class_name("participant-imglink")
                        teams_url_data = np.array(teams_url_data)
                        teams_url_data = teams_url_data[[1, 3]]
                        print(len(teams_url_data), ' - количество команд')
                        for team in teams_url_data:
                            team_name = team.text
                            team_url = team.get_attribute("onclick")
                            # clearing url from
                            team_url = team_url.replace('window.open(\'', '')
                            team_url = team_url.replace('\'); return false;', '')
                            print(team_name, '- название команды')
                            print(team_url, '- ссылка на страницу')
                            self.team_urls.update({team_name: team_url})
                        driver.close()
                        driver.switch_to.window(window_before)
                        return
                    else:
                        print("нет такой пары команд")
        else:
            print("другой спорт")

    def get_all_teams_url(self, sport, driver):
        if sport == "Футбол":
            soccer_bloсks = driver.find_elements_by_class_name("soccer")
            window_before = driver.window_handles[0]
            for block in soccer_bloсks[1:]:
                tbody = block.find_element_by_tag_name("tbody")
                trs = tbody.find_elements_by_tag_name("tr")
                for el in trs:
                    el.click()
                    window_after = driver.window_handles[1]
                    driver.switch_to.window(window_after)
                    teams_url_data = driver.find_elements_by_class_name("participant-imglink")
                    teams_url_data = np.array(teams_url_data)
                    teams_url_data = teams_url_data[[1, 3]]
                    for team in teams_url_data:
                        team_name = team.text
                        team_url = team.get_attribute("onclick")
                        # clearing url from
                        team_url = team_url.replace('window.open(\'', '')
                        team_url = team_url.replace('\'); return false;', '')
                        self.team_urls.update({team_name: team_url})
                    driver.close()
                    driver.switch_to.window(window_before)
        else:
            print("другой спорт")

    def FootBall(self): # Footbal
        teams_home_array = []
        teams_away_array = []
        all_games_scores_array = []
        games_statuses_array = []
        games_start_times_array = []
        league_array = []

        chrome_options = webdriver.ChromeOptions()

        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        # driver = webdriver.Chrome(self.docker,chrome_options=chrome_options) # for docker

        # driver = webdriver.Chrome('/home/prazd/selenium/chromedriver')
        driver = webdriver.Chrome('/Users/Koroba/Downloads/chromedriver')
     
        url = self.url + self.urls["Футбол"]
        driver.get(url)

        self.GetLeagues("Футбол", driver)
        soccer_bloсks = driver.find_elements_by_class_name("soccer")
        last_block = ""
        for block in soccer_bloсks:
            country = block.find_element_by_class_name("country_part")
            tournament = block.find_element_by_class_name("tournament_part")
            league_string = country.text + tournament.text
            if last_block == league_string:
                continue

            last_block = league_string
            tbody = block.find_element_by_tag_name("tbody")
            trs = tbody.find_elements_by_tag_name("tr")
            for i in trs:
                league_array.append(league_string)

        # check number of games in league_array --  May be deleted
        print(len(league_array))

        teams_home = driver.find_elements_by_class_name("padr")
        teams_away = driver.find_elements_by_class_name("padl")
        all_games_scores = driver.find_elements_by_class_name("cell_sa")
        games_statuses = driver.find_elements_by_class_name("cell_aa")
        games_start_times = driver.find_elements_by_class_name("cell_ad")

        for team in teams_home:
            teams_home_array.append(team.text)
        for team in teams_away:
            teams_away_array.append(team.text)
        for score in all_games_scores:
            all_games_scores_array.append(score.text.replace('\xa0', ''))
        for game in games_statuses:
            games_statuses_array.append(game.text)
        for time in games_start_times:
            games_start_times_array.append(time.text)

        d = {'start_time': games_start_times_array, 'game_status': games_statuses_array, 'home_team': teams_home_array,
             'score': all_games_scores_array, 'away_team': teams_away_array, 'league': league_array}

        # check number of games in league_array --  May be deleted
        print(len(d['home_team']))

        # test get two teams urls
        # расскоменти, что бы попробовать!
        self.get_two_teams_url(d['home_team'][20], d['away_team'][20], "Футбол", driver)

        # test get all teams urls
        # расскоменти, что бы попробовать!
        # self.get_all_teams_url("Футбол", driver)

        # check the results of url parsing. May be deleted
        print(self.team_urls)
        print(len(self.team_urls))
        driver.close()
        return d


if __name__ == "__main__":
    full = Parser()
    test = input("Введите название спорта:")
    full.SportToday(test)
