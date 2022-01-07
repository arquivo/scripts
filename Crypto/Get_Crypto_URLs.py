import requests
import json
import pandas as pd
import coinmarketcapapi
from string import printable
import time
import click
from pycoingecko import CoinGeckoAPI

### Get data from coingecko.com
cg = CoinGeckoAPI()
data = cg.get_coins_list()

#List to add each entrie of each coin
data_coins = []

with click.progressbar(length=len(data), show_pos=True) as progress_bar:
    for elem in data:
        progress_bar.update(1)
        json_coin = cg.get_coin_by_id(id=elem['id'])
        
        #1. Get the the Homepages
        data_homepage = []
        if json_coin['links']['homepage'] != []:
            for homepage in json_coin['links']['homepage']:
                if homepage != "":
                    data_homepage.append(homepage)
        data_homepage = [x for x in data_homepage if x is not None]

        #2. Get the Categories
        data_categories = []
        if json_coin['categories'] != []:
            for categories in json_coin['categories']:
                if categories != "" and categories != None:
                    data_categories.append(categories)
        data_categories = [x for x in data_categories if x is not None]

        #3. Get the Platforms
        data_platforms = list(json_coin['platforms'].keys())
        data_platforms = [x for x in data_platforms if x is not None]

        #4. Get the Github
        data_github = []
        if json_coin['links']['repos_url']['github'] != []:
            for github in json_coin['links']['repos_url']['github']:
                if github != "":
                    data_github.append(github)
        data_github = [x for x in data_github if x is not None]

        #5. Get the Twitter
        data_twitter = ""
        ## Check if the value is not None and empty
        if json_coin['links']['twitter_screen_name'] != None and json_coin['links']['twitter_screen_name'] != '':
            data_twitter = 'https://twitter.com/' + json_coin['links']['twitter_screen_name']

        #6. Get the Facebook
        data_facebook = ""
        ## Check if the value is not None and empty
        if json_coin['links']['facebook_username'] != None and json_coin['links']['facebook_username'] != '':
            data_facebook = 'https://facebook.com/' + json_coin['links']['facebook_username']

        #7. Get the Reddit
        data_reddit = ""
        ## Check if the value is not None and empty
        if json_coin['links']['subreddit_url'] != None and json_coin['links']['subreddit_url'] != '':
            data_reddit = json_coin['links']['subreddit_url']
        
        # Append the information of the coin processed
        data_coins.append([json_coin['id'], json_coin['name'], json_coin['symbol'], ', '.join(data_homepage), ', '.join(data_categories), ', '.join(data_platforms), ', '.join(data_github), data_twitter, data_facebook, data_reddit])
        
        # wait 1 second (not overload)
        time.sleep(1)

#Transform the list into a dataframe
df = pd.DataFrame(data_coins, columns=['ID', 'Name', 'Symbol', 'URLs_HomePage', 'Categories', 'Platforms', 'Github', 'Twitter', 'Facebook', 'Reddit'])
#Convert dataframe to csv
df.to_csv('FINAL_CRYPTO_coingecko.csv', sep=';', encoding='utf-8')

######################################################################################################################################################
######################################################################################################################################################

#Get URLs from coinmarketcap.com (API with limit request)

#Connect coinmarketcap api
cmc = coinmarketcapapi.CoinMarketCapAPI('YOUT_KEY_COINMAKERTCAP')

#Get the map with all the symbols from coinmarketcap
data_id_map = cmc.cryptocurrency_map()

#Parse the data into a list
df = pd.DataFrame(data_id_map.data, columns =['name','symbol'])
list_symbols = df['symbol'].tolist()

#Request can't handle with too many parametrs, so we need to do 0 to 1000, 1000 to 2000 ....
#Attention we need to go from 0 to len(df['symbol'].tolist()) 1000 each time. We may need to update the list_value if len(df['symbol'].tolist()) is to large
list_value =[1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, len(df['symbol'].tolist())]

#List to add each entrie of each coin
data_coinmarketcap = []

for i in range(1, len(list_value)):

    list_symbols_aux = list_symbols[list_value[i-1]:list_value[i]]
    for elem in list_symbols_aux:
        if not elem.isalnum(): # remove element not alphanumeric. The API can not deal with not alphanumeric symbols
            list_symbols_aux.remove(elem)
        elif set(elem).difference(printable): #some symbols pass the isalnum
            list_symbols_aux.remove(elem)

    #sting with the list of symbols
    string_one_list = ','.join(list_symbols_aux)

    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/info"

    #parameters for the request
    parameters = {
        'symbol' : string_one_list
    }

    #headers for the request
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'YOUT_KEY_COINMAKERTCAP'
    }

    #Get metadata of each coin
    response = requests.get(url, params=parameters, headers=headers)
    json = response.json()

    #Process json
    for elem in json['data']:
        
        id_coin = json['data'][elem]['id']
        name = json['data'][elem]['name']
        symbol = json['data'][elem]['symbol']
        
        #1. Get the the Homepages
        homepages = ""
        if json['data'][elem]['urls']['website'] != None: 
            homepages = ', '.join(json['data'][elem]['urls']['website'])

        #2. Get the Categories
        tag_names = ""
        if json['data'][elem]['tag-names'] != None:
            tag_names = ', '.join(json['data'][elem]['tag-names'])

        #3. Get the Platforms
        data_platform = []
        if json['data'][elem]['contract_address'] != None:
            for elem_platform in json['data'][elem]['contract_address']:
                data_platform.append(elem_platform['platform']['name'])
        platform =  ', '.join(data_platform)

        #4. Get the Github
        source_code = ""
        if json['data'][elem]['urls']['source_code'] != None:
            source_code = ', '.join(json['data'][elem]['urls']['source_code'])

        #5. Get the Twitter
        twitter = ""
        if json['data'][elem]['urls']['twitter'] != None:
            twitter = ', '.join(json['data'][elem]['urls']['twitter'])

        #6. Get the Facebook
        facebook = ""
        if json['data'][elem]['urls']['facebook'] != None:
            facebook = ', '.join(json['data'][elem]['urls']['facebook'])

        #7. Get the Reddit
        reddit = ""
        if json['data'][elem]['urls']['reddit'] != None:
            reddit = ', '.join(json['data'][elem]['urls']['reddit'])
        
        # Append the information of the coin processed
        data_coinmarketcap.append([id_coin, name, symbol, homepages, tag_names, platform, source_code, twitter, facebook, reddit])

#Transform the list into a dataframe
df = pd.DataFrame(data_coinmarketcap, columns=['ID', 'Name', 'Symbol', 'URLs_HomePage', 'Categories', 'Platforms', 'Github', 'Twitter', 'Facebook', 'Reddit'])
#Convert dataframe to csv
df.to_csv('FINAL_CRYPTO_coinmarketcap.csv', sep=';', encoding='utf-8')