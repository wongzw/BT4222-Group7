import pandas as pd
import numpy as np
from ast import literal_eval
def get_data():
    df_tracks = pd.read_csv('Negative Dataset/negative_hit_songs_2016.csv')
    df_tracks = df_tracks.drop(columns=['Unnamed: 0'])
    df_tracks["artists"] = df_tracks["artists"].apply(lambda x: literal_eval(x))
    return [list(df_tracks.iloc[i]) for i in range(len(df_tracks.index))]

