from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException
from selectorlib import Extractor
import json
import time
import urllib.request
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import csv
import numpy as np
from datetime import date
import bs4
import requests
import pandas as pd

ChromeOptions = webdriver.ChromeOptions()
ChromeOptions.add_argument('ignore-certificate-errors')
driver = webdriver.Chrome(ChromeDriverManager().install(), options=ChromeOptions)

##All scrapers were built/tested in fbref_scraper notebook

##example url:
# url = "https://fbref.com/en/comps/20/3248/stats/2019-2020-Bundesliga-Stats"

def standard_stats_scraper(url):
    '''This function takes as an argument the url from fbref (see example above)
    returns a df with all the stats from the standard stats page of fbref for a league and season'''
    
    driver.get(url)
    html = driver.execute_script('return document.body.innerHTML;')
    soup = bs4.BeautifulSoup(html,'lxml')

    data_tables = soup.find_all(class_='table_outer_container')
    
    players = data_tables[1].find_all(attrs={'data-stat':"player"})
    nationality = data_tables[1].find_all(attrs={'data-stat':'nationality'})
    team = data_tables[1].find_all(attrs={'data-stat':'squad'})
    position = data_tables[1].find_all(attrs={'data-stat':'position'})
    age = data_tables[1].find_all(attrs={'data-stat':'age'})
    birth_year = data_tables[1].find_all(attrs={'data-stat':'birth_year'})

    games = data_tables[1].find_all(attrs={'data-stat':'games'})
    games_start = data_tables[1].find_all(attrs={'data-stat':'games_starts'})
    mins = data_tables[1].find_all(attrs={'data-stat':'minutes'})
    goals = data_tables[1].find_all(attrs={'data-stat':'goals'})
    assists = data_tables[1].find_all(attrs={'data-stat':'assists'})
    pens_successful = data_tables[1].find_all(attrs={'data-stat':'pens_made'})
    pens_attempts = data_tables[1].find_all(attrs={'data-stat':'pens_att'})
    yellow_cards = data_tables[1].find_all(attrs={'data-stat':'cards_yellow'})
    red_cards = data_tables[1].find_all(attrs={'data-stat':'cards_red'})

    goals_per_90 = data_tables[1].find_all(attrs={'data-stat':'goals_per90'})
    assists_per_90 = data_tables[1].find_all(attrs={'data-stat':'assists_per90'})
    goals_and_assists_per_90 = data_tables[1].find_all(attrs={'data-stat':'goals_assists_per90'})
    goals_pk_per_90 = data_tables[1].find_all(attrs={'data-stat':'goals_pens_per90'})
    goals_assists_pk_per_90 = data_tables[1].find_all(attrs={'data-stat':'goals_assists_pens_per90'})

    xg = data_tables[1].find_all(attrs={'data-stat':'xg'})
    npxp = data_tables[1].find_all(attrs={'data-stat':'npxg'})
    xa = data_tables[1].find_all(attrs={'data-stat':'xa'})
    xg_per90 = data_tables[1].find_all(attrs={'data-stat':'xg_per90'})
    xa_per90 = data_tables[1].find_all(attrs={'data-stat':'xa_per90'})
    xg_xa_per90 = data_tables[1].find_all(attrs={'data-stat':'xg_xa_per90'})
    npxg_per90 = data_tables[1].find_all(attrs={'data-stat':'npxg_per90'})
    npxg_xa_per90 = data_tables[1].find_all(attrs={'data-stat':'npxg_xa_per90'})
    
    players_list = []
    nationality_list = [] 
    team_list = []
    position_list = []
    age_list = [] 
    birth_year_list = [] 
    games_list = [] 
    games_start_list = []
    mins_list = []
    goals_list = [] 
    assists_list = [] 
    pens_successful_list = []
    pens_attempts_list = []
    yellow_cards_list = [] 
    red_cards_list = []
    goals_per_90_list = []
    assists_per_90_list = [] 
    goals_and_assists_per_90_list = []
    goals_pk_per_90_list = []
    goals_assists_pk_per_90_list = []
    xg_list = [] 
    npxp_list = [] 
    xa_list = []
    xg_per90_list = [] 
    xa_per90_list = []
    xg_xa_per90_list = [] 
    npxg_per90_list = []
    npxg_xa_per90_list = [] 

    for n in range(len(players)):
        players_list.append(players[n].text)
        nationality_list.append(nationality[n].text)
        team_list.append(team[n].text)
        position_list.append(position[n].text)
        age_list.append(age[n].text)
        birth_year_list.append(birth_year[n].text)
        games_list.append(games[n].text)
        games_start_list.append(games_start[n].text)
        mins_list.append(mins[n].text)
        goals_list.append(goals[n].text)
        assists_list.append(assists[n].text)
        pens_successful_list.append(pens_successful[n].text)
        pens_attempts_list.append(pens_attempts[n].text)
        yellow_cards_list.append(yellow_cards[n].text)
        red_cards_list.append(red_cards[n].text)
        goals_per_90_list.append(goals_per_90[n].text)
        assists_per_90_list.append(assists_per_90[n].text)
        goals_and_assists_per_90_list.append(goals_and_assists_per_90[n].text)
        goals_pk_per_90_list.append(goals_pk_per_90[n].text)
        goals_assists_pk_per_90_list.append(goals_assists_pk_per_90[n].text)
        xg_list.append(xg[n].text)
        npxp_list.append(npxp[n].text)
        xa_list.append(xa[n].text)
        xg_per90_list.append(xg_per90[n].text)
        xa_per90_list.append(xa_per90[n].text)
        xg_xa_per90_list.append(xg_xa_per90[n].text)
        npxg_per90_list.append(npxg_per90[n].text)
        npxg_xa_per90_list.append(npxg_xa_per90[n].text)

    giant_list = [players_list,nationality_list,team_list,position_list,age_list,
    birth_year_list,games_list,games_start_list,mins_list,goals_list,assists_list,
    pens_successful_list,pens_attempts_list,yellow_cards_list,red_cards_list,
    goals_per_90_list,assists_per_90_list,goals_and_assists_per_90_list,goals_pk_per_90_list,
    goals_assists_pk_per_90_list,xg_list,npxp_list,xa_list,xg_per90_list,xa_per90_list,
    xg_xa_per90_list,npxg_per90_list,npxg_xa_per90_list]

    df_standard = pd.DataFrame(giant_list).transpose()

    df_standard.columns = ['players','nationality','team','position','age',
    'birth_year','games','games_start','mins','goals','assists',
    'pens_successful','pens_attempts','yellow_cards','red_cards',
    'goals_per_90','assists_per_90','goals_and_assists_per_90','goals_pk_per_90',
    'goals_assists_pk_per_90','xg','npxp','xa','xg_per90','xa_per90',
    'xg_xa_per90_list','npxg_per90_list','npxg_xa_per90']
    
    df_standard2 = df_standard.loc[df_standard['players'] != 'Player',:]

    df_standard2.set_index(keys=['players','nationality','team','position','age','birth_year'], inplace=True)
    
    return df_standard2

