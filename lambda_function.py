#!/bin/env/python
import requests
import pprint
import boto3
import json
from datetime import datetime
from yt import *
from boto3.dynamodb.conditions import Key
import logging

logging.getLogger('googleapicliet.discovery_cache').setLevel(logging.ERROR)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('iwclivestream_stats')





def lambda_handler(event, context):
    now = datetime.now()
    dt_string = now.strftime("%m-%d-%Y %H:%M:%S")
    date = now.strftime("%m-%d-%Y")
    print(now)
    connections = requests.get("http://nj.cdn.ironworkschurch.com/nginx_status_json")
    nj_connections = connections.json()
    connections = requests.get("http://nyc.cdn.ironworkschurch.com/nginx_status_json")
    ny_connections = connections.json()
    try:
        yt_connections = youtube_con_viewers()
    except:
        yt_connections = 0
    
    total_connections = nj_connections["connections_active"] + ny_connections["connections_active"] + int(yt_connections) - 2
    print(total_connections)


    if total_connections > 3:
        entry = {"datetime": dt_string, "date": date, "nj": nj_connections["connections_active"] - 1, "ny": ny_connections["connections_active"] - 1, "YouTube": int(yt_connections), "Total": int(total_connections)}
        table.put_item(Item = entry)
    return {
        'statusCode': 200,
        'body': json.dumps("Completed")
    }
lambda_handler("test", "test")


