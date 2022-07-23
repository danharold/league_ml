import json
import os

import boto3

from riot_request.request import RiotRequest

ddb = boto3.resource('dynamodb')
table = ddb.Table(os.environ['MASTER_PUUIDS'])
_lambda = boto3.client('lambda')

api_key = "RGAPI-94402067-bb26-4a4c-b517-216bd4d50a4f"
riot = RiotRequest(api_key)

def handler(event, context):
    print('request: {}'.format(json.dumps(event)))

    f = open('../data/master_puuids.txt')
    master_puuids = json.load(f)
    puuids = master_puuids['data']

    table.update_item(
        Key = {'puuid': puuids}
    )