######################################################################################################
def shooting_stats_scraper(url):
    '''This function takes as an argument the url from fbref (see example above)
    returns a df with all the stats from the shooting stats page of fbref for a league and season'''
    
    driver.get(url)
    html = driver.execute_script('return document.body.innerHTML;')
    soup = bs4.BeautifulSoup(html,'lxml')

    data_tables = soup.find_all(class_='table_outer_container')
    
    players = data_tables[1].find_all(attrs={'data-stat':"player"})
    nationality = data_tables[1].find_all(attrs={'data-stat':'nationality'})
    team = data_tables[1].find_all(attrs={'data-stat':'squad'})
    league = data_tables[1].find_all(attrs={'data-stat':'comp_level'})
    position = data_tables[1].find_all(attrs={'data-stat':'position'})
    age = data_tables[1].find_all(attrs={'data-stat':'age'})
    birth_year = data_tables[1].find_all(attrs={'data-stat':'birth_year'})

    full_90s_played = data_tables[1].find_all(attrs={'data-stat':"minutes_90s"})
    goals = data_tables[1].find_all(attrs={'data-stat':"goals"})
    shots_total = data_tables[1].find_all(attrs={'data-stat':'shots_total'})
    shots_on_target = data_tables[1].find_all(attrs={'data-stat':'shots_on_target'})
    shots_on_target_pct = data_tables[1].find_all(attrs={'data-stat':'shots_on_target_pct'})
    shots_total_per90 = data_tables[1].find_all(attrs={'data-stat':'shots_total_per90'})
    shots_on_target_per90 = data_tables[1].find_all(attrs={'data-stat':'shots_on_target_per90'})
    goals_per_shot = data_tables[1].find_all(attrs={'data-stat':'goals_per_shot'})
    goals_per_shot_on_target = data_tables[1].find_all(attrs={'data-stat':'goals_per_shot_on_target'})
    avg_shot_dist = data_tables[1].find_all(attrs={'data-stat':'average_shot_distance'})

    pens_successful = data_tables[1].find_all(attrs={'data-stat':'pens_made'})
    pens_attempts = data_tables[1].find_all(attrs={'data-stat':'pens_att'})
    xg = data_tables[1].find_all(attrs={'data-stat':'xg'})
    npxg = data_tables[1].find_all(attrs={'data-stat':'npxg'})
    npxg_per_shot = data_tables[1].find_all(attrs={'data-stat':'npxg_per_shot'})
    xg_net = data_tables[1].find_all(attrs={'data-stat':'xg_net'})
    npxg_net = data_tables[1].find_all(attrs={'data-stat':'npxg_net'})

    players_list = []
    nationality_list = []
    team_list = []
    # league_list = []
    position_list = []
    age_list = []
    birth_year_list = []
    full_90s_played_list = []
    goals_list = []
    shots_total_list = []
    shots_on_target_list = []
    shots_on_target_pct_list = []
    shots_total_per90_list = []
    shots_on_target_per90_list = []
    goals_per_shot_list = []
    goals_per_shot_on_target_list = []
    avg_shot_dist_list = []
    pens_successful_list = []
    pens_attempts_list = []
    xg_list = []
    npxg_list = []
    npxg_per_shot_list = []
    xg_net_list = []
    npxg_net_list = [] 

    for n in range(len(players)):
        players_list.append(players[n].text)
        nationality_list.append(nationality[n].text)
        team_list.append(team[n].text)
    #     league_list.append(league[n].text)
        position_list.append(position[n].text)
        age_list.append(age[n].text)
        birth_year_list.append(birth_year[n].text)
        full_90s_played_list.append(full_90s_played[n].text)
        goals_list.append(goals[n].text)
        shots_total_list.append(shots_total[n].text)
        shots_on_target_list.append(shots_on_target[n].text)
        shots_on_target_pct_list.append(shots_on_target_pct[n].text)
        shots_total_per90_list.append(shots_total_per90[n].text)
        shots_on_target_per90_list.append(shots_on_target_per90[n].text)
        goals_per_shot_list.append(goals_per_shot[n].text)
        goals_per_shot_on_target_list.append(goals_per_shot_on_target[n].text)
        avg_shot_dist_list.append(avg_shot_dist[n].text)
        pens_successful_list.append(pens_successful[n].text)
        pens_attempts_list.append(pens_attempts[n].text)
        xg_list.append(xg[n].text)
        npxg_list.append(npxg[n].text)
        npxg_per_shot_list.append(npxg_per_shot[n].text)
        xg_net_list.append(xg_net[n].text)
        npxg_net_list.append(npxg_net[n].text)

    giant_list = [players_list, nationality_list, team_list, position_list,
                  age_list, birth_year_list, full_90s_played_list, goals_list, 
                  shots_total_list, shots_on_target_list, shots_on_target_pct_list, 
                  shots_total_per90_list, shots_on_target_per90_list, goals_per_shot_list, 
                  goals_per_shot_on_target_list, avg_shot_dist_list, pens_successful_list, 
                  pens_attempts_list, xg_list, npxg_list, npxg_per_shot_list, xg_net_list, 
                  npxg_net_list]

    df = pd.DataFrame(giant_list).transpose()

    df.columns=['players' ,'nationality' ,'team' ,'position' ,'age' ,'birth_year'
    ,'full_90s_played' ,'goals' ,'shots_total' ,'shots_on_target' ,'shots_on_target_pct' 
    ,'shots_total_per90' ,'shots_on_target_per90' ,'goals_per_shot' ,'goals_per_shot_on_target' 
    ,'avg_shot_dist' ,'pens_successful' ,'pens_attempts' ,'xg','npxg' ,'npxg_per_shot' 
    ,'xg_net' ,'npxg_net'] 

    df2 = df.loc[df['players'] != 'Player',:]    
    
    df2.set_index(keys=['players','nationality','team','position','age','birth_year'], inplace=True)
    
    return df2
