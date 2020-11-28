#!/bin/env/python
import os
import time
import requests
x = 0
while x == 0:
    stream = os.popen('netstat | grep 1935')
    output = stream.read()
    if "1935" in output:
        requests.get("https://s7fv6gymxa.execute-api.us-east-1.amazonaws.com/default/record_video_sessions")
    time.sleep(10)