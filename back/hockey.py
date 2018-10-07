from bs4 import BeautifulSoup
import requests
from requests_html import HTMLSession
import sys
from selenium import webdriver
import selenium
import numpy as np
import pandas as pnd
import time as t

team_urls={}

def get_two_teams_url(team1, team2, sport, driver):
            window_before = driver.window_handles[0]
            sport_bloсks = driver.find_elements_by_class_name("hockey")
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
                            t.sleep(2)
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
                            team_urls.update({team_name: team_url})
                        driver.close()
                        driver.switch_to.window(window_before)
                        return
                    else:
                        print("нет такой пары команд")


def light_matches_info(sport, driver):
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
            bloсks = driver.find_elements_by_class_name("hockey")
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
                df.to_csv("light_football_games_info.csv", sep=';', header=True, index=False, encoding='utf-8')
                return d

def Hockey(first,second):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome('/home/prazd/selenium/chromedriver')
        driver.get("https://www.myscore.ru/hockey")
        t.sleep(2)
        start = t.time()
        d = light_matches_info("Хоккей", driver) # Хоккей
        end = t.time()
        print("время выполнения парсинга - ", end - start, " секунд.")
        if d == "Bad":
            print("BAD")
            return
        if len(first) == 0:
            get_two_teams_url(d['home_team'][10], d['away_team'][10], "Хоккей", driver) # Хоккей
            print(team_urls)
            print(len(team_urls))
            driver.close()
            return d
        else:
            get_two_teams_url(first, second, "Хоккей", driver) # Хоккей
            # t.sleep(10)
            print(team_urls)
            print(len(team_urls))
            driver.close()
            return d


if __name__ == "__main__":
    Hockey("Ирселон","Аугсбюргер")