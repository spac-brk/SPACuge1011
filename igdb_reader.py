import pandas as pd
import json
from datetime import datetime
from igdb.wrapper import IGDBWrapper
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


def my_func():
    return


def main():
    path = 'data/'

    wrapper = IGDBWrapper("xds7ncmcl3m6rx9lvvr02cpc5r4zpa", "ssjwa1posopjtl56fztpabte4arb02")

    vgsales = pd.read_csv(path + 'vgsales_out.csv')
    year_missing = vgsales.loc[pd.isna(vgsales['Year'])]
    publ_missing = vgsales.loc[vgsales['Publisher'] == 'Unknown']

    # for game_name in year_missing['Name']:
    game_name = 'Madden NFL 2004'
    endpoint = 'games'
    query = f'fields id, genres.name, involved_companies.publisher, platforms.name, first_release_date; where name = "{game_name}" and parent_game = null;'
    game_search_json = wrapper.api_request(endpoint,query)
    game_search = json.loads(game_search_json)
    release_year = datetime.utcfromtimestamp(game_search['first_release_date']).strftime('%Y')
    time.sleep(1)
    print('Hello World!')
    print(game_search)
    print(f'{game_name}: {release_year}')

if __name__ == '__main__':
    main()