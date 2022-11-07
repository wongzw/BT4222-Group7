import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import csv
from multiprocessing import Pool

def write_rows(lst):
    with open('positive_fill.csv', 'a') as f:
        writer = csv.writer(f)
        for val in lst:
            if val != None:
                writer.writerow(val)


def func(lst):
    try:
        cid = ''
        secret = ''
        client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
        sp = spotipy.Spotify(client_credentials_manager
        =
        client_credentials_manager)
        artist, song = lst[3], lst[2]
        track_results = sp.search(q=f'artist: {artist.lower()}%20track: {song.lower()}', type='track', limit=10)
        final = []
        for i, t in enumerate(track_results['tracks']['items']):
            artist_lst, artist_id_lst = [], []
            for a in (t['artists']):
                artist_lst.append(a["name"])
                artist_id_lst.append(a["id"])
            dic = sp.audio_features([t['id']])[0]
            dance = dic['danceability']
            energy = dic['energy']
            key = dic['key']
            loudness = dic['loudness']
            mode = dic['mode']
            speechiness = dic['speechiness']
            acoustic = dic['acousticness']
            instru = dic['instrumentalness']
            live = dic['liveness']
            valence = dic['valence']
            tempo = dic['tempo']
            duration = dic['duration_ms']
            final.append([t['id'], t['name'], artist_lst, artist_id_lst, t['track_number'], dance, energy, key, loudness, mode, speechiness, acoustic, instru, live, valence, tempo, t['explicit'], duration, t['popularity']])
        return sorted(final, key=lambda x: x[-1], reverse=True)[0][:-1]
    except:
        return []

if __name__ == "__main__":
    df = pd.read_csv("../raw-data/charts.csv")
    df["year"] = df["date"].apply(lambda x: x.split("/")[-1])
    df = df[(df["year"] < "21") & (df["year"] >= "00")]
    df = df.drop_duplicates(['song', 'artist'])
    lst = [list(df.iloc[i]) for i in range(len(df.index))]
    pool = Pool()
    for i in range(4, len(lst), 4):
        ret = pool.map(func, lst[i-4:i])
        print(ret)
        write_rows(ret)
    ret_last = pool.map(func, lst[i:])
    write_rows(ret_last)
