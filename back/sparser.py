from bs4 import BeautifulSoup
import requests
from requests_html import HTMLSession
import sys
import os.path
from selenium import webdriver
import selenium
import numpy as np
import pandas as pnd
import time as t
import threading
import subprocess
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

# Today
class Parser:
    def __init__(self):
        self.url = 'https://www.myscore.ru'
        self.urls = {
            "Хоккей": "/hockey", "Теннис": "/tennis", "Баскетбол": "/basketball",
            "Волейбол": "/volleyball", "Гандбол": "/handball", "Футзал": "/futsal",
            "Бейсбол": "/baseball", "Футбол": "/"}
        self.team_urls = {}

        self.homeTeamDF = None
        self.awayTeamDF = None
        self.homeTeamOppDF = None
        self.awayTeamOppDF = None

        self.homeSecondTeamDF = None
        self.awaySecondTeamDF = None
        self.homeSecondTeamOppDF = None
        self.awaySecondTeamOppDF = None
        self.counter = 0

        
        # self.selDriver =  '/home/prazd/selenium/chromedriver' # for prazd
        # self.selDriver =  '/Users/Koroba/Downloads/chromedriver' # for koroba
        self.selDriver =  '/app/back/chromedriver' # for docker

        self.forPngCount = 0

        #self.my_path = '/Users/Koroba/PycharmProjects/SportPredictTask/back'
        # self.my_path = '/home/prazd/projects/SportPredictTask/back/'
        self.my_path =  '/app/back'
      

    def SportToday(self, sport, first, sec):
        teams_home_array = []
        teams_away_array = []
        teams_home_scores = []
        teams_away_scores = []
        games_statuses_array = []
        games_start_times_array = []

        if sport == "Футбол":
            if len(first) == 0:
                t = self.FootBall()
                return 
            else:
                t = self.FootBall(first, sec)
                return t
        else:
            t = self.Sport(first,sec,sport)
            return t

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
            for block in soccer_bloсks[1:]:
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
            df.to_csv("light_football_games_info.csv", header=True, index=False, encoding='utf-8')
            return d
        else:
            teams_home_array = []
            teams_away_array = []
            all_games_scores_array = []
            league_array = []
            all_team_array = []
            teams_home_scores = []
            teams_away_scores = []
            games_statuses_array = []
            games_start_times_array = []
            find = self.urls[sport][1:]
            bloсks = driver.find_elements_by_class_name(find)
            
            last_block = ""
            for block in bloсks[1:]:
                country = block.find_element_by_class_name("country_part")
                tournament = block.find_element_by_class_name("tournament_part")
                count = block.find_elements_by_class_name("cell_sc")
                print(len(count))
                league_string = country.text + tournament.text
                for i in range(len(count)):
                    league_array.append(league_string)

            teams = driver.find_elements_by_class_name("padl")
            i = 0
            while i < len(teams):
                teams_home_array += [teams[i].text]
                teams_away_array += [teams[i + 1].text]
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

                print(len(league_array))
                print(len(teams_home_array), 'count of team_home')
                print(len(teams_away_array), 'count of team_away')
                print(len(teams_home_scores), 'count of scores')
                print(len(games_statuses_array), 'count of statuses')
                print(len(games_start_times_array), 'count of start_times')
                
                d = {'start_time': games_start_times_array, 'game_status': games_statuses_array,
                 'home_team': teams_home_array, 'away_team': teams_away_array,
                 'score_home':teams_home_scores,"score_away":teams_away_scores,'league':league_array}
                df = pnd.DataFrame(data=d)
                
                # saving to csv
                df.to_csv("light_"+find+"_games_info.csv", header=True, index=False, encoding='utf-8')
                return d

    def get_two_teams_url(self, team1, team2, sport, driver):
        window_before = driver.window_handles[0]
        if sport == "Футбол":
            soccer_bloсks = driver.find_elements_by_class_name("soccer")
            for block in soccer_bloсks[1:]:
                try:
                    tbody = block.find_element_by_tag_name("tbody")
                except selenium.common.exceptions.NoSuchElementException:
                        continue
                trs = tbody.find_elements_by_tag_name("tr")
                print(len(trs), '- количество игр в лиге')
                for el in trs:
                    padr = el.find_element_by_class_name("padr")
                    padl = el.find_element_by_class_name("padl")
                    if (padr.text.strip() == team1 and padl.text.strip() == team2 or
                            padr.text.strip() == team2 and padl.text.strip() == team1):
                        el.click()
                        t.sleep(2)
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
                            
                            team_url += "/results"
                            # <---------------------------------------- Обрати внимание
                            print(team_name, '- название команды')
                            print(team_url, '- ссылка на страницу')
                            self.team_urls.update({team_name: team_url})
                        driver.close()
                        driver.switch_to.window(window_before)
                        return 
                    else:
                        print("нет такой пары команд")
                        print("Спарсилось:", padr.text.strip(),padl.text.strip())
        else:
            find = self.urls[sport][1:]
            sport_bloсks = driver.find_elements_by_class_name(find)
            
            print(sport_bloсks)
            for block in sport_bloсks[1:]:
                tbody = block.find_element_by_tag_name("tbody")
                trs = tbody.find_elements_by_tag_name("tr")
                print(len(trs)//2, '- количество игр в лиге')
                for el in trs:
                    try:
                        padl = el.find_element_by_class_name("padl")
                    except selenium.common.exceptions.NoSuchElementException:
                        continue
                    print(padl.text)
                    if padl.text == team2 or padl.text == team1:
                        try:
                            el.click()
                            t.sleep(4)
                        except selenium.common.exceptions.NoSuchElementException:
                            continue
                        window_after = driver.window_handles[1]
                        driver.switch_to.window(window_after)
                        teams_url_data = driver.find_elements_by_class_name("participant-imglink")
                        teams_url_data = np.array(teams_url_data)
                        teams_url_data = teams_url_data[[1, 3]]
                        print(len(teams_url_data), ' - количество команд')
                        for team in teams_url_data:
                            team_name = team.text
                            team_url = team.get_attribute("onclick")
                            team_url = team_url.replace('window.open(\'', '')
                            team_url = team_url.replace('\'); return false;', '')

                            team_url += "/results"
                            # <---------------------------------------- Обрати внимание
                            print(team_name, '- название команды')
                            print(team_url, '- ссылка на страницу')
                            self.team_urls.update({team_name: team_url})
                        driver.close()
                        driver.switch_to.window(window_before)
                        return
                    else:
                        print("нет такой пары команд")

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

        driver = webdriver.Chrome(self.selDriver,chrome_options=chrome_options) 
        # driver = webdriver.Chrome(self.selDriver)
        # driver = webdriver.Chrome('/home/prazd/selenium/chromedriver',chrome_options=chrome_options)
        # driver = webdriver.Chrome('/Users/Koroba/Downloads/chromedriver')

        url = self.url + self.urls["Футбол"]
        driver.get(url)
        # t.sleep(20)
        t.sleep(10)
        start = t.time()

        # call for data grabbing func. Light version
        d = self.light_matches_info("Футбол", driver)
        # Full version

        # d = self.get_all_matches_info("Футбол", driver)
        end = t.time()
        print("время выполнения парсинга - ", end - start, " секунд.")
        if d == "Bad":
            print("BAD")
            return "bad"
        if len(first) == 0:
            self.get_two_teams_url(d['home_team'][0], d['away_team'][0], "Футбол", driver)
            # t.sleep(10)
            print(self.team_urls)
            print(len(self.team_urls))
            driver.close()
            if len(self.team_urls)==0:
                return "bad"
            else: 
                return "nice"
        else:
            self.get_two_teams_url(first, sec, "Футбол", driver)
            # t.sleep(10)
            print(self.team_urls)
            print(len(self.team_urls))
            driver.close()
            if len(self.team_urls)==0:
                return "bad"
            else: 
                return "nice"


    def Sport(self,first,second,sport):

        chrome_options = webdriver.ChromeOptions()

        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        # driver = webdriver.Chrome(self.selDriver)
        driver = webdriver.Chrome(self.selDriver,chrome_options=chrome_options)
        # driver = webdriver.Chrome('/home/prazd/selenium/chromedriver',chrome_options=chrome_options)
        # driver = webdriver.Chrome('/Users/Koroba/Downloads/chromedriver')

        change = self.url + self.urls[sport]
        driver.get(change)
        t.sleep(2)
        start = t.time()
        d = self.light_matches_info(sport, driver)
        end = t.time()
        print("время выполнения парсинга - ", end - start, " секунд.")
        if d == "Bad":
            print("BAD")
            return "bad"
        if len(first) == 0:
            self.get_two_teams_url(d['home_team'][10], d['away_team'][10],sport, driver) 
            print(self.team_urls)
            print(len(self.team_urls))
            driver.close()
            if len(self.team_urls)==0:
                return "bad"
            else: 
                return "nice"
        else:
            self.get_two_teams_url(first, second, sport, driver) 
            # t.sleep(10)
            print(self.team_urls)
            print(len(self.team_urls))
            driver.close()
            if len(self.team_urls)==0:
                return "bad"
            else: 
                return "nice"
    
    def searchFootballInfo(self, teamName, url, writer):
        
        chrome_options = webdriver.ChromeOptions()

        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(self.selDriver,chrome_options=chrome_options) 
        # driver = webdriver.Chrome(self.selDriver)
        # driver = webdriver.Chrome('/home/prazd/selenium/chromedriver',chrome_options=chrome_options)
        # driver = webdriver.Chrome('/Users/Koroba/Downloads/chromedriver')
        print('Начинаем собирать информацию для ', teamName)

        driver.get(url)
        t.sleep(2)
        window_before = driver.window_handles[0]
        ### Your part

        me_home_game_name = []
        me_home_good_goals = []
        me_home_missed_goals = []
        me_home_total_goals = []
        me_home_ball_control = []
        me_home_own_ball_hits = []
        me_home_enemy_ball_hits = []
        me_home_own_target_ball_hits = []
        me_home_own_missed_ball_hits = []
        me_home_enemy_blocked_hits = []
        me_home_standarts = [] # штрафные
        me_home_corner_kicks = []
        me_home_offsides = []
        me_home_saves = []
        me_home_fauls = []
        me_home_yc = []
        me_home_rc = []

        #my team home calculated arrays
        me_home_percent_goals_kicks = []
        me_home_percent_target_goals_kicks = []
        me_home_percent_enemy_blocked_kicks = []
        me_home_sum_of_badthings = []

        #
        # my team away arrays
        #

        me_away_game_name = []
        me_away_good_goals = []
        me_away_missed_goals = []
        me_away_total_goals = []
        me_away_ball_control = []
        me_away_own_ball_hits = []
        me_away_enemy_ball_hits = []
        me_away_own_target_ball_hits = []
        me_away_own_missed_ball_hits = []
        me_away_enemy_blocked_hits = []
        me_away_standarts = []  # штрафные
        me_away_corner_kicks = []
        me_away_offsides = []
        me_away_saves = []
        me_away_fauls = []
        me_away_yc = []
        me_away_rc = []

        # my team away calculated arrays
        me_away_percent_goals_kicks = []
        me_away_percent_target_goals_kicks = []
        me_away_percent_enemy_blocked_kicks = []
        me_away_sum_of_badthings = []

        #
        # enemy team away arrays
        #

        enemy_away_game_name = []
        enemy_away_good_goals = []
        enemy_away_missed_goals = []
        enemy_away_total_goals = []
        enemy_away_ball_control = []
        enemy_away_own_ball_hits = []
        enemy_away_me_ball_hits = []
        enemy_away_own_target_ball_hits = []
        enemy_away_own_missed_ball_hits = []
        enemy_away_me_blocked_hits = []
        enemy_away_standarts = []  # штрафные
        enemy_away_corner_kicks = []
        enemy_away_offsides = []
        enemy_away_saves = []
        enemy_away_fauls = []
        enemy_away_yc = []
        enemy_away_rc = []

        # enemy team away calculated arrays
        enemy_away_percent_goals_kicks = []
        enemy_away_percent_target_goals_kicks = []
        enemy_away_percent_me_blocked_kicks = []
        enemy_away_sum_of_badthings = []

        #
        # enemy team home arrays
        #

        enemy_home_game_name = []
        enemy_home_good_goals = []
        enemy_home_missed_goals = []
        enemy_home_total_goals = []
        enemy_home_ball_control = []
        enemy_home_own_ball_hits = []
        enemy_home_me_ball_hits = []
        enemy_home_own_target_ball_hits = []
        enemy_home_own_missed_ball_hits = []
        enemy_home_me_blocked_hits = []
        enemy_home_standarts = []  # штрафные
        enemy_home_corner_kicks = []
        enemy_home_offsides = []
        enemy_home_saves = []
        enemy_home_fauls = []
        enemy_home_yc = []
        enemy_home_rc = []

        # enemy team home calculated arrays
        enemy_home_percent_goals_kicks = []
        enemy_home_percent_target_goals_kicks = []
        enemy_home_percent_me_blocked_kicks = []
        enemy_home_sum_of_badthings = []


        soccer_bloсks = driver.find_elements_by_class_name("soccer")
        forPngCount = 0
        # for tr in trs:

        for block in soccer_bloсks[1:]:
            if self.counter == 7:
                self.counter = 0
                break
            try:
                tbody = block.find_element_by_tag_name("tbody")
            except selenium.common.exceptions.NoSuchElementException:
                continue
            trs = tbody.find_elements_by_tag_name("tr")
            for tr in trs:
                    padr = tr.find_element_by_class_name('padr')
                    padl = tr.find_element_by_class_name('padl')


            # home_df updating
                    if teamName == padr.text.strip():
                        try:
                            tr.click()
                        except selenium.common.exceptions.StaleElementReferenceException: 
                            print("Unclick")
                            driver.close()
                            driver.switch_to.window(window_before)
                            continue

                        window_after = driver.window_handles[1]
                        driver.switch_to.window(window_after)
                        t.sleep(2)
                        try:
                            stats = driver.find_element_by_id('a-match-statistics')
                        except selenium.common.exceptions.NoSuchElementException:
                            print('\nНет статистики матча!\n')
                            driver.close()
                            driver.switch_to.window(window_before)
                            continue

                        away_team_name = driver.find_elements_by_class_name('participant-imglink')
                        # game name append
                        game_name = teamName + ' - ' + away_team_name[3].text
                        print(game_name)
                        me_home_game_name.append(game_name)
                        enemy_away_game_name.append(game_name)
                        
                        ############## for unclick
                        try:
                            stats.click()
                            t.sleep(2)
                        except selenium.common.exceptions.ElementNotVisibleException:
                            t.sleep(2)
                            stats.click()
                            t.sleep(2)
                        except selenium.common.exceptions.StaleElementReferenceException: 
                            print("Unclick")
                            me_home_game_name.pop()
                            enemy_away_game_name.pop()
                            driver.close()
                            driver.switch_to.window(window_before)
                            continue
                        

                        # goals detection
                        score = driver.find_elements_by_class_name('scoreboard')
                        print(score[0].text, score[1].text)
                        me_home_good_goals.append(score[0].text)
                        me_home_missed_goals.append(score[1].text)
                        me_home_total_goals.append(int(score[0].text) + int(score[1].text))

                        enemy_away_good_goals.append(score[1].text)
                        enemy_away_missed_goals.append(score[0].text)
                        enemy_away_total_goals.append(int(score[0].text) + int(score[1].text))
                        table = driver.find_element_by_id('tab-statistics-0-statistic')
                        rows = table.find_elements_by_class_name('statRow')
                        for row in rows:
                            group = row.find_element_by_class_name('statTextGroup')
                            param_name = group.find_element_by_css_selector('.statText.statText--titleValue')
                            home_value = group.find_element_by_css_selector('.statText.statText--homeValue')
                            away_value = group.find_element_by_css_selector('.statText.statText--awayValue')

                            if param_name.text == "Владение мячом":
                                if home_value.text.startswith('-') and home_value.text[1:].isdigit():
                                    me_home_ball_control.append('0')
                                else:
                                    me_home_ball_control.append(home_value.text)
                                if away_value.text.startswith('-') and away_value.text[1:].isdigit():
                                    enemy_away_ball_control.append('0')
                                else:
                                    enemy_away_ball_control.append(away_value.text)
                            if param_name.text == "Удары":
                                if home_value.text.startswith('-') and home_value.text[1:].isdigit():
                                    me_home_own_ball_hits.append('0')
                                    enemy_away_me_ball_hits.append('0')
                                else:
                                    me_home_own_ball_hits.append(home_value.text)
                                    enemy_away_me_ball_hits.append(home_value.text)
                                if away_value.text.startswith('-') and away_value.text[1:].isdigit():
                                    me_home_enemy_ball_hits.append('0')
                                    enemy_away_own_ball_hits.append('0')
                                else:
                                    me_home_enemy_ball_hits.append(away_value.text)
                                    enemy_away_own_ball_hits.append(away_value.text)
                            if param_name.text == "Удары в створ":
                                if home_value.text.startswith('-') and home_value.text[1:].isdigit():
                                    me_home_own_target_ball_hits.append('0')
                                else:
                                    me_home_own_target_ball_hits.append(home_value.text)
                                if away_value.text.startswith('-') and away_value.text[1:].isdigit():
                                    enemy_away_own_target_ball_hits.append('0')
                                else:
                                    enemy_away_own_target_ball_hits.append(away_value.text)
                            if param_name.text == "Удары мимо":
                                if home_value.text.startswith('-') and home_value.text[1:].isdigit():
                                    me_home_own_missed_ball_hits.append('0')
                                else:
                                    me_home_own_missed_ball_hits.append(home_value.text)
                                if away_value.text.startswith('-') and away_value.text[1:].isdigit():
                                    enemy_away_own_missed_ball_hits.append('0')
                                else:
                                    enemy_away_own_missed_ball_hits.append(away_value.text)
                            if param_name.text == "Блок-но ударов":
                                if home_value.text.startswith('-') and home_value.text[1:].isdigit():
                                    enemy_away_me_blocked_hits.append('0')
                                else:
                                    enemy_away_me_blocked_hits.append(home_value.text)
                                if away_value.text.startswith('-') and away_value.text[1:].isdigit():
                                    me_home_enemy_blocked_hits.append('0')
                                else:
                                    me_home_enemy_blocked_hits.append(away_value.text)
                            if param_name.text == "Штрафные":
                                if home_value.text.startswith('-') and home_value.text[1:].isdigit():
                                    me_home_standarts.append('0')
                                else:
                                    me_home_standarts.append(home_value.text)
                                if away_value.text.startswith('-') and away_value.text[1:].isdigit():
                                    enemy_away_standarts.append('0')
                                else:
                                    enemy_away_standarts.append(away_value.text)
                            if param_name.text == "Угловые":
                                if home_value.text.startswith('-') and home_value.text[1:].isdigit():
                                    me_home_corner_kicks.append('0')
                                else:
                                    me_home_corner_kicks.append(home_value.text)
                                if away_value.text.startswith('-') and away_value.text[1:].isdigit():
                                    enemy_away_corner_kicks.append('0')
                                else:
                                    enemy_away_corner_kicks.append(away_value.text)
                            if param_name.text == "Офсайды":
                                if home_value.text.startswith('-') and home_value.text[1:].isdigit():
                                    me_home_offsides.append('0')
                                else:
                                    me_home_offsides.append(home_value.text)
                                if away_value.text.startswith('-') and away_value.text[1:].isdigit():
                                    enemy_away_offsides.append('0')
                                else:
                                    enemy_away_offsides.append(away_value.text)
                            if param_name.text == "Сэйвы":
                                if home_value.text.startswith('-') and home_value.text[1:].isdigit():
                                    me_home_saves.append('0')
                                else:
                                    me_home_saves.append(home_value.text)
                                if away_value.text.startswith('-') and away_value.text[1:].isdigit():
                                    enemy_away_saves.append('0')
                                else:
                                    enemy_away_saves.append(away_value.text)
                            if param_name.text == "Фолы":
                                if home_value.text.startswith('-') and home_value.text[1:].isdigit():
                                    me_home_fauls.append('0')
                                else:
                                    me_home_fauls.append(home_value.text)
                                if away_value.text.startswith('-') and away_value.text[1:].isdigit():
                                    enemy_away_fauls.append('0')
                                else:
                                    enemy_away_fauls.append(away_value.text)
                            if param_name.text == "Желтые карточки":
                                if home_value.text.startswith('-') and home_value.text[1:].isdigit():
                                    me_home_yc.append('0')
                                else:
                                    me_home_yc.append(home_value.text)
                                if away_value.text.startswith('-') and away_value.text[1:].isdigit():
                                    enemy_away_yc.append('0')
                                else:
                                    enemy_away_yc.append(away_value.text)
                            if param_name.text == "Красные карточки":
                                if home_value.text.startswith('-') and home_value.text[1:].isdigit():
                                    me_home_rc.append('0')
                                else:
                                    me_home_rc.append(home_value.text)
                                if away_value.text.startswith('-') and away_value.text[1:].isdigit():
                                    enemy_away_rc.append('0')
                                else:
                                    enemy_away_rc.append(away_value.text)

                        counter = len(me_home_game_name)

                        while (counter != len(me_home_ball_control) or counter != len(me_home_own_ball_hits) or counter
                            != len(me_home_enemy_ball_hits) or counter != len(me_home_own_target_ball_hits) or counter
                            != len(me_home_own_missed_ball_hits) or counter != len(me_home_enemy_blocked_hits) or counter
                            != len(me_home_standarts) or counter != len(me_home_corner_kicks) or counter
                            != len(me_home_offsides) or counter != len(me_home_saves) or counter != len(me_home_fauls) or
                            counter != len(me_home_yc) or counter != len(me_home_rc)):

                            if len(me_home_ball_control) != counter:
                                me_home_ball_control.append('-')
                            if len(me_home_own_ball_hits) != counter:
                                me_home_own_ball_hits.append('-')
                            if len(me_home_enemy_ball_hits) != counter:
                                me_home_enemy_ball_hits.append('-')
                            if len(me_home_own_target_ball_hits) != counter:
                                me_home_own_target_ball_hits.append('-')
                            if len(me_home_own_missed_ball_hits) != counter:
                                me_home_own_missed_ball_hits.append('-')
                            if len(me_home_enemy_blocked_hits) != counter:
                                me_home_enemy_blocked_hits.append('-')
                            if len(me_home_standarts) != counter:
                                me_home_standarts.append('-')
                            if len(me_home_corner_kicks) != counter:
                                me_home_corner_kicks.append('-')
                            if len(me_home_offsides) != counter:
                                me_home_offsides.append('-')
                            if len(me_home_saves) != counter:
                                me_home_saves.append('-')
                            if len(me_home_fauls) != counter:
                                me_home_fauls.append('-')
                            if len(me_home_yc) != counter:
                                me_home_yc.append('-')
                            if len(me_home_rc) != counter:
                                me_home_rc.append('-')

                        # calculated arrays
                        me_home_percent_goals_kicks.append(int((100 / int(me_home_own_ball_hits[counter - 1])) *
                                                            int(me_home_good_goals[counter - 1])))
                        if me_home_own_target_ball_hits[counter - 1] != '-' and me_home_own_target_ball_hits[counter - 1] != '0':
                            me_home_percent_target_goals_kicks.append(int((100 / int(me_home_own_target_ball_hits[counter - 1]))
                                                                    * int(me_home_good_goals[counter - 1])))
                        else:
                            me_home_percent_target_goals_kicks.append('-')

                        if (me_home_enemy_ball_hits[counter - 1] != '-' and me_home_enemy_blocked_hits[counter - 1] != '-'
                                and me_home_enemy_ball_hits[counter - 1] != '0'):
                            me_home_percent_enemy_blocked_kicks.append(int((100 / int(me_home_enemy_ball_hits[counter - 1])) *
                                                            int(me_home_enemy_blocked_hits[counter - 1])))
                        else:
                            me_home_percent_enemy_blocked_kicks.append('-')

                        if (me_home_fauls[counter - 1] != '-' and me_home_yc[counter - 1] != '-' and
                            me_home_rc[counter - 1] != '-' and me_home_fauls[counter - 1] != '0'):
                            me_home_sum_of_badthings.append(int((100 / int(me_home_fauls[counter - 1])) *
                                int(me_home_yc[counter - 1]) + (100 / int(me_home_fauls[counter - 1])) *
                                                            int(me_home_rc[counter - 1])))
                        else:
                            me_home_sum_of_badthings.append('-')

                        print(counter, ' домашних матча выравлены')

                        counter = len(enemy_away_game_name)
                        while (counter != len(enemy_away_ball_control) or counter != len(enemy_away_own_ball_hits) or
                            counter != len(enemy_away_me_ball_hits) or counter != len(enemy_away_own_target_ball_hits)
                            or counter != len(enemy_away_own_missed_ball_hits) or counter
                            != len(enemy_away_me_blocked_hits) or counter != len(enemy_away_standarts) or counter
                            != len(enemy_away_corner_kicks) or counter != len(enemy_away_offsides) or counter
                            != len(enemy_away_saves) or counter != len(enemy_away_fauls) or counter != len(enemy_away_yc)
                            or counter != len(enemy_away_rc)):

                            if len(enemy_away_ball_control) != counter:
                                enemy_away_ball_control.append('-')
                            if len(enemy_away_own_ball_hits) != counter:
                                enemy_away_own_ball_hits.append('-')
                            if len(enemy_away_me_ball_hits) != counter:
                                enemy_away_me_ball_hits.append('-')
                            if len(enemy_away_own_target_ball_hits) != counter:
                                enemy_away_own_target_ball_hits.append('-')
                            if len(enemy_away_own_missed_ball_hits) != counter:
                                enemy_away_own_missed_ball_hits.append('-')
                            if len(enemy_away_me_blocked_hits) != counter:
                                enemy_away_me_blocked_hits.append('-')
                            if len(enemy_away_standarts) != counter:
                                enemy_away_standarts.append('-')
                            if len(enemy_away_corner_kicks) != counter:
                                enemy_away_corner_kicks.append('-')
                            if len(enemy_away_offsides) != counter:
                                enemy_away_offsides.append('-')
                            if len(enemy_away_saves) != counter:
                                enemy_away_saves.append('-')
                            if len(enemy_away_fauls) != counter:
                                enemy_away_fauls.append('-')
                            if len(enemy_away_yc) != counter:
                                enemy_away_yc.append('-')
                            if len(enemy_away_rc) != counter:
                                enemy_away_rc.append('-')

                        enemy_away_percent_goals_kicks.append(int((100 / int(enemy_away_own_ball_hits[counter - 1])) *
                                                        int(enemy_away_good_goals[counter - 1])))
                        if (enemy_away_own_target_ball_hits[counter - 1] != '-' and
                                enemy_away_own_target_ball_hits[counter - 1] != '0'):
                            enemy_away_percent_target_goals_kicks.append(int((100 / int(enemy_away_own_target_ball_hits[counter - 1]))
                                                                    * int(enemy_away_good_goals[counter - 1])))
                        else:
                            enemy_away_percent_target_goals_kicks.append('-')

                        if (enemy_away_me_ball_hits[counter - 1] != '-' and enemy_away_me_blocked_hits[counter - 1] != '-'
                                and enemy_away_me_ball_hits[counter - 1] != '0'):
                            enemy_away_percent_me_blocked_kicks.append(int((100 / int(enemy_away_me_ball_hits[counter - 1])) *
                                                                    int(enemy_away_me_blocked_hits[counter - 1])))
                        else:
                            enemy_away_percent_me_blocked_kicks.append('-')

                        if (enemy_away_fauls[counter - 1] != '-' and enemy_away_yc[counter - 1] != '-' and
                                enemy_away_rc[counter - 1] != '-' and enemy_away_fauls[counter - 1] != '0'):
                            enemy_away_sum_of_badthings.append(int((100 / int(enemy_away_fauls[counter - 1])) *
                                                            int(enemy_away_yc[counter - 1]) + (
                                                                        100 / int(enemy_away_fauls[counter - 1])) *
                                                            int(enemy_away_rc[counter - 1])))
                        else:
                            enemy_away_sum_of_badthings.append('-')
                        print(counter, ' мачта противника в гостях выравлены')

                        driver.close()
                        driver.switch_to.window(window_before)

                    # away_df updating
                    elif teamName == padl.text.strip():
                        try:
                            tr.click()
                        except selenium.common.exceptions.StaleElementReferenceException:
                            continue
                        window_after = driver.window_handles[1]
                        driver.switch_to.window(window_after)
                        t.sleep(2)
                        try:
                            stats = driver.find_element_by_id('a-match-statistics')
                        except selenium.common.exceptions.NoSuchElementException:
                            print('нет статистики матча')
                            driver.close()
                            driver.switch_to.window(window_before)
                            continue

                        home_team_name = driver.find_elements_by_class_name('participant-imglink')
                        # game name append
                        game_name = home_team_name[1].text + ' - ' + teamName
                        print(game_name)
                        enemy_home_game_name.append(game_name)
                        me_away_game_name.append(game_name)

                        try:
                            stats.click()
                            t.sleep(2)
                        except selenium.common.exceptions.StaleElementReferenceException:
                            print("Unclick")
                            driver.close()
                            driver.switch_to.window(window_before)
                            continue
                        except selenium.common.exceptions.ElementNotVisibleException:
                            t.sleep(2)
                            stats.click()
                            t.sleep(2)

                        # goals detection
                        score = driver.find_elements_by_class_name('scoreboard')
                        print(score[0].text, score[1].text)
                        enemy_home_good_goals.append(score[0].text)
                        enemy_home_missed_goals.append(score[1].text)
                        enemy_home_total_goals.append(int(score[0].text) + int(score[1].text))

                        me_away_good_goals.append(score[1].text)
                        me_away_missed_goals.append(score[0].text)
                        me_away_total_goals.append(int(score[0].text) + int(score[1].text))
                        table = driver.find_element_by_id('tab-statistics-0-statistic')
                        rows = table.find_elements_by_class_name('statRow')
                        for row in rows:
                            group = row.find_element_by_class_name('statTextGroup')
                            param_name = group.find_element_by_css_selector('.statText.statText--titleValue')
                            home_value = group.find_element_by_css_selector('.statText.statText--homeValue')
                            away_value = group.find_element_by_css_selector('.statText.statText--awayValue')

                            if param_name.text == "Владение мячом":
                                if home_value.text.startswith('-') and home_value.text[1:].isdigit():
                                    enemy_home_ball_control.append('0')
                                else:
                                    enemy_home_ball_control.append(home_value.text)
                                if away_value.text.startswith('-') and away_value.text[1:].isdigit():
                                    me_away_ball_control.append('0')
                                else:
                                    me_away_ball_control.append(away_value.text)
                            if param_name.text == "Удары":
                                print("in Удары:")
                                print(home_value.text,away_value.text)

                                if home_value.text.startswith('-') and home_value.text[1:].isdigit():
                                    enemy_home_own_ball_hits.append('0')
                                    me_away_enemy_ball_hits.append('0')
                                else:
                                    enemy_home_own_ball_hits.append(home_value.text)
                                    me_away_enemy_ball_hits.append(home_value.text)
                                if away_value.text.startswith('-') and away_value.text[1:].isdigit():
                                    enemy_home_me_ball_hits.append('0')
                                    me_away_own_ball_hits.append('0')
                                else:
                                    enemy_home_me_ball_hits.append(away_value.text)
                                    me_away_own_ball_hits.append(away_value.text)
                            if param_name.text == "Удары в створ":
                                if home_value.text.startswith('-') and home_value.text[1:].isdigit():
                                    enemy_home_own_target_ball_hits.append('0')
                                else:
                                    enemy_home_own_target_ball_hits.append(home_value.text)
                                if away_value.text.startswith('-') and away_value.text[1:].isdigit():
                                    me_away_own_target_ball_hits.append('0')
                                else:
                                    me_away_own_target_ball_hits.append(away_value.text)
                            if param_name.text == "Удары мимо":
                                if home_value.text.startswith('-') and home_value.text[1:].isdigit():
                                    enemy_home_own_missed_ball_hits.append('0')
                                else:
                                    enemy_home_own_missed_ball_hits.append(home_value.text)
                                if away_value.text.startswith('-') and away_value.text[1:].isdigit():
                                    me_away_own_missed_ball_hits.append('0')
                                else:
                                    me_away_own_missed_ball_hits.append(away_value.text)
                            if param_name.text == "Блок-но ударов":
                                if home_value.text.startswith('-') and home_value.text[1:].isdigit():
                                    me_away_enemy_blocked_hits.append('0')
                                else:
                                    me_away_enemy_blocked_hits.append(home_value.text)
                                if away_value.text.startswith('-') and away_value.text[1:].isdigit():
                                    enemy_home_me_blocked_hits.append('0')
                                else:
                                    enemy_home_me_blocked_hits.append(away_value.text)
                            if param_name.text == "Штрафные":
                                if home_value.text.startswith('-') and home_value.text[1:].isdigit():
                                    enemy_home_standarts.append('0')
                                else:
                                    enemy_home_standarts.append(home_value.text)
                                if away_value.text.startswith('-') and away_value.text[1:].isdigit():
                                    me_away_standarts.append('0')
                                else:
                                    me_away_standarts.append(away_value.text)
                            if param_name.text == "Угловые":
                                if home_value.text.startswith('-') and home_value.text[1:].isdigit():
                                    enemy_home_corner_kicks.append('0')
                                else:
                                    enemy_home_corner_kicks.append(home_value.text)
                                if away_value.text.startswith('-') and away_value.text[1:].isdigit():
                                    me_away_corner_kicks.append('0')
                                else:
                                    me_away_corner_kicks.append(away_value.text)
                            if param_name.text == "Офсайды":
                                if home_value.text.startswith('-') and home_value.text[1:].isdigit():
                                    enemy_home_offsides.append('0')
                                else:
                                    enemy_home_offsides.append(home_value.text)
                                if away_value.text.startswith('-') and away_value.text[1:].isdigit():
                                    me_away_offsides.append('0')
                                else:
                                    me_away_offsides.append(away_value.text)
                            if param_name.text == "Сэйвы":
                                if home_value.text.startswith('-') and home_value.text[1:].isdigit():
                                    enemy_home_saves.append('0')
                                else:
                                    enemy_home_saves.append(home_value.text)
                                if away_value.text.startswith('-') and away_value.text[1:].isdigit():
                                    me_away_saves.append('0')
                                else:
                                    me_away_saves.append(away_value.text)
                            if param_name.text == "Фолы":
                                if home_value.text.startswith('-') and home_value.text[1:].isdigit():
                                    enemy_home_fauls.append('0')
                                else:
                                    enemy_home_fauls.append(home_value.text)
                                if away_value.text.startswith('-') and away_value.text[1:].isdigit():
                                    me_away_fauls.append('0')
                                else:
                                    me_away_fauls.append(away_value.text)
                            if param_name.text == "Желтые карточки":
                                if home_value.text.startswith('-') and home_value.text[1:].isdigit():
                                    enemy_home_yc.append('0')
                                else:
                                    enemy_home_yc.append(home_value.text)
                                if away_value.text.startswith('-') and away_value.text[1:].isdigit():
                                    me_away_yc.append('0')
                                else:
                                    me_away_yc.append(away_value.text)
                            if param_name.text == "Красные карточки":
                                if home_value.text.startswith('-') and home_value.text[1:].isdigit():
                                    enemy_home_rc.append('0')
                                else:
                                    enemy_home_rc.append(home_value.text)
                                if away_value.text.startswith('-') and away_value.text[1:].isdigit():
                                    me_away_rc.append('0')
                                else:
                                    me_away_rc.append(away_value.text)

                        counter = len(me_away_game_name)
                        print("check for length")
                        print(counter, len(me_away_ball_control),len(me_away_own_ball_hits))

                        while (counter != len(me_away_ball_control) or counter != len(me_away_own_ball_hits) or counter
                            != len(me_away_enemy_ball_hits) or counter != len(me_away_own_target_ball_hits) or counter
                            != len(me_away_own_missed_ball_hits) or counter != len(me_away_enemy_blocked_hits) or counter
                            != len(me_away_standarts) or counter != len(me_away_corner_kicks) or counter
                            != len(me_away_offsides) or counter != len(me_away_saves) or counter != len(me_away_fauls) or
                            counter != len(me_away_yc) or counter != len(me_away_rc)):

                            if len(me_away_ball_control) != counter:
                                me_away_ball_control.append('-')
                            if len(me_away_own_ball_hits) != counter:
                                me_away_own_ball_hits.append('-')
                            if len(me_away_enemy_ball_hits) != counter:
                                me_away_enemy_ball_hits.append('-')
                            if len(me_away_own_target_ball_hits) != counter:
                                me_away_own_target_ball_hits.append('-')
                            if len(me_away_own_missed_ball_hits) != counter:
                                me_away_own_missed_ball_hits.append('-')
                            if len(me_away_enemy_blocked_hits) != counter:
                                me_away_enemy_blocked_hits.append('-')
                            if len(me_away_standarts) != counter:
                                me_away_standarts.append('-')
                            if len(me_away_corner_kicks) != counter:
                                me_away_corner_kicks.append('-')
                            if len(me_away_offsides) != counter:
                                me_away_offsides.append('-')
                            if len(me_away_saves) != counter:
                                me_away_saves.append('-')
                            if len(me_away_fauls) != counter:
                                me_away_fauls.append('-')
                            if len(me_away_yc) != counter:
                                me_away_yc.append('-')
                            if len(me_away_rc) != counter:
                                me_away_rc.append('-')

                        # calculated arrays
                        me_away_percent_goals_kicks.append(int((100 / int(me_away_own_ball_hits[counter - 1])) *
                                                            int(me_away_good_goals[counter - 1])))
                        if (me_away_own_target_ball_hits[counter - 1] != '-' and
                                me_away_own_target_ball_hits[counter - 1] != '0'):
                            me_away_percent_target_goals_kicks.append(int((100 / int(me_away_own_target_ball_hits[counter - 1]))
                                                                    * int(me_away_good_goals[counter - 1])))
                        else:
                            me_away_percent_target_goals_kicks.append('-')

                        if (me_away_enemy_ball_hits[counter - 1 ] != '-' and me_away_enemy_blocked_hits[counter - 1] != '-'
                                and me_away_enemy_ball_hits[counter - 1] != '0'):
                            me_away_percent_enemy_blocked_kicks.append(int((100 / int(me_away_enemy_ball_hits[counter - 1])) *
                                                            int(me_away_enemy_blocked_hits[counter - 1])))
                        else:
                            me_away_percent_enemy_blocked_kicks.append('-')

                        if (me_away_fauls[counter - 1] != '-' and me_away_yc[counter - 1] != '-' and
                            me_away_rc[counter - 1] != '-' and me_away_fauls[counter - 1] != '0'):
                            me_away_sum_of_badthings.append(int((100 / int(me_away_fauls[counter - 1])) *
                                int(me_away_yc[counter - 1]) + (100 / int(me_away_fauls[counter - 1])) *
                                                            int(me_away_rc[counter - 1])))
                        else:
                            me_away_sum_of_badthings.append('-')

                        print(counter, ' матча в гостях выравлены')

                        counter = len(enemy_home_game_name)
                        while (counter != len(enemy_home_ball_control) or counter != len(enemy_home_own_ball_hits) or
                            counter != len(enemy_home_me_ball_hits) or counter != len(enemy_home_own_target_ball_hits)
                            or counter != len(enemy_home_own_missed_ball_hits) or counter
                            != len(enemy_home_me_blocked_hits) or counter != len(enemy_home_standarts) or counter
                            != len(enemy_home_corner_kicks) or counter != len(enemy_home_offsides) or counter
                            != len(enemy_home_saves) or counter != len(enemy_home_fauls) or counter != len(enemy_home_yc)
                            or counter != len(enemy_home_rc)):

                            if len(enemy_home_ball_control) != counter:
                                enemy_home_ball_control.append('-')
                            if len(enemy_home_own_ball_hits) != counter:
                                enemy_home_own_ball_hits.append('-')
                            if len(enemy_home_me_ball_hits) != counter:
                                enemy_home_me_ball_hits.append('-')
                            if len(enemy_home_own_target_ball_hits) != counter:
                                enemy_home_own_target_ball_hits.append('-')
                            if len(enemy_home_own_missed_ball_hits) != counter:
                                enemy_home_own_missed_ball_hits.append('-')
                            if len(enemy_home_me_blocked_hits) != counter:
                                enemy_home_me_blocked_hits.append('-')
                            if len(enemy_home_standarts) != counter:
                                enemy_home_standarts.append('-')
                            if len(enemy_home_corner_kicks) != counter:
                                enemy_home_corner_kicks.append('-')
                            if len(enemy_home_offsides) != counter:
                                enemy_home_offsides.append('-')
                            if len(enemy_home_saves) != counter:
                                enemy_home_saves.append('-')
                            if len(enemy_home_fauls) != counter:
                                enemy_home_fauls.append('-')
                            if len(enemy_home_yc) != counter:
                                enemy_home_yc.append('-')
                            if len(enemy_home_rc) != counter:
                                enemy_home_rc.append('-')
                            

                        print("enemy_home_percent_goals_kicks:",enemy_home_percent_goals_kicks)

                        # print()

                        enemy_home_percent_goals_kicks.append(int((100 / int(enemy_home_own_ball_hits[counter - 1])) *
                                                            int(enemy_home_good_goals[counter - 1])))
                        if (enemy_home_own_target_ball_hits[counter - 1] != '-' and
                                enemy_home_own_target_ball_hits[counter - 1] != '0'):
                            enemy_home_percent_target_goals_kicks.append(int(
                                (100 / int(enemy_home_own_target_ball_hits[counter - 1]))
                                * int(enemy_home_good_goals[counter - 1])))
                        else:
                            enemy_home_percent_target_goals_kicks.append('-')

                        if (enemy_home_me_ball_hits[counter - 1] != '-' and enemy_home_me_blocked_hits[counter - 1] != '-'
                                and enemy_home_me_ball_hits[counter - 1] != '0'):
                            enemy_home_percent_me_blocked_kicks.append(int((100 / int(enemy_home_me_ball_hits[counter - 1])) *
                                                                    int(enemy_home_me_blocked_hits[counter - 1])))
                        else:
                            enemy_home_percent_me_blocked_kicks.append('-')

                        if (enemy_home_fauls[counter - 1] != '-' and enemy_home_yc[counter - 1] != '-' and
                                enemy_home_rc[counter - 1] != '-' and enemy_home_fauls[counter - 1] != '0'):
                            enemy_home_sum_of_badthings.append(int((100 / int(enemy_home_fauls[counter - 1])) *
                                                            int(enemy_home_yc[counter - 1]) + (
                                                                    100 / int(enemy_home_fauls[counter - 1])) *
                                                            int(enemy_home_rc[counter - 1])))
                        else:
                            enemy_home_sum_of_badthings.append('-')
                        print(counter, ' мачта противника дома выравлены')
                        self.counter += 1
                        driver.close()
                        driver.switch_to.window(window_before)

        listOfColumnsFoot = ['match_name', 'goals', 'missed',  'total', 'ball_control', 'own_kicks', 'enemy_kicks',
                              'target_kicks', 'missed_kicks', 'enemy_blocked', 'standarts', 'corner_kicks', 'offsides',
                              'saves', 'fauls', 'yellow_cards', 'red_cards','%goals_from_kicks',
                              '%goals_from_targets_kicks','%blocked_kicks_by_defence', 'fauls_proportion']

        me_home_d = {'match_name': me_home_game_name, 'goals': me_home_good_goals, 'missed': me_home_missed_goals,
                     'total': me_home_total_goals, 'ball_control': me_home_ball_control,
                     'own_kicks': me_home_own_ball_hits, 'enemy_kicks': me_home_enemy_ball_hits,
                     'target_kicks': me_home_own_target_ball_hits, 'missed_kicks': me_home_own_missed_ball_hits,
                     'enemy_blocked': me_home_enemy_blocked_hits, 'standarts': me_home_standarts,
                     'corner_kicks': me_home_corner_kicks, 'offsides': me_home_offsides, 'saves': me_home_saves,
                     'fauls': me_home_fauls, 'yellow_cards': me_home_yc, 'red_cards': me_home_rc,
                     '%goals_from_kicks': me_home_percent_goals_kicks,
                     '%goals_from_targets_kicks': me_home_percent_target_goals_kicks,
                     '%blocked_kicks_by_defence': me_home_percent_enemy_blocked_kicks,
                     'fauls_proportion': me_home_sum_of_badthings}

        me_home_df = pnd.DataFrame(data=me_home_d)
        # me_home_df.to_csv(teamName+"_team_home_games.csv", header=True, index=False, encoding='utf8')
        me_home_df.to_excel(writer,sheet_name=teamName+"_home_games", columns=listOfColumnsFoot)
        if self.forPngCount == 0:
            self.homeTeamDF = me_home_df
        elif self.forPngCount == 1:
            self.homeSecondTeamDF = me_home_df

        me_away_d = {'match_name': me_away_game_name, 'goals': me_away_good_goals, 'missed': me_away_missed_goals,
                     'total': me_away_total_goals, 'ball_control': me_away_ball_control,
                     'own_kicks': me_away_own_ball_hits, 'enemy_kicks': me_away_enemy_ball_hits,
                     'target_kicks': me_away_own_target_ball_hits, 'missed_kicks': me_away_own_missed_ball_hits,
                     'enemy_blocked': me_away_enemy_blocked_hits, 'standarts': me_away_standarts,
                     'corner_kicks': me_away_corner_kicks, 'offsides': me_away_offsides, 'saves': me_away_saves,
                     'fauls': me_away_fauls, 'yellow_cards': me_away_yc, 'red_cards': me_away_rc,
                     '%goals_from_kicks': me_away_percent_goals_kicks,
                     '%goals_from_targets_kicks': me_away_percent_target_goals_kicks,
                     '%blocked_kicks_by_defence': me_away_percent_enemy_blocked_kicks,
                     'fauls_proportion': me_away_sum_of_badthings}

        me_away_df = pnd.DataFrame(data=me_away_d)
        # me_away_df.to_csv(teamName+"_team_away_games.csv", header=True, index=False, encoding='utf8')
        me_away_df.to_excel(writer,sheet_name=teamName+"_away_games", columns=listOfColumnsFoot)
        if self.forPngCount == 0:
            self.awayTeamDF = me_away_df
        elif self.forPngCount == 1:
            self.awaySecondTeamDF = me_away_df

        opponent_away_d = {'match_name': enemy_away_game_name, 'goals': enemy_away_good_goals,
                     'missed': enemy_away_missed_goals,
                     'total': enemy_away_total_goals, 'ball_control': enemy_away_ball_control,
                     'own_kicks': enemy_away_own_ball_hits, 'enemy_kicks': enemy_away_me_ball_hits,
                     'target_kicks': enemy_away_own_target_ball_hits,
                     'missed_kicks': enemy_away_own_missed_ball_hits,
                     'enemy_blocked': enemy_away_me_blocked_hits, 'standarts': enemy_away_standarts,
                     'corner_kicks': enemy_away_corner_kicks, 'offsides': enemy_away_offsides,
                     'saves': enemy_away_saves,
                     'fauls': enemy_away_fauls, 'yellow_cards': enemy_away_yc, 'red_cards': enemy_away_rc,
                     '%goals_from_kicks': enemy_away_percent_goals_kicks,
                     '%goals_from_targets_kicks': enemy_away_percent_target_goals_kicks,
                     '%blocked_kicks_by_defence': enemy_away_percent_me_blocked_kicks,
                     'fauls_proportion': enemy_away_sum_of_badthings}

        opponent_away_df = pnd.DataFrame(data=opponent_away_d)
        # opponent_away_df.to_csv(teamName+"_team_opp_away.csv", header=True, index=False, encoding='utf8')
        opponent_away_df.to_excel(writer,sheet_name=teamName+"_opp_away", columns=listOfColumnsFoot)
        if self.forPngCount == 0:
            self.awayTeamOppDF = opponent_away_df
        elif self.forPngCount == 1:
            self.awaySecondTeamOppDF = opponent_away_df

        opponent_home_d = {'match_name': enemy_home_game_name, 'goals': enemy_home_good_goals,
                           'missed': enemy_home_missed_goals,
                           'total': enemy_home_total_goals, 'ball_control': enemy_home_ball_control,
                           'own_kicks': enemy_home_own_ball_hits, 'enemy_kicks': enemy_home_me_ball_hits,
                           'target_kicks': enemy_home_own_target_ball_hits,
                           'missed_kicks': enemy_home_own_missed_ball_hits,
                           'enemy_blocked': enemy_home_me_blocked_hits, 'standarts': enemy_home_standarts,
                           'corner_kicks': enemy_home_corner_kicks, 'offsides': enemy_home_offsides,
                           'saves': enemy_home_saves,
                           'fauls': enemy_home_fauls, 'yellow_cards': enemy_home_yc, 'red_cards': enemy_home_rc,
                           '%goals_from_kicks': enemy_home_percent_goals_kicks,
                           '%goals_from_targets_kicks': enemy_home_percent_target_goals_kicks,
                           '%blocked_kicks_by_defence': enemy_home_percent_me_blocked_kicks,
                           'fauls_proportion': enemy_home_sum_of_badthings}

        opponent_home_df = pnd.DataFrame(data=opponent_home_d)
        # opponent_home_df.to_csv(teamName+"_team_opponents_home.csv", header=True, index=False, encoding='utf8')
        opponent_home_df.to_excel(writer,sheet_name=teamName+"_opp_home", columns=listOfColumnsFoot)
        if self.forPngCount == 0:
            self.homeTeamOppDF = opponent_home_df
        elif self.forPngCount == 1:
            self.homeSecondTeamOppDF = opponent_home_df
        driver.close()
        # writer.save()

    def searchHockeyInfo(self, teamName, url, writer):
        chrome_options = webdriver.ChromeOptions()

        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(self.selDriver,chrome_options=chrome_options) 
        # driver = webdriver.Chrome(self.selDriver)
        # driver = webdriver.Chrome('/home/prazd/selenium/chromedriver',chrome_options=chrome_options)
        # driver = webdriver.Chrome('/Users/Koroba/Downloads/chromedriver')

        print('Начинаем собирать информацию для ', teamName)

        driver.get(url)
        t.sleep(10)
        window_before = driver.window_handles[0]
        ### Your part

        #
        # my team home arrays
        #

        me_home_game_name = []
        me_home_shots = []
        me_home_enemy_shots = []
        me_home_good_goals = []
        me_home_missed_goals = []
        me_home_blocked_kicks =[]
        me_home_parry_shots = []
        me_home_players_bans = []
        me_home_penalty_time = []
        me_home_enemy_players_bans = []
        me_home_enemy_penalty_time = []
        me_home_goals_full = [] #шайбы в большинстве
        me_home_goals_minor = [] #шайбы в меньшинстве
        me_home_strength_usage = [] #силовые приемы
        me_home_won_throw_ins = []
        me_home_lost_throw_ins = []
        me_home_goals_in_emtpy = []

        # my team home calculated arrays
        me_home_total_shots_to_home_team = []
        me_home_total_throw_ins = []
        me_home_percent_blocked_kicks = []
        me_home_percent_parry_shots = []
        me_home_percent_full_realization = []
        me_home_percent_won_throw_ins = []

        #
        # my team away arrays
        #

        me_away_game_name = []
        me_away_shots = []
        me_away_enemy_shots = []
        me_away_good_goals = []
        me_away_missed_goals = []
        me_away_blocked_kicks = []
        me_away_parry_shots = []
        me_away_players_bans = []
        me_away_penalty_time = []
        me_away_enemy_players_bans = []
        me_away_enemy_penalty_time = []
        me_away_goals_full = []  # шайбы в большинстве
        me_away_goals_minor = []  # шайбы в меньшинстве
        me_away_strength_usage = []  # силовые приемы
        me_away_won_throw_ins = []
        me_away_lost_throw_ins = []
        me_away_goals_in_emtpy = []

        # my team away calculated arrays
        me_away_total_shots_to_home_team = []
        me_away_total_throw_ins = []
        me_away_percent_blocked_kicks = []
        me_away_percent_parry_shots = []
        me_away_percent_full_realization = []
        me_away_percent_won_throw_ins = []

        #
        # enemy team away arrays
        #

        enemy_away_game_name = []
        enemy_away_shots = []
        enemy_away_enemy_shots = []
        enemy_away_good_goals = []
        enemy_away_missed_goals = []
        enemy_away_blocked_kicks = []
        enemy_away_parry_shots = []
        enemy_away_players_bans = []
        enemy_away_penalty_time = []
        enemy_away_me_players_bans = []
        enemy_away_me_penalty_time = []
        enemy_away_goals_full = []  # шайбы в большинстве
        enemy_away_goals_minor = []  # шайбы в меньшинстве
        enemy_away_strength_usage = []  # силовые приемы
        enemy_away_won_throw_ins = []
        enemy_away_lost_throw_ins = []
        enemy_away_goals_in_emtpy = []

        # enemy team away calculated arrays
        enemy_away_total_shots_to_guest_team = []
        enemy_away_total_throw_ins = []
        enemy_away_percent_blocked_kicks = []
        enemy_away_percent_parry_shots = []
        enemy_away_percent_full_realization = []
        enemy_away_percent_won_throw_ins = []

        #
        # enemy team home arrays
        #

        enemy_home_game_name = []
        enemy_home_shots = []
        enemy_home_enemy_shots = []
        enemy_home_good_goals = []
        enemy_home_missed_goals = []
        enemy_home_blocked_kicks = []
        enemy_home_parry_shots = []
        enemy_home_players_bans = []
        enemy_home_penalty_time = []
        enemy_home_me_players_bans = []
        enemy_home_me_penalty_time = []
        enemy_home_goals_full = []  # шайбы в большинстве
        enemy_home_goals_minor = []  # шайбы в меньшинстве
        enemy_home_strength_usage = []  # силовые приемы
        enemy_home_won_throw_ins = []
        enemy_home_lost_throw_ins = []
        enemy_home_goals_in_emtpy = []

        # enemy team home calculated arrays
        enemy_home_total_shots_to_guest_team = []
        enemy_home_total_throw_ins = []
        enemy_home_percent_blocked_kicks = []
        enemy_home_percent_parry_shots = []
        enemy_home_percent_full_realization = []
        enemy_home_percent_won_throw_ins = []

        # block = driver.find_element_by_id('fs-summary-results')
        # tbodys = block.find_elements_by_tag_name('tbody')
        # for tbody in tbodys:
        #     trs = tbody.find_elements_by_tag_name('tr')
        # find = self.urls[sport][1:]
        sport_bloсks = driver.find_elements_by_class_name('hockey')
            
        print(sport_bloсks)
        for block in sport_bloсks[1:]:
            if self.counter == 7:
                self.counter = 0
                break
            self.counter += 1
            tbody = block.find_element_by_tag_name("tbody")
            trs = tbody.find_elements_by_tag_name("tr")

            for tr in trs:
                # TODO! kick usual games from here. (Товарищеские матчи)
                padr = tr.find_elements_by_class_name('padl')[0]
                padl = tr.find_elements_by_class_name('padl')[1]
                # home_df updating
                if teamName == padr.text.strip():
                    
                    try:
                        tr.click()
                    except selenium.common.exceptions.StaleElementReferenceException:
                        print("Unclick")
                        driver.close()
                        driver.switch_to.window(window_before)
                        continue
                    except selenium.common.exceptions.ElementNotVisibleException:
                        t.sleep(2)
                        stats.click()
                        t.sleep(2)
                    
                    window_after = driver.window_handles[1]
                    driver.switch_to.window(window_after)
                    t.sleep(2)
                    try:
                        stats = driver.find_element_by_id('a-match-statistics')
                    except selenium.common.exceptions.NoSuchElementException:
                        print('\nНет статистики матча!\n')
                        driver.close()
                        driver.switch_to.window(window_before)
                        continue

                    away_team_name = driver.find_elements_by_class_name('participant-imglink')
                    # game name append
                    game_name = teamName + ' - ' + away_team_name[3].text
                    print(game_name)
                    me_home_game_name.append(game_name)
                    enemy_away_game_name.append(game_name)

                    try:
                        stats.click()
                        t.sleep(2)
                    except selenium.common.exceptions.ElementNotVisibleException:
                        t.sleep(2)
                        stats.click()
                        t.sleep(2)
                    except selenium.common.exceptions.StaleElementReferenceException: 
                        print("Unclick")
                        driver.close()
                        driver.switch_to.window(window_before)
                        continue

                    # goals detection
                    score = driver.find_elements_by_class_name('scoreboard')
                    print(score[0].text, score[1].text)
                    me_home_good_goals.append(score[0].text)
                    me_home_missed_goals.append(score[1].text)

                    enemy_away_good_goals.append(score[1].text)
                    enemy_away_missed_goals.append(score[0].text)
                    table = driver.find_element_by_id('tab-statistics-0-statistic')
                    rows = table.find_elements_by_class_name('statRow')
                    for row in rows:
                        group = row.find_element_by_class_name('statTextGroup')
                        param_name = group.find_element_by_css_selector('.statText.statText--titleValue')
                        home_value = group.find_element_by_css_selector('.statText.statText--homeValue')
                        away_value = group.find_element_by_css_selector('.statText.statText--awayValue')

                        if param_name.text == "Броски в створ ворот":
                            if home_value.text.startswith('-') and home_value.text[1:].isdigit():
                                me_home_shots.append('0')
                                enemy_away_enemy_shots.append('0')
                            else:
                                me_home_shots.append(home_value.text)
                                enemy_away_enemy_shots.append(home_value.text)
                            if away_value.text.startswith('-') and away_value.text[1:].isdigit():
                                me_home_enemy_shots.append('0')
                                enemy_away_shots.append('0')
                            else:
                                me_home_enemy_shots.append(away_value.text)
                                enemy_away_shots.append(away_value.text)
                        if param_name.text == "Блок-но ударов":
                            if home_value.text.startswith('-') and home_value.text[1:].isdigit():
                                me_home_blocked_kicks.append('0')
                            else:
                                me_home_blocked_kicks.append(home_value.text)
                            if away_value.text.startswith('-') and away_value.text[1:].isdigit():
                                enemy_away_blocked_kicks.append('0')
                            else:
                                enemy_away_blocked_kicks.append(away_value.text)
                        if param_name.text == "Отраженные броски":
                            if home_value.text.startswith('-') and home_value.text[1:].isdigit():
                                me_home_parry_shots.append('0')
                            else:
                                me_home_parry_shots.append(home_value.text)
                            if away_value.text.startswith('-') and away_value.text[1:].isdigit():
                                enemy_away_parry_shots.append('0')
                            else:
                                enemy_away_parry_shots.append(away_value.text)
                        if param_name.text == "Удаления":
                            if home_value.text.startswith('-') and home_value.text[1:].isdigit():
                                me_home_players_bans.append('0')
                                enemy_away_me_players_bans.append('0')
                            else:
                                me_home_players_bans.append(home_value.text)
                                enemy_away_me_players_bans.append(home_value.text)
                            if away_value.text.startswith('-') and away_value.text[1:].isdigit():
                                enemy_away_players_bans.append('0')
                                me_home_enemy_players_bans.append('0')
                            else:
                                enemy_away_players_bans.append(away_value.text)
                                me_home_enemy_players_bans.append(away_value.text)
                        if param_name.text == "Штрафное время":
                            if home_value.text.startswith('-') and home_value.text[1:].isdigit():
                                me_home_penalty_time.append('0')
                                enemy_away_me_penalty_time.append('0')
                            else:
                                me_home_penalty_time.append(home_value.text)
                                enemy_away_me_penalty_time.append(home_value.text)
                            if away_value.text.startswith('-') and away_value.text[1:].isdigit():
                                enemy_away_penalty_time.append('0')
                                me_home_enemy_penalty_time.append('0')
                            else:
                                enemy_away_penalty_time.append(away_value.text)
                                me_home_enemy_penalty_time.append(away_value.text)
                        if param_name.text == "Шайбы в большинстве":
                            if home_value.text.startswith('-') and home_value.text[1:].isdigit():
                                me_home_goals_full.append('0')
                            else:
                                me_home_goals_full.append(home_value.text)
                            if away_value.text.startswith('-') and away_value.text[1:].isdigit():
                                enemy_away_goals_full.append('0')
                            else:
                                enemy_away_goals_full.append(away_value.text)
                        if param_name.text == "Шайбы в меньшинстве":
                            if home_value.text.startswith('-') and home_value.text[1:].isdigit():
                                me_home_goals_minor.append('0')
                            else:
                                me_home_goals_minor.append(home_value.text)
                            if away_value.text.startswith('-') and away_value.text[1:].isdigit():
                                enemy_away_goals_minor.append('0')
                            else:
                                enemy_away_goals_minor.append(away_value.text)
                        if param_name.text == "Силовые приемы":
                            if home_value.text.startswith('-') and home_value.text[1:].isdigit():
                                me_home_strength_usage.append('0')
                            else:
                                me_home_strength_usage.append(home_value.text)
                            if away_value.text.startswith('-') and away_value.text[1:].isdigit():
                                enemy_away_strength_usage.append('0')
                            else:
                                enemy_away_strength_usage.append(away_value.text)
                        if param_name.text == "Выигр. вбрасывания":
                            if home_value.text.startswith('-') and home_value.text[1:].isdigit():
                                me_home_won_throw_ins.append('0')
                                enemy_away_lost_throw_ins.append('0')
                            else:
                                me_home_won_throw_ins.append(home_value.text)
                                enemy_away_lost_throw_ins.append(home_value.text)
                            if away_value.text.startswith('-') and away_value.text[1:].isdigit():
                                enemy_away_won_throw_ins.append('0')
                                me_home_lost_throw_ins.append('0')
                            else:
                                enemy_away_won_throw_ins.append(away_value.text)
                                me_home_lost_throw_ins.append(away_value.text)
                        if param_name.text == "Голы в пустые ворота":
                            if home_value.text.startswith('-') and home_value.text[1:].isdigit():
                                me_home_goals_in_emtpy.append('0')
                            else:
                                me_home_goals_in_emtpy.append(home_value.text)
                            if away_value.text.startswith('-') and away_value.text[1:].isdigit():
                                enemy_away_goals_in_emtpy.append('0')
                            else:
                                enemy_away_goals_in_emtpy.append(away_value.text)

                    counter = len(me_home_game_name)

                    while (counter != len(me_home_shots) or counter != len(me_home_enemy_shots) or counter
                           != len(me_home_blocked_kicks) or counter != len(me_home_parry_shots) or counter
                           != len(me_home_players_bans) or counter != len(me_home_penalty_time) or counter
                           != len(me_home_enemy_players_bans) or counter != len(me_home_enemy_penalty_time) or counter
                           != len(me_home_goals_full) or counter != len(me_home_goals_minor) or counter
                           != len(me_home_strength_usage) or counter != len(me_home_won_throw_ins) or
                           counter != len(me_home_lost_throw_ins) or counter != len(me_home_goals_in_emtpy)):

                        if len(me_home_shots) != counter:
                            me_home_shots.append('-')
                        if len(me_home_enemy_shots) != counter:
                            me_home_enemy_shots.append('-')
                        if len(me_home_blocked_kicks) != counter:
                            me_home_blocked_kicks.append('-')
                        if len(me_home_parry_shots) != counter:
                            me_home_parry_shots.append('-')
                        if len(me_home_players_bans) != counter:
                            me_home_players_bans.append('-')
                        if len(me_home_penalty_time) != counter:
                            me_home_penalty_time.append('-')
                        if len(me_home_enemy_players_bans) != counter:
                            me_home_enemy_players_bans.append('-')
                        if len(me_home_enemy_penalty_time) != counter:
                            me_home_enemy_penalty_time.append('-')
                        if len(me_home_goals_full) != counter:
                            me_home_goals_full.append('-')
                        if len(me_home_goals_minor) != counter:
                            me_home_goals_minor.append('-')
                        if len(me_home_strength_usage) != counter:
                            me_home_strength_usage.append('-')
                        if len(me_home_won_throw_ins) != counter:
                            me_home_won_throw_ins.append('-')
                        if len(me_home_lost_throw_ins) != counter:
                            me_home_lost_throw_ins.append('-')
                        if len(me_home_goals_in_emtpy) != counter:
                            me_home_goals_in_emtpy.append('-')

                    # calculated arrays
                    if me_home_enemy_shots[counter - 1] != '-' and me_home_blocked_kicks[counter - 1] != '-':
                        me_home_total_shots_to_home_team.append(int(me_home_enemy_shots[counter - 1]) +
                                                            int(me_home_blocked_kicks[counter - 1]))
                    else:
                        me_home_total_shots_to_home_team.append('-')

                    if me_home_won_throw_ins[counter - 1] != '-' and me_home_lost_throw_ins[counter - 1] != '-':
                        me_home_total_throw_ins.append(int(me_home_won_throw_ins[counter - 1]) +
                                                       int(me_home_lost_throw_ins[counter - 1]))
                    else:
                        me_home_total_throw_ins.append('-')
                    if (me_home_total_shots_to_home_team[counter - 1] != '-' and me_home_blocked_kicks[counter - 1] != '-'
                            and me_home_total_shots_to_home_team[counter - 1] != '0' and
                            me_home_blocked_kicks[counter - 1] != '0'):
                        me_home_percent_blocked_kicks.append(int((100 / int(me_home_total_shots_to_home_team[counter - 1]))) *
                                                                   int(me_home_blocked_kicks[counter - 1]))
                    else:
                        me_home_percent_blocked_kicks.append('-')

                    if (me_home_enemy_shots[counter - 1] != '-' and me_home_parry_shots[counter - 1] != '-' and
                            me_home_enemy_shots[counter - 1] != '0' and me_home_parry_shots[counter - 1] != '0'):
                        me_home_percent_parry_shots.append(int((100 / int(me_home_enemy_shots[counter - 1]))) *
                                                        int(me_home_parry_shots[counter - 1]))
                    else:
                        me_home_percent_parry_shots.append('-')
                    if (me_home_enemy_players_bans[counter - 1] != '-' and me_home_goals_full[counter - 1] != '-' and
                            me_home_enemy_players_bans[counter - 1] != '0' and me_home_goals_full[counter - 1] != '0'):
                        me_home_percent_full_realization.append(int((100 / int(me_home_enemy_players_bans[counter - 1]))) *
                                                                   int(me_home_goals_full[counter - 1]))
                    else:
                        me_home_percent_full_realization.append('-')
                    if (me_home_total_throw_ins[counter - 1] != '-' and me_home_won_throw_ins[counter - 1] != '-' and
                            me_home_total_throw_ins[counter - 1] != '0' and me_home_won_throw_ins[counter - 1] != '0'):
                        me_home_percent_won_throw_ins.append(int((100 / int(me_home_total_throw_ins[counter - 1]))) *
                                                                   int(me_home_won_throw_ins[counter - 1]))
                    else:
                        me_home_percent_won_throw_ins.append('-')

                    print(counter, ' домашних матча выравлены')

                    counter = len(enemy_away_game_name)
                    while (counter != len(enemy_away_shots) or counter != len(enemy_away_enemy_shots) or counter
                           != len(enemy_away_blocked_kicks) or counter != len(enemy_away_parry_shots) or counter
                           != len(enemy_away_players_bans) or counter != len(enemy_away_penalty_time) or counter
                           != len(enemy_away_me_players_bans) or counter != len(enemy_away_me_penalty_time) or counter
                           != len(enemy_away_goals_full) or counter != len(enemy_away_goals_minor) or counter
                           != len(enemy_away_strength_usage) or counter != len(enemy_away_won_throw_ins) or
                           counter != len(enemy_away_lost_throw_ins) or counter != len(enemy_away_goals_in_emtpy)):

                        if len(enemy_away_shots) != counter:
                            enemy_away_shots.append('-')
                        if len(enemy_away_enemy_shots) != counter:
                            enemy_away_enemy_shots.append('-')
                        if len(enemy_away_blocked_kicks) != counter:
                            enemy_away_blocked_kicks.append('-')
                        if len(enemy_away_parry_shots) != counter:
                            enemy_away_parry_shots.append('-')
                        if len(enemy_away_players_bans) != counter:
                            enemy_away_players_bans.append('-')
                        if len(enemy_away_penalty_time) != counter:
                            enemy_away_penalty_time.append('-')
                        if len(enemy_away_me_players_bans) != counter:
                            enemy_away_me_players_bans.append('-')
                        if len(enemy_away_me_penalty_time) != counter:
                            enemy_away_me_penalty_time.append('-')
                        if len(enemy_away_goals_full) != counter:
                            enemy_away_goals_full.append('-')
                        if len(enemy_away_goals_minor) != counter:
                            enemy_away_goals_minor.append('-')
                        if len(enemy_away_strength_usage) != counter:
                            enemy_away_strength_usage.append('-')
                        if len(enemy_away_won_throw_ins) != counter:
                            enemy_away_won_throw_ins.append('-')
                        if len(enemy_away_lost_throw_ins) != counter:
                            enemy_away_lost_throw_ins.append('-')
                        if len(enemy_away_goals_in_emtpy) != counter:
                            enemy_away_goals_in_emtpy.append('-')

                    # calculated arrays
                    if enemy_away_enemy_shots[counter - 1] != '-' and enemy_away_blocked_kicks[counter - 1] != '-':
                        enemy_away_total_shots_to_guest_team.append(int(enemy_away_enemy_shots[counter - 1]) +
                                                                int(enemy_away_blocked_kicks[counter - 1]))
                    else:
                        enemy_away_total_shots_to_guest_team.append('-')

                    if enemy_away_won_throw_ins[counter - 1] != '-' and enemy_away_lost_throw_ins[counter - 1] != '-':
                        enemy_away_total_throw_ins.append(int(enemy_away_won_throw_ins[counter - 1]) +
                                                       int(enemy_away_lost_throw_ins[counter - 1]))
                    else:
                        enemy_away_total_throw_ins.append('-')
                    if (enemy_away_total_shots_to_guest_team[counter - 1] != '-' and enemy_away_blocked_kicks[
                        counter - 1] != '-' and enemy_away_total_shots_to_guest_team[counter - 1] != '0' and
                            enemy_away_blocked_kicks[counter - 1] != '0'):
                        enemy_away_percent_blocked_kicks.append(int((100 / int(enemy_away_total_shots_to_guest_team[counter - 1]))) *
                            int(enemy_away_blocked_kicks[counter - 1]))
                    else:
                        enemy_away_percent_blocked_kicks.append('-')

                    if (enemy_away_enemy_shots[counter - 1] != '-' and enemy_away_parry_shots[counter - 1] != '-' and
                            enemy_away_enemy_shots[counter - 1] != '0' and enemy_away_parry_shots[counter - 1] != '0'):
                        enemy_away_percent_parry_shots.append(int((100 / int(enemy_away_enemy_shots[counter - 1]))) *
                                                           int(enemy_away_parry_shots[counter - 1]))
                    else:
                        enemy_away_percent_parry_shots.append('-')
                    if (enemy_away_me_players_bans[counter - 1] != '-' and enemy_away_goals_full[counter - 1] != '-' and
                            enemy_away_me_players_bans[counter - 1] != '0' and enemy_away_goals_full[counter - 1] != '0'):
                        enemy_away_percent_full_realization.append(int((100 / int(enemy_away_me_players_bans[counter - 1]))) *
                            int(enemy_away_goals_full[counter - 1]))
                    else:
                        enemy_away_percent_full_realization.append('-')
                    if (enemy_away_total_throw_ins[counter - 1] != '-' and enemy_away_won_throw_ins[counter - 1] != '-' and
                            enemy_away_total_throw_ins[counter - 1] != '0' and enemy_away_won_throw_ins[counter - 1] != '0'):
                        enemy_away_percent_won_throw_ins.append(int((100 / int(enemy_away_total_throw_ins[counter - 1]))) *
                                                                int(enemy_away_won_throw_ins[counter - 1]))
                    else:
                        enemy_away_percent_won_throw_ins.append('-')

                    print(counter, ' мачта противника в гостях выравлены')

                    driver.close()
                    driver.switch_to.window(window_before)

                # away_df updating
                elif teamName == padl.text.strip():
                    try:
                        tr.click()
                    except selenium.common.exceptions.StaleElementReferenceException:
                        continue
                    window_after = driver.window_handles[1]
                    driver.switch_to.window(window_after)
                    t.sleep(3)
                    try:
                        stats = driver.find_element_by_id('a-match-statistics')
                    except selenium.common.exceptions.NoSuchElementException:
                        print('\nНет статистики матча!\n')
                        driver.close()
                        driver.switch_to.window(window_before)
                        continue

                    home_team_name = driver.find_elements_by_class_name('participant-imglink')
                    # game name append
                    game_name = home_team_name[1].text + ' - ' + teamName
                    print(game_name)
                    enemy_home_game_name.append(game_name)
                    me_away_game_name.append(game_name)

                    try:
                        stats.click()
                        t.sleep(2)
                    except selenium.common.exceptions.ElementNotVisibleException:
                        t.sleep(2)
                        stats.click()
                        t.sleep(2)
                    except selenium.common.exceptions.StaleElementReferenceException:
                        print("...")
                        continue

                    # goals detection
                    score = driver.find_elements_by_class_name('scoreboard')
                    print(score[0].text, score[1].text)
                    enemy_home_good_goals.append(score[0].text)
                    enemy_home_missed_goals.append(score[1].text)

                    me_away_good_goals.append(score[1].text)
                    me_away_missed_goals.append(score[0].text)
                    table = driver.find_element_by_id('tab-statistics-0-statistic')
                    rows = table.find_elements_by_class_name('statRow')
                    for row in rows:
                        group = row.find_element_by_class_name('statTextGroup')
                        param_name = group.find_element_by_css_selector('.statText.statText--titleValue')
                        home_value = group.find_element_by_css_selector('.statText.statText--homeValue')
                        away_value = group.find_element_by_css_selector('.statText.statText--awayValue')

                        if param_name.text == "Броски в створ ворот":
                            if home_value.text.startswith('-') and home_value.text[1:].isdigit():
                                enemy_home_shots.append('0')
                                me_away_enemy_shots.append('0')
                            else:
                                enemy_home_shots.append(home_value.text)
                                me_away_enemy_shots.append(home_value.text)
                            if away_value.text.startswith('-') and away_value.text[1:].isdigit():
                                enemy_home_enemy_shots.append('0')
                                me_away_shots.append('0')
                            else:
                                enemy_home_enemy_shots.append(away_value.text)
                                me_away_shots.append(away_value.text)
                        if param_name.text == "Блок-но ударов":
                            if home_value.text.startswith('-') and home_value.text[1:].isdigit():
                                enemy_home_blocked_kicks.append('0')
                            else:
                                enemy_home_blocked_kicks.append(home_value.text)
                            if away_value.text.startswith('-') and away_value.text[1:].isdigit():
                                me_away_blocked_kicks.append('0')
                            else:
                                me_away_blocked_kicks.append(away_value.text)
                        if param_name.text == "Отраженные броски":
                            if home_value.text.startswith('-') and home_value.text[1:].isdigit():
                                enemy_home_parry_shots.append('0')
                            else:
                                enemy_home_parry_shots.append(home_value.text)
                            if away_value.text.startswith('-') and away_value.text[1:].isdigit():
                                me_away_parry_shots.append('0')
                            else:
                                me_away_parry_shots.append(away_value.text)
                        if param_name.text == "Удаления":
                            if home_value.text.startswith('-') and home_value.text[1:].isdigit():
                                enemy_home_players_bans.append('0')
                                me_away_enemy_players_bans.append('0')
                            else:
                                enemy_home_players_bans.append(home_value.text)
                                me_away_enemy_players_bans.append(home_value.text)
                            if away_value.text.startswith('-') and away_value.text[1:].isdigit():
                                me_away_players_bans.append('0')
                                enemy_home_me_players_bans.append('0')
                            else:
                                me_away_players_bans.append(away_value.text)
                                enemy_home_me_players_bans.append(away_value.text)
                        if param_name.text == "Штрафное время":
                            if home_value.text.startswith('-') and home_value.text[1:].isdigit():
                                enemy_home_penalty_time.append('0')
                                me_away_enemy_penalty_time.append('0')
                            else:
                                enemy_home_penalty_time.append(home_value.text)
                                me_away_enemy_penalty_time.append(home_value.text)
                            if away_value.text.startswith('-') and away_value.text[1:].isdigit():
                                me_away_penalty_time.append('0')
                                enemy_home_me_penalty_time.append('0')
                            else:
                                me_away_penalty_time.append(away_value.text)
                                enemy_home_me_penalty_time.append(away_value.text)
                        if param_name.text == "Шайбы в большинстве":
                            if home_value.text.startswith('-') and home_value.text[1:].isdigit():
                                enemy_home_goals_full.append('0')
                            else:
                                enemy_home_goals_full.append(home_value.text)
                            if away_value.text.startswith('-') and away_value.text[1:].isdigit():
                                me_away_goals_full.append('0')
                            else:
                                me_away_goals_full.append(away_value.text)
                        if param_name.text == "Шайбы в меньшинстве":
                            if home_value.text.startswith('-') and home_value.text[1:].isdigit():
                                enemy_home_goals_minor.append('0')
                            else:
                                enemy_home_goals_minor.append(home_value.text)
                            if away_value.text.startswith('-') and away_value.text[1:].isdigit():
                                me_away_goals_minor.append('0')
                            else:
                                me_away_goals_minor.append(away_value.text)
                        if param_name.text == "Силовые приемы":
                            if home_value.text.startswith('-') and home_value.text[1:].isdigit():
                                enemy_home_strength_usage.append('0')
                            else:
                                enemy_home_strength_usage.append(home_value.text)
                            if away_value.text.startswith('-') and away_value.text[1:].isdigit():
                                me_away_strength_usage.append('0')
                            else:
                                me_away_strength_usage.append(away_value.text)
                        if param_name.text == "Выигр. вбрасывания":
                            if home_value.text.startswith('-') and home_value.text[1:].isdigit():
                                enemy_home_won_throw_ins.append('0')
                                me_away_lost_throw_ins.append('0')
                            else:
                                enemy_home_won_throw_ins.append(home_value.text)
                                me_away_lost_throw_ins.append(home_value.text)
                            if away_value.text.startswith('-') and away_value.text[1:].isdigit():
                                me_away_won_throw_ins.append('0')
                                enemy_home_lost_throw_ins.append('0')
                            else:
                                me_away_won_throw_ins.append(away_value.text)
                                enemy_home_lost_throw_ins.append(away_value.text)
                        if param_name.text == "Голы в пустые ворота":
                            if home_value.text.startswith('-') and home_value.text[1:].isdigit():
                                enemy_home_goals_in_emtpy.append('0')
                            else:
                                enemy_home_goals_in_emtpy.append(home_value.text)
                            if away_value.text.startswith('-') and away_value.text[1:].isdigit():
                                me_away_goals_in_emtpy.append('0')
                            else:
                                me_away_goals_in_emtpy.append(away_value.text)

                    counter = len(me_away_game_name)

                    while (counter != len(me_away_shots) or counter != len(me_away_enemy_shots) or counter
                           != len(me_away_blocked_kicks) or counter != len(me_away_parry_shots) or counter
                           != len(me_away_players_bans) or counter != len(me_away_penalty_time) or counter
                           != len(me_away_enemy_players_bans) or counter != len(me_away_enemy_penalty_time) or counter
                           != len(me_away_goals_full) or counter != len(me_away_goals_minor) or counter
                           != len(me_away_strength_usage) or counter != len(me_away_won_throw_ins) or
                           counter != len(me_away_lost_throw_ins) or counter != len(me_away_goals_in_emtpy)):

                        if len(me_away_shots) != counter:
                            me_away_shots.append('-')
                        if len(me_away_enemy_shots) != counter:
                            me_away_enemy_shots.append('-')
                        if len(me_away_blocked_kicks) != counter:
                            me_away_blocked_kicks.append('-')
                        if len(me_away_parry_shots) != counter:
                            me_away_parry_shots.append('-')
                        if len(me_away_players_bans) != counter:
                            me_away_players_bans.append('-')
                        if len(me_away_penalty_time) != counter:
                            me_away_penalty_time.append('-')
                        if len(me_away_enemy_players_bans) != counter:
                            me_away_enemy_players_bans.append('-')
                        if len(me_away_enemy_penalty_time) != counter:
                            me_away_enemy_penalty_time.append('-')
                        if len(me_away_goals_full) != counter:
                            me_away_goals_full.append('-')
                        if len(me_away_goals_minor) != counter:
                            me_away_goals_minor.append('-')
                        if len(me_away_strength_usage) != counter:
                            me_away_strength_usage.append('-')
                        if len(me_away_won_throw_ins) != counter:
                            me_away_won_throw_ins.append('-')
                        if len(me_away_lost_throw_ins) != counter:
                            me_away_lost_throw_ins.append('-')
                        if len(me_away_goals_in_emtpy) != counter:
                            me_away_goals_in_emtpy.append('-')

                    # calculated arrays
                    if me_away_enemy_shots[counter - 1] != '-' and me_away_blocked_kicks[counter - 1] != '-':
                        me_away_total_shots_to_home_team.append(int(me_away_enemy_shots[counter - 1]) +
                                                                int(me_away_blocked_kicks[counter - 1]))
                    else:
                        me_away_total_shots_to_home_team.append('-')

                    if me_away_won_throw_ins[counter - 1] != '-' and me_away_lost_throw_ins[counter - 1] != '-':
                        me_away_total_throw_ins.append(int(me_away_won_throw_ins[counter - 1]) +
                                                       int(me_away_lost_throw_ins[counter - 1]))
                    else:
                        me_away_total_throw_ins.append('-')
                    if (me_away_total_shots_to_home_team[counter - 1] != '-' and me_away_blocked_kicks[counter - 1] != '-'
                            and me_away_total_shots_to_home_team[counter - 1] != '0' and
                            me_away_blocked_kicks[counter - 1] != '0'):
                        me_away_percent_blocked_kicks.append(int((100 / int(me_away_total_shots_to_home_team[counter - 1]))) *
                                                             int(me_away_blocked_kicks[counter - 1]))
                    else:
                        me_away_percent_blocked_kicks.append('-')

                    if (me_away_enemy_shots[counter - 1] != '-' and me_away_parry_shots[counter - 1] != '-' and
                            me_away_enemy_shots[counter - 1] != '0' and me_away_parry_shots[counter - 1] != '0'):
                        me_away_percent_parry_shots.append(int((100 / int(me_away_enemy_shots[counter - 1]))) *
                                                           int(me_away_parry_shots[counter - 1]))
                    else:
                        me_away_percent_parry_shots.append('-')
                    if (me_away_enemy_players_bans[counter - 1] != '-' and me_away_goals_full[counter - 1] != '-' and
                            me_away_enemy_players_bans[counter - 1] != '0' and me_away_goals_full[counter - 1] != '0'):
                        me_away_percent_full_realization.append(int((100 / int(me_away_enemy_players_bans[counter - 1]))) *
                                                                int(me_away_goals_full[counter - 1]))
                    else:
                        me_away_percent_full_realization.append('-')
                    if (me_away_total_throw_ins[counter - 1] != '-' and me_away_won_throw_ins[counter - 1] != '-'
                            and me_away_total_throw_ins[counter - 1] != '0' and me_away_won_throw_ins[counter - 1] != '0'):
                        me_away_percent_won_throw_ins.append(int((100 / int(me_away_total_throw_ins[counter - 1]))) *
                                                             int(me_away_won_throw_ins[counter - 1]))
                    else:
                        me_away_percent_won_throw_ins.append('-')

                    print(counter, ' матча в гостях выравлены')

                    counter = len(enemy_home_game_name)
                    while (counter != len(enemy_home_shots) or counter != len(enemy_home_enemy_shots) or counter
                           != len(enemy_home_blocked_kicks) or counter != len(enemy_home_parry_shots) or counter
                           != len(enemy_home_players_bans) or counter != len(enemy_home_penalty_time) or counter
                           != len(enemy_home_me_players_bans) or counter != len(enemy_home_me_penalty_time) or counter
                           != len(enemy_home_goals_full) or counter != len(enemy_home_goals_minor) or counter
                           != len(enemy_home_strength_usage) or counter != len(enemy_home_won_throw_ins) or
                           counter != len(enemy_home_lost_throw_ins) or counter != len(enemy_home_goals_in_emtpy)):

                        if len(enemy_home_shots) != counter:
                            enemy_home_shots.append('-')
                        if len(enemy_home_enemy_shots) != counter:
                            enemy_home_enemy_shots.append('-')
                        if len(enemy_home_blocked_kicks) != counter:
                            enemy_home_blocked_kicks.append('-')
                        if len(enemy_home_parry_shots) != counter:
                            enemy_home_parry_shots.append('-')
                        if len(enemy_home_players_bans) != counter:
                            enemy_home_players_bans.append('-')
                        if len(enemy_home_penalty_time) != counter:
                            enemy_home_penalty_time.append('-')
                        if len(enemy_home_me_players_bans) != counter:
                            enemy_home_me_players_bans.append('-')
                        if len(enemy_home_me_penalty_time) != counter:
                            enemy_home_me_penalty_time.append('-')
                        if len(enemy_home_goals_full) != counter:
                            enemy_home_goals_full.append('-')
                        if len(enemy_home_goals_minor) != counter:
                            enemy_home_goals_minor.append('-')
                        if len(enemy_home_strength_usage) != counter:
                            enemy_home_strength_usage.append('-')
                        if len(enemy_home_won_throw_ins) != counter:
                            enemy_home_won_throw_ins.append('-')
                        if len(enemy_home_lost_throw_ins) != counter:
                            enemy_home_lost_throw_ins.append('-')
                        if len(enemy_home_goals_in_emtpy) != counter:
                            enemy_home_goals_in_emtpy.append('-')

                    # calculated arrays
                    if enemy_home_enemy_shots[counter - 1] != '-' and enemy_home_blocked_kicks[counter - 1] != '-':
                        enemy_home_total_shots_to_guest_team.append(int(enemy_home_enemy_shots[counter - 1]) +
                                                                    int(enemy_home_blocked_kicks[counter - 1]))
                    else:
                        enemy_home_total_shots_to_guest_team.append('-')

                    if (enemy_home_won_throw_ins[counter - 1] != '-' and enemy_home_lost_throw_ins[counter - 1] != '-' and
                        enemy_home_won_throw_ins[counter - 1] != '0' and enemy_home_lost_throw_ins[counter - 1] != '0'):
                        enemy_home_total_throw_ins.append(int(enemy_home_won_throw_ins[counter - 1]) +
                                                          int(enemy_home_lost_throw_ins[counter - 1]))
                    else:
                        enemy_home_total_throw_ins.append('-')
                    if (enemy_home_total_shots_to_guest_team[counter - 1] != '-' and enemy_home_blocked_kicks[
                        counter - 1] != '-' and enemy_home_total_shots_to_guest_team[counter - 1] != '0' and
                        enemy_home_blocked_kicks[counter - 1] != '0'):
                        enemy_home_percent_blocked_kicks.append(int((100 / int(enemy_home_total_shots_to_guest_team[counter - 1]))) *
                            int(enemy_home_blocked_kicks[counter - 1]))
                    else:
                        enemy_home_percent_blocked_kicks.append('-')

                    if (enemy_home_enemy_shots[counter - 1] != '-' and enemy_home_parry_shots[counter - 1] != '-' and
                            enemy_home_enemy_shots[counter - 1] != '0' and enemy_home_parry_shots[counter - 1] != '0'):
                        enemy_home_percent_parry_shots.append(int((100 / int(enemy_home_enemy_shots[counter - 1]))) *
                                                              int(enemy_home_parry_shots[counter - 1]))
                    else:
                        enemy_home_percent_parry_shots.append('-')
                    if (enemy_home_me_players_bans[counter - 1] != '-' and enemy_home_goals_full[counter - 1] != '-' and
                            enemy_home_me_players_bans[counter - 1] != '0' and enemy_home_goals_full[counter - 1] != '0'):
                        enemy_home_percent_full_realization.append(int((100 / int(enemy_home_me_players_bans[counter - 1]))) *
                            int(enemy_home_goals_full[counter - 1]))
                    else:
                        enemy_home_percent_full_realization.append('-')
                    if (enemy_home_total_throw_ins[counter - 1] != '-' and enemy_home_won_throw_ins[counter - 1] != '-' and
                            enemy_home_total_throw_ins[counter - 1] != '0' and enemy_home_won_throw_ins[counter - 1] != '0'):
                        enemy_home_percent_won_throw_ins.append(int((100 / int(enemy_home_total_throw_ins[counter - 1]))) *
                                                                int(enemy_home_won_throw_ins[counter - 1]))
                    else:
                        enemy_home_percent_won_throw_ins.append('-')

                        print(counter, ' мачта противника дома выравлены')

                    driver.close()
                    driver.switch_to.window(window_before)

        listOfColumnsHock1 = ['match_name', 'shots', 'enemy_shots', 'goals', 'missed', 'total_shots_to_home_team',
                          'blocked_kicks', 'parry_shots', 'players_bans', 'penalty_time', 'enemy_players_bans',
                          'enemy_penalty_time', 'goals_full',  'goals_minority', 'strength_usage', 'won_throw_ins',
                          'lost_throw_ins', 'total_throw_ins', 'goals_to_empty',  'percent_of_blocked_kicks',
                          'percent_of_parry_shots', 'percent_full_realization', 'percent_of_won_throw_ins']

        me_home_d = {'match_name': me_home_game_name, 'shots': me_home_shots, 'enemy_shots': me_home_enemy_shots,
            'goals': me_home_good_goals, 'missed': me_home_missed_goals,
            'total_shots_to_home_team': me_home_total_shots_to_home_team , 'blocked_kicks': me_home_blocked_kicks,
            'parry_shots': me_home_parry_shots, 'players_bans': me_home_players_bans,
            'penalty_time': me_home_penalty_time, 'enemy_players_bans': me_home_enemy_players_bans,
            'enemy_penalty_time': me_home_enemy_penalty_time, 'goals_full': me_home_goals_full,
            'goals_minority' : me_home_goals_minor, 'strength_usage': me_home_strength_usage,
            'won_throw_ins': me_home_won_throw_ins, 'lost_throw_ins': me_home_lost_throw_ins,
            'total_throw_ins': me_home_total_throw_ins, 'goals_to_empty': me_home_goals_in_emtpy,
            'percent_of_blocked_kicks': me_home_percent_blocked_kicks,
            'percent_of_parry_shots': me_home_percent_parry_shots,
            'percent_full_realization': me_home_percent_full_realization,
            'percent_of_won_throw_ins': me_home_percent_won_throw_ins}
        me_home_df = pnd.DataFrame(data=me_home_d)
        # me_home_df.to_csv(teamName + "_team_home_games.csv", header=True, index=False, encoding='utf8')
        me_home_df.to_excel(writer, sheet_name=teamName + "_home_games", columns=listOfColumnsHock1)
        if self.forPngCount == 0:
                self.homeTeamDF = me_home_df
        elif self.forPngCount == 1:
                self.homeSecondTeamDF = me_home_df
        # print(self.homeTeamDF.head())
        # print(me_home_df.head())

        me_away_d = {'match_name': me_away_game_name, 'shots': me_away_shots, 'enemy_shots': me_away_enemy_shots,
                     'goals': me_away_good_goals, 'missed': me_away_missed_goals,
                     'total_shots_to_home_team': me_away_total_shots_to_home_team,
                     'blocked_kicks': me_away_blocked_kicks,
                     'parry_shots': me_away_parry_shots, 'players_bans': me_away_players_bans,
                     'penalty_time': me_away_penalty_time, 'enemy_players_bans': me_away_enemy_players_bans,
                     'enemy_penalty_time': me_away_enemy_penalty_time, 'goals_full': me_away_goals_full,
                     'goals_minority': me_away_goals_minor, 'strength_usage': me_away_strength_usage,
                     'won_throw_ins': me_away_won_throw_ins, 'lost_throw_ins': me_away_lost_throw_ins,
                     'total_throw_ins': me_away_total_throw_ins, 'goals_to_empty': me_away_goals_in_emtpy,
                     'percent_of_blocked_kicks': me_away_percent_blocked_kicks,
                     'percent_of_parry_shots': me_away_percent_parry_shots,
                     'percent_full_realization': me_away_percent_full_realization,
                     'percent_of_won_throw_ins': me_away_percent_won_throw_ins}
        me_away_df = pnd.DataFrame(data=me_away_d)
        # me_away_df.to_csv(teamName + "_team_away_games.csv", header=True, index=False, encoding='utf8')
        me_away_df.to_excel(writer, sheet_name=teamName + "_away_games",  columns=listOfColumnsHock1)
        if self.forPngCount == 0:
            self.awayTeamDF = me_away_df
        elif self.forPngCount == 1:
            self.awaySecondTeamDF = me_away_df
        # print(self.awayTeamDF.head())
        # print(me_away_df.head())

        opponent_away_d = {'match_name': enemy_away_game_name, 'shots': enemy_away_shots, 'enemy_shots': enemy_away_enemy_shots,
                     'goals': enemy_away_good_goals, 'missed': enemy_away_missed_goals,
                     'total_shots_to_guest_team': enemy_away_total_shots_to_guest_team,
                     'blocked_kicks': enemy_away_blocked_kicks,
                     'parry_shots': enemy_away_parry_shots, 'players_bans': enemy_away_players_bans,
                     'penalty_time': enemy_away_penalty_time, 'enemy_players_bans': enemy_away_me_players_bans,
                     'enemy_penalty_time': enemy_away_me_penalty_time, 'goals_full': enemy_away_goals_full,
                     'goals_minority': enemy_away_goals_minor, 'strength_usage': enemy_away_strength_usage,
                     'won_throw_ins': enemy_away_won_throw_ins, 'lost_throw_ins': enemy_away_lost_throw_ins,
                     'total_throw_ins': enemy_away_total_throw_ins, 'goals_to_empty': enemy_away_goals_in_emtpy,
                     'percent_of_blocked_kicks': enemy_away_percent_blocked_kicks,
                     'percent_of_parry_shots': enemy_away_percent_parry_shots,
                     'percent_full_realization': enemy_away_percent_full_realization,
                     'percent_of_won_throw_ins': enemy_away_percent_won_throw_ins}
        opponent_away_df = pnd.DataFrame(data=opponent_away_d)
        # opponent_away_df.to_csv(teamName + "_team_enemy_away_games.csv", header=True, index=False, encoding='utf8')
        opponent_away_df.to_excel(writer, sheet_name=teamName + "_opp_away")
        if self.forPngCount == 0: 
            self.awayTeamOppDF = opponent_away_df
        elif self.forPngCount == 1:
            self.awaySecondTeamOppDF = opponent_away_df
        # print(self.awayTeamOppDF.head())
        # print(opponent_away_df.head())

        opponent_home_d = {'match_name': enemy_home_game_name, 'shots': enemy_home_shots, 'enemy_shots': enemy_home_enemy_shots,
                     'goals': enemy_home_good_goals, 'missed': enemy_home_missed_goals,
                     'total_shots_to_guest_team': enemy_home_total_shots_to_guest_team,
                     'blocked_kicks': enemy_home_blocked_kicks,
                     'parry_shots': enemy_home_parry_shots, 'players_bans': enemy_home_players_bans,
                     'penalty_time': enemy_home_penalty_time, 'enemy_players_bans': enemy_home_me_players_bans,
                     'enemy_penalty_time': enemy_home_me_penalty_time, 'goals_full': enemy_home_goals_full,
                     'goals_minority': enemy_home_goals_minor, 'strength_usage': enemy_home_strength_usage,
                     'won_throw_ins': enemy_home_won_throw_ins, 'lost_throw_ins': enemy_home_lost_throw_ins,
                     'total_throw_ins': enemy_home_total_throw_ins, 'goals_to_empty': enemy_home_goals_in_emtpy,
                     'percent_of_blocked_kicks': enemy_home_percent_blocked_kicks,
                     'percent_of_parry_shots': enemy_home_percent_parry_shots,
                     'percent_full_realization': enemy_home_percent_full_realization,
                     'percent_of_won_throw_ins': enemy_home_percent_won_throw_ins}
        opponent_home_df = pnd.DataFrame(data=opponent_home_d)
        # opponent_home_df.to_csv(teamName + "_team_enemy_home_games.csv", header=True, index=False, encoding='utf8')
        opponent_home_df.to_excel(writer, sheet_name=teamName + "_opp_home")
        # print(opponent_home_df.head())
        if self.forPngCount == 0:
            self.homeTeamOppDF = opponent_home_df
        elif self.forPngCount == 1:
            self.homeSecondTeamOppDF = opponent_home_df
        # print(self.homeTeamOppDF.head())
        driver.close()
        # writer.save()


    def team_detailed_info(self, sport):
        print(self.team_urls)
        if len(self.team_urls) == 0:
            return "bad"
        team_list = list(iter(self.team_urls.items()))
        team_name1, url_c1 = team_list[0]
        team_name2, url_c2 = team_list[1]
        url1 = self.url + url_c1
        url2 = self.url + url_c2
        # print('Начинаем собирать информацию для ', team_name1)
        if sport == "Футбол":
            subprocess.call('rm /app/back/*xlsx',shell=True)
            writer = pnd.ExcelWriter('Football.xlsx', engine='xlsxwriter')
            try:
                #  t1 = threading.Thread(target=self.searchFootballInfo,args=(team_name1,url1,writer))
                #  t2 = threading.Thread(target=self.searchFootballInfo,args=(team_name2,url2,writer))
                #  t1.start()
                #  t2.start()
                #  t1.join()
                #  t2.join()
                self.searchFootballInfo(team_name1,url1,writer)
                self.forPngCount = 1
                self.searchFootballInfo(team_name2,url2,writer)
                self.forPngCount = 0
                self.allDFList = [
                    self.homeTeamDF,
                    self.awayTeamDF,
                    self.homeTeamOppDF,
                    self.awayTeamOppDF,

                    self.homeSecondTeamDF,
                    self.awaySecondTeamDF,
                    self.homeSecondTeamOppDF,
                    self.awaySecondTeamOppDF
                ]
                self.EFW(self.allDFList)
                return "ok"

            finally:
                writer.close()
                # subprocess.call("rm /app/vue/dist/static/*xlsx;cp /app/back/Football.xlsx /app/vue/dist/static/", shell=True)

        elif sport == "Хоккей":
            subprocess.call('rm /app/back/*xlsx',shell=True)
            writer = pnd.ExcelWriter('Hockey.xlsx', engine='xlsxwriter')
            try:
                # t1 = threading.Thread(target=self.searchHockeyInfo, args=(team_name1, url1, writer))
                # t2 = threading.Thread(target=self.searchHockeyInfo, args=(team_name2, url2, writer))
                # t1.start()
                # t2.start()
                # t1.join()
                # t2.join()
                self.searchHockeyInfo(team_name1, url1, writer)
                self.forPngCount = 1
                self.searchHockeyInfo(team_name2, url2, writer)
                self.forPngCount = 0
                self.allDFList = [
                    self.homeTeamDF,
                    self.awayTeamDF,
                    self.homeTeamOppDF,
                    self.awayTeamOppDF,

                    self.homeSecondTeamDF,
                    self.awaySecondTeamDF,
                    self.homeSecondTeamOppDF,
                    self.awaySecondTeamOppDF
                ]
                self.EFW(self.allDFList)
                return "ok"
            finally:
                writer.close() 
                # subprocess.call("rm /app/vue/dist/static/*xlsx;cp /app/back/Hockey.xlsx /app/vue/dist/static/", shell=True)
        
    def EFW(self, dfList):
        subprocess.call("cd /app/back/pngs;rm *;", shell=True)
        subprocess.call("cd /app/back;rm *zip", shell=True)

        team_list = list(iter(self.team_urls.items()))
        team_name1, url_c1 = team_list[0]
        team_name2, url_c2 = team_list[1]

        for i in range(len(dfList)):
            # try:
                    df = dfList[i]
                    df = df.drop('match_name', axis=1)
                    col_list = df.columns.tolist()
                    # firstTeamHomeDF
                    if i == 0:
                        for name in col_list:
                            graph_name = team_name1 + "_home_" + name
                            current_df = df[[name]]
                            current_df = current_df.astype(str)
                            current_df[name][current_df[name] == '-'] = np.nan
                            # print(current_df, type(current_df))
                            if name == "ball_control":
                                current_df[name] = current_df[name].str.rstrip('%')
                                current_df = current_df.dropna().astype(int)
                            else:
                                current_df = current_df.dropna().astype(int)
                            # print(current_df, type(current_df))
                            infoFromDf = current_df[name].tolist()
                            if len(infoFromDf) != 0:
                                self.create_EFW_graph(infoFromDf, graph_name, name)
                    # firstTeamAwayDF
                    if i == 1:
                        for name in col_list:
                            graph_name = team_name1 + "_away_" + name
                            current_df = df[[name]]
                            current_df = current_df.astype(str)
                            current_df[name][current_df[name] == '-'] = np.nan
                            # print(current_df, type(current_df))
                            if name == "ball_control":
                                current_df[name] = current_df[name].str.rstrip('%')
                                current_df = current_df.dropna().astype(int)
                            else:
                                current_df = current_df.dropna().astype(int)
                            # print(current_df, type(current_df))
                            infoFromDf = current_df[name].tolist()
                            if len(infoFromDf) != 0:
                                self.create_EFW_graph(infoFromDf, graph_name, name)

                    # firstTeamOpponentsHomeDF
                    if i == 2:
                        for name in col_list:
                            graph_name = team_name1 + "_opponents_home_" + name
                            current_df = df[[name]]
                            current_df = current_df.astype(str)
                            current_df[name][current_df[name] == '-'] = np.nan
                            # print(current_df, type(current_df))
                            if name == "ball_control":
                                current_df[name] = current_df[name].str.rstrip('%')
                                current_df = current_df.dropna().astype(int)
                            else:
                                current_df = current_df.dropna().astype(int)
                            # print(current_df, type(current_df))
                            infoFromDf = current_df[name].tolist()
                            if len(infoFromDf) != 0:
                                self.create_EFW_graph(infoFromDf, graph_name, name)

                    # firstTeamOpponentsAwayDF
                    if i == 3:
                        for name in col_list:
                            graph_name = team_name1 + "_opponents_away_" + name
                            current_df = df[[name]]
                            current_df = current_df.astype(str)
                            current_df[name][current_df[name] == '-'] = np.nan
                            # print(current_df, type(current_df))
                            if name == "ball_control":
                                current_df[name] = current_df[name].str.rstrip('%')
                                current_df = current_df.dropna().astype(int)
                            else:
                                current_df = current_df.dropna().astype(int)
                            # print(current_df, type(current_df))
                            infoFromDf = current_df[name].tolist()
                            if len(infoFromDf) != 0:
                                self.create_EFW_graph(infoFromDf, graph_name, name)

                    # secondTeamHomeDF
                    if i == 4:
                        for name in col_list:
                            graph_name = team_name2 + "_home_" + name
                            current_df = df[[name]]
                            current_df = current_df.astype(str)
                            current_df[name][current_df[name] == '-'] = np.nan
                            # print(current_df, type(current_df))
                            if name == "ball_control":
                                current_df[name] = current_df[name].str.rstrip('%')
                                current_df = current_df.dropna().astype(int)
                            else:
                                current_df = current_df.dropna().astype(int)
                            # print(current_df, type(current_df))
                            infoFromDf = current_df[name].tolist()
                            if len(infoFromDf) != 0:
                                self.create_EFW_graph(infoFromDf, graph_name, name)
                    # secondTeamAwayDF
                    if i == 5:
                        for name in col_list:
                            graph_name = team_name2 + "_away_" + name
                            current_df = df[[name]]
                            current_df = current_df.astype(str)
                            current_df[name][current_df[name] == '-'] = np.nan
                            # print(current_df, type(current_df))
                            if name == "ball_control":
                                current_df[name] = current_df[name].str.rstrip('%')
                                current_df = current_df.dropna().astype(int)
                            else:
                                current_df = current_df.dropna().astype(int)
                            # print(current_df, type(current_df))
                            infoFromDf = current_df[name].tolist()
                            if len(infoFromDf) != 0:
                                self.create_EFW_graph(infoFromDf, graph_name, name)

                    # secondTeamOpponentsHomeDF
                    if i == 6:
                        for name in col_list:
                            graph_name = team_name2 + "_opponents_home_" + name
                            current_df = df[[name]]
                            current_df = current_df.astype(str)
                            current_df[name][current_df[name] == '-'] = np.nan
                            # print(current_df, type(current_df))
                            if name == "ball_control":
                                current_df[name] = current_df[name].str.rstrip('%')
                                current_df = current_df.dropna().astype(int)
                            else:
                                current_df = current_df.dropna().astype(int)
                            # print(current_df, type(current_df))
                            infoFromDf = current_df[name].tolist()
                            if len(infoFromDf) != 0:
                                self.create_EFW_graph(infoFromDf, graph_name, name)

                    # secondTeamOpponentsAwayDF
                    if i == 7:
                        for name in col_list:
                            graph_name = team_name2 + "_opponents_away_" + name
                            current_df = df[[name]]
                            current_df = current_df.astype(str)
                            current_df[name][current_df[name] == '-'] = np.nan
                            # print(current_df, type(current_df))
                            if name == "ball_control":
                                current_df[name] = current_df[name].str.rstrip('%')
                                current_df = current_df.dropna().astype(int)
                            else:
                                current_df = current_df.dropna().astype(int)
                            # print(current_df, type(current_df))
                            infoFromDf = current_df[name].tolist()
                            if len(infoFromDf) != 0:
                                self.create_EFW_graph(infoFromDf, graph_name, name)
            # except ValueError:
            #     continue

        subprocess.call('ls -l',shell=True)
        subprocess.call("cd " + self.my_path + ";zip -r results pngs", shell=True)

        # subprocess.call("mv *zip ../vue/dist/static",shell=True)


    def create_EFW_graph(self, data, name, legend):
        fig, ax = plt.subplots()
        ax.plot(data, color='black', label=legend)

        price_min = min(data)
        price_max = max(data)
        # # Fibonacci Levels considering original trend as upward move
        diff = price_max - price_min
        level1 = price_max - 0.236 * diff
        level2 = price_max - 0.382 * diff
        level3 = price_max - 0.618 * diff
        ax.axhspan(level1, price_min, alpha=0.4, color='lightsalmon')
        ax.axhspan(level2, level1, alpha=0.5, color='palegoldenrod')
        ax.axhspan(level3, level2, alpha=0.5, color='palegreen')
        ax.axhspan(price_max, level3, alpha=0.5, color='powderblue')

        ax.set_ylabel('Value')
        ax.set_xlabel('Games Number')
        ax.set_xticklabels([])
        ax.legend(loc=2)

        plt.title(name)
        plt.savefig(self.my_path + '/pngs/' + name + '.png')
        print("image saved!")


if __name__ == "__main__":
    full = Parser()
    test = input("Спорт:")
    first = input("Первая команда:")
    second = input("Вторая команда:")
    full.SportToday(test, first, second)
    full.team_detailed_info(test)
    
