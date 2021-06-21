import pdftotext
import pdfplumber
import tika
from tika import parser
import fitz

from urlextract import URLExtract
import xurls

import re


##Font
##https://stackoverflow.com/questions/55767511/how-to-extract-text-from-pdf-in-python-3-7
##https://macxima.medium.com/python-extracting-urls-from-strings-21dc82e2142b


"""
List Problems? maybe?
--> https://www.nytimes.com/2017/11/20/\n   h.html
--> sfsdfhttp://lanic.utexas.edu/
"""

#import pdb;pdb.set_trace()

## Global list with all the URLs from PDFs
list_urls_output = []

### 1. pdftotext
##https://www.xpdfreader.com/pdftotext-man.html

print("################          pdftotext        ##########################")

# Load PDF
with open("./PDF/Gomes.pdf", "rb") as f:
    pdf = pdftotext.PDF(f)


text = "\t\t".join(pdf)
text = re.sub('\n +','', text)

#URLExtract
extractor = URLExtract()
urls = extractor.find_urls(text)
for url in urls:
    url = url.replace(",", "")
    if "http" in url:
        url = url[url.find('http'):]
    if url not in list_urls_output:
        list_urls_output.append(url)

#xurls
extractor = xurls.Strict()
urls = extractor.findall(text)
for url in urls:
    url = url.replace(",", "")
    if "http" in url:
        url = url[url.find('http'):]
    if url not in list_urls_output:
        list_urls_output.append(url)


### 2. pdfplumber

print("################          pdfplumber               ##########################")

## Very good, no encoding problems, with separator (it's not as good visually as pdftotext, but it's better for manipulating the text which is what we want)
## Problems with page numbers, paragraphs with dots.

# Load PDF
pdf = pdfplumber.open('./PDF/Gomes.pdf')
text = ""
for i in range(0, len(pdf.pages)-1):
    page = pdf.pages[i]
    text += str(page.extract_text())#.replace('\n','')

#URLExtract
extractor = URLExtract()
urls = extractor.find_urls(text)
for url in urls:
    url = url.replace(",", "")
    if "http" in url:
        url = url[url.find('http'):]
    if url not in list_urls_output:
        list_urls_output.append(url)

#xurls
extractor = xurls.Strict()
urls = extractor.findall(text)
for url in urls:
    url = url.replace(",", "")
    if "http" in url:
        url = url[url.find('http'):]
    if url not in list_urls_output:
        list_urls_output.append(url)


### 3. Tika

print("################          TIKA               ##########################")

## We need to execute the tika-server-1.25.jar

tika.initVM()

# Load PDF
rawText = parser.from_file('./PDF/Gomes.pdf')

text = rawText['content'].replace('\n','')
text = ' '.join(text.split())

#URLExtract
extractor = URLExtract()
urls = extractor.find_urls(text)
for url in urls:
    url = url.replace(",", "")
    if "http" in url:
        url = url[url.find('http'):]
    if url not in list_urls_output:
        list_urls_output.append(url)

#xurls
extractor = xurls.Strict()
urls = extractor.findall(text)
for url in urls:
    url = url.replace(",", "")
    if "http" in url:
        url = url[url.find('http'):]
    if url not in list_urls_output:
        list_urls_output.append(url)


### 4. fitz

print("################          fitz               ##########################")

# Load PDF
with fitz.open('./PDF/Gomes.pdf') as doc:
    text = ""
    for page in doc:
        text += page.getText().strip()#.replace("\n", "")

text = ' '.join(text.split())

# or? Which is the best?
#text = text.replace('.\n','. ')
#text = text.replace('\n','')
#text = ' '.join(text.split())

#URLExtract
extractor = URLExtract()
urls = extractor.find_urls(text)
for url in urls:
    url = url.replace(",", "")
    if "http" in url:
        url = url[url.find('http'):]
    if url not in list_urls_output:
        list_urls_output.append(url)

#xurls
extractor = xurls.Strict()
urls = extractor.findall(text)
for url in urls:
    url = url.replace(",", "")
    if "http" in url:
        url = url[url.find('http'):]
    if url not in list_urls_output:
        list_urls_output.append(url)


print(list_urls_output)