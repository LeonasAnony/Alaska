import spotipy
from spotipy.oauth2 import SpotifyOAuth
import config as cfg
import jellyfish


class SpotifyControl:
    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cfg.sp_cfg["client_id"],
                                                            client_secret=cfg.sp_cfg["client_secret"],
                                                            redirect_uri=cfg.sp_cfg["redirect_uri"],
                                                            scope=cfg.sp_cfg["scopes"]))

    def play(self):
        self.sp.start_playback(device_id=cfg.sp_cfg["devices"]["Alaska"])

    def pause(self):
        self.sp.pause_playback()

    def play_playlist(self, pl_search):
        highest = {"index": None, "score": -1}
        results = self.sp.current_user_playlists(limit=50)
        for pl in results['items']:
            similarity = jellyfish.jaro_winkler_similarity(str(pl_search), pl["name"].lower())
            if similarity > highest["score"]:
                highest["index"] = results["items"].index(pl)
                highest["score"] = similarity
        self.sp.start_playback(device_id=cfg.sp_cfg["devices"]["Alaska"],
                               context_uri=results["items"][highest["index"]]["uri"])
        return results["items"][highest["index"]]["name"]

    def shuffle(self, toggle=False):
        if not toggle:
            ss = self.sp.current_playback()["shuffle_state"]
            if ss:
                self.sp.shuffle(False, self.sp.current_playback()["device"]["id"])
                return "off"
            else:
                self.sp.shuffle(True, self.sp.current_playback()["device"]["id"])
                return "on"
        else:
            if toggle == "on":
                self.sp.shuffle(True, self.sp.current_playback()["device"]["id"])
                return "on"
            if toggle == "off":
                self.sp.shuffle(False, self.sp.current_playback()["device"]["id"])
                return "off"

    def set_volume(self, vol):
        if int(vol) < 0:
            self.sp.volume(volume_percent=0)
        elif int(vol) > 100:
            self.sp.volume(volume_percent=100)
        else:
            self.sp.volume(volume_percent=int(vol))

    def volume(self, vol):
        cv = self.sp.current_playback()["device"]["volume_percent"]
        if int(cv) + int(vol) < 0:
            self.sp.volume(volume_percent=0)
        elif int(cv) + int(vol) > 100:
            self.sp.volume(volume_percent=100)
        else:
            self.sp.volume(volume_percent=int(cv) + int(vol))

    def save_current_track(self):
        ct = [self.sp.current_playback()["item"]["id"]]
        self.sp.current_user_saved_tracks_add(tracks=ct)

    def delete_current_track(self):
        ct = [self.sp.current_playback()["item"]["id"]]
        self.sp.current_user_saved_tracks_delete(tracks=ct)

    def search_track(self, query):
        result = self.sp.search(q=str(query),
                                limit=1,
                                offset=0,
                                type="track",
                                market="DE")
        self.sp.start_playback(device_id=cfg.sp_cfg["devices"]["Alaska"],
                               uris=[result["tracks"]["items"][0]["uri"]])
        return result["tracks"]["items"][0]["name"]

    def search_show(self, query):
        result = self.sp.search(q=query,
                                limit=1,
                                offset=0,
                                type="show",
                                market="DE")
        episodes = self.sp.show_episodes(show_id=result["shows"]["items"][0]["uri"], limit=1)
        self.sp.start_playback(device_id=cfg.sp_cfg["devices"]["Alaska"],
                               uris=[episodes["items"][0]["uri"]])
        return result["shows"]["items"][0]["name"]

    def skip_track(self):
        self.sp.next_track()

    def back_track(self):
        self.sp.previous_track()

    # def add_current_track_to_playlist(self):
