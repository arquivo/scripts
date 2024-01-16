import requests
import json
import pandas as pd
import coinmarketcapapi
from string import printable
import time
import click
from pycoingecko import CoinGeckoAPI

########################################################################################################################
########################################################################################################################
########################################################################################################################

###Coingecko###
###Current not working###
#requests are hitting 429. We'll probably have to redo the code
#DOCS
#https://www.coingecko.com/api/documentation

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
        time.sleep(2)

#Transform the list into a dataframe
df = pd.DataFrame(data_coins, columns=['ID', 'Name', 'Symbol', 'URLs_HomePage', 'Categories', 'Platforms', 'Github', 'Twitter', 'Facebook', 'Reddit'])
#Convert dataframe to csv
df.to_csv('FINAL_CRYPTO_coingecko.csv', sep=';', encoding='utf-8')


########################################################################################################################
########################################################################################################################
########################################################################################################################


###Coinmarketcap###
#DOCS
#https://coinmarketcap.com/api/documentation/v1/

data_coinmarketcap = []

for start in range(1, 20000, 500):

    time.sleep(10)

    url = 'https://web-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

    params = {
        'start': start,
        'limit': 500,
    }

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'YOUR KEY'
    }

    r = requests.get(url, params=params, headers=headers)
    data = r.json()
    #print(data)

    list_symbols = []
    for item in data['data']:
        if item['symbol'].isalnum() and not set(item['symbol']).difference(printable): # remove element not alphanumeric. The API can not deal with not alphanumeric symbols #some symbols pass the isalnum
            list_symbols.append(item['symbol'])

    string_one_list = ','.join(list_symbols)

    if string_one_list != "":

        time.sleep(10)

        url = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/info"

        #parameters for the request
        parameters = {
            'symbol' : string_one_list,
            'aux' : "urls,logo,description,tags,platform,date_added"
        }

        #headers for the request
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': 'b4cbfe1d-1388-493e-8bcc-9367ee522f6e'
        }

        #Get metadata of each coin
        response = requests.get(url, params=parameters, headers=headers)
        json = response.json()
        #print(json)
        #Process json
        with click.progressbar(length=len(json['data']), show_pos=True) as progress_bar:
            print("sdfadsfdfsdf")
            for elem in json['data']:
                #import pdb;pdb.set_trace()
                progress_bar.update(1)
                
                id_coin = json['data'][elem][0]['id']
                name = json['data'][elem][0]['name']
                symbol = json['data'][elem][0]['symbol']
                description = json['data'][elem][0]['description']
                logo = json['data'][elem][0]['logo']
                date_added = json['data'][elem][0]['date_added']
                date_launched = json['data'][elem][0]['date_launched']
                
                #1. Get the the Homepages
                homepages = ""
                if json['data'][elem][0]['urls']['website'] != None: 
                    homepages = ', '.join(json['data'][elem][0]['urls']['website'])

                #2. Get the Categories
                tag_names = ""
                if json['data'][elem][0]['tag-names'] != None:
                    tag_names = ', '.join(json['data'][elem][0]['tag-names'])

                #3. Get the Platforms
                data_platform = []
                data_contract_address = []
                if json['data'][elem][0]['contract_address'] != None:
                    for elem_platform in json['data'][elem][0]['contract_address']:
                        data_platform.append(elem_platform['platform']['name'])
                    for elem_platform in json['data'][elem][0]['contract_address']:
                        data_platform.append(elem_platform['contract_address'])
                platform =  ', '.join(data_platform)
                contract_address =  ', '.join(data_platform)

                #4. Get the Github
                source_code = ""
                if json['data'][elem][0]['urls']['source_code'] != None:
                    source_code = ', '.join(json['data'][elem][0]['urls']['source_code'])

                #5. Get the Twitter
                twitter = ""
                if json['data'][elem][0]['urls']['twitter'] != None:
                    twitter = ', '.join(json['data'][elem][0]['urls']['twitter'])

                #6. Get the Facebook
                facebook = ""
                if json['data'][elem][0]['urls']['facebook'] != None:
                    facebook = ', '.join(json['data'][elem][0]['urls']['facebook'])

                #7. Get the Reddit
                reddit = ""
                if json['data'][elem][0]['urls']['reddit'] != None:
                    reddit = ', '.join(json['data'][elem][0]['urls']['reddit'])
                
                # Append the information of the coin processed
                data_coinmarketcap.append([id_coin, name, symbol, description, logo, date_added, date_launched, homepages, tag_names, contract_address, platform, source_code, twitter, facebook, reddit])