######################################################################################################
def passing_stats_scraper(url):
    '''This function takes as an argument the url from fbref (see example above)
    returns a df with all the stats from the passing stats page of fbref for a league and season'''
    
    driver.get(url)
    html = driver.execute_script('return document.body.innerHTML;')
    soup = bs4.BeautifulSoup(html,'lxml')

    data_tables = soup.find_all(class_='table_outer_container')
    
    players = data_tables[1].find_all(attrs={'data-stat':"player"})
    nationality = data_tables[1].find_all(attrs={'data-stat':'nationality'})
    team = data_tables[1].find_all(attrs={'data-stat':'squad'})
    position = data_tables[1].find_all(attrs={'data-stat':'position'})
    age = data_tables[1].find_all(attrs={'data-stat':'age'})
    birth_year = data_tables[1].find_all(attrs={'data-stat':'birth_year'})

    full_90s_played = data_tables[1].find_all(attrs={'data-stat':"minutes_90s"})
    passes_completed = data_tables[1].find_all(attrs={'data-stat':'passes_completed'})
    passes_attempted = data_tables[1].find_all(attrs={'data-stat':'passes'})
    pass_percent = data_tables[1].find_all(attrs={'data-stat':'passes_pct'})
    passes_total_dist = data_tables[1].find_all(attrs={'data-stat':'passes_total_distance'})
    passes_prog_dist = data_tables[1].find_all(attrs={'data-stat':'passes_progressive_distance'})

    passes_completed_short = data_tables[1].find_all(attrs={'data-stat':'passes_completed_short'})
    passes_attempted_short = data_tables[1].find_all(attrs={'data-stat':'passes_short'})
    pass_percent_short = data_tables[1].find_all(attrs={'data-stat':'passes_pct_short'})

    passes_completed_medium = data_tables[1].find_all(attrs={'data-stat':'passes_completed_medium'})
    passes_attempted_medium = data_tables[1].find_all(attrs={'data-stat':'passes_medium'})
    pass_percent_medium = data_tables[1].find_all(attrs={'data-stat':'passes_pct_medium'})

    passes_completed_long = data_tables[1].find_all(attrs={'data-stat':'passes_completed_long'})
    passes_attempted_long = data_tables[1].find_all(attrs={'data-stat':'passes_long'})
    pass_percent_long = data_tables[1].find_all(attrs={'data-stat':'passes_pct_long'})

    assists = data_tables[1].find_all(attrs={'data-stat':'assists'}) #should be the same as on stand stats
    xa = data_tables[1].find_all(attrs={'data-stat':'xa'}) #should be the same as on stand stats
    xa_net = data_tables[1].find_all(attrs={'data-stat':'xa_net'})
    assisted_shots = data_tables[1].find_all(attrs={'data-stat':'assisted_shots'})
    passes_into_final_third = data_tables[1].find_all(attrs={'data-stat':'passes_into_final_third'})
    passes_into_penalty_area = data_tables[1].find_all(attrs={'data-stat':'passes_into_penalty_area'})
    crosses_into_penalty_area = data_tables[1].find_all(attrs={'data-stat':'crosses_into_penalty_area'})
    progressive_passes = data_tables[1].find_all(attrs={'data-stat':'progressive_passes'})

    players_list = []
    nationality_list = []
    team_list = []
    position_list = []
    age_list = []
    birth_year_list = []
    full_90s_played_list = []
    passes_completed_list = []
    passes_attempted_list = []
    pass_percent_list = []
    passes_total_dist_list = []
    passes_prog_dist_list = []
    passes_completed_short_list = [] 
    passes_attempted_short_list = []
    pass_percent_short_list = []
    passes_completed_medium_list = [] 
    passes_attempted_medium_list = [] 
    pass_percent_medium_list  = []
    passes_completed_long_list = [] 
    passes_attempted_long_list = [] 
    pass_percent_long_list = [] 
    assists_list = [] 
    xa_list = [] 
    xa_net_list = []
    assisted_shots_list = [] 
    passes_into_final_third_list = [] 
    passes_into_penalty_area_list = [] 
    crosses_into_penalty_area_list = [] 
    progressive_passes_list = []

    for n in range(len(players)):
        players_list.append(players[n].text)
        nationality_list.append(nationality[n].text)
        team_list.append(team[n].text)
        position_list.append(position[n].text)
        age_list.append(age[n].text)
        birth_year_list.append(birth_year[n].text)
        full_90s_played_list.append(full_90s_played[n].text)
        passes_completed_list.append(passes_completed[n].text)
        passes_attempted_list.append(passes_attempted[n].text)
        pass_percent_list.append(pass_percent[n].text)
        passes_total_dist_list.append(passes_total_dist[n].text)
        passes_prog_dist_list.append(passes_prog_dist[n].text)
        passes_completed_short_list.append(passes_completed_short[n].text) 
        passes_attempted_short_list.append(passes_attempted_short[n].text) 
        pass_percent_short_list.append(pass_percent_short[n].text) 
        passes_completed_medium_list.append(passes_completed_medium[n].text) 
        passes_attempted_medium_list.append(passes_attempted_medium[n].text) 
        pass_percent_medium_list.append(pass_percent_medium[n].text) 
        passes_completed_long_list.append(passes_completed_long[n].text) 
        passes_attempted_long_list.append(passes_attempted_long[n].text) 
        pass_percent_long_list.append(pass_percent_long[n].text) 
        assists_list.append(assists[n].text) 
        xa_list.append(xa[n].text) 
        xa_net_list.append(xa_net[n].text)
        assisted_shots_list.append(assisted_shots[n].text) 
        passes_into_final_third_list.append(passes_into_final_third[n].text) 
        passes_into_penalty_area_list.append(passes_into_penalty_area[n].text) 
        crosses_into_penalty_area_list.append(crosses_into_penalty_area[n].text) 
        progressive_passes_list.append(progressive_passes[n].text) 

    giant_list = [players_list,nationality_list,team_list,position_list,age_list,birth_year_list,
    full_90s_played_list,passes_completed_list,passes_attempted_list,pass_percent_list
    ,passes_total_dist_list,passes_prog_dist_list,passes_completed_short_list 
    ,passes_attempted_short_list,pass_percent_short_list,passes_completed_medium_list 
    ,passes_attempted_medium_list ,pass_percent_medium_list ,passes_completed_long_list 
    ,passes_attempted_long_list ,pass_percent_long_list ,assists_list ,xa_list 
    ,xa_net_list,assisted_shots_list ,passes_into_final_third_list ,passes_into_penalty_area_list 
    ,crosses_into_penalty_area_list ,progressive_passes_list ]

    df = pd.DataFrame(giant_list).transpose()

    df.columns = ['players','nationality' ,'team' ,'position' ,'age' ,'birth_year' 
    ,'full_90s_played' ,'passes_completed' ,'passes_attempted' ,'pass_percent' ,'passes_total_dist' 
    ,'passes_prog_dist' ,'passes_completed_short' ,'passes_attempted_short' ,'pass_percent_short' 
    ,'passes_completed_medium' ,'passes_attempted_medium' ,'pass_percent_medium' ,'passes_completed_long' 
    ,'passes_attempted_long' ,'pass_percent_long' ,'assists' ,'xa' ,'xa_net','assisted_shots' 
    ,'passes_into_final_third','passes_into_penalty_area','crosses_into_penalty_area', 'progressive_passes']

    df2 = df.loc[df['players'] != 'Player',:]    
    
    df2.set_index(keys=['players','nationality','team','position','age','birth_year'], inplace=True)
    
    return df2
