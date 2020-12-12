import bs4
import requests
import pandas as pd

def transfer_value_gather(table):
    '''function that takes in as an argument a bs4 result set that is the table of transfer
    information (for season for league).  Each webpage has 40 tables: one table for transfers
    into the club (even index) and one for transfers out (odd index) for each of the 20 clubs.
    ''' 
    player_list = []
    club_left_list = []
    age_list = []
    position_list = []
    est_market_value = []
    fee_list = []
    nationality = []
    previous_league = []

    player = table.find_all(class_="spielprofil_tooltip tooltipstered")
    #The player tag gives two values - the full name, and first initial and 
    #last name.  Use modulo operator to grab full name (even entries).
    club_left = table.find_all(class_="vereinprofil_tooltip tooltipstered")
    #club_left returns a blank cell every other entry. First entry is blank
    #Use modulo operator to grab odds entries
    for i in range(len(player)):
        if i % 2 == 0:
            player_list.append(player[i].text)
    
    #Can't only use class_="vereinprofil_tooltip tooltipstered" because there are "without club entries"
    #that use a different tag.  The image tags for selling club appear to have same tag.  Getting the text
    #from the nested alt tag.
    club_left = table.find_all(class_="no-border-rechts zentriert")
    for i in range(len(club_left)):
        club_img = club_left[i].find_all("img")
        club_left_list.append(club_img[0]['alt'])
        #club_img comes as a single entry list so index with 0 before grabbing the 'alt' text

    age = table.find_all(class_="zentriert alter-transfer-cell")
    position = table.find_all(class_="pos-transfer-cell")
    #age and position have one entry per person and have a header
    # as the first entry - skip by indexing greater than 0
    for i in range(len(age)):
        if i > 0:
            age_list.append(age[i].text)
            position_list.append(position[i].text)

    fee = table.find_all("td", class_="rechts")
    #the fee tag grabs both estimate market value and actual fee in alternating
    #fashion
    for i in range(len(fee)):
        if i % 2 == 0:
            est_market_value.append(fee[i].text)
        if i % 2 == 1:
            fee_list.append(fee[i].text)


    nat_flag = table.find_all(class_="zentriert nat-transfer-cell")
    #Going to only grab the first nationality of a player
    for i in range(len(nat_flag)):
        if i > 0:
        #this has to start at 1 to get past the header    
            nation = nat_flag[i].find(class_="flaggenrahmen")
            nationality.append(nation['title'])

    league_flag = table.find_all(class_="no-border-links verein-flagge-transfer-cell")
    #The flaggenrahmen tag is on all flags and the indexing is messed up when dual nationals 
    #appear.  So using the outter tag on league to distinguish
    #League flag, unlike national flag doesn't have a header.  When a player is picked up without
    #a league they don't have a flag to grab from using try/except
    for i in range(len(league_flag)):
        try:
            league = league_flag[i].find(class_="flaggenrahmen")
            previous_league.append(league['title'])
        except TypeError:
            previous_league.append('Without Club')            
        
    giant_list = [player_list,age_list,nationality,position_list,
                  club_left_list,previous_league,est_market_value,fee_list]
    df = pd.DataFrame(giant_list).transpose()
    df.columns = ['player','age','nationality','position','selling_club','previous_league','est_market_value','fee']

    #Use this to get the buying club: The table-header tag is used twice on each page before
    #getting to the tables of in's and out's.  The in's and out's have same header therefore,
    # start at 2 and increment by 1 for each iteration through response table
#     table_header = soup.find_all(class_='table-header')
#     club = table_header[2].find_all(class_="vereinprofil_tooltip tooltipstered")
#     df['buying_club'] = club[1].text
#     buying_club = club[1].text
    return df