#Transform the list into a dataframe
df = pd.DataFrame(data_coinmarketcap, columns=['ID', 'Name', 'Symbol', 'Description', 'Logo', 'Date_Added', 'Date_Lauched', 'URLs_HomePage', 'Categories', 'Contract_Address', 'Platforms', 'Github', 'Twitter', 'Facebook', 'Reddit'])
#Convert dataframe to csv
df.to_csv('FINAL_CRYPTO_coinmarketcap.csv', sep=';', encoding='utf-8')

########################################################################################################################
########################################################################################################################
########################################################################################################################


###****OPENSEA.IO****###
###Current not working###
#problems getting a key. due to lack of time we moved on. We can come back to this API later.
#DOCS
#https://docs.opensea.io/reference/api-overview

#Since we have not a paid API we have limits on the URLs we can extract from the API.
#So, we make requests to 3 different endpoints to try to get as many URLs from different compoments as possible.

offset = 0
data_opensea = []
list_urls_processed = []

while True:

    #50000 is the limit (free api key)
    if offset <= 50000:

        url = "https://api.opensea.io/api/v1/collections?offset=" + str(offset) + "&limit=100"

        headers = {"Accept": "application/json"}

        response = requests.request("GET", url, headers=headers)

        json = response.json()

        for elem in json["collections"]:
            if elem["external_url"] != None:
                if (elem["external_url"], elem["name"]) not in list_urls_processed:
                    if elem["instagram_username"] != None:
                        if "https://www.instagram.com/" not in elem["instagram_username"]:
                            instagram = "https://www.instagram.com/" + elem["instagram_username"].replace("@", "")
                        else:
                            instagram = elem["instagram_username"]
                    else:
                        instagram = ""
                    data_opensea.append([elem["name"], elem["created_date"], elem["external_url"], elem["banner_image_url"], elem["description"], elem["discord_url"], elem["image_url"], elem["telegram_url"], instagram])
        
                    list_urls_processed.append((elem["external_url"], elem["name"]))
        offset += 100
        time.sleep(1)
    else:
        break

# Starting again
offset = 0

while True:

    #10000 is the limit (free api key)
    if offset <= 10000:
        url = "https://api.opensea.io/api/v1/bundles?offset=" + str(offset) + "&limit=50"

        headers = {"Accept": "application/json"}

        response = requests.request("GET", url, headers=headers)
        json = response.json()
        
        for elem in json["bundles"]:
            for asset in elem["assets"]:               
                if asset["collection"]["external_url"] != None:
                    if (asset["collection"]["external_url"], asset["collection"]["name"]) not in list_urls_processed:
                        if asset["collection"]["instagram_username"] != None:
                            if "https://www.instagram.com/" not in asset["collection"]["instagram_username"]:
                                instagram = "https://www.instagram.com/" + asset["collection"]["instagram_username"].replace("@", "")
                            else:
                                instagram = asset["collection"]["instagram_username"]
                        else:
                            instagram = ""
                        data_opensea.append([asset["collection"]["name"], asset["collection"]["created_date"], asset["collection"]["external_url"], asset["collection"]["banner_image_url"], asset["collection"]["description"], asset["collection"]["discord_url"], asset["collection"]["image_url"], asset["collection"]["telegram_url"], instagram])
                        
                        list_urls_processed.append((asset["collection"]["external_url"], asset["collection"]["name"]))
        offset += 50
        time.sleep(1)
    else:
        break

# Starting again
offset = 0

while True:

    #10000 is the limit (free api key)
    if offset <= 10000:
        url = "https://testnets-api.opensea.io/api/v1/assets?offset=" + str(offset) + "&limit=50"

        headers = {"Accept": "application/json"}

        response = requests.request("GET", url, headers=headers)
        json = response.json()
        
        for asset in elem["assets"]:               
            if asset["collection"]["external_url"] != None:
                if (asset["collection"]["external_url"], asset["collection"]["name"]) not in list_urls_processed:

                    if asset["collection"]["instagram_username"] != None:
                        if "https://www.instagram.com/" not in asset["collection"]["instagram_username"]:
                            instagram = "https://www.instagram.com/" + asset["collection"]["instagram_username"].replace("@", "")
                        else:
                            instagram = asset["collection"]["instagram_username"]
                    else:
                        instagram = ""
                    data_opensea.append([asset["collection"]["name"], asset["collection"]["created_date"], asset["collection"]["external_url"], asset["collection"]["banner_image_url"], asset["collection"]["description"], asset["collection"]["discord_url"], asset["collection"]["image_url"], asset["collection"]["telegram_url"], instagram])
                    
                    list_urls_processed.append((asset["collection"]["external_url"], asset["collection"]["name"]))
        offset += 50
        time.sleep(1)
    else:
        break

