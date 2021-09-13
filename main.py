import time
# import os
# import random
import threading
from weather import WeatherInfo
from sound import SoundHandler
from mqtt import AlaskaMQTT
import pytz
import pyjokes
import wikipedia
import wolframalpha
import BlynkLib
import config as cfg

blynk = BlynkLib.Blynk(cfg.blynk_cfg["auth"])

said = 0
voice = 0
thread_num = 0

sh = SoundHandler()
mqtt = AlaskaMQTT()
wikipedia.set_lang("de")

"""
def song_play(song_name, action):
    global song
    if action == 0:
        song.stop()

    if action == 1:
        song = vlc.Media(song_name)
        song.play()
"""

"""
def playlist_play(pl_name, play_rand):
    print(pl_name)
    path = "playlists/" + pl_name + "/"
    pl_path_list = os.listdir(path)
    if play_rand == 1:
        random.shuffle(pl_path_list)
        time.sleep(0.2)
        random.shuffle(pl_path_list)
        time.sleep(0.2)
        random.shuffle(pl_path_list)

    print(pl_path_list)
    for pl_song in pl_path_list:
        pl_path = "playlists/" + pl_name + "/" + pl_song
        song_play(pl_path, 1)
        print(pl_song)
        if paus == 1:
            while paus == 1:
                time.sleep(1)
                print("waiting...")

        elif paus == 0:
            time_left = get_remaining_song_length()
            time.sleep(time_left)


def get_song_length():
    time.sleep(0.2)
    date_left = datetime.datetime.fromtimestamp(song.get_length() / 1000.0)
    minute = date_left.strftime("%M")
    second = date_left.strftime("%S")
    if minute[0] == "0":
        minute = minute.replace("0", "", 1)

    tl = int(second) + int(minute) * 60
    print(tl)
    return tl


def get_remaining_song_length():
    time.sleep(0.2)
    date_remaining = datetime.datetime.fromtimestamp(song.get_time() / 1000.0)
    minute = date_remaining.strftime("%M")
    second = date_remaining.strftime("%S")
    if minute[0] == "0":
        minute = minute.replace("0", "", 1)

    td = int(second) + int(minute) * 60
    print(td)
    sl = get_song_length()
    tr = sl - td
    print(tr)
    return tr
"""


"""
def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message
"""


