from lib2to3.fixes.fix_operator import invocation

import pandas as pd
import json
from datetime import datetime
from igdb.wrapper import IGDBWrapper
import pprint as pp
import time


pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', None)

# Client ID    : xds7ncmcl3m6rx9lvvr02cpc5r4zpa
# Client Secret: gz1xj7mr6l1feboioggmygx6u33q7t
# Access token : ssjwa1posopjtl56fztpabte4arb02

# POST request to get new access token
# url = 'https://id.twitch.tv/oauth2/token'
# obj = ({'client_id': 'xds7ncmcl3m6rx9lvvr02cpc5r4zpa',
#         'client_secret': 'gz1xj7mr6l1feboioggmygx6u33q7t',
#         'grant_type': 'client_credentials'})
# access_token = requests.post(url, obj)


path = 'data/'

wrapper = IGDBWrapper("xds7ncmcl3m6rx9lvvr02cpc5r4zpa", "ssjwa1posopjtl56fztpabte4arb02")

vgsales = pd.read_csv(path + 'vgsales_info.csv')
year_missing = vgsales.loc[pd.isna(vgsales['Year'])]
publ_missing = vgsales.loc[vgsales['Publisher'] == 'Unknown']

game_name = 'NHL Slapshot'
endpoint = 'games'
query = (f'fields id, genres.name, involved_companies.publisher, involved_companies.company.name, '
         f'platforms.name, first_release_date, url, parent_game; where name = "{game_name}";')
game_search_json = wrapper.api_request(endpoint,query)
game_search = json.loads(game_search_json)
release_year = datetime.fromtimestamp(game_search[0]['first_release_date']).strftime('%Y')
game_publisher = [x.get('company').get('name') for x in game_search[0]['involved_companies'] if x.get('publisher')][0]
game_url = game_search[0]['url']

print('IGDB API json response:')
pp.pp(game_search)
print(f'\n{game_name} was released by {game_publisher} in {release_year}.')
print(game_url)