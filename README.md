# LivestreamAttendance
A collection of python scripts to automatically record livestream attendance whenever the RTMP server is receiving a stream.

yt.py = This queries Youtube for our account to see if there is an active livestream, and if so, to record the number of concurrent viewers.

lambda_function.py = This function, when called, will query the CDN servers and call the yt.py script and will write the data to DynamoDb.

videostats.py = This script is run on startup for the RTMP server.  It checks once per minute for an active RTMP stream, and when present, calls our API gateway to query the servers.

dynamo.py = This script runs in a separate lambda and is called whenver the RTMP server is destroyed, so that the totals from the day's streaming sessions are emailed to IWC staff.
