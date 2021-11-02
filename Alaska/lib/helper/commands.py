import time
import pyjokes
import pytz
import wikipedia
import wolframalpha

from Alaska import config as cfg
from Alaska import lib



class Commands:
    def __init__(self, disablemqtt):
        self.sh = lib.modules.Sound()
        wikipedia.set_lang("de")
        self.sp = lib.modules.Spotify()
        if not disablemqtt:
            self.mqtt = lib.modules.MQTT()
        print("Commands started")
        
        
    def greeting(self, msg, response):
        self.sh.speak(str(response))


    def howlate(self, msg):
        hour = time.strftime("%H", time.localtime())
        minute = time.strftime("%M", time.localtime())
        if hour[0] == "0":
            hour = hour.replace("0", "", 1)

        if minute[0] == "0":
            minute = minute.replace("0", "", 1)

        self.sh.speak("Es ist " + hour + " Uhr " + minute)
        
    
    def weather(self, msg):
        info = lib.modules.Weather(msg)
        location, status = info.status()
        self.sh.speak("Aktuell in " + str(location) + ": " + str(status) + ".")


    def wind(self, msg):
        wind = lib.modules.Weather(msg)
        location, speed, deg, direc = wind.wind()
        self.sh.speak("Aktuell in " + str(location) + ": " + str(speed) + " Meter die Sekunde, aus " + str(deg) + " " +
                 str(direc))


    def sunrise(self, msg):
        sunrise = lib.modules.Weather(msg)
        location, sunrise_datetime = sunrise.sunrise()
        sunrise_datetime = sunrise_datetime.astimezone(pytz.timezone("Europe/Berlin"))
        self.sh.speak("In " + str(location) + " geht die Sonne um " + str(sunrise_datetime.strftime("%H:%M")) + " auf.")


    def sunset(self, msg):
        sunset = lib.modules.Weather(msg)
        location, sunset_datetime = sunset.sunset()
        sunset_datetime = sunset_datetime.astimezone(pytz.timezone("Europe/Berlin"))
        self.sh.speak("In " + str(location) + " geht die Sonne um " + str(sunset_datetime.strftime("%H:%M")) + " unter.")


    def voicechange(self, msg):
        self.sh.change_voice()


    def joke(self, msg):
        self.sh.speak(pyjokes.get_joke("de", "neutral"))


    def definition(self, msg):
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


    def capitalof(self, msg):
        msg_split = msg.split(" ")
        if "von" in msg:
            pos = msg_split.index("von")
            country = msg_split[pos+1]
        else:
            print("KeyWord 'von' not said...")
            return
        
        info = lib.modules.CountryInfo(str(country))
        self.sh.speak(info.capital())
        
        
    def timezone(self, msg):



    def calc(self, msg):
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


    def lighton(self, msg):
        self.mqtt.light("light/all", 1)


    def lightoff(self, msg):
        self.mqtt.light("light/all", 0)


    def lampon(self, msg):
        msg_split = msg.split(" ")
        pos = msg_split.index("lampe")
        lamp = msg_split[pos +1]
        self.mqtt.light("light/n", 1, lamp)
                
    
    def lampoff(self, msg):
        msg_split = msg.split(" ")
        pos = msg_split.index("lampe")
        lamp = msg_split[pos + 1]
        self.mqtt.light("light/n", 0, lamp)
    
    
    def multilampon(self, msg):
        msg_split = msg.split(" ")
        pos = msg_split.index("lampe")
        lamp = msg_split[pos + 1]
        self.mqtt.light("light/n", 0, lamp)
        andpos = [i for i, x in enumerate(msg_split) if x == "und"]
        for pos in andpos:
            lamp = msg_split[pos + 1]
            self.mqtt.light("light/n", 0, lamp)
    
    
    def multilampoff(self, msg):
        msg_split = msg.split(" ")
        pos = msg_split.index("lampe")
        lamp = msg_split[pos + 1]
        self.mqtt.light("light/n", 1, lamp)
        andpos = [i for i, x in enumerate(msg_split) if x == "und"]
        for pos in andpos:
            lamp = msg_split[pos + 1]
            self.mqtt.light("light/n", 1, lamp)


    def playlistplay(self, msg):
        msg_split = msg.split(" ")
        if "playlist" in msg:
            playlist = msg_split[msg_split.index("playlist")+1:]
        else:
            print("KeyWord 'Playlist' not said...")
            return
        ret = self.sp.play_playlist(playlist)
        self.sh.speak("Spiele " + str(ret))


    def play(self, msg):
        self.sp.play()


    def pause(self, msg):
        self.sp.pause()


    def randomon(self, msg):
        ret = self.sp.shuffle(toggle="on")
        if ret == "on":
            self.sh.speak("Zufallswiedergabe an")
        else:
            self.sh.speak("Etwas ist schiefgelaufen")


    def randomoff(self, msg):
        ret = self.sp.shuffle(toggle="off")
        if ret == "off":
            self.sh.speak("Zufallswiedergabe aus")
        else:
            self.sh.speak("Etwas ist schiefgelaufen")


    def random(self, msg):
        ret = self.sp.shuffle()
        if ret == "on":
            self.sh.speak("Zufallswiedergabe an")
        if ret == "off":
            self.sh.speak("Zufallswiedergabe aus")
        else:
            self.sh.speak("Etwas ist schiefgelaufen")


    def setvolume(self, msg):
        msg_split = self.msg.split(" ")
        if "auf" in msg:
            vol = msg_split[msg_split.index("auf")+1]
        else:
            print("KeyWord 'auf' not said...")
            return
        self.sp.set_volume(vol)


    def volumeup(self, msg):
        msg_split = self.msg.split(" ")
        if "um" in msg:
            vol = msg_split[msg_split.index("um")+1]
            self.sp.volume(vol)
        else:
            self.sp.volume(10)


    def volumedown(self, msg):
        msg_split = self.msg.split(" ")
        if "um" in msg:
            vol = msg_split[msg_split.index("um")+1]
            self.sp.volume(f"-{vol}")
        else:
            self.sp.volume(-10)


    def songlike(self, msg):
        self.sp.save_current_track()


    def songdislike(self, msg):
        self.sp.delete_current_track()


    def songplay(self, msg):
        msg_split = self.msg.split(" ")
        if "lied" in msg:
            song = msg_split[msg_split.index("lied")+1:]
        elif "song" in msg:
            song = msg_split[msg_split.index("song")+1:]
        else:
            print("KeyWord 'song'/'lied' not said...")
            return
        ret = self.sp.search_track(song)
        self.sh.speak("Spiele das Lied " + str(ret))


    def showplay(self, msg):
        msg_split = self.msg.split(" ")
        if "podcast" in msg and "starten" in msg:
            podcast = msg_split[msg_split.index("podcast")+1:msg_split.index("starten")-1]
        elif "podcast" in msg:
            podcast = msg_split[msg_split.index("podcast")+1:]
        else:
            print("KeyWord 'podcast' not said...")
            return
        ret = self.sp.search_self.show(podcast)
        self.sh.speak("Spiele den Podcast " + str(ret))


    def trackskip(self, msg):
        self.sp.skip_track()


    def trackback(self, msg):
        self.sp.back_track()



# class CommandsException(Exception):
