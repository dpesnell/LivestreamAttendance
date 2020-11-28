#!/bin/env/python
import json
import boto3
from boto3.dynamodb.conditions import Key
from datetime import datetime

def total_numbers(response, site):
    total = 0
    for i in response["Items"]:
        if int(i[site]) > total:
            total = int(i[site])
    return(total)

def lambda_handler(event, context):
    ssm = boto3.client('ssm')
    sns = boto3.client('sns')
    sns_topic = ssm.get_parameter(Name='sns_iwc_staff')["Parameter"]["Value"]
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('iwclivestream_stats')
    now = datetime.now()


    dt_string = now.strftime("%m-%d-%Y %H:%M:%S")
    date = now.strftime("%m-%d-%Y")


    response = table.query(
            KeyConditionExpression=Key('date').eq(date)
        )
    nj = total_numbers(response, "nj")
    ny = total_numbers(response, "ny")
    yt = total_numbers(response, "YouTube")
    total = total_numbers(response, "Total")
    sns.publish(TopicArn=sns_topic, Message=("NJ: " + str(nj) + " NY: " + str(ny) + " YouTube: " + str(yt) + " Total: " + str(total)))
lambda_handler("test", "test")