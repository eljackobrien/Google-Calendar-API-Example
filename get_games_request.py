# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 14:31:37 2023

@author: eljac
"""

import requests
from bs4 import BeautifulSoup as BS

#%% Check how many pages
r = requests.get("https://www.rugbykickoff.com/")
soup0 = BS(r.text, 'html.parser')
last_page = int( soup0.get_text().split('\nPrevious\n1')[-1].split('\nNext')[0].split('\n')[-1] )



#%% Loop through pages and get all rugby games
soups = []

# Get all the games from rugbykickoff
for i in range(15):
    r = requests.get(f"https://www.rugbykickoff.com/?page={i+1}")
    soups.append( BS(r.text, 'html.parser') )

# Parse the HTML into a big list with [ day -> [time, teams, league-stadium] ]
games = []
for soup in soups:
    string = soup.get_text()
    string = string.split('Filter\nReset')[-1].split('\nPrevious\n1')[0]

    string = string.split('\n')
    games = games + [string_i for string_i in string if len(string_i.replace(' ','')) > 0]

# Make a game class where the info is stored as attributes
class Game:
    def __init__(self, day, time, league, home_team, away_team, stadium):
        self.day = day
        self.time = time
        self.league = league
        self.home_team = home_team
        self.away_team = away_team
        self.stadium = stadium

    def print_info(self):
        print(f"{self.day}\t{self.time}\t{self.home_team} vs {self.away_team} in {self.stadium}\t({self.league})\n")

# Loop over the big list and create the game classes, will fail if list format changes
Game_classes = []
game_counter = 0
for row in games:
    if 'Friday' in row or 'Saturday' in row or 'Sunday' in row:
        day = row
        continue

    if ':' in row:
        time = row.strip()
        continue

    if ' v ' in row:
        home_team = row.strip().split(' v ')[0]
        away_team = row.strip().split(' v ')[1]
        continue

    if ' - ' in row:
        league = row.split(' - ')[0].replace('United Rugby Championship','URC (Best League)').replace('Prem','English Prem')
        stadium = row.split(' - ')[1]

    Game_classes.append(Game(day, time, league, home_team, away_team, stadium))


# Check leagues
all_leagues = []
for Game_class in Game_classes:
    all_leagues.append(Game_class.league)
#print(np.unique(all_leagues))



#%% Clear the rugby calendar
# Use list_calendar.py to check the id of the calendar you want to use
with open("calendar_id.txt", "r") as file: calendar_id = file.read()

from calendar_setup import get_calendar_service
service = get_calendar_service()

page_token, del_ids = None, []
while True:
    events = service.events().list(calendarId=calendar_id, pageToken=page_token).execute()
    for event in events['items']:
        del_ids.append(event['id'])
    page_token = events.get('nextPageToken')
    if not page_token:
        break

for del_id in del_ids:
    service.events().delete(calendarId=calendar_id, eventId=del_id).execute()



#%% Add events to calendar
from add_calendar_event import add_event

months_dict = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7, 'August':8, 'September':9, 'October':10, 'November':11, 'December':12}

for Game_class in Game_classes:
    # Skip uninteresting leagues to avoid overcrowding
    leagues = ['URC', 'English Premiership', 'Top 14', 'Champions', 'Challenge', 'World Cup']
    bad_league = 1
    for league in leagues:
        if league in Game_class.league:
            bad_league = 0
            break
    if bad_league: continue


    name = f"{Game_class.home_team} - {Game_class.away_team}"
    desc = Game_class.league + "\nAdded by eljackobrien@gmail.com script"
    year = 2023
    month = months_dict[ Game_class.day.split()[2] ]
    day = int(Game_class.day.split()[1])
    start_hour = int(Game_class.time.split(':')[0])
    start_min = int(Game_class.time.split(':')[1])
    rugby_calendar_id = calendar_id

    add_event(name, desc, year, month, day, start_hour, start_min, length_hours=2, calendarID=rugby_calendar_id)


