import pandas as pd
import numpy as np
import requests
import base64
import datetime
import time
from urllib.parse import urlencode

#Fill this in
client_id = ''
client_secret = ''

client_credentials = f"{client_id}:{client_secret}"

client_cred_bs4 = base64.b64encode(client_credentials.encode())
print(client_cred_bs4)

token_url = "https://accounts.spotify.com/api/token"
method = 'POST'

token_data = {
    "grant_type": "client_credentials"
}

token_headers = {
    "Authorization": f"Basic {client_cred_bs4.decode()}"
}

print(token_headers)


req = requests.post(token_url, data=token_data, headers=token_headers)
token_response_data = req.json()


access_token = token_response_data['access_token']
expires_in = token_response_data['expires_in']  # in seconds
token_type = token_response_data['token_type']

print(token_response_data)

df = pd.read_csv('data/final_compiled_final.csv', low_memory=False)

# change this to target == 0 for neg dataset
pos_dataset = df[df['target'] == 1]
pos_dataset["release_date"] = pos_dataset.release_date.astype(str)
# print(pos_dataset['release_date'])
# time.sleep(10)

song_ids = pos_dataset['id']
split_ids = []
index = 0
total_index = 0
temp_id_array = []

for song in song_ids:
    if index == 50:
        split_ids.append(temp_id_array)
        temp_id_array = []
        index = 0

    if total_index == (len(song_ids) - 1):
        split_ids.append(temp_id_array)

    temp_id_array.append(song)
    index += 1
    total_index += 1


headers = {
    "Authorization": f'Bearer {access_token}'
}

count = 0
song_release_dates = []

for song_list in split_ids:
    song_list_new = ",".join(song_list)
    print(song_list_new)
    endpoint = f'https://api.spotify.com/v1/tracks?ids={song_list_new}'
    req = requests.get(url=endpoint, headers=headers).json()
    for song in req['tracks']:
        id = song['id']
        rel_date = song['album']['release_date']
        print(rel_date)
        rel_date = pd.to_datetime(rel_date, format='%Y/%m/%d')

        rel_date = rel_date.strftime("%d/%m/%Y")
        # dd/mm/yyyy
        print("Formatted ", rel_date, type(rel_date))

        song_release_dates.append([id, rel_date])

        # try:
        #     rel_date = pd.to_datetime(rel_date, format='%Y/%m/%d')
        #     print(rel_date)
        # except:
        #     print("Conversion Failure")
        # print(pos_dataset.iloc[index]["release_date"])
        # pos_dataset.iloc[index]["release_date"] = rel_date
        # print(pos_dataset.iloc[index]["release_date"])
        # print(
        #     f"Updating Spotify {id} - {id==pos_dataset.iloc[index]['id']}, song_name {pos_dataset.iloc[index]['name']} with release date {pos_dataset.iloc[index]['release_date']}")
        print(
            f"Song {count} Retrieving release date {rel_date} for song with {id}...")
        count += 1

    print("Sleep")
    time.sleep(0.1)

songs_with_dates = pd.DataFrame(song_release_dates, columns=[
                                'song_id', 'release_date'])

songs_with_dates.to_csv("positive_songs_with_rel_date.csv")
