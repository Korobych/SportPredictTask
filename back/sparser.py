from bs4 import BeautifulSoup
import requests
from requests_html import HTMLSession
import sys
from selenium import webdriver
import selenium
import numpy as np
import pandas as pnd
import time as t


# Today
class Parser:
    def __init__(self):
        self.url = 'https://www.myscore.ru'
        self.urls = {
            "Хоккей": "/hockey", "Теннис": "/tennis", "Баскетбол": "/basketball",
            "Волейбол": "/volleyball", "Гандбол": "/handball", "Футзал": "/futsal",
            "Бейсбол": "/baseball", "Футбол": "/"}
        self.team_urls = {}
        self.docker = '/app/back/chromedriver'

    def SportToday(self, sport, first="", sec=""):
        teams_home_array = []
        teams_away_array = []
        teams_home_scores = []
        teams_away_scores = []
        games_statuses_array = []
        games_start_times_array = []

        if sport == "Футбол":
            if len(first) == 0:
                t = self.FootBall()
                return t
            else:
                t = self.FootBall(first, sec)
                return t

        driver = webdriver.Chrome('/home/prazd/selenium/chromedriver')
        # driver = webdriver.Chrome('/Users/Koroba/Downloads/chromedriver')
        url = self.url + self.urls[sport]
        driver.get(url)
        teams_home = driver.find_elements_by_class_name("padl")
        i = 0
        while i < len(teams_home):
            teams_home_array += [teams_home[i].text]
            teams_away_array += [teams_home[i + 1].text]
            i += 2

        if len(teams_away_array) == len(teams_home_array) and len(teams_away_array) > 0:
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

            d = {'start_time': games_start_times_array, 'game_status': games_statuses_array,
                 'home_team': teams_home_array,
                 'score_home': teams_home_scores, 'score_away': teams_away_scores, 'away_team': teams_away_array}
            # todayDataFrame = pnd.DataFrame(data = d)
            # print(todayDataFrame)
        else:
            return "Bad"

    # def GetLeagues(self, sport, driver):
    #     if sport == "Футбол":
    #         check = driver.find_elements_by_class_name("expand-league")
    #         i = 0
    #         while i < len(check):
    #             try:
    #                 check[i].click()
    #                 i += 1
    #             except selenium.common.exceptions.WebDriverException:
    #                 i + 1
    #         print("end")
    #         t.sleep(2)
    #         driver.execute_script("window.scrollTo(0,0);")
    #         t.sleep(2)
    #         return driver
    #     else:
    #         pass

    def get_all_matches_info(self, sport, driver):
        if sport == "Футбол":
            # init clicks
            driver = self.GetLeagues("Футбол", driver)

            teams_home_array = []
            teams_away_array = []
            all_games_scores_array = []
            games_statuses_array = []
            games_start_times_array = []
            league_array = []
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
                for item in trs:
                    team_home = item.find_element_by_class_name("padr")
                    teams_home_array.append(team_home.text)

                    team_away = item.find_element_by_class_name("padl")
                    teams_away_array.append(team_away.text)

                    game_score = item.find_element_by_class_name("cell_sa")
                    all_games_scores_array.append(game_score.text.replace('\xa0', ''))

                    game_status = item.find_element_by_class_name("cell_aa")
                    games_statuses_array.append(game_status.text)

                    game_start_time = item.find_element_by_class_name("cell_ad")
                    games_start_times_array.append(game_start_time.text)

                    league_array.append(league_string)

            # check number of games in league_array --  May be deleted
            print(len(league_array))

            print(len(teams_home_array), 'count of team_home')
            print(len(teams_away_array), 'count of team_away')
            print(len(all_games_scores_array), 'count of scores')
            print(len(games_statuses_array), 'count of statuses')
            print(len(games_start_times_array), 'count of start_times')

            d = {'start_time': games_start_times_array, 'game_status': games_statuses_array,
                 'home_team': teams_home_array,
                 'score': all_games_scores_array, 'away_team': teams_away_array, 'league': league_array}
            df = pnd.DataFrame(data=d)
            #saving to csv
            df.to_csv("full_football_games_info.csv", sep=';', header=True, index=False, encoding='utf-8')
            return d

    def light_matches_info(self, sport, driver):
        if sport == "Футбол":
            teams_home_array = []
            teams_away_array = []
            all_games_scores_array = []
            games_statuses_array = []
            games_start_times_array = []
            league_array = []
            soccer_bloсks = driver.find_elements_by_class_name("soccer")
            last_block = ""
            for block in soccer_bloсks:
                country = block.find_element_by_class_name("country_part")
                tournament = block.find_element_by_class_name("tournament_part")
                league_string = country.text + tournament.text
                if last_block == league_string:
                    continue

                last_block = league_string
                try:
                    tbody = block.find_element_by_tag_name("tbody")
                except selenium.common.exceptions.NoSuchElementException:
                    continue

                trs = tbody.find_elements_by_tag_name("tr")
                for item in trs:
                    team_home = item.find_element_by_class_name("padr")
                    teams_home_array.append(team_home.text)

                    team_away = item.find_element_by_class_name("padl")
                    teams_away_array.append(team_away.text)

                    game_score = item.find_element_by_class_name("cell_sa")
                    all_games_scores_array.append(game_score.text.replace('\xa0', ''))

                    game_status = item.find_element_by_class_name("cell_aa")
                    games_statuses_array.append(game_status.text)

                    game_start_time = item.find_element_by_class_name("cell_ad")
                    games_start_times_array.append(game_start_time.text)

                    league_array.append(league_string)

            # check number of games in league_array --  May be deleted
            print(len(league_array))

            print(len(teams_home_array), 'count of team_home')
            print(len(teams_away_array), 'count of team_away')
            print(len(all_games_scores_array), 'count of scores')
            print(len(games_statuses_array), 'count of statuses')
            print(len(games_start_times_array), 'count of start_times')
            print(league_array)

            d = {'start_time': games_start_times_array, 'game_status': games_statuses_array,
                 'home_team': teams_home_array,
                 'score': all_games_scores_array, 'away_team': teams_away_array, 'league': league_array}

            df = pnd.DataFrame(data=d)
            # saving to csv
            df.to_csv("light_football_games_info.csv", sep=';', header=True, index=False, encoding='utf-8')
            return d

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
                        # t.sleep(5)
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

    def FootBall(self, first="", sec=""):  # Footbal
        chrome_options = webdriver.ChromeOptions()

        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        # driver = webdriver.Chrome(self.docker,chrome_options=chrome_options) # for docker

        driver = webdriver.Chrome('/home/prazd/selenium/chromedriver')
        # driver = webdriver.Chrome('/Users/Koroba/Downloads/chromedriver')

        url = self.url + self.urls["Футбол"]
        driver.get(url)
        # t.sleep(20)
        t.sleep(2)
        start = t.time()

        # call for data grabbing func. Light version
        d = self.light_matches_info("Футбол", driver)

        # Full version
        # d = self.get_all_matches_info("Футбол", driver)

        end = t.time()
        print("время выполнения парсинга - ", end - start, " секунд.")

        # test get two teams urls
        # расскоменти, что бы попробовать!
        # self.get_two_teams_url(d['home_team'][20], d['away_team'][20], "Футбол", driver)

        # test get all teams urls
        # расскоменти, что бы попробовать!
        # self.get_all_teams_url("Футбол", driver)

        if len(first) == 0:
            self.get_two_teams_url(d['home_team'][0], d['away_team'][0], "Футбол", driver)
            # t.sleep(10)
            print(self.team_urls)
            print(len(self.team_urls))
            driver.close()
            return d
        else:
            self.get_two_teams_url(first, sec, "Футбол", driver)
            # t.sleep(10)
            print(self.team_urls)
            print(len(self.team_urls))
            driver.close()
            return d


if __name__ == "__main__":
    full = Parser()
    test = input("Введите название спорта:")
    full.SportToday(test, "Атлетико", "Бетис")
