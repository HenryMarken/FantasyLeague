from bs4 import BeautifulSoup
import requests
import pandas as pd
from selenium import webdriver
import time

# Accessing Chrome Web Browser # 
PATH = 'C://Program Files (x86)//chromedriver.exe' # this is setup look it up after
URL = 'https://www.espn.com/nba/stats/player/_/table/offensive/sort/avgPoints/dir/desc'
driver = webdriver.Chrome(PATH) # .Chrome is the browser we want to ue and is located at path 
driver.get(URL)

# Show More #
i = 0
while i < 5:
    show_more = driver.find_element_by_link_text("Show More")
    show_more.click()
    time.sleep(2)
    i += 1

# Obtaining HTML #
html_text = driver.page_source
soup = BeautifulSoup(html_text, 'html.parser')

# Creating Data Frame #
column_names = [
    'Player Name',
    'Team Name',
    'Fantasy Points',
    'Points Per Game',
    'Field Goals Made',
    'Field Goals Attempted',
    'Free Throws Made',
    'Free Throws Attempted',
    'Three Pointers Made',
    'Rebounds',
    'Assists',
    'Steals',
    'Blocks',
    'Turnovers'
]

df = pd.DataFrame(columns = column_names)


# Finding Players #
table_player = soup.find('table', class_ = 'Table Table--align-right Table--fixed Table--fixed-left')
players = table_player.find_all('tr', class_ = 'Table__TR Table__TR--sm Table__even')

# Placing Player Names in Data Frame #
i = 0
for player in players:
    df.at[i, 'Player Name'] = player.find('a', class_ = 'AnchorLink').text
    df.at[i, 'Team Name'] = player.find('span', class_ = 'pl2 n10 athleteCell__teamAbbrev').text
    i += 1
   
# Finding Stats #   
table_stats = soup.find('div', class_ = 'Table__ScrollerWrapper relative overflow-hidden')
stats = table_stats.find_all('tr', class_ = 'Table__TR Table__TR--sm Table__even')

# Placing Stats in Data Frame # 
i = 0
for stat in stats:
    player = stat.find_all('td', class_ = 'Table__TD')
    ppg = df.at[i, 'Points Per Game'] = float(player[3].text)
    fgm = df.at[i, 'Field Goals Made'] = float(player[4].text)
    fga = df.at[i, 'Field Goals Attempted'] = float(player[5].text)
    ftm = df.at[i, 'Free Throws Made'] = float(player[10].text)
    fta = df.at[i, 'Free Throws Attempted'] = float(player[11].text)
    tpm = df.at[i, 'Three Points Made'] = float(player[7].text)
    reb = df.at[i, 'Rebounds'] = float(player[13].text)
    ast = df.at[i, 'Assists'] = float(player[14].text)
    stl = df.at[i, 'Steals'] = float(player[15].text)
    blk = df.at[i, 'Blocks'] = float(player[16].text)
    to = df.at[i, 'Turnovers'] = float(player[17].text)
    df.at[i, 'Fantasy Points'] = ppg + fgm*2 -fga  + ftm - fta + tpm + reb + ast*2 + stl*4 + blk*4 - to*2 # Dependant on League
    i += 1

# Creating Excel File # 
df = df.sort_values('Fantasy Points', ascending = False)
excel_file = 'Basketball.xlsx'
df.to_excel(excel_file, sheet_name = 'Stats')  





