# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
import pprint
import pickle
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import logging

logging.getLogger('googleapicliet.discovery_cache').setLevel(logging.ERROR)


SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]
CREDENTIALS_PICKLE_FILE = "token.pickle"
CLIENT_SECRETS_FILE = "client_id.json"
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

def youtube_con_viewers():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_id.json"
    if os.path.exists(CREDENTIALS_PICKLE_FILE):
        with open(CREDENTIALS_PICKLE_FILE, 'rb') as f:
            credentials = pickle.load(f)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
        credentials = flow.run_console()
        with open(CREDENTIALS_PICKLE_FILE, 'wb') as f:
            pickle.dump(credentials, f)
    youtube = build(API_SERVICE_NAME, API_VERSION, credentials = credentials, cache_discovery=False)

    request = youtube.liveBroadcasts().list(
        part="snippet,contentDetails,status",
        broadcastStatus="active",
        broadcastType="all"
    )
    response = request.execute()

    video_id = response["items"][0]["id"]

    request = youtube.videos().list(
        part="snippet,liveStreamingDetails,status", id=video_id
    )

    response = request.execute()

    return(response["items"][0]["liveStreamingDetails"]["concurrentViewers"])