######################################################################################################
def gsc_stats_scraper(url):
    '''This function takes as an argument the url from fbref (see example above)
    returns a df with all the stats from the GSC stats page of fbref for a league and season'''
    
    driver.get(url)
    html = driver.execute_script('return document.body.innerHTML;')
    soup = bs4.BeautifulSoup(html,'lxml')

    data_tables = soup.find_all(class_='table_outer_container')
    
    players = data_tables[1].find_all(attrs={'data-stat':"player"})
    nationality = data_tables[1].find_all(attrs={'data-stat':'nationality'})
    team = data_tables[1].find_all(attrs={'data-stat':'squad'})
    position = data_tables[1].find_all(attrs={'data-stat':'position'})
    age = data_tables[1].find_all(attrs={'data-stat':'age'})
    birth_year = data_tables[1].find_all(attrs={'data-stat':'birth_year'})

    sca = data_tables[1].find_all(attrs={'data-stat':'sca'})
    sca_per90 = data_tables[1].find_all(attrs={'data-stat':'sca_per90'})
    sca_passes_live = data_tables[1].find_all(attrs={'data-stat':'sca_passes_live'})
    sca_passes_dead = data_tables[1].find_all(attrs={'data-stat':'sca_passes_dead'})
    sca_dribbles = data_tables[1].find_all(attrs={'data-stat':'sca_dribbles'})
    sca_shots = data_tables[1].find_all(attrs={'data-stat':'sca_shots'})
    sca_fouled = data_tables[1].find_all(attrs={'data-stat':'sca_fouled'})
    sca_defense = data_tables[1].find_all(attrs={'data-stat':'sca_defense'})

    gca = data_tables[1].find_all(attrs={'data-stat':'gca'})
    gca_per90 = data_tables[1].find_all(attrs={'data-stat':'gca_per90'})
    gca_passes_live = data_tables[1].find_all(attrs={'data-stat':'gca_passes_live'})
    gca_passes_dead = data_tables[1].find_all(attrs={'data-stat':'gca_passes_dead'})
    gca_dribbles = data_tables[1].find_all(attrs={'data-stat':'gca_dribbles'})
    gca_shots = data_tables[1].find_all(attrs={'data-stat':'gca_shots'})
    gca_fouled = data_tables[1].find_all(attrs={'data-stat':'gca_fouled'})
    gca_defense = data_tables[1].find_all(attrs={'data-stat':'gca_defense'})
    gca_og_for = data_tables[1].find_all(attrs={'data-stat':'gca_og_for'})    

    players_list = []
    nationality_list = []
    team_list = []
    position_list = []
    age_list = []
    birth_year_list = []
    sca_list = []
    sca_per90_list = []
    sca_passes_live_list = []
    sca_passes_dead_list = []
    sca_dribbles_list = []
    sca_shots_list = []
    sca_fouled_list = []
    sca_defense_list = []
    gca_list = []
    gca_per90_list = []
    gca_passes_live_list = []
    gca_passes_dead_list = []
    gca_dribbles_list = []
    gca_shots_list = []
    gca_fouled_list = []
    gca_defense_list = []
    gca_og_for_list = []

    for n in range(len(players)):
        players_list.append(players[n].text)
        nationality_list.append(nationality[n].text)
        team_list.append(team[n].text)
        position_list.append(position[n].text)
        age_list.append(age[n].text)
        birth_year_list.append(birth_year[n].text)
        sca_list.append(sca[n].text)
        sca_per90_list.append(sca_per90[n].text)
        sca_passes_live_list.append(sca_passes_live[n].text)
        sca_passes_dead_list.append(sca_passes_dead[n].text)
        sca_dribbles_list.append(sca_dribbles[n].text)
        sca_shots_list.append(sca_shots[n].text)
        sca_fouled_list.append(sca_fouled[n].text)
        sca_defense_list.append(sca_defense[n].text)
        gca_list.append(gca[n].text)
        gca_per90_list.append(gca_per90[n].text)
        gca_passes_live_list.append(gca_passes_live[n].text)
        gca_passes_dead_list.append(gca_passes_dead[n].text)
        gca_dribbles_list.append(gca_dribbles[n].text)
        gca_shots_list.append(gca_shots[n].text)
        gca_fouled_list.append(gca_fouled[n].text)
        gca_defense_list.append(gca_defense[n].text)
        gca_og_for_list.append(gca_og_for[n].text)

    giant_list = [players_list, nationality_list, team_list, position_list, 
                  age_list, birth_year_list, sca_list, sca_per90_list, 
                  sca_passes_live_list, sca_passes_dead_list, sca_dribbles_list, 
                  sca_shots_list, sca_fouled_list, sca_defense_list, gca_list, 
                  gca_per90_list, gca_passes_live_list, gca_passes_dead_list, 
                  gca_dribbles_list, gca_shots_list, gca_fouled_list, gca_defense_list, 
                  gca_og_for_list]
    df = pd.DataFrame(giant_list).transpose()

    df.columns=['players' ,'nationality' ,'team','position' ,'age' ,'birth_year' 
    ,'sca' ,'sca_per90' ,'sca_passes_live' ,'sca_passes_dead' ,'sca_dribbles' 
    ,'sca_shots' ,'sca_fouled' ,'sca_defense' ,'gca' ,'gca_per90' ,'gca_passes_live' 
    ,'gca_passes_dead' ,'gca_dribbles','gca_shots' ,'gca_fouled' ,'gca_defense' ,'gca_og_for' ]

    df2 = df.loc[df['players'] != 'Player',:]    
    
    df2.set_index(keys=['players','nationality','team','position','age','birth_year'], inplace=True)
    
    return df2

