# virtualenv -p python3 venv
# . venv/bin/activate
#
# pip install azure-cognitiveservices-search-websearch
#
# 
# AZURE_KEY=xxxxxxxxxxxxxxxxxxxx python ../bing_search.py queries_list.txt query_results.tsv 20
#

import argparse
import os
import time

from azure.cognitiveservices.search.websearch import WebSearchClient
from msrest.authentication import CognitiveServicesCredentials

parser = argparse.ArgumentParser(description="Bing WebSearch API v7")
parser.add_argument('queries_list_file', help="File with list of queries to be performed. (ex: queries_list.txt)")
parser.add_argument('-rf', dest='results_file', default="query_results.tsv", help="Tsv file to write out results. (query_results.tsv)")
parser.add_argument('-n', dest='results_number', type=int, default=20, help="Number of results returned (max=50). (20)")
parser.add_argument('-s', dest='subscription_key_env_name', default="AZURE_KEY",
                    help="Environment variable with Bing Service Subscription Key. (AZURE_KEY)")
parser.add_argument('-e', dest='endpoint', default="https://seeds-search.cognitiveservices.azure.com/", help="URL to your Azure Cognitive Service. (https://seeds-search.cognitiveservices.azure.com/)")

args = parser.parse_args()

subscription_key = os.environ[args.subscription_key_env_name]

client = WebSearchClient(endpoint=args.endpoint, credentials=CognitiveServicesCredentials(subscription_key))

with open(args.queries_list_file, mode='r') as input_file:
    for line in input_file:
        query = line.rstrip()
        print("Querying for: {}".format(query))
        try:
            web_data = client.web.search(query=query, count=args.results_number)

            if web_data.web_pages.value:
                print("Webpage Results #{}".format(len(web_data.web_pages.value)))

                with open(args.results_file, mode='a') as output_file:
                    for i,result in enumerate(web_data.web_pages.value):
                        print("Writing result: {}".format(result.url))
                        output_file.write("{}\t{}\t{}\t{}\n".format(query, i+1, result.name, result.url))

        except Exception as err:
            print("Exception {}".format(err))
            
        time.sleep(1)
