import argparse
import os

from azure.cognitiveservices.search.websearch import WebSearchAPI
from msrest.authentication import CognitiveServicesCredentials

SUBSCRIPTION_KEY_ENV_NAME = "AZURE_KEY"

parser = argparse.ArgumentParser(description="Bing WebSearch API v7")
parser.add_argument(dest='queries_list_file', nargs='?', default="queries_list.txt",
                    help="File with list of queries to be performed.")
parser.add_argument(dest='results_file', nargs='?', default="query_results.csv", help="Csv file to write out results.")

args = parser.parse_args()

subscription_key = os.environ[SUBSCRIPTION_KEY_ENV_NAME]

client = WebSearchAPI(CognitiveServicesCredentials(subscription_key))

with open(args.queries_list_file, mode='r') as input_file:
    for line in input_file:
        print("Querying for: {}".format(line))
        try:
            web_data = client.web.search(query=line, count=10)

            if web_data.web_pages.value:
                print("Webpage Results #{}".format(len(web_data.web_pages.value)))

                with open(args.results_file, mode='a') as output_file:
                    for result in web_data.web_pages.value:
                        print("Writing result: {}".format(result.url))
                        output_file.write("{},{},{}\n".format(line, result.name, result.url))

        except Exception as err:
            print("Exception {}".format(err))
