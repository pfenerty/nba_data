from data_getters.requests import StatsRequestData, NBARequestClient
from data_getters.urls.stats import PULL_UP_SHOOTING
from data_getters.util import year_num_to_str
from viz import generate_table
import pandas as pd

c = NBARequestClient()
rd = StatsRequestData(PULL_UP_SHOOTING)
rd.params['PerMode'] = 'Totals'

dfs = []
for year in range(2013, 2020):
    year_str = year_num_to_str(year)
    rd.params['Season']=year_str
    ydf = c.get_stats(rd, as_pandas=True)
    ydf = ydf[['PLAYER_ID', 'PLAYER_NAME', 'PULL_UP_FG3A', 'PULL_UP_FG3M']]
    ydf['SEASON'] = year_str
    dfs.append(ydf)

df = pd.concat(dfs).groupby(['PLAYER_ID', 'PLAYER_NAME']).sum().sort_values(by='PULL_UP_FG3M', ascending=False).head(100).reset_index()
df['PULL_UP_FG3_PCT'] = df['PULL_UP_FG3M'] / df['PULL_UP_FG3A'] * 100

# df = pd.concat(dfs)
# df = df[df['PULL_UP_FG3A'] >= 200]
# df['PULL_UP_FG3_PCT'] = df['PULL_UP_FG3M'] / df['PULL_UP_FG3A'] * 100
# df = df.sort_values(by='PULL_UP_FG3_PCT', ascending=False).reset_index()

# df = pd.concat(dfs)
# df['PULL_UP_FG3_PCT'] = df['PULL_UP_FG3M'] / df['PULL_UP_FG3A'] * 100
# df = df[df['PLAYER_NAME'] == 'Kyle Lowry']
# df = df.reset_index()

generate_table(df)

x = 0