def alaska(audio):
    if "wie geht es dir" in audio or "wie gehts dir" in audio:
        sh.speak("Es geht mir gut. Danke.")

    if "wie spät ist es" in audio or "wie viel uhr ist es" in audio:
        hour = time.strftime("%H", time.localtime())
        minute = time.strftime("%M", time.localtime())
        if hour[0] == "0":
            hour = hour.replace("0", "", 1)

        if minute[0] == "0":
            minute = minute.replace("0", "", 1)

        sh.speak("Es ist " + hour + " Uhr " + minute)

    if "wetter in" in audio or "wetter für" in audio:
        info = WeatherInfo(audio)
        location, status = info.status()
        sh.speak("Aktuell in " + str(location) + ": " + str(status) + ".")

    if "wind in" in audio or "wie windig in" in audio:
        wind = WeatherInfo(audio)
        location, speed, deg, direc = wind.wind()
        sh.speak("Aktuell in " + str(location) + ": " + str(speed) + " Meter die Sekunde, aus " + str(deg) + " " +
                 str(direc))

    if "wann geht die sonne auf" in audio or "wann geht in" and "die sonne auf" in audio:
        sunrise = WeatherInfo(audio)
        location, sunrise_datetime = sunrise.sunrise()
        sunrise_datetime = sunrise_datetime.astimezone(pytz.timezone("Europe/Berlin"))
        sh.speak("In " + str(location) + " geht die Sonne um " + str(sunrise_datetime.strftime("%H:%M")) + " auf.")

    if "wann geht die sonne unter" in audio or "wann geht in" and "die sonne unter" in audio:
        sunset = WeatherInfo(audio)
        location, sunset_datetime = sunset.sunset()
        sunset_datetime = sunset_datetime.astimezone(pytz.timezone("Europe/Berlin"))
        sh.speak("In " + str(location) + " geht die Sonne um " + str(sunset_datetime.strftime("%H:%M")) + " unter.")

    #     if "top nachrichten" in audio:

    #    if audio == "pause":
    #        paus = 1
    #        song.pause()

    #    if audio == "play":
    #        paus = 0
    #        song.play()

    if "wechsel deine stimme" in audio:
        sh.change_voice()

    if "erzähle mir einen witz" in audio or "erzähl mir einen witz" in audio:
        sh.speak(pyjokes.get_joke("de", "neutral"))

    if "wikipedia" in audio:
        sh.speak("Durchsuche Wikipedia...")
        search = audio.replace("wikipedia", "")
        if search:
            try:
                results = wikipedia.summary(search, sentences=2)
                time.sleep(1)
                sh.speak(results)

            except wikipedia.PageError:
                sh.speak("Die Suche ergab kein Ergebnis.")

            except wikipedia.DisambiguationError:
                sh.speak("Bitte grenze deine Suche ein.")

        else:
            sh.speak("Bitte nenne wonach ich suchen soll, nach dem Wort Wikipedia.")

    if "rechne" in audio:
        sh.speak("Stelle eine Frage:")
        time.sleep(1)
        question = sh.record_audio()
        wa_client = wolframalpha.Client(cfg.wa_cfg["app_id"])
        res = wa_client.query(question)
        try:
            answer = next(res.results).text
            sh.speak(answer)

        except StopIteration:
            sh.speak("Keine Ergebnisse")

    if "licht an" in audio:
        mqtt.publish("light/all", 1)

    if "licht aus" in audio:
        mqtt.publish("light/all", 0)

    if "lampe" in audio:
        audio_split = audio.split(" ")
        if " an" in audio:
            if " und " in audio:
                undpos = [i for i, x in enumerate(audio_split) if x == "und"]
                for pos in undpos:
                    light = audio_split[pos - 1]
                    mqtt.publish("light/n", 1, light)
                anpos = audio_split.index("an")
                light = audio_split[anpos - 1]
                mqtt.publish("light/n", 1, light)
            else:
                anpos = audio_split.index("an")
                light = audio_split[anpos - 1]
                mqtt.publish("light/n", 1, light)

        elif " aus" in audio:
            if " und " in audio:
                undpos = audio_split.index("und")
                for pos in undpos:
                    light = audio_split[pos - 1]
                    mqtt.publish("light/n", 0, light)
                auspos = audio_split.index("aus")
                light = audio_split[auspos - 1]
                mqtt.publish("light/n", 0, light)
            else:
                auspos = audio_split.index("aus")
                light = audio_split[auspos - 1]
                mqtt.publish("light/n", 0, light)



    if "spiele die playlist" in audio:
        data_split = audio.split(" ")
        playlist = data_split[3]
        if len(data_split) >= 5:
            rand = data_split[4]
            if rand == "zufällig":
                ran = 1

        playlist_play(playlist, ran)
        t2 = MyFred(2, "t2")
        t2.start()
        paus = 0



def wake_word(record):
    global said
    if said == 0:
        if "alaska" in record:
            sh.file_play("recognition.mp3")
            time.sleep(0.2)
            said = 1

        else:
            print("Alaska wasn´t called")
            said = 0

    elif said == 1:
        alaska(record)
        said = 0


def wakeword_loop():
    while True:
        wake_word(sh.record_audio())


def blynk_loop():
    while True:
        blynk.run()


class MyFred(threading.Thread):
    def __init__(self, fredid, name):
        threading.Thread.__init__(self)
        self.iD = fredid
        self.name = name


time.sleep(2)
sh.file_play("welcome.mp3")
time.sleep(2)

wl = threading.Thread(target=wakeword_loop())
bl = threading.Thread(target=blynk_loop())

wl.start()
bl.start()
