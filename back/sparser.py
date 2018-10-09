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
                return t
            else:
                t = self.FootBall(first, sec)
                return t
        else:
            t = self.Sport(first,sec,sport)
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
            for block in soccer_bloсks[1:]:
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
            df.to_csv("full_football_games_info.csv", header=True, index=False, encoding='utf-8')
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
            # saving to csv
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
            # Test ###############

            find = self.urls[sport][1:]
            # if sport == "Баскетбол":
            #     find = "basketball"
            # elif sport == "Хоккей":
            #     find = "hockey"
            # elif sport == "Бейсбол":
            #     find = "baseball"

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
                    if padr.text == team1 and padl.text == team2 or padr.text == team2 and padl.text == team1:
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
                            print(team_name, '- название команды')
                            print(team_url, '- ссылка на страницу')
                            self.team_urls.update({team_name: team_url})
                        driver.close()
                        driver.switch_to.window(window_before)
                        return
                    else:
                        print("нет такой пары команд")
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

    def Sport(self,first,second,sport):

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        # driver = webdriver.Chrome('/home/prazd/selenium/chromedriver')
        driver = webdriver.Chrome('/Users/Koroba/Downloads/chromedriver')

        change = self.url + self.urls[sport]
        driver.get(change)
        t.sleep(2)
        start = t.time()
        d = self.light_matches_info(sport, driver)
        end = t.time()
        print("время выполнения парсинга - ", end - start, " секунд.")
        if d == "Bad":
            print("BAD")
            return
        if len(first) == 0:
            self.get_two_teams_url(d['home_team'][10], d['away_team'][10],sport, driver) 
            print(self.team_urls)
            print(len(self.team_urls))
            driver.close()
            return d
        else:
            self.get_two_teams_url(first, second, sport, driver) 
            # t.sleep(10)
            print(self.team_urls)
            print(len(self.team_urls))
            driver.close()
            return d
    
    def searchFootballInfo(self,teamName,url):
            chrome_options = webdriver.ChromeOptions()

            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')

        # driver = webdriver.Chrome(self.docker,chrome_options=chrome_options) # for docker

            driver = webdriver.Chrome('/home/prazd/selenium/chromedriver')
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

            block = driver.find_element_by_id('fs-summary-results')
            tbody = block.find_element_by_tag_name('tbody')
            trs = tbody.find_elements_by_tag_name('tr')
            for tr in trs:
                # TODO! kick usual games from here. (Товарищеские матчи)

                padr = tr.find_element_by_class_name('padr')
                padl = tr.find_element_by_class_name('padl')
                # home_df updating
                if teamName == padr.text.strip():
                    tr.click()
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

                    stats.click()
                    t.sleep(2)

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
                            me_home_ball_control.append(home_value.text)
                            enemy_away_ball_control.append(away_value.text)
                        if param_name.text == "Удары":
                            me_home_own_ball_hits.append(home_value.text)
                            me_home_enemy_ball_hits.append(away_value.text)

                            enemy_away_own_ball_hits.append(away_value.text)
                            enemy_away_me_ball_hits.append(home_value.text)
                        if param_name.text == "Удары в створ":
                            me_home_own_target_ball_hits.append(home_value.text)
                            enemy_away_own_target_ball_hits.append(away_value.text)
                        if param_name.text == "Удары мимо":
                            me_home_own_missed_ball_hits.append(home_value.text)
                            enemy_away_own_missed_ball_hits.append(away_value.text)
                        if param_name.text == "Блок-но ударов":
                            me_home_enemy_blocked_hits.append(away_value.text)
                            enemy_away_me_blocked_hits.append(home_value.text)
                        if param_name.text == "Штрафные":
                            me_home_standarts.append(home_value.text)
                            enemy_away_standarts.append(away_value.text)
                        if param_name.text == "Угловые":
                            me_home_corner_kicks.append(home_value.text)
                            enemy_away_corner_kicks.append(away_value.text)
                        if param_name.text == "Офсайды":
                            me_home_offsides.append(home_value.text)
                            enemy_away_offsides.append(away_value.text)
                        if param_name.text == "Сэйвы":
                            me_home_saves.append(home_value.text)
                            enemy_away_saves.append(away_value.text)
                        if param_name.text == "Фолы":
                            me_home_fauls.append(home_value.text)
                            enemy_away_fauls.append(away_value.text)
                        if param_name.text == "Желтые карточки":
                            me_home_yc.append(home_value.text)
                            enemy_away_yc.append(away_value.text)
                        if param_name.text == "Красные карточки":
                            me_home_rc.append(home_value.text)
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
                    me_home_percent_goals_kicks.append((100 / int(me_home_own_ball_hits[counter - 1])) *
                                                        int(me_home_good_goals[counter - 1]))
                    if me_home_own_target_ball_hits[counter - 1] != "-":
                        me_home_percent_target_goals_kicks.append((100 / int(me_home_own_target_ball_hits[counter - 1]))
                                                                   * int(me_home_good_goals[counter - 1]))
                    else:
                        me_home_percent_target_goals_kicks.append('-')

                    if me_home_enemy_ball_hits[counter - 1 ] != '-' and  me_home_enemy_blocked_hits[counter - 1] != '-':
                        me_home_percent_enemy_blocked_kicks.append((100 / int(me_home_enemy_ball_hits[counter - 1])) *
                                                        int(me_home_enemy_blocked_hits[counter - 1]))
                    else:
                        me_home_percent_enemy_blocked_kicks.append('-')

                    if (me_home_fauls[counter - 1] != '-' and me_home_yc[counter - 1] != '-' and
                        me_home_rc[counter - 1] != '-'):
                        me_home_sum_of_badthings.append((100 / int(me_home_fauls[counter - 1])) *
                            int(me_home_yc[counter - 1]) + (100 / int(me_home_fauls[counter - 1])) *
                                                        int(me_home_rc[counter - 1]))
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

                    enemy_away_percent_goals_kicks.append((100 / int(enemy_away_own_ball_hits[counter - 1])) *
                                                       int(enemy_away_good_goals[counter - 1]))
                    if enemy_away_own_target_ball_hits[counter - 1] != "-":
                        enemy_away_percent_target_goals_kicks.append((100 / int(enemy_away_own_target_ball_hits[counter - 1]))
                                                                  * int(enemy_away_good_goals[counter - 1]))
                    else:
                        enemy_away_percent_target_goals_kicks.append('-')

                    if enemy_away_me_ball_hits[counter - 1] != '-' and enemy_away_me_blocked_hits[counter - 1] != '-':
                        enemy_away_percent_me_blocked_kicks.append((100 / int(enemy_away_me_ball_hits[counter - 1])) *
                                                                   int(enemy_away_me_blocked_hits[counter - 1]))
                    else:
                        enemy_away_percent_me_blocked_kicks.append('-')

                    if (enemy_away_fauls[counter - 1] != '-' and enemy_away_yc[counter - 1] != '-' and
                            enemy_away_rc[counter - 1] != '-'):
                        enemy_away_sum_of_badthings.append((100 / int(enemy_away_fauls[counter - 1])) *
                                                        int(enemy_away_yc[counter - 1]) + (
                                                                    100 / int(enemy_away_fauls[counter - 1])) *
                                                        int(enemy_away_rc[counter - 1]))
                    else:
                        enemy_away_sum_of_badthings.append('-')
                    print(counter, ' мачта противника в гостях выравлены')

                    driver.close()
                    driver.switch_to.window(window_before)

                # away_df updating
                elif teamName == padl.text.strip():
                    tr.click()
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
                            enemy_home_ball_control.append(home_value.text)
                            me_away_ball_control.append(away_value.text)
                        if param_name.text == "Удары":
                            enemy_home_own_ball_hits.append(home_value.text)
                            enemy_home_me_ball_hits.append(away_value.text)

                            me_away_own_ball_hits.append(away_value.text)
                            me_away_enemy_ball_hits.append(home_value.text)
                        if param_name.text == "Удары в створ":
                            enemy_home_own_target_ball_hits.append(home_value.text)
                            me_away_own_target_ball_hits.append(away_value.text)
                        if param_name.text == "Удары мимо":
                            enemy_home_own_missed_ball_hits.append(home_value.text)
                            me_away_own_missed_ball_hits.append(away_value.text)
                        if param_name.text == "Блок-но ударов":
                            enemy_home_me_blocked_hits.append(away_value.text)
                            me_away_enemy_blocked_hits.append(home_value.text)
                        if param_name.text == "Штрафные":
                            enemy_home_standarts.append(home_value.text)
                            me_away_standarts.append(away_value.text)
                        if param_name.text == "Угловые":
                            enemy_home_corner_kicks.append(home_value.text)
                            me_away_corner_kicks.append(away_value.text)
                        if param_name.text == "Офсайды":
                            enemy_home_offsides.append(home_value.text)
                            me_away_offsides.append(away_value.text)
                        if param_name.text == "Сэйвы":
                            enemy_home_saves.append(home_value.text)
                            me_away_saves.append(away_value.text)
                        if param_name.text == "Фолы":
                            enemy_home_fauls.append(home_value.text)
                            me_away_fauls.append(away_value.text)
                        if param_name.text == "Желтые карточки":
                            enemy_home_yc.append(home_value.text)
                            me_away_yc.append(away_value.text)
                        if param_name.text == "Красные карточки":
                            enemy_home_rc.append(home_value.text)
                            me_away_rc.append(away_value.text)

                    counter = len(me_away_game_name)

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
                    me_away_percent_goals_kicks.append((100 / int(me_away_own_ball_hits[counter - 1])) *
                                                        int(me_away_good_goals[counter - 1]))
                    if me_away_own_target_ball_hits[counter - 1] != "-":
                        me_away_percent_target_goals_kicks.append((100 / int(me_away_own_target_ball_hits[counter - 1]))
                                                                   * int(me_away_good_goals[counter - 1]))
                    else:
                        me_away_percent_target_goals_kicks.append('-')

                    if me_away_enemy_ball_hits[counter - 1 ] != '-' and  me_away_enemy_blocked_hits[counter - 1] != '-':
                        me_away_percent_enemy_blocked_kicks.append((100 / int(me_away_enemy_ball_hits[counter - 1])) *
                                                        int(me_away_enemy_blocked_hits[counter - 1]))
                    else:
                        me_away_percent_enemy_blocked_kicks.append('-')

                    if (me_away_fauls[counter - 1] != '-' and me_away_yc[counter - 1] != '-' and
                        me_away_rc[counter - 1] != '-'):
                        me_away_sum_of_badthings.append((100 / int(me_away_fauls[counter - 1])) *
                            int(me_away_yc[counter - 1]) + (100 / int(me_away_fauls[counter - 1])) *
                                                        int(me_away_rc[counter - 1]))
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

                    enemy_home_percent_goals_kicks.append((100 / int(enemy_home_own_ball_hits[counter - 1])) *
                                                          int(enemy_home_good_goals[counter - 1]))
                    if enemy_home_own_target_ball_hits[counter - 1] != "-":
                        enemy_home_percent_target_goals_kicks.append(
                            (100 / int(enemy_home_own_target_ball_hits[counter - 1]))
                            * int(enemy_home_good_goals[counter - 1]))
                    else:
                        enemy_home_percent_target_goals_kicks.append('-')

                    if enemy_home_me_ball_hits[counter - 1] != '-' and enemy_home_me_blocked_hits[counter - 1] != '-':
                        enemy_home_percent_me_blocked_kicks.append((100 / int(enemy_home_me_ball_hits[counter - 1])) *
                                                                   int(enemy_home_me_blocked_hits[counter - 1]))
                    else:
                        enemy_home_percent_me_blocked_kicks.append('-')

                    if (enemy_home_fauls[counter - 1] != '-' and enemy_home_yc[counter - 1] != '-' and
                            enemy_home_rc[counter - 1] != '-'):
                        enemy_home_sum_of_badthings.append((100 / int(enemy_home_fauls[counter - 1])) *
                                                           int(enemy_home_yc[counter - 1]) + (
                                                                   100 / int(enemy_home_fauls[counter - 1])) *
                                                           int(enemy_home_rc[counter - 1]))
                    else:
                        enemy_home_sum_of_badthings.append('-')
                    print(counter, ' мачта противника дома выравлены')

                    driver.close()
                    driver.switch_to.window(window_before)

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
            me_home_df.to_csv(teamName+"_team_home_games.csv", header=True, index=False, encoding='utf8')
            print(me_home_df.head())

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
            me_away_df.to_csv(teamName+"_team_away_games.csv", header=True, index=False, encoding='utf8')
            print(me_away_df.head())

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
            opponent_away_df.to_csv(teamName+"team_opponents_away.csv", header=True, index=False, encoding='utf8')
            print(opponent_away_df.head())

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
            opponent_home_df.to_csv(teamName+"team_opponents_home.csv", header=True, index=False, encoding='utf8')
            print(opponent_home_df.head())


    def team_detailed_info(self, sport):
        team_list = list(iter(self.team_urls.items()))
        team_name1, url_c1 = team_list[0]
        team_name2, url_c2 = team_list[1]
        url1 = self.url + url_c1
        url2 = self.url + url_c2
        # print('Начинаем собирать информацию для ', team_name1)
        if sport == "Футбол":
            self.searchFootballInfo(team_name1,url1)
            self.searchFootballInfo(team_name2,url2)

            # move to team №2
            # TODO The same big process with the second team
            # print('Начинаем собирать информацию для ', team_name2)
            # url = self.url + url_c2
            # driver.get(url)
            # t.sleep(2)

            # block = driver.find_element_by_id('fs-summary-results')
            # tbody = block.find_element_by_tag_name('tbody')
            # trs = tbody.find_elements_by_tag_name('tr')
            # for tr in trs:
            #     print(tr.get_attribute('innerHTML'))
            # driver.close()

        # elif sport == "Хоккей":
        #     print('парсинг хоккейной истории игр')



if __name__ == "__main__":
    full = Parser()
    test = input("Спорт:")
    first = input("Первая команда:")
    second = input("Вторая команда:")

    full.SportToday(test, first, second)
    full.team_detailed_info(test)
