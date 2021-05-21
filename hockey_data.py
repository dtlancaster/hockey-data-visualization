# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 16:12:22 2021

@author: Dylan Lancaster
"""
import urllib.robotparser
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'}
base_url = 'https://www.quanthockey.com'
forwards_page = 'https://www.quanthockey.com/nhl/seasons/2020-21-active-nhl-forwards-stats.html'
next_forwards_page = 'https://www.quanthockey.com/scripts/AjaxPaginate.php?cat=Season&pos=Forwards&SS=2020-21&af=1&nat=2020-21&st=reg&sort=P&so=DESC&page=2&league=NHL&lang=en&rnd=814329382&dt=2&sd=undefined&ed=undefined'
defense_page = 'https://www.quanthockey.com/nhl/seasons/2020-21-active-nhl-defensemen-stats.html'
next_defense_page = 'https://www.quanthockey.com/scripts/AjaxPaginate.php?cat=Season&pos=Defensemen&SS=2020-21&af=1&nat=2020-21&st=reg&sort=P&so=DESC&page=2&league=NHL&lang=en&rnd=588854378&dt=2&sd=undefined&ed=undefined'
goaltender_page = 'https://www.quanthockey.com/nhl/seasons/2020-21-active-nhl-goalies-stats.html'
next_goaltender_page = 'https://www.quanthockey.com/scripts/AjaxPaginate.php?cat=Season&pos=Goalies&SS=2020-21&af=1&nat=2020-21&st=reg&sort=GP&so=DESC&page=2&league=NHL&lang=en&rnd=423088039&dt=1&sd=undefined&ed=undefined'
robot_url = 'https://www.quanthockey.com/robots.txt'
pages = []
forward_data = []
defense_data = []
goaltender_data = []


"""
Access the Robots.txt file to determine if we have permission to scrape the site.
"""
def get_rp(robot_url):
    r = requests.get(robot_url, headers=headers)
    rp = urllib.robotparser.RobotFileParser()
    rp.parse(r.text.split('\n'))
    print('Allow Robot to fetch robot.txt:',  rp.can_fetch('*', r.text))
    print()
    
"""
Uses RobotFileParser to access index page to determine if we have permission to scrape the page.
If we do, we return a BeautifulSoup object with the parsed html.
"""
def get_page(url):
    r = requests.get(url, headers=headers)
    rp = urllib.robotparser.RobotFileParser()
    rp.parse(r.text)
    if(rp.can_fetch('*', r.text)):
        html = requests.get(url)
        bs = BeautifulSoup(html.text, "html.parser")
        return bs
    else:
        return None
    
"""
Function to return abbrevations of NHL teams.
"""

def abbreviate_team(team):
    return {
        'Boston Bruins': 'BOS',
        'Anaheim Ducks': 'ANA',
        'Arizona Coyotes': 'ARI',
        'Carolina Hurricanes': 'CAR',
        'Buffalo Sabres': 'BUF',
        'Chicago Blackhawks': 'CHI',
        'Calgary Flames': 'CGY',
        'Dallas Stars': 'DAL',
        'New Jersey Devils': 'NJD',
        'New York Islanders': 'NYI',
        'New York Rangers': 'NYR',
        'Philadelphia Flyers': 'PHI',
        'Pittsburgh Penguins': 'PIT',
        'Washington Capitals': 'WSH',
        'Columbus Blue Jackets': 'CBJ',
        'Detroit Red Wings': 'DET',
        'Florida Panthers': 'FLA',
        'Nashville Predators': 'NSH',
        'Colorado Avalanche': 'COL',
        'Los Angeles Kings': 'LAK',
        'Minnesota Wild': 'MIN',
        'San Jose Sharks': 'SJS',
        'St. Louis Blues': 'STL',
        'Vegas Golden Knights': 'VGK',
        'Edmonton Oilers': 'EDM',
        'Montreal Canadiens': 'MTL',
        'Ottawa Senators': 'OTT',
        'Toronto Maple Leafs': 'TOR',
        'Vancouver Canucks': 'VAN',
        'Winnipeg Jets': 'WPG',
        'Tampa Bay Lightning': 'TBL'
        }[team]

"""
Function utilizing RegEx to collect all internal links of desired item pages.
"""
def recompile(page_name):
    x = re.compile('^(/hockey-stats/en/profile)')
    for links in get_page(page_name).find_all("a", href = x):
        if "href" in links.attrs:
            internal_link = links.attrs["href"]
            pages.append(internal_link)
    for i in range(len(pages)):
        pages[i] = pages[i][:13] + '-nhl' + pages[i][13:]

"""
Function to parse HTML of forward page and append desired attributes to a list.
"""
def get_forward_attributes(num):
    for i in range(num):
        n = get_page(base_url + pages[i])
        lname = n.select_one("h1[id=pp_title]").text.split(' ')[1]
        if lname == 'van':
            lname = 'van Riemsdyk'
        elif lname == 'Di':
            lname = 'Di Giuseppe'
        elif lname == 'de':
            lname = 'de Leo'
        fname = n.select_one("h1[id=pp_title]").text.split(' ')[0]
        table = n.find('table', id='r_stats')
        table = table('tr')[-2]
        age = table('td')[0].text
        height = n.find(id="player-bio").contents[8].split('(')[0].replace(" ", "")
        weight = n.find(id="player-bio").contents[8].split(' ')[6].replace(" ", "")
        team = table('td')[2].text
        abbr = abbreviate_team(team)
        gp = table('td')[3].text
        g = table('td')[4].text
        a = table('td')[5].text
        p = table('td')[6].text
        toi = table('td')[9].text
        hits = table('td')[43].text
        pim = table('td')[7].text
        pm = table('td')[8].text

        print("Last Name: " + lname)
        print("First Name: " + fname)
        print("Age: " + age)
        print("Height: " + height)
        print("Weight: " + weight)
        print("Team: " + team)
        print("Abbr: " + abbr)
        print("GP: " + gp)
        print("G: " + g)
        print("A: " + a)
        print("P: " + p)
        print("TOI: " + toi)
        print("Hits: " + hits)
        print("PIM: " + pim)
        print("+/-: " + pm + '\n')
    
        forward_data.append({'Last Name':lname, 'First Name':fname, 'Age':age, 'Height':height, 'Weight':weight,
                             'Team':team, 'Abbr':abbr, 'GP':gp, 'G':g, 'A':a, 'P':p, 'TOI':toi, 'Hits':hits, 'PIM':pim, '+/-':pm})

"""
Function to parse HTML of defenseman page and append desired attributes to a list.
"""
def get_defense_attributes(num):
    for i in range(num):
        n = get_page(base_url + pages[i])
        lname = n.select_one("h1[id=pp_title]").text.split(' ')[1]
        if lname == 'Del':
            lname = 'Del Zotto'
        elif lname == 'de':
            lname = 'de Haan'
        elif lname == 'Van':
            lname = 'van Riemsdyk'
        fname = n.select_one("h1[id=pp_title]").text.split(' ')[0]
        table = n.find('table', id='r_stats')
        table = table('tr')[-2]
        age = table('td')[0].text
        height = n.find(id="player-bio").contents[8].split('(')[0].replace(" ", "")
        weight = n.find(id="player-bio").contents[8].split(' ')[6].replace(" ", "")
        team = table('td')[2].text
        abbr = abbreviate_team(team)
        gp = table('td')[3].text
        g = table('td')[4].text
        a = table('td')[5].text
        p = table('td')[6].text
        toi = table('td')[9].text
        hits = table('td')[43].text
        pim = table('td')[7].text
        pm = table('td')[8].text
        
        print("Last Name: " + lname)
        print("First Name: " + fname)
        print("Age: " + age)
        print("Height: " + height)
        print("Weight: " + weight)
        print("Team: " + team)
        print("Abbr: " + abbr)
        print("GP: " + gp)
        print("G: " + g)
        print("A: " + a)
        print("P: " + p)
        print("TOI: " + toi)
        print("Hits: " + hits)
        print("PIM: " + pim)
        print("+/-: " + pm + '\n')
        
        defense_data.append({'Last Name':lname, 'First Name':fname, 'Age':age, 'Height':height, 'Weight':weight, 
                             'Team':team, 'Abbr':abbr, 'GP':gp, 'G':g, 'A':a, 'P':p, 'TOI':toi, 'Hits':hits, 'PIM':pim, '+/-':pm})


"""
Function to parse HTML of goaltender page and append desired attributes to a list.
"""
def get_goaltender_attributes(num):
    for i in range(num):
        n = get_page(base_url + pages[i])
        lname = n.select_one("h1[id=pp_title]").text.split(' ')[1]
        fname = n.select_one("h1[id=pp_title]").text.split(' ')[0]
        table = n.find('table', id='p_stats')
        table = table('tr')[-2]
        age = table('td')[0].text
        height = n.find(id="player-bio").contents[8].split('(')[0].replace(" ", "")
        weight = n.find(id="player-bio").contents[8].split(' ')[6].replace(" ", "")
        team = table('td')[2].text
        abbr = abbreviate_team(team)
        gp = table('td')[3].text
        gaa = table('td')[4].text
        sv_pctg = table('td')[5].text
        ga = table('td')[8].text
        sv = table('td')[9].text
        so = table('td')[11].text
        
        print('Last Name: ' + lname)
        print("First Name: " + fname)
        print("Age: " + age)
        print("Height: " + height)
        print("Weight: " + weight)
        print("Team: " + team)
        print("Abbr: " + abbr)
        print("GP: " + gp)
        print("GAA: " + gaa)
        print("SV%: " + sv_pctg)
        print("GA: " + ga)
        print("SV: " + sv)
        print("SO: " + so + '\n')
        
        goaltender_data.append({'Last Name':lname, 'First Name':fname, 'Age':age, 'Height':height, 'Weight':weight, 
                                'Team':team, 'Abbr':abbr, 'GP':gp, 'GAA':gaa, 'SV%':sv_pctg, 'GA':ga, 'SV':sv, 'SO':so})


"""
Function to recompile internal links and return attributes from Forwards.
"""
def get_forward_data(url):
    recompile(url)
    get_forward_attributes(len(pages))

"""
Function to recompile internal links and return attributes from Defensemen.
"""
def get_defense_data(url):
    recompile(url)
    get_defense_attributes(len(pages))

"""
Function to recompile internal links and return attributes from Goaltenders.
"""
def get_goaltender_data(url):
    recompile(url)
    get_goaltender_attributes(len(pages))
   

get_rp(robot_url)

print('Getting Forward Data...\n')
get_forward_data(forwards_page)
pages.clear()
get_forward_data(next_forwards_page)
pages.clear()
next_forwards_page = next_forwards_page.replace('page=2', 'page=3')
get_forward_data(next_forwards_page)
pages.clear()
next_forwards_page = next_forwards_page.replace('page=3', 'page=4')
get_forward_data(next_forwards_page)
pages.clear()
next_forwards_page = next_forwards_page.replace('page=4', 'page=5')
get_forward_data(next_forwards_page)
pages.clear()
next_forwards_page = next_forwards_page.replace('page=5', 'page=6')
get_forward_data(next_forwards_page)
pages.clear()
next_forwards_page = next_forwards_page.replace('page=6', 'page=7')
get_forward_data(next_forwards_page)
pages.clear()
next_forwards_page = next_forwards_page.replace('page=7', 'page=8')
get_forward_data(next_forwards_page)
pages.clear()
next_forwards_page = next_forwards_page.replace('page=8', 'page=9')
get_forward_data(next_forwards_page)
pages.clear()
next_forwards_page = next_forwards_page.replace('page=9', 'page=10')
get_forward_data(next_forwards_page)
pages.clear()
next_forwards_page = next_forwards_page.replace('page=10', 'page=11')
get_forward_data(next_forwards_page)
pages.clear()
next_forwards_page = next_forwards_page.replace('page=11', 'page=12')
get_forward_data(next_forwards_page)
pages.clear()
print('Total Forward Data Entries: ' + str(len(forward_data)) + '\n')

print('Getting Defensemen Data...\n')
get_defense_data(defense_page)
pages.clear()
get_defense_data(next_defense_page)
pages.clear()
next_defense_page = next_defense_page.replace('page=2', 'page=3')
get_defense_data(next_defense_page)
pages.clear()
next_defense_page = next_defense_page.replace('page=3', 'page=4')
get_defense_data(next_defense_page)
pages.clear()
next_defense_page = next_defense_page.replace('page=4', 'page=5')
get_defense_data(next_defense_page)
pages.clear()
next_defense_page = next_defense_page.replace('page=5', 'page=6')
get_defense_data(next_defense_page)
pages.clear()
next_defense_page = next_defense_page.replace('page=6', 'page=7')
get_defense_data(next_defense_page)
pages.clear()
print('Total Defensemen Data Entries: ' + str(len(defense_data)) + '\n')

print('Getting Goaltender Data...\n')
get_goaltender_data(goaltender_page)
pages.clear()
get_goaltender_data(next_goaltender_page)
print('Total Goaltender Data Entries: ' + str(len(goaltender_data)) + '\n\n')

print('TOTAL DATA ENTRIES: ' + str(len(forward_data) + len(defense_data) + len(goaltender_data)))


forward_df = pd.DataFrame(forward_data)
forward_df = forward_df.to_csv('forward_data.csv', index = False)
defense_df = pd.DataFrame(defense_data)
defense_df = defense_df.to_csv('defense_data.csv', index = False)
goalie_df = pd.DataFrame(goaltender_data)
goalie_df = goalie_df.to_csv('goaltender_data.csv', index = False)