#Transform the list into a dataframe
df = pd.DataFrame(data_opensea, columns=['name','created_date', 'external_url', 'banner_image_url', 'description', 'discord_url', "image_url", "telegram_url", "instagram_username"])
#Convert dataframe to csv
df.to_csv('FINAL_opeansea.csv', sep=';', encoding='utf-8')


########################################################################################################################
########################################################################################################################
########################################################################################################################

###livecoinwatch
#simple API call to get just the URLs
#DOCS
#https://livecoinwatch.github.io/lcw-api-docs/

data_livecoinwatch = []

#livecoinwatch endpoit
url = "https://api.livecoinwatch.com/coins/list"

#payload
payload = json.dumps({
  "currency": "USD",
  "sort": "rank",
  "order": "ascending",
  "offset": 0,
  "limit": 32000,
  "meta": True
})

headers = {
  'content-type': 'application/json',
  'x-api-key': 'YOUR KEY'
}

#Get URLs
response = requests.request("POST", url, headers=headers, data=payload)
for elem in response.json():
    data_livecoinwatch.append([value for key, value in elem["links"].items() if key == 'website' and value is not None])

#Transform the list into a dataframe
df = pd.DataFrame(data_livecoinwatch, columns=['URL'])
#Convert dataframe to csv
df.to_csv('FINAL_livecoinwatch.csv', sep=';', encoding='utf-8')


########################################################################################################################
########################################################################################################################
########################################################################################################################

###nftscan
#simple API call to get just the URLs
#DOCS
#https://docs.nftscan.com/reference/evm/model/asset-model

def request_data_nftscan(url, data_nftscan, headers):
    #Get URLs
    response = requests.request("GET", url, headers=headers)
    data = response.json()['data']
    for elem in data:
        data_nftscan.append([elem['website']])

data_nftscan = []

#The nftscan API has different internal APIs for each chain\coin. 
#Thus, It is necessary to make requests to different internal APIs

headers = {
  'content-type': 'application/json',
  'X-API-KEY': 'YOUR KEY'
}

url = "https://restapi.nftscan.com/api/v2/collections/rankings?sort_field=volume_total&sort_direction=desc&limit=100000"
request_data_nftscan(url, data_nftscan, headers)

url = "https://bnbapi.nftscan.com/api/v2/collections/rankings?sort_field=volume_total&sort_direction=desc&limit=100000"
request_data_nftscan(url, data_nftscan, headers)

url = "https://polygonapi.nftscan.com/api/v2/collections/rankings?sort_field=volume_total&sort_direction=desc&limit=100000"
request_data_nftscan(url, data_nftscan, headers)

url = "https://arbitrumapi.nftscan.com/api/v2/collections/rankings?sort_field=volume_total&sort_direction=desc&limit=100000"
request_data_nftscan(url, data_nftscan, headers)

url = "https://optimismapi.nftscan.com/api/v2/collections/rankings?sort_field=volume_total&sort_direction=desc&limit=100000"
request_data_nftscan(url, data_nftscan, headers)

url = "https://zksyncapi.nftscan.com/api/v2/collections/rankings?sort_field=volume_total&sort_direction=desc&limit=100000"
request_data_nftscan(url, data_nftscan, headers)

url = "https://lineaapi.nftscan.com/api/v2/collections/rankings?sort_field=volume_total&sort_direction=desc&limit=100000"
request_data_nftscan(url, data_nftscan, headers)

url = "https://baseapi.nftscan.com/api/v2/collections/rankings?sort_field=volume_total&sort_direction=desc&limit=100000"
request_data_nftscan(url, data_nftscan, headers)

url = "https://scrollapi.nftscan.com/api/v2/collections/rankings?sort_field=volume_total&sort_direction=desc&limit=100000"
request_data_nftscan(url, data_nftscan, headers)

url = "https://starknetapi.nftscan.com/api/v2/collections/rankings?sort_field=volume_total&sort_direction=desc&limit=100000"
request_data_nftscan(url, data_nftscan, headers)

url = "https://avaxapi.nftscan.com/api/v2/collections/rankings?sort_field=volume_total&sort_direction=desc&limit=100000"
request_data_nftscan(url, data_nftscan, headers)

url = "https://fantomapi.nftscan.com/api/v2/collections/rankings?sort_field=volume_total&sort_direction=desc&limit=100000"
request_data_nftscan(url, data_nftscan, headers)

#Transform the list into a dataframe
df = pd.DataFrame(data_nftscan, columns=['URL'])
#Convert dataframe to csv
df.to_csv('FINAL_nftscan.csv', sep=';', encoding='utf-8')