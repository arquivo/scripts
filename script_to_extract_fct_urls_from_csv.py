import pandas as pd
import re
import argparse

####Examples

#If the filename is "Websites_Arquivo.xlsx" and it is in the same directory of the script_fct.py:
#Example:  python script_fct.py

#If the filename has a different name and it is not in the same directory:
#Example:  python script_fct.py -f /path/xpto.xlsx

#If you want to change the name and/or directory of the output file:
#Example:  python script_fct.py -o /path/urls.txt


###############################################################################################################

#Parameters
parser = argparse.ArgumentParser(description='Process seeds FCT project')
parser.add_argument('-f','--file', help='Localization of the file (.xlsx)', default= "Websites_Arquivo.xlsx")
parser.add_argument('-o','--output', help='Localization and name of the output file', default= "urls_fct.txt")
args = vars(parser.parse_args())

##Read inputs
file_to_process = args['file']
output_file = args['output']

##Check if the input file is a excel file. If not, it is probably necessary to change the function used (pandas).
if not file_to_process.endswith(".xlsx"):
    raise ValueError('The file needs to be .xlsx')

##Read input file into pandas
df = pd.read_excel(file_to_process)

##Process input file
with open(output_file, "w") as file:
    for i in df.index:
        websites = df.at[i, 'Websites']
        ##Check if row is not null
        if not pd.isnull(websites):
        	##Extract all urls from the column "Websites"
            for url in re.findall('(https?://\S+)', websites):
                url = url.replace(";", "")
                url = url.replace(",", "")
                file.write(url + "\n")
