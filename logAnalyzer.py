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
	
	pathRead  = '/data/logs2016-apache/apache_logs_2016/'
	#pathWrite = '/data/AutomaticAccess2016.txt'
	pathWrite = '/data/WrongUrl2016'
	regex = '([(\d\.)]+) - - \[(.*?)\] "(.*?)" (\d+) (.*?) "(.*?)" "(.*?)"'

	fw = open( pathWrite, 'w')
	counterGlobal 		= 0
	counterOpensearch 	= 0
	counterMemento 		= 0
	counterNoMatch 		= 0
	counterWrongUrl		= 0
	pastDate 			= ''
	userAgents 			= [ ]
	for filename in os.listdir( pathRead ):
		#print filename
		try:
			with gzip.open( pathRead + filename , 'rb' ) as f:
			    for line in f:
			    	counterGlobal += 1
			    	#print counterGlobal
			    	Result = re.match( regex , line )
			    	if Result:
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

						if "opensearch?query=" in resourceRequest:
							if not ip.startswith( "193.136." ):
								counterOpensearch += 1

						if 'TimeTravelAggregator-lanl;Browser - timetravel' in userAgent  or 'memgator' in userAgent.lower( ):
							counterMemento += 1
						
						
						if "/wayback/id" in resourceRequest:
							print resourceRequest , data , line
							fw.write( "{0} {1}\n".format( resourceRequest , data ) )
							counterWrongUrl += 1
					else:
			    	#	print "Error, no match [{0}]".format( line )
			    		counterNoMatch += 1

		except ( OSError , IOError ) as e:
			print( "Wrong file or file path" )

	print "Number of Requests Memento = [{0}] OpenSearch = [{1}] counterWrongUrl = [{2}] total[{3}] sirens.fccn.pt[{4}]".format( counterMemento , counterOpensearch , counterWrongUrl , counterGlobal , counterNoMatch )
	#fw.write( "Number of Requests Memento = [{0}] OpenSearch = [{1}] total[{2}]".format( counterMemento , counterOpensearch , counterGlobal ) )
	fw.close( )

