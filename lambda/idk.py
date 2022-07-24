import json
import os

import boto3

from riot_request.request import RiotRequest

ddb = boto3.resource('dynamodb')
table = ddb.Table(os.environ['Puuids'])
_lambda = boto3.client('lambda')

api_key = "RGAPI-94402067-bb26-4a4c-b517-216bd4d50a4f"
riot = RiotRequest(api_key)

def handler(event, context):
    print('request: {}'.format(json.dumps(event)))

    puuid = "meow"
    table.update_item(
        Key = {'puuid': puuid}
    )