######################################################################################################
def defense_stats_scraper(url):
    '''This function takes as an argument the url from fbref (see example above)
    returns a df with all the stats from the defensive actions stats page of fbref for a league and season'''
    
    driver.get(url)
    html = driver.execute_script('return document.body.innerHTML;')
    soup = bs4.BeautifulSoup(html,'lxml')

    data_tables = soup.find_all(class_='table_outer_container')
    
    players = data_tables[1].find_all(attrs={'data-stat':"player"})
    nationality = data_tables[1].find_all(attrs={'data-stat':'nationality'})
    team = data_tables[1].find_all(attrs={'data-stat':'squad'})
    position = data_tables[1].find_all(attrs={'data-stat':'position'})
    age = data_tables[1].find_all(attrs={'data-stat':'age'})
    birth_year = data_tables[1].find_all(attrs={'data-stat':'birth_year'})

    tackles = data_tables[1].find_all(attrs={'data-stat':'tackles'})
    tackles_won = data_tables[1].find_all(attrs={'data-stat':'tackles_won'})
    tackles_def_3rd = data_tables[1].find_all(attrs={'data-stat':'tackles_def_3rd'})
    tackles_mid_3rd = data_tables[1].find_all(attrs={'data-stat':'tackles_mid_3rd'})
    tackles_att_3rd = data_tables[1].find_all(attrs={'data-stat':'tackles_att_3rd'})

    dribble_tackles = data_tables[1].find_all(attrs={'data-stat':'dribble_tackles'}) #number of dribblers tackled
    dribble_vs = data_tables[1].find_all(attrs={'data-stat':'dribbles_vs'})
    dribble_tackles_pct = data_tables[1].find_all(attrs={'data-stat':'dribble_tackles_pct'})
    dribbled_past = data_tables[1].find_all(attrs={'data-stat':'dribbled_past'})

    pressures = data_tables[1].find_all(attrs={'data-stat':'pressures'})
    pressure_regains = data_tables[1].find_all(attrs={'data-stat':'pressure_regains'})
    pressure_regain_pct = data_tables[1].find_all(attrs={'data-stat':'pressure_regain_pct'})
    pressures_def_3rd = data_tables[1].find_all(attrs={'data-stat':'pressures_def_3rd'})
    pressures_mid_3rd = data_tables[1].find_all(attrs={'data-stat':'pressures_mid_3rd'})
    pressures_att_3rd = data_tables[1].find_all(attrs={'data-stat':'pressures_att_3rd'})

    blocks = data_tables[1].find_all(attrs={'data-stat':'blocks'})
    blocked_shots = data_tables[1].find_all(attrs={'data-stat':'blocked_shots'})
    blocked_shots_saves = data_tables[1].find_all(attrs={'data-stat':'blocked_shots_saves'})
    blocked_passes = data_tables[1].find_all(attrs={'data-stat':'blocked_passes'})
    interceptions = data_tables[1].find_all(attrs={'data-stat':'interceptions'})
    tackles_interceptions = data_tables[1].find_all(attrs={'data-stat':'tackles_interceptions'})
    clearances = data_tables[1].find_all(attrs={'data-stat':'clearances'})
    errors = data_tables[1].find_all(attrs={'data-stat':'errors'})    

    players_list = []
    nationality_list = []
    team_list = []
    position_list = []
    age_list = []
    birth_year_list= [] 
    tackles_list = []
    tackles_won_list = []
    tackles_def_3rd_list = []
    tackles_mid_3rd_list = []
    tackles_att_3rd_list = []
    dribble_tackles_list = []
    dribble_vs_list = []
    dribble_tackles_pct_list= [] 
    dribbled_past_list = []
    pressures_list = []
    pressure_regains_list= [] 
    pressure_regain_pct_list = []
    pressures_def_3rd_list = []
    pressures_mid_3rd_list = []
    pressures_att_3rd_list = []
    blocks_list = []
    blocked_shots_list= []
    blocked_shots_saves_list= [] 
    blocked_passes_list = []
    interceptions_list = []
    tackles_interceptions_list= [] 
    clearances_list = []
    errors_list = []

    for n in range(len(players)):
        players_list.append(players[n].text)
        nationality_list.append(nationality[n].text) 
        team_list.append(team[n].text) 
        position_list.append(position[n].text) 
        age_list.append(age[n].text) 
        birth_year_list.append(birth_year[n].text) 
        tackles_list.append(tackles[n].text) 
        tackles_won_list.append(tackles_won[n].text) 
        tackles_def_3rd_list.append(tackles_def_3rd[n].text) 
        tackles_mid_3rd_list.append(tackles_mid_3rd[n].text) 
        tackles_att_3rd_list.append(tackles_att_3rd[n].text) 
        dribble_tackles_list.append(dribble_tackles[n].text)
        dribble_vs_list.append(dribble_vs[n].text) 
        dribble_tackles_pct_list.append(dribble_tackles_pct[n].text) 
        dribbled_past_list.append(dribbled_past[n].text) 
        pressures_list.append(pressures[n].text) 
        pressure_regains_list.append(pressure_regains[n].text) 
        pressure_regain_pct_list.append(pressure_regain_pct[n].text) 
        pressures_def_3rd_list.append(pressures_def_3rd[n].text) 
        pressures_mid_3rd_list.append(pressures_mid_3rd[n].text) 
        pressures_att_3rd_list.append(pressures_att_3rd[n].text)
        blocks_list.append(blocks[n].text)
        blocked_shots_list.append(blocked_shots[n].text)
        blocked_shots_saves_list.append(blocked_shots_saves[n].text) 
        blocked_passes_list.append(blocked_passes[n].text) 
        interceptions_list.append(interceptions[n].text) 
        tackles_interceptions_list.append(tackles_interceptions[n].text) 
        clearances_list.append(clearances[n].text) 
        errors_list.append(errors[n].text)

    giant_list=[players_list,nationality_list,team_list,position_list,age_list,birth_year_list 
    ,tackles_list,tackles_won_list,tackles_def_3rd_list,tackles_mid_3rd_list,tackles_att_3rd_list 
    ,dribble_tackles_list,dribble_vs_list,dribble_tackles_pct_list,dribbled_past_list 
    ,pressures_list ,pressure_regains_list ,pressure_regain_pct_list ,pressures_def_3rd_list 
    ,pressures_mid_3rd_list ,pressures_att_3rd_list ,blocks_list ,blocked_shots_list
    ,blocked_shots_saves_list ,blocked_passes_list ,interceptions_list ,tackles_interceptions_list 
    ,clearances_list ,errors_list ]

    df = pd.DataFrame(giant_list).transpose()

    df.columns =['players' ,'nationality' ,'team' ,'position' ,'age' ,'birth_year' ,'tackles' 
    ,'tackles_won' ,'tackles_def_3rd' ,'tackles_mid_3rd' ,'tackles_att_3rd' ,'dribble_tackles' 
    ,'dribble_vs' ,'dribble_tackles_pct' ,'dribbled_past' ,'pressures' ,'pressure_regains' 
    ,'pressure_regain_pct' ,'pressures_def_3rd' ,'pressures_mid_3rd' ,'pressures_att_3rd' 
    ,'blocks' ,'blocked_shots','blocked_shots_saves' ,'blocked_passes' ,'interceptions' 
    ,'tackles_interceptions' ,'clearances' ,'errors'] 

    df2 = df.loc[df['players'] != 'Player',:]    
    
    df2.set_index(keys=['players','nationality','team','position','age','birth_year'], inplace=True)
    
    return df2

