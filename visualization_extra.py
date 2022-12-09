import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

SPOTIPY_CLIENT_ID = '46282d85ebe64cfa9fc2d7de035bce0e'
SPOTIPY_CLIENT_SECRET= '355ae8f3f3b14ee19a7a470d22413bdc'
auth_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)


def get_features(track_id):
    track_features_x = sp.audio_features(track_id)
    dfx = pd.DataFrame(track_features_x, index=[0])
    dfx_features = dfx.loc[: ,['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'speechiness', 'valence']]
    return dfx_features

def feature_plot2(features1,features2):
    #Import Libraries for Feature plot
    
    
    labels= list(features1)[:]
    stats= features1.mean().tolist()
    stats2 = features2.mean().tolist()

    angles=np.linspace(0, 2*np.pi, len(labels), endpoint=False)

    # close the plot
    stats=np.concatenate((stats,[stats[0]]))
    stats2 =np.concatenate((stats2,[stats2[0]])) 
    angles=np.concatenate((angles,[angles[0]]))

    #Size of the figure
    fig=plt.figure(figsize = (18,18))

    ax = fig.add_subplot(221, polar=True)
    ax.plot(angles, stats, 'o-', linewidth=2, label = "Features 1", color= 'gray')
    ax.fill(angles, stats, alpha=0.25, facecolor='blue')
    ax.set_thetagrids(angles[0:7] * 180/np.pi, labels , fontsize = 13)

    ax.set_rlabel_position(250)
    plt.yticks([0.2 , 0.4 , 0.6 , 0.8  ], ["0.2",'0.4', "0.6", "0.8"], color="grey", size=12)
    plt.ylim(0,1)

    ax.plot(angles, stats2, 'o-', linewidth=2, label = "Features 2", color = 'm')
    ax.fill(angles, stats2, alpha=0.25, facecolor='m' )
    ax.set_title('Mean Values of the audio features')
    ax.grid(True)

    plt.legend(loc='best', bbox_to_anchor=(0.1, 0.1))
    plt.show()



def main():
    song1_features = get_features("6dBUzqjtbnIa1TwYbyw5CM")
    song2_features = get_features("7AQim7LbvFVZJE3O8TYgf2")
    feature_plot2(song1_features,song2_features)
    

if __name__ == "__main__":
    main()