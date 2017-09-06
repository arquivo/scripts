import os
import sys
import gzip
import re


'''
LogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-agent}i\"" combined
	%h is the remote host (ie the client IP)
	%l is the identity of the user determined by identd (not usually used since not reliable)
	%u is the user name determined by HTTP authentication
	%t is the time the request was received.
	%r is the request line from the client. ("GET / HTTP/1.0")
	%>s is the status code sent from the server to the client (200, 404 etc.)
	%b is the size of the response to the client (in bytes)
	Referer is the Referer header of the HTTP request (containing the URL of the page from which this request was initiated) if any is present, and "-" otherwise.
	User-agent is the browser identification string.
'''
if __name__ == '__main__':
	
	pathRead  = '/data/logs2017/'
	pathWrite = '/data/AutomaticAccess2017.txt'
	#pathWrite = '/data/WrongUrl2016'
	pathWriteBot = '/data/Googlebot2Q-2017.txt'
	regex = '([(\d\.)]+) - - \[(.*?)\] "(.*?)" (\d+) (.*?) "(.*?)" "(.*?)"'

	fw = open( pathWrite, 'w' )
	fwBot = open( pathWriteBot, 'w' )
	counterGlobal 		= 0
	counterOpensearch 	= 0
	counterMemento 		= 0
	counterMementoAPI	= 0
	counterNoMatch 		= 0
	counterWrongUrl		= 0
	countertGoogleBot	= 0
	pastDate 			= ''
	userAgents 			= [ ]
	countertXmlQuery	= 0
	boolTest			= 0
	nagiosCounter		= 0
	wrongsUrlList		= [ ]

	for filename in os.listdir( pathRead ):
		try:
			with gzip.open( pathRead + filename , 'rb' ) as f:
				for line in f:
					
					#print counterGlobal
					Result = re.match( regex , line )
					if Result:
						counterGlobal += 1
						boolTest = 0
						#print Result.groups( )[ 2 ]
						refer 			= Result.groups( )[ 4 ]
						ip 				= Result.groups( )[ 0 ]
						code 			= Result.groups( )[ 3 ]
						data 			= Result.groups( )[ 1 ]
						resource 		= Result.groups( )[ 2 ].split( )
						
						if len( Result.groups( ) ) == 7:
							userAgent 		= Result.groups( )[ 6 ]
						else:
							userAgent = "-"
							print " UserAgent error [{0}]".format( Result.groups( ) )

						if len( resource ) == 3 :
							typeofRequest 	= resource[ 0 ]
							resourceRequest = resource[ 1 ]
						else:
							continue

						if "/wayback/id" in resourceRequest:
							if not ip.startswith( "193.136." ):
								#print resourceRequest , data , line
								#fw.write( "{0} {1}\n".format( resourceRequest , data ) )
								wrongsUrlList.append( resourceRequest )
								counterWrongUrl += 1
								boolTest = 1

						if "opensearch?query=" in resourceRequest:
							if not ip.startswith( "193.136." ):
								counterOpensearch += 1
								boolTest = 1

						if 'TimeTravelAggregator-lanl;Browser - timetravel' in userAgent  or 'memgator' in userAgent.lower( ):
							counterMemento += 1
							boolTest = 1
						
						if "/wayback/timemap/*/" in resourceRequest:
							counterMementoAPI += 1
							boolTest = 1

						if "googlebot" in userAgent.lower( ):
							countertGoogleBot += 1
							boolTest = 1
						
						if '/wayback/wayback/xmlqueryhttp:' in resourceRequest:
							countertXmlQuery += 1
							boolTest = 1

						if 'nagios-plugins' in userAgent:
							nagiosCounter += 1
							boolTest = 1

						#if boolTest == 0:
							#print "refer[{0}] ip[{1}] code[{2}] data[{3}] resource[{4}] user-agent[{5}]\n\n".format( refer, ip, code, data, resource, userAgent )
						

				print "{0} {1}".format( filename[8:18], countertGoogleBot )
				fwBot.write( "{0} {1}\n".format( filename[8:18], countertGoogleBot ) )
				countertGoogleBot = 0
					
					#else:
						#print "Don't Match!!! = {0}".format( line )						
						


		except ( OSError , IOError ) as e:
			print( "Wrong file or file path" )

	wrongsUrlSet = set( wrongsUrlList )
	print wrongsUrlSet

	print "Number of Requests Memento = [{0}] MementoAPI[{1}] OpenSearch = [{2}] counterWrongUrl = [{3}] countertXmlQuery[{4}] nagios[{5}] total[{6}] ".format( counterMemento , counterMementoAPI , counterOpensearch , counterWrongUrl , countertXmlQuery , nagiosCounter , counterGlobal )
	fw.write( "Number of Requests Memento = [{0}] MementoAPI[{1}] OpenSearch = [{2}] countertXmlQuery[{3}] nagios[{4}] total[{5}]".format( counterMemento , counterMementoAPI , counterOpensearch , countertXmlQuery , nagiosCounter , counterGlobal ) )
	fw.close( )
	fwBot.close( )

