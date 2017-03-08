#get List of unique fully qualified server names from a CDXJ index file
#!/usr/bin/python
import sys
import json
from urlparse import urlparse
from sets import Set

if (len(sys.argv) != 3):
	print "Usage: python getFQDs.py inputFile.cdxj outputfile.txt"
	exit()

inputfile = sys.argv[1]
outputfile = sys.argv[2]

uniqueUrls = Set()

outputF = open(outputfile, "w")

with open(inputfile, "r") as f:
    for line in f:
       try:
	    jsonLine = json.loads(' '.join(line.split()[2:]))
	    hostnamewww = urlparse(jsonLine['url']).hostname
	    if(hostnamewww is None):
	 	    continue
	    if(hostnamewww.startswith("www.")):
		    hostnamewww = hostnamewww[4:]
	    uniqueUrls.add(hostnamewww)
       except Exception:
           continue

for uniqueUrl in uniqueUrls:
	outputF.write(uniqueUrl+"\n");
outputF.close()

