import json
import requests
from riotwatcher import LolWatcher, ApiError
import time

class RiotRequest:
    
    def __init__(self, api_key, summoner, region):
        self.api_key = api_key
        self.summoner = summoner
        self.region = region

        self.watcher = LolWatcher(api_key)
        self.me = self.watcher.summoner.by_name(self.region, self.summoner)

        latest = self.watcher.data_dragon.versions_for_region(region)['n']['champion']
        static_champ_list = self.watcher.data_dragon.champions(latest, False, 'en_GB')
        self.champ_dict = {}
        for key in static_champ_list['data']:
            row = static_champ_list['data'][key]
            self.champ_dict[row['key']] = row['id']


    ## MATCH DATA RETRIEVAL
    
    def get_match(self, match_id):
        """
        Returns match data given match id

            Parameters:
                match_id (str): Desired match_id
            
            Returns:
                match_data (dict): Response for the match with match_id
        """
        r = requests.get('https://europe.api.riotgames.com/lol/match/v5/matches/{}/'.format(match_id), headers={"X-Riot-Token": self.api_key})
        return r.json()
    
    def get_matchlist(self, puuid, queue = 420, start = 0, count = 20, startTime = None, endTime = None):
        """
        """
        url = 'https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{}/ids?queue={}&start={}&count={}'.format(
            puuid, queue, start, count
        )

        if startTime != None:
            url = url + "&startTime={}".format(startTime)
        if endTime != None:
            url = url + "&endTime={}".format(endTime)

        r = requests.get(url, headers={"X-Riot-Token": self.api_key})
        return r.json()
    
    def get_matches_from_puuids(self, puuids, queue = 420, start = 0, count = 20, startTime = None, endTime = None):
        match_ids = []

        for i in range(len(puuids)):
            puuid = puuids[i]
            while True:
                print('Retrieving last {} matches from {} players (i = {})'.format(count, len(puuids), i))
                url = 'https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{}/ids?queue=420&type=ranked&start_time={}&start=0&count={}'.format(
                    puuid, queue, start, count
                )
                if startTime != None:
                    url = url + "&startTime={}".format(startTime)
                if endTime != None:
                    url = url + "&endTime={}".format(endTime)
                r = requests.get(url, headers = {"X-Riot-Token": self.api_key})
                if r.status_code == 200:
                    break
                time.sleep(60)
            match_ids.append(r.json())

        return match_ids

    ## ID RETRIEVAL
    
    def get_master_players(self):
        r = requests.get('https://euw1.api.riotgames.com/lol/league/v4/masterleagues/by-queue/RANKED_SOLO_5x5', headers={"X-Riot-Token": self.api_key})
        return r.json()
    
    def get_grandmaster_players(self):
        r = requests.get('https://euw1.api.riotgames.com/lol/league/v4/grandmasterleagues/by-queue/RANKED_SOLO_5x5', headers={"X-Riot-Token": self.api_key})
        return r.json()
    
    def get_challenger_players(self):
        r = requests.get('https://euw1.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5', headers={"X-Riot-Token": self.api_key})
        return r.json()
    
    def get_summonerIds_from_players(self, players):
        summonerIds = []
        for i in range(len(players['entries'])):
            summonerIds.append(players['entries'][i]['summonerId'])
        return summonerIds
    
    def get_puuids_from_summonerIds(self, summonerIds):
        puuids = []
        n = len(summonerIds)
        for i in range(n):
            summonerId = summonerIds[i]
            while True:
                print('Retrieving puuids (i = {} of {})'.format(i, n))
                r = requests.get('https://euw1.api.riotgames.com/lol/summoner/v4/summoners/{}'.format(summonerId), headers={"X-Riot-Token": self.api_key})
                if r.status_code == 200:
                    break
                time.sleep(60)
            puuids.append(r.json()['puuid'])
        return puuids
        