######################################################################################################
def possession_stats_scraper(url):
    '''This function takes as an argument the url from fbref (see example above)
    returns a df with all the stats from the possession stats page of fbref for a league and season'''
    
    driver.get(url)
    html = driver.execute_script('return document.body.innerHTML;')
    soup = bs4.BeautifulSoup(html,'lxml')

    data_tables = soup.find_all(class_='table_outer_container')
    
    players = data_tables[1].find_all(attrs={'data-stat':"player"})
    nationality = data_tables[1].find_all(attrs={'data-stat':'nationality'})
    team = data_tables[1].find_all(attrs={'data-stat':'squad'})
    position = data_tables[1].find_all(attrs={'data-stat':'position'})
    age = data_tables[1].find_all(attrs={'data-stat':'age'})
    birth_year = data_tables[1].find_all(attrs={'data-stat':'birth_year'})

    full_90s_played = data_tables[1].find_all(attrs={'data-stat':"minutes_90s"})
    touches = data_tables[1].find_all(attrs={'data-stat':"touches"})
    touches_def_pen_area = data_tables[1].find_all(attrs={'data-stat':"touches_def_pen_area"})
    touches_def_3rd = data_tables[1].find_all(attrs={'data-stat':"touches_def_3rd"})
    touches_mid_3rd = data_tables[1].find_all(attrs={'data-stat':"touches_mid_3rd"})
    touches_att_3rd = data_tables[1].find_all(attrs={'data-stat':"touches_att_3rd"})
    touches_att_pen_area = data_tables[1].find_all(attrs={'data-stat':"touches_att_pen_area"})
    touches_live_ball = data_tables[1].find_all(attrs={'data-stat':"touches_live_ball"})
    dribbles_completed = data_tables[1].find_all(attrs={'data-stat':"dribbles_completed"})
    dribbles = data_tables[1].find_all(attrs={'data-stat':"dribbles"})
    dribbles_completed_pct = data_tables[1].find_all(attrs={'data-stat':"dribbles_completed_pct"})
    players_dribbled_past = data_tables[1].find_all(attrs={'data-stat':"players_dribbled_past"})
    nutmegs = data_tables[1].find_all(attrs={'data-stat':"nutmegs"})
    carries = data_tables[1].find_all(attrs={'data-stat':"carries"})
    carry_distance = data_tables[1].find_all(attrs={'data-stat':"carry_distance"})
    carry_progressive_distance = data_tables[1].find_all(attrs={'data-stat':"carry_progressive_distance"})
    pass_targets = data_tables[1].find_all(attrs={'data-stat':"pass_targets"})
    passes_received = data_tables[1].find_all(attrs={'data-stat':"passes_received"})
    passes_received_pct = data_tables[1].find_all(attrs={'data-stat':"passes_received_pct"})
    miscontrols = data_tables[1].find_all(attrs={'data-stat':"miscontrols"})
    dispossessed = data_tables[1].find_all(attrs={'data-stat':"dispossessed"})

    players_list = []
    nationality_list = []
    team_list = []
    position_list = []
    age_list = []
    birth_year_list = []
    full_90s_played_list = []
    touches_list = []
    touches_def_pen_area_list = []
    touches_def_3rd_list = []
    touches_mid_3rd_list = []
    touches_att_3rd_list = []
    touches_att_pen_area_list = []
    touches_live_ball_list = []
    dribbles_completed_list = []
    dribbles_list = []
    dribbles_completed_pct_list = []
    players_dribbled_past_list = []
    nutmegs_list = []
    carries_list = []
    carry_distance_list = []
    carry_progressive_distance_list = []
    pass_targets_list = []
    passes_received_list = []
    passes_received_pct_list = []
    miscontrols_list = []
    dispossessed_list = []

    for n in range(len(players)):
        players_list.append(players[n].text)
        nationality_list.append(nationality[n].text)
        team_list.append(team[n].text)
        position_list.append(position[n].text)
        age_list.append(age[n].text)
        birth_year_list.append(birth_year[n].text)
        full_90s_played_list.append(full_90s_played[n].text)
        touches_list.append(touches[n].text)
        touches_def_pen_area_list.append(touches_def_pen_area[n].text)
        touches_def_3rd_list.append(touches_def_3rd[n].text)
        touches_mid_3rd_list.append(touches_mid_3rd[n].text)
        touches_att_3rd_list.append(touches_att_3rd[n].text)
        touches_att_pen_area_list.append(touches_att_pen_area[n].text)
        touches_live_ball_list.append(touches_live_ball[n].text)
        dribbles_completed_list.append(dribbles_completed[n].text)
        dribbles_list.append(dribbles[n].text)
        dribbles_completed_pct_list.append(dribbles_completed_pct[n].text)
        players_dribbled_past_list.append(players_dribbled_past[n].text)
        nutmegs_list.append(nutmegs[n].text)
        carries_list.append(carries[n].text)
        carry_distance_list.append(carry_distance[n].text)
        carry_progressive_distance_list.append(carry_progressive_distance[n].text)
        pass_targets_list.append(pass_targets[n].text)
        passes_received_list.append(passes_received[n].text)
        passes_received_pct_list.append(passes_received_pct[n].text)
        miscontrols_list.append(miscontrols[n].text)
        dispossessed_list.append(dispossessed[n].text)

    giant_list = [players_list, nationality_list, team_list, position_list, age_list, 
                  birth_year_list, full_90s_played_list, touches_list, 
                  touches_def_pen_area_list, touches_def_3rd_list, touches_mid_3rd_list, 
                  touches_att_3rd_list, touches_att_pen_area_list, touches_live_ball_list, 
                  dribbles_completed_list, dribbles_list, dribbles_completed_pct_list, 
                  players_dribbled_past_list, nutmegs_list, carries_list, carry_distance_list
                  , carry_progressive_distance_list, pass_targets_list, passes_received_list, 
                  passes_received_pct_list, miscontrols_list, dispossessed_list]

    df = pd.DataFrame(giant_list).transpose()

    df.columns = ['players' ,'nationality' ,'team' ,'position' ,'age' ,'birth_year' ,'full_90s_played' 
    ,'touches' ,'touches_def_pen_area','touches_def_3rd' ,'touches_mid_3rd' ,'touches_att_3rd' 
    ,'touches_att_pen_area','touches_live_ball' ,'dribbles_completed','dribbles' ,'dribbles_completed_pct'
    ,'players_dribbled_past' ,'nutmegs' ,'carries' ,'carry_distance' ,'carry_progressive_distance' 
    ,'pass_targets' ,'passes_received' ,'passes_received_pct' ,'miscontrols' ,'dispossessed']    

    df2 = df.loc[df['players'] != 'Player',:]    
    
    df2.set_index(keys=['players','nationality','team','position','age','birth_year'], inplace=True)
    
    return df2

