import random
import re
import json
import requests
from bs4 import BeautifulSoup, Comment


global players
players = {}


def separate_names_and_team(name_string):
    first_name = ''
    last_name = ''
    full_name, team = name_string.split('(')
    team = team[:len(team)-1]
    names = full_name.split()
    if len(names) == 2:
        first_name = names[0]
        last_name = names[1]
    elif len(names) == 3:
        # Longer names require a bit more context - John Ryan Murphy vs. Ken Griffey Jr.
        # Functionally this has little impact at time of this comment but could later on
        # (and is just generally better for data organization)
        if names[2] in ['Jr.', 'Sr.', 'I', 'II', 'III', 'IV', 'V', 'VI']:
            first_name = names[0]
            last_name = f'{names[1]} {names[2]}'
        else:
            first_name = f'{names[0]} {names[1]}'
            last_name = names[2]
    return first_name, last_name, team


def traverse_yearly_leaders():
    # this will go through table on https://www.baseball-reference.com/leaders/ page
    page = requests.get('https://www.baseball-reference.com/leaders/')
    page_content = page.content
    soup = BeautifulSoup(page_content, 'html.parser')
    # The table I want is commented out for some reason, gotta find a way to get to it
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    table = ''
    for comment in comments:
        comment = BeautifulSoup(str(comment), 'html.parser')
        table = comment.find('table', id='leaders_index')
        if table:
            break
    table = BeautifulSoup(str(table), 'html.parser')
    links = table.find_all('a', string='Year-by-Year Top-Tens')
    for i in range(len(links)):
        parts = str(links[i]).split('\"')
        links[i] = parts[1]
    # add a [:1] to the end of next line to only test the WAR page
    for link in links:
        get_category_leaders(link)


def get_category_leaders(url_part):
    url = f'https://baseball-reference.com{url_part}'
    page = requests.get(url)
    page_content = page.content
    soup = BeautifulSoup(page_content, 'html.parser')
    category = soup.find('h1').getText()[44:]
    yearly = soup.find_all('div', id=re.compile('leaders_.*_y'))
    global players
    for box in yearly:
        year = box.find('caption').getText()
        leaders = box.find_all('tr', class_='first_place')
        for leader in leaders:
            link = leader.find('a')
            url = link['href']
            first_name, last_name, team = separate_names_and_team(link['title'])
            value = leader.find('td', class_='value').getText().strip()
            if url not in players:
                players[url] = {
                    'firstname': first_name,
                    'lastname': last_name,
                    'leads': [{
                        'category': category,
                        'value': value,
                        'year': year,
                        'team': team
                    }]
                }
            else:
                players[url]['leads'].append(
                    {
                        'category': category,
                        'value': value,
                        'year': year,
                        'team': team
                    }
                )


def save_to_json(filename):
    global players
    out_file = open(filename, 'w')
    json.dump(players, out_file)
    out_file.close()