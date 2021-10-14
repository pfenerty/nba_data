from typing import Dict, Any
import urllib.parse
from pymongo import MongoClient
from pandas import DataFrame
from mongo_cached_requests import CachedRequestClient
import datetime
from .headers import HEADERS
from .settings import MONGO_HOST, MONGO_USER, MONGO_PASSWORD, MONGO_PORT

class DataRequestData:
    url: str
    
    def __init__(self, url: str):
        self.url = url

class StatsRequestData:
    url: str
    params: Dict

    def __init__(self, url: str):
        parsed_url = urllib.parse.urlsplit(url)
        self.url = 'https://' + parsed_url.hostname + parsed_url.path
        params = urllib.parse.parse_qs(parsed_url.query, keep_blank_values=True)
        self.params = {p: params[p][0] for p in params}

class NBARequestClient:
    mongo_client = MongoClient(f'mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}')
    cached_request_client = CachedRequestClient(mongo_client, headers=HEADERS)

    def get_stats(self, rd: StatsRequestData, as_pandas: bool = False,
                  time_diff_allowance=datetime.timedelta(days=100)):
        response = self.cached_request_client.get(rd.url, params=rd.params, time_diff_allowance=time_diff_allowance)['resultSets'][0]
        if as_pandas:
            return DataFrame(data=response['rowSet'], columns=response['headers'])
        else:
            return response
        
    def get_data(self, rd: DataRequestData):
        return self.cached_request_client.get(rd.url, mode='flat', send_headers=False)