######################################################################################################
def pass_type_stats_scraper(url):
    '''This function takes as an argument the url from fbref (see example above)
    returns a df with all the stats from the pass type stats page (to get footedness) of fbref for a league and season'''
    
    driver.get(url)
    html = driver.execute_script('return document.body.innerHTML;')
    soup = bs4.BeautifulSoup(html,'lxml')

    data_tables = soup.find_all(class_='table_outer_container')
    
    players = data_tables[1].find_all(attrs={'data-stat':"player"})
    nationality = data_tables[1].find_all(attrs={'data-stat':'nationality'})
    team = data_tables[1].find_all(attrs={'data-stat':'squad'})
    position = data_tables[1].find_all(attrs={'data-stat':'position'})
    age = data_tables[1].find_all(attrs={'data-stat':'age'})
    birth_year = data_tables[1].find_all(attrs={'data-stat':'birth_year'})

    passes_left_foot = data_tables[1].find_all(attrs={'data-stat':'passes_left_foot'})
    passes_right_foot = data_tables[1].find_all(attrs={'data-stat':'passes_right_foot'})

    players_list = []
    nationality_list = []
    team_list = []
    position_list = []
    age_list = []
    birth_year_list = []
    full_90s_played_list = []
    passes_left_foot_list = []
    passes_right_foot_list = []

    for n in range(len(players)):
        players_list.append(players[n].text)
        nationality_list.append(nationality[n].text)
        team_list.append(team[n].text)
        position_list.append(position[n].text)
        age_list.append(age[n].text)
        birth_year_list.append(birth_year[n].text)
        passes_left_foot_list.append(passes_left_foot[n].text)
        passes_right_foot_list.append(passes_right_foot[n].text)


    giant_list = [players_list, nationality_list, team_list, position_list, age_list, 
                  birth_year_list, passes_left_foot_list, passes_right_foot_list]

    df = pd.DataFrame(giant_list).transpose()

    df.columns = ['players' ,'nationality' ,'team' ,'position' ,'age' ,'birth_year' ,
                  'passes_left_foot','passes_right_foot']    

    df2 = df.loc[df['players'] != 'Player',:]    
    
    df2.set_index(keys=['players','nationality','team','position','age','birth_year'], inplace=True)
    
    return df2

######################################################################################################
def miscellaneous_stats_scraper(url):
    '''This function takes as an argument the url from fbref (see example above)
    returns a df with all the stats from the miscellaneous stats page (to get aerial duels) of fbref for a league and season'''
    
    driver.get(url)
    html = driver.execute_script('return document.body.innerHTML;')
    soup = bs4.BeautifulSoup(html,'lxml')

    data_tables = soup.find_all(class_='table_outer_container')
    
    players = data_tables[1].find_all(attrs={'data-stat':"player"})
    nationality = data_tables[1].find_all(attrs={'data-stat':'nationality'})
    team = data_tables[1].find_all(attrs={'data-stat':'squad'})
    position = data_tables[1].find_all(attrs={'data-stat':'position'})
    age = data_tables[1].find_all(attrs={'data-stat':'age'})
    birth_year = data_tables[1].find_all(attrs={'data-stat':'birth_year'})

    aerials_won = data_tables[1].find_all(attrs={'data-stat':'aerials_won'})
    aerials_lost = data_tables[1].find_all(attrs={'data-stat':'aerials_lost'})
    aerials_won_pct = data_tables[1].find_all(attrs={'data-stat':'aerials_won_pct'})

    players_list = []
    nationality_list = []
    team_list = []
    position_list = []
    age_list = []
    birth_year_list = []
    full_90s_played_list = []
    aerials_won_list = []
    aerials_lost_list = []
    aerials_won_pct_list = []

    for n in range(len(players)):
        players_list.append(players[n].text)
        nationality_list.append(nationality[n].text)
        team_list.append(team[n].text)
        position_list.append(position[n].text)
        age_list.append(age[n].text)
        birth_year_list.append(birth_year[n].text)

        aerials_won_list.append(aerials_won[n].text)
        aerials_lost_list.append(aerials_lost[n].text)
        aerials_won_pct_list.append(aerials_won_pct[n].text)

    giant_list = [players_list, nationality_list, team_list, position_list, age_list, 
                  birth_year_list, aerials_won_list, aerials_lost_list, aerials_won_pct_list]

    df = pd.DataFrame(giant_list).transpose()

    df.columns = ['players' ,'nationality' ,'team' ,'position' ,'age' ,'birth_year' ,
                  'aerials_won','aerials_lost','aerials_won_pct']
    

    df2 = df.loc[df['players'] != 'Player',:]    
    
    df2.set_index(keys=['players','nationality','team','position','age','birth_year'], inplace=True)
    
    return df2

