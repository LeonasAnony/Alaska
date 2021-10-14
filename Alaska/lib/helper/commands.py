import time
import pyjokes
import pytz
import wikipedia
import wolframalpha

from Alaska import config as cfg
from Alaska import lib



class Commands():
    def __init__(self):
        self.sh = lib.modules.Sound()
        self.mqtt = lib.modules.MQTT()
        wikipedia.set_lang("de")
        self.sp = lib.modules.Spotify()
        print("Commands started")
        
        
    def greeting(self):
        self.sh.speak("Es geht mir gut. Danke.")


    def howlate(self):
        hour = time.strftime("%H", time.localtime())
        minute = time.strftime("%M", time.localtime())
        if hour[0] == "0":
            hour = hour.replace("0", "", 1)

        if minute[0] == "0":
            minute = minute.replace("0", "", 1)

        self.sh.speak("Es ist " + hour + " Uhr " + minute)
        
    
    def weather(self):
        info = lib.modules.Weather(self.audio)
        location, status = info.status()
        self.sh.speak("Aktuell in " + str(location) + ": " + str(status) + ".")


    def wind(self):
        wind = lib.modules.Weather(self.audio)
        location, speed, deg, direc = wind.wind()
        self.sh.speak("Aktuell in " + str(location) + ": " + str(speed) + " Meter die Sekunde, aus " + str(deg) + " " +
                 str(direc))


    def sunrise(self):
        sunrise = lib.modules.Weather(self.audio)
        location, sunrise_datetime = sunrise.sunrise()
        sunrise_datetime = sunrise_datetime.astimezone(pytz.timezone("Europe/Berlin"))
        self.sh.speak("In " + str(location) + " geht die Sonne um " + str(sunrise_datetime.strftime("%H:%M")) + " auf.")


    def sunset(self):
        sunset = lib.modules.Weather(self.audio)
        location, sunset_datetime = sunset.sunset()
        sunset_datetime = sunset_datetime.astimezone(pytz.timezone("Europe/Berlin"))
        self.sh.speak("In " + str(location) + " geht die Sonne um " + str(sunset_datetime.strftime("%H:%M")) + " unter.")


    def voicechange(self):
        self.sh.change_voice()


    def joke(self):
        self.sh.speak(pyjokes.get_joke("de", "neutral"))


    def definition(self):
        self.sh.speak("Durchsuche Wikipedia...")
        search = self.audio.replace("wikipedia ", "")
        if search:
            try:
                results = wikipedia.summary(search, sentences=2)
                time.sleep(1)
                self.sh.speak(results)

            except wikipedia.PageError:
                self.sh.speak("Die Suche ergab kein Ergebnis.")

            except wikipedia.DisambiguationError:
                self.sh.speak("Bitte grenze deine Suche ein.")

        else:
            self.sh.speak("Bitte nenne wonach ich suchen soll, nach dem Wort Wikipedia.")


#	def capitalof(self):



    def calc(self):
        self.sh.speak("Stelle eine Frage:")
        time.sleep(1)
        question = self.sh.record_audio()
        wa_client = wolframalpha.Client(cfg.wa_cfg["app_id"])
        res = wa_client.query(question)
        try:
            answer = next(res.results).text
            self.sh.speak(answer)

        except StopIteration:
            self.sh.speak("Keine Ergebnisse")


    def lighton(self):
        self.mqtt.light("light/all", 1)


    def lightoff(self):
        self.mqtt.light("light/all", 0)


    def lampon(self):
        audio_split = self.audio.split(" ")
        if " an" in self.audio:
            if " und " in self.audio:
                undpos = [i for i, x in enumerate(audio_split) if x == "und"]
                for pos in undpos:
                    light = audio_split[pos - 1]
                    self.mqtt.light("light/n", 1, light)
                anpos = audio_split.index("an")
                light = audio_split[anpos - 1]
                self.mqtt.light("light/n", 1, light)
            else:
                anpos = audio_split.index("an")
                light = audio_split[anpos - 1]
                self.mqtt.light("light/n", 1, light)

        elif " aus" in self.audio:
            if " und " in self.audio:
                undpos = audio_split.index("und")
                for pos in undpos:
                    light = audio_split[pos - 1]
                    self.mqtt.light("light/n", 0, light)
                auspos = audio_split.index("aus")
                light = audio_split[auspos - 1]
                self.mqtt.light("light/n", 0, light)
            else:
                auspos = audio_split.index("aus")
                light = audio_split[auspos - 1]
                self.mqtt.light("light/n", 0, light)


    def playlistplay(self):
        data_split = self.audio.split(" ")
        playlist = data_split[3:]
        ret = self.sp.play_playlist(playlist)
        self.sh.speak("Spiele " + str(ret))


    def play(self):
        self.sp.play()


    def pause(self):
        self.sp.pause()


    def randomon(self):
        ret = self.sp.self.shuffle(toggle="on")
        if ret == "on":
            self.sh.speak("Zufallswiedergabe an")
        else:
            self.sh.speak("Etwas ist schiefgelaufen")


    def randomoff(self):
        ret = self.sp.self.shuffle(toggle="off")
        if ret == "off":
            self.sh.speak("Zufallswiedergabe aus")
        else:
            self.sh.speak("Etwas ist schiefgelaufen")


    def random(self):
        ret = self.sp.self.shuffle()
        if ret == "on":
            self.sh.speak("Zufallswiedergabe an")
        if ret == "off":
            self.sh.speak("Zufallswiedergabe aus")
        else:
            self.sh.speak("Etwas ist schiefgelaufen")


    def setvolume(self):
        data_split = self.audio.split(" ")
        vol = data_split[2]
        self.sp.set_volume(vol)


    def volumeup(self):
        data_split = self.audio.split(" ")
        vol = data_split[0]
        if len(data_split) >= 2:
            self.sp.volume(vol)
        elif len(data_split) == 1:
            self.sp.volume(10)


    def volumedown(self):
        data_split = self.audio.split(" ")
        vol = data_split[0]
        if len(data_split) >= 2:
            self.sp.volume("-" + vol)
        elif len(data_split) == 1:
            self.sp.volume(-10)


    def songlike(self):
        self.sp.save_current_track()


    def songdislike(self):
        self.sp.delete_current_track()


    def songplay(self):
        data_split = self.audio.split(" ")
        ret = self.sp.search_track(data_split[3:])
        self.sh.speak("Spiele das Lied " + str(ret))


    def showplay(self):
        data_split = self.audio.split(" ")
        ret = self.sp.search_self.show(data_split[3:])
        self.sh.speak("Spiele den Podcast " + str(ret))


    def trackskip(self):
        self.sp.skip_track()


    def trackback(self):
        self.sp.back_track()



# class CommandsException(Exception):
