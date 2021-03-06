# virtualenv -p python3 venv
# . venv/bin/activate
# pip install azure
# pip install azure-cognitiveservices-search-websearch
#
# 
# AZURE_KEY=xxxxxxxxxxxxxxxxxxxx python ../bing_search.py queries_list.txt query_results.tsv 20
#

import argparse
import os
import time

# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from azure.cognitiveservices.search.websearch import WebSearchAPI
from msrest.authentication import CognitiveServicesCredentials

parser = argparse.ArgumentParser(description="Bing WebSearch API v7")
parser.add_argument(dest='queries_list_file', nargs='?', default="queries_list.txt",
                    help="File with list of queries to be performed.")
parser.add_argument(dest='results_file', nargs='?', default="query_results.tsv", help="Tsv file to write out results.")
parser.add_argument(dest='results_number', nargs='?', type=int, default=20, help="Number of results returned (max=50)")
parser.add_argument(dest='subscription_key_env_name', nargs='?', default="AZURE_KEY",
                    help="Environment variable with Bing Service Subscription Key")

args = parser.parse_args()

subscription_key = os.environ[args.subscription_key_env_name]

client = WebSearchAPI(CognitiveServicesCredentials(subscription_key))

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