######################################################################################################
def gk_stats_scraper(url):
    '''This function takes as an argument the url from fbref (see example above)
    returns a df with all the stats from the goal keeping stats page of fbref for a league and season'''
    
    driver.get(url)
    html = driver.execute_script('return document.body.innerHTML;')
    soup = bs4.BeautifulSoup(html,'lxml')

    data_tables = soup.find_all(class_='table_outer_container')
    
    players = data_tables[1].find_all(attrs={'data-stat':"player"})
    nationality = data_tables[1].find_all(attrs={'data-stat':'nationality'})
    team = data_tables[1].find_all(attrs={'data-stat':'squad'})
    position = data_tables[1].find_all(attrs={'data-stat':'position'})
    age = data_tables[1].find_all(attrs={'data-stat':'age'})
    birth_year = data_tables[1].find_all(attrs={'data-stat':'birth_year'})

    games = data_tables[1].find_all(attrs={'data-stat':'games_gk'})
    starts = data_tables[1].find_all(attrs={'data-stat':'games_starts_gk'})
    minutes = data_tables[1].find_all(attrs={'data-stat':'minutes_gk'})
    goals_conceded = data_tables[1].find_all(attrs={'data-stat':'goals_against_gk'})
    goals_conceded_per_90 = data_tables[1].find_all(attrs={'data-stat':'goals_against_per90_gk'})

    shots_on_target_against = data_tables[1].find_all(attrs={'data-stat':'shots_on_target_against'})
    saves = data_tables[1].find_all(attrs={'data-stat':'saves'})
    save_pct = data_tables[1].find_all(attrs={'data-stat':'save_pct'})
    wins = data_tables[1].find_all(attrs={'data-stat':'wins_gk'})
    draws = data_tables[1].find_all(attrs={'data-stat':'draws_gk'})
    losses = data_tables[1].find_all(attrs={'data-stat':'losses_gk'})
    clean_sheets = data_tables[1].find_all(attrs={'data-stat':'clean_sheets'})
    clean_sheets_pct = data_tables[1].find_all(attrs={'data-stat':'clean_sheets_pct'})

    pens_att_gk = data_tables[1].find_all(attrs={'data-stat':'pens_att_gk'})
    pens_allowed = data_tables[1].find_all(attrs={'data-stat':'pens_allowed'})
    pens_saved = data_tables[1].find_all(attrs={'data-stat':'pens_saved'})
    pens_missed_gk = data_tables[1].find_all(attrs={'data-stat':'pens_missed_gk'})

    players_list = []
    nationality_list = []
    team_list = []
    position_list = []
    age_list = []
    birth_year_list = []
    games_list = []
    starts_list = []
    minutes_list = []
    goals_conceded_list = []
    goals_conceded_per_90_list = []
    shots_on_target_against_list = []
    saves_list = []
    save_pct_list = []
    wins_list = []
    draws_list = []
    losses_list = []
    clean_sheets_list = []
    clean_sheets_pct_list = []
    pens_att_gk_list = []
    pens_allowed_list = []
    pens_saved_list = []
    pens_missed_gk_list = []

    for n in range(len(players)):
        players_list.append(players[n].text)
        nationality_list.append(nationality[n].text)
        team_list.append(team[n].text)
        position_list.append(position[n].text)
        age_list.append(age[n].text)
        birth_year_list.append(birth_year[n].text)
        games_list.append(games[n].text)
        starts_list.append(starts[n].text)
        minutes_list.append(minutes[n].text)
        goals_conceded_list.append(goals_conceded[n].text)
        goals_conceded_per_90_list.append(goals_conceded_per_90[n].text)
        shots_on_target_against_list.append(shots_on_target_against[n].text)
        saves_list.append(saves[n].text)
        save_pct_list.append(save_pct[n].text)
        wins_list.append(wins[n].text)
        draws_list.append(draws[n].text)
        losses_list.append(losses[n].text)
        clean_sheets_list.append(clean_sheets[n].text)
        clean_sheets_pct_list.append(clean_sheets_pct[n].text)
        pens_att_gk_list.append(pens_att_gk[n].text)
        pens_allowed_list.append(pens_allowed[n].text)
        pens_saved_list.append(pens_saved[n].text)
        pens_missed_gk_list.append(pens_missed_gk[n].text)

    giant_list = [players_list, nationality_list, team_list, position_list, age_list, 
                  birth_year_list, games_list, starts_list, minutes_list, goals_conceded_list,
                  goals_conceded_per_90_list, shots_on_target_against_list, saves_list, 
                  save_pct_list, wins_list, draws_list, losses_list, clean_sheets_list, 
                  clean_sheets_pct_list, pens_att_gk_list, pens_allowed_list, pens_saved_list,
                  pens_missed_gk_list]

    df = pd.DataFrame(giant_list).transpose()

    df.columns=['players' ,'nationality' ,'team' ,'position' ,'age' ,'birth_year' ,'games' 
    ,'starts' ,'minutes' ,'goals_conceded' ,'goals_conceded_per_90' ,'shots_on_target_against' 
    ,'saves' ,'save_pct' ,'wins','draws' ,'losses' ,'clean_sheets' ,'clean_sheets_pct' 
    ,'pens_att_gk' ,'pens_allowed' ,'pens_saved' ,'pens_missed_gk' ]    

    df2 = df.loc[df['players'] != 'Player',:]    
    
    df2.set_index(keys=['players','nationality','team','position','age','birth_year'], inplace=True)
    
    return df2