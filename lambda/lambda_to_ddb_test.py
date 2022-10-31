import json
import os

import boto3

ddb = boto3.resource('dynamodb')
table = ddb.Table(os.environ['MEOW_TABLE_NAME'])
_lambda = boto3.client('lambda')

def handler(event, context):
    print('request: {}'.format(json.dumps(event)))
    #k = "meow"
    #table.put_item(Item = {'meows': k})
    
    return json.dumps(event)