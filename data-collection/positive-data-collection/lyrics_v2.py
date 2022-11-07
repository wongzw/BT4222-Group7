import api_key
import requests
import csv
from multiprocessing import Pool
from bs4 import BeautifulSoup
from lyrics_retrieve import get_data
import lyricsgenius as lg

genius = lg.Genius(api_key.client_access_token,  # Client access token from Genius Client API page
                             skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"],
                             remove_section_headers=True)


def write_csv(lst):
    with open('positive_filled.csv', 'a', encoding='utf-8') as f:
        writer = csv.writer(f)
        for row in lst:
            if row != None:
                writer.writerow(row)

# song = genius.search_song("To You", artist.name)
def get_lyrics(arr):  # Write lyrics of k songs by each artist in arr
    try:
        temp = arr
        name, artist = temp[-4], temp[-3]
        song = genius.search_song(name, artist)
        str_song = str(song.lyrics)
        val = " ".join("".join(str_song.split("Lyrics")[1:]).splitlines()[:])
        if len(val) >= 32000:
            val = ''
        elif val[0] == "/" :
            val = ''
        elif "ft." in val or "feat." in val or "EP" in val or "Featuring" in val or 'featuring' in val or ('1.' in val and '2.' in val):
            val = ''
        elif val[-8].isnumeric():
            val = val[1:-8]
        else:
            val = val[1:-7]
        temp[-1] = val
        return temp #if #criteria else []]
    except Exception as err:  #  Broad catch which will give us the name of artist and song that threw the exception
        return arr

if __name__ == "__main__":
    pool = Pool()
    data = get_data()
    for i in range(4, len(data), 4):
        ret = pool.map(get_lyrics, data[i-4:i])
        write_csv(ret)
    print(ret[0])
    ret_last = pool.map(get_lyrics, data[i:])
    write_csv(ret_last)
    pool.close()