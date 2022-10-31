import json
import os
import time
import requests

import boto3

#from riot_request import RiotRequest

ddb = boto3.resource('dynamodb')
match_table = ddb.Table(os.environ['MATCH_TABLE_NAME'])
puuid_table = ddb.Table(os.environ['PUUID_TABLE_NAME'])

api_key = "RGAPI-4a68c077-9045-47dc-8ffb-3d085ff72cad"

def get_matches_from_puuids(puuids, queue = 420, start = 0, count = 20, startTime = None, endTime = None):
        match_ids = []

        for i in range(len(puuids)):
            puuid = puuids[i]['puuid']
            while True:
                print('Retrieving last {} matches from {} players (i = {})'.format(count, len(puuids), i))
                url = 'https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{}/ids?queue={}&type=ranked&start={}&count={}'.format(
                    puuid, queue, start, count
                )
                if startTime != None:
                    url = url + "&startTime={}".format(startTime)
                if endTime != None:
                    url = url + "&endTime={}".format(endTime)
                r = requests.get(url, headers = {"X-Riot-Token": api_key})
                if r.status_code == 200:
                    break
                time.sleep(60)
            match_ids.append(r.json())

        return match_ids

def get_matchlist(puuid, queue = 420, start = 0, count = 20, startTime = None, endTime = None):
        url = 'https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{}/ids?queue={}&start={}&count={}'.format(
            puuid, queue, start, count
        )

        if startTime != None:
            url = url + "&startTime={}".format(startTime)
        if endTime != None:
            url = url + "&endTime={}".format(endTime)

        r = requests.get(url, headers={"X-Riot-Token": api_key})
        return r.json()

def collect_match_ids():
    current_time = time.time()
    previous_time = int(current_time - 20*60)
    puuids = puuid_table.scan()['Items']

    matches = get_matches_from_puuids(puuids, startTime= previous_time)
    #matches = get_matchlist(puuids[0]['puuid'])

    print('current_time : ', current_time)
    print('previous_time: ', previous_time)
    print('puuids:' , puuids)
    print('puuids len: ', len(puuids))
    print('match_ids:', matches)
    print('match_ids len:', len(matches))


def handler(event, context):
    print('request: {}'.format(json.dumps(event)))

    collect_match_ids()
    
    return json.dumps(event)