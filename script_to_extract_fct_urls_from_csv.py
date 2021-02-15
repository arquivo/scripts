import pandas as pd
import re
import argparse
from urlextract import URLExtract
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


####Examples

#If the filename is "Websites_Arquivo.xlsx" and it is in the same directory of the script_fct.py:
#Example:  python script_fct.py

#If the filename has a different name and it is not in the same directory:
#Example:  python script_fct.py -f /path/xpto.xlsx

#If you want to change the name and/or directory of the output file:
#Example:  python script_fct.py -o /path/urls.txt


###############################################################################################################

#Parameters
parser = argparse.ArgumentParser(description='Process seeds from excel')
parser.add_argument('-f','--file', help='Localization of the file (.xlsx)', default= "Websites_Arquivo.xlsx")
parser.add_argument('-o','--output', help='Localization and name of the output file', default= "urls.txt")
args = vars(parser.parse_args())

##Read inputs
file_to_process = args['file']
output_file = args['output']

##Check if the input file is a excel file. If not, it is probably necessary to change the function used (pandas).
if not file_to_process.endswith(".xlsx"):
    raise ValueError('The file needs to be .xlsx')

##Read input file into pandas
df = pd.read_excel(file_to_process)

validate = URLValidator()

def url_validator(url, file):
    try:
        validate(url)
        file.write(url + "\n")
    except ValidationError as exception:
        if not url.startswith("http") and not url.startswith("www"):
            url = "http://www." + url
            file.write(url + "\n")
        elif not url.startswith("http"):
            url = "http://" + url
            file.write(url + "\n")
        else:
            import pdb;pdb.set_trace()

#import pdb;pdb.set_trace()

##Process input file
with open(output_file, mode="a") as file:
    for i in df.index:
        websites = df.at[i, 'URL']
        extractor = URLExtract()
        ##Check if row is not null
        if not pd.isnull(websites):
            ##Extract all urls from the column "Websites"
            for url in extractor.find_urls(websites):
                #if "http://www.artis.letras.ulisboa.pt/pro" in url:
                #    import pdb;pdb.set_trace()
                if "," in url:
                    if re.match(".*,http.*|.*,www.*", url) is not None:
                        list_urls_common = url.split(",")
                        for elem in list_urls_common:
                            if elem != "":
                                url_validator(elem, file)
                    else:
                        #http://www.artis.letras.ulisboa.pt/proj_n,7,89,1293,detalhe.aspx
                        url = re.sub(",$", "", url)
                        url_validator(url, file)
                else:
                    url_validator(url, file)