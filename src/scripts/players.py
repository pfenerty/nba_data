from data_getters.urls.data import PLAYERS
from data_getters.requests import DataRequestData, NBARequestClient
import requests

c = NBARequestClient()
rd = DataRequestData(PLAYERS)

x = c.get_data(rd)
a = 0