import spotipy
from spotipy.oauth2 import SpotifyOAuth
import config as cfg


class SpotifyControl:
    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(cfg.sp_cfg["client_id"], cfg.sp_cfg["client_secret"],
                                                            cfg.sp_cfg["redirect_uri"], scope=cfg.sp_cfg["scopes"]))


    def play_playlist(self, pl_name):
        results = self.sp.current_user_playlists(limit=50)
        for pl in results['items']:
            print(pl['name'])


    def shuffle(self):


    def volume(self):


    def save_current_track(self):


    def delete_current_track(self):


    def search_track(self):


    def skip_track(self):


    def back_track(self):


    def add_current_track_to_playlist(self):


