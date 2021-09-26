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
from spotify import SpotifyControl

blynk = BlynkLib.Blynk(cfg.blynk_cfg["auth"])

said = 0
voice = 0
thread_num = 0

sh = SoundHandler()
mqtt = AlaskaMQTT()
wikipedia.set_lang("de")
sp = SpotifyControl()
zahlen = "null eins zwei drei vier fünf sechs sieben acht neun zehn elf zwölf dreizehn vierzehn fünfzehn sechzehn " \
         "siebzehn achtzehn neunzehn zwanzig einundzwanzig zweiundzwanzig dreiundzwanzig vierundzwanzig " \
         "fünfundzwanzig sechsundzwanzig siebenundzwanzig achtundzwanzig neunundzwanzig dreißig einunddreißig " \
         "zweiunddreißig dreiunddreißig vierunddreißig fünfunddreißig sechsunddreißig siebenunddreißig achtunddreißig " \
         "neununddreißig vierzig einundvierzig zweiundvierzig dreiundvierzig vierundvierzig fünfundvierzig " \
         "sechsundvierzig siebenundvierzig achtundvierzig neunundvierzig fünfzig einundfünfzig zweiundfünfzig " \
         "dreiundfünfzig vierundfünfzig fünfundfünfzig sechsundfünfzig siebenundfünfzig achtundfünfzig neunundfünfzig " \
         "sechzig einundsechzig zweiundsechzig dreiundsechzig vierundsechzig fünfundsechzig sechsundsechzig " \
         "siebenundsechzig achtundsechzig neunundsechzig siebzig einundsiebzig zweiundsiebzig dreiundsiebzig " \
         "vierundsiebzig fünfundsiebzig sechsundsiebzig siebenundsiebzig achtundsiebzig neunundsiebzig achtzig " \
         "einundachtzig zweiundachtzig dreiundachtzig vierundachtzig fünfundachtzig sechsundachtzig siebenundachtzig " \
         "achtundachtzig neunundachtzig neunzig einundneunzig zweiundneunzig dreiundneunzig vierundneunzig " \
         "fünfundneunzig sechsundneunzig siebenundneunzig achtundneunzig neunundneunzig einhundert".split()

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

    if "wechsel deine stimme" in audio:
        sh.change_voice()

    if "erzähle mir einen witz" in audio or "erzähl mir einen witz" in audio:
        sh.speak(pyjokes.get_joke("de", "neutral"))

    if "wikipedia" in audio:
        sh.speak("Durchsuche Wikipedia...")
        search = audio.replace("wikipedia ", "")
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
        mqtt.light("light/all", 1)

    if "licht aus" in audio:
        mqtt.light("light/all", 0)

    if "lampe" in audio:
        audio_split = audio.split(" ")
        if " an" in audio:
            if " und " in audio:
                undpos = [i for i, x in enumerate(audio_split) if x == "und"]
                for pos in undpos:
                    light = audio_split[pos - 1]
                    if light in zahlen:
                        light = zahlen.index(light)
                    mqtt.publish("light/n", 1, light)
                anpos = audio_split.index("an")
                light = audio_split[anpos - 1]
                if light in zahlen:
                    light = zahlen.index(light)
                mqtt.publish("light/n", 1, light)
            else:
                anpos = audio_split.index("an")
                light = audio_split[anpos - 1]
                if light in zahlen:
                    light = zahlen.index(light)
                mqtt.publish("light/n", 1, light)

        elif " aus" in audio:
            if " und " in audio:
                undpos = audio_split.index("und")
                for pos in undpos:
                    light = audio_split[pos - 1]
                    if light in zahlen:
                        light = zahlen.index(light)
                    mqtt.publish("light/n", 0, light)
                auspos = audio_split.index("aus")
                light = audio_split[auspos - 1]
                if light in zahlen:
                    light = zahlen.index(light)
                mqtt.publish("light/n", 0, light)
            else:
                auspos = audio_split.index("aus")
                light = audio_split[auspos - 1]
                if light in zahlen:
                    light = zahlen.index(light)
                mqtt.publish("light/n", 0, light)

    if "spiele meine playlist" in audio or "spiele die playlist" in audio:
        data_split = audio.split(" ")
        playlist = data_split[3:]
        ret = sp.play_playlist(playlist)
        sh.speak("Spiele " + str(ret))

    if "play" in audio:
        sp.play()

    if "pause" in audio:
        sp.pause()

    if "spiele zufällig" in audio or "zufall an" in audio:
        ret = sp.shuffle(toggle="on")
        if ret == "on":
            sh.speak("Zufallswiedergabe an")
        else:
            sh.speak("Etwas ist schiefgelaufen")

    if "zufall aus" in audio:
        ret = sp.shuffle(toggle="off")
        if ret == "off":
            sh.speak("Zufallswiedergabe aus")
        else:
            sh.speak("Etwas ist schiefgelaufen")

    if "zufallsmodus" in audio:
        ret = sp.shuffle()
        if ret == "on":
            sh.speak("Zufallswiedergabe an")
        if ret == "off":
            sh.speak("Zufallswiedergabe aus")
        else:
            sh.speak("Etwas ist schiefgelaufen")

    if "lautstärke auf" in audio:
        data_split = audio.split(" ")
        vol = data_split[2]
        if vol in zahlen:
            vol = zahlen.index(vol)
        sp.set_volume(vol)

    if "lauter" in audio:
        data_split = audio.split(" ")
        vol = data_split[0]
        if vol in zahlen:
            vol = zahlen.index(vol)
        if len(data_split) >= 2:
            sp.volume(vol)
        elif len(data_split) == 1:
            sp.volume(10)

    if "leiser" in audio:
        data_split = audio.split(" ")
        vol = data_split[0]
        if vol in zahlen:
            vol = zahlen.index(vol)
        if len(data_split) >= 2:
            sp.volume("-" + vol)
        elif len(data_split) == 1:
            sp.volume(-10)

    if "ich mag diesen song" in audio or "ich mag dieses lied" in audio or "lied speichern" in audio or "song speichern" in audio:
        sp.save_current_track()

    if "ich mag diesen song nicht" in audio or "ich mag dieses lied nicht" in audio or "lied löschen" in audio or "song löschen" in audio:
        sp.delete_current_track()

    if "spiele das lied" in audio or "spiele den song" in audio:
        data_split = audio.split(" ")
        ret = sp.search_track(data_split[3:])
        sh.speak("Spiele das Lied " + str(ret))

    if "spiele den podcast" in audio:
        data_split = audio.split(" ")
        ret = sp.search_show(data_split[3:])
        sh.speak("Spiele den Podcast " + str(ret))

    if "nächster song" in audio or "nächstes lied" in audio or "weiter" in audio or "skip" in audio:
        sp.skip_track()

    if "letzter song" in audio or "letztes lied" in audio or "zurück" in audio:
        sp.back_track()

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
