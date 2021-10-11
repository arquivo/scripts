import requests
import json
import pandas as pd
import coinmarketcapapi
from string import printable
import time

#import pdb;pdb.set_trace()

#Get URLs from coingecko

# Making a get request
response = requests.get('https://api.coingecko.com/api/v3/coins/list')

# wait 10 second (not overload)
time.sleep(10)

# Get response with the list of coins
json = response.json()

list_website = [] 
with open("website.txt", "w") as file:
    for elem in json:
        
        #Get all information of each coin
        response_coin = requests.get('https://api.coingecko.com/api/v3/coins/' + elem['id'])
        json_coin = response_coin.json()

        #Get the first homepage
        file.write(json_coin['links']['homepage'][0] + "\n")

        # wait 1 second (not overload)
        time.sleep(1)

#Get URLs from coinmarketcap (API with limit request)

#Connect coinmarketcapapi
cmc = coinmarketcapapi.CoinMarketCapAPI('YOUT_KEY_COINMAKERTCAP')

#Get the map with all the symbols from coinmarketcap
data_id_map = cmc.cryptocurrency_map()

#Parse the data into a list
df = pd.DataFrame(data_id_map.data, columns =['name','symbol'])
list_symbols = df['symbol'].tolist()

#Request can't handle with too many parametrs, so we need to do 0 to 1000, 1000 to 2000 ....
list_value =[1000, 2000, 3000, 4000, 5000, 6000, len(df['symbol'].tolist())]

#list URLs from coinmarketcap
list_URLs_crypto = []

for i in range(1, len(list_value)):

    list_symbols_aux = list_symbols[list_value[i-1]:list_value[i]]
    for elem in list_symbols_aux:
        if not elem.isalnum(): # remove element not alphanumeric. The API can not deal with not alphanumeric symbols
            list_symbols_aux.remove(elem)
        elif set(elem).difference(printable): #some symbols pass the isalnum
            list_symbols_aux.remove(elem)

    #sting with the list of symbols separate with ,
    string_one_list = ','.join(list_symbols_aux)

    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/info"

    parameters = {
        'symbol' : string_one_list
    }

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'YOUT_KEY_COINMAKERTCAP'
    }

    #Get all metadata of each symbol
    response = requests.get(url, params=parameters, headers=headers)
    json = response.json()

    #Process Json result
    for elem in json['data']:
        list_URLs_crypto.append(json['data'][elem]['urls']['website'])

print(list_URLs_crypto)