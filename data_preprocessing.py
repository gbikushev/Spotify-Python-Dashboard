import pandas as pd
import numpy as np

df = pd.read_csv('universal_top_spotify_songs.csv')

# drop unnecessary columns
df = df.drop(['spotify_id', 'key', 'mode', 'liveness', 'time_signature', 'album_name', 'album_release_date','daily_movement', 'weekly_movement'], axis=1)

# leave only countries 'US'(United States), 'IN'(india), 'IE'(Ireland)
df = df[df['country'].isin(['US', 'IN', 'IE'])]
df.reset_index(drop=True, inplace=True)
print(df.info())

# check popularity column for 0 values
print(df.loc[df.popularity == 0, 'artists'].value_counts())
# since it is impossible that there are so many songs with 0 popularity in Top-50 Spotify songs,
# let's make our own 'popularity' column based on 'daily_rank' value:
# popularity = 100 - (daily_rank - 1) * 2, so the range of popularity is [2 - 100]

df.drop(['popularity'], axis=1, inplace=True)
df['popularity'] = 100 - (df['daily_rank'] - 1) * 2

# let's divide the dataset by countries of interest:
# leave only countries 'US'(United States), 'IN'(india), 'IE'(Ireland)
US_df = df[df['country'] == 'US']
IN_df = df[df['country'] == 'IN']
IE_df = df[df['country'] == 'IE']

# save to csv files
US_df.to_csv('US.csv', index=False)
IN_df.to_csv('IN.csv', index=False)
IE_df.to_csv('IE.csv', index=False)

