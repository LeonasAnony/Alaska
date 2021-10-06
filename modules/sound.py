import speech_recognition as sr
import vlc
from gtts import gTTS
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import TextToSpeechV1

import config as cfg

authenticator = IAMAuthenticator(cfg.ibm_cfg["api_key"])
text_to_speech = TextToSpeechV1(authenticator=authenticator)
text_to_speech.set_service_url(cfg.ibm_cfg["service_url"])

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


class Sound:
    def __init__(self):
        self.vlc_speak = vlc.MediaPlayer()
        self.vlc_speak.set_rate(cfg.so_cfg["vlc_speed"])
        self.vlc_speak.audio_set_volume(cfg.so_cfg["vlc_vol"])

        self.vlc_file = vlc.MediaPlayer()
        self.vlc_file.set_rate(1)
        self.vlc_file.audio_set_volume(cfg.so_cfg["vlc_vol"])

        self.voice = 0

        self.r = sr.Recognizer()

    def speak(self, tts_string):
        W = '\033[0m'  # white (normal)
        P = '\033[35m'  # purple
        print(P + tts_string + W)
        if self.voice == 0:
            tts = gTTS(text=tts_string, lang='de', )
            tts.save("audio-files/speak.mp3")

        elif self.voice == 1:
            with open('audio-files/speak.mp3', 'wb') as audio_file:
                audio_file.write(text_to_speech.synthesize(tts_string, voice='de-DE_DieterV3Voice', accept='audio/mp3')
                                 .get_result().content)

        speak_file = vlc.Media("audio-files/speak.mp3")
        self.vlc_speak.set_media(speak_file)
        self.vlc_speak.play()

    def file_play(self, file_name):
        print(file_name)
        file = vlc.Media(file_name)
        self.vlc_file.set_media(file)
        self.vlc_file.play()

    def record_audio(self):
        understood = False
        while not understood:
            with sr.Microphone(device_index=cfg.so_cfg["mic_index"]) as source:
                W = '\033[0m'  # white (normal)
                R = '\033[31m'  # red
                G = '\033[32m'  # green
                O = '\033[33m'  # orange
                B = '\033[34m'  # blue
                P = '\033[35m'  # purple
                print(O + "Say something!" + W)
                self.r.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.r.listen(source, timeout=15, phrase_time_limit=10)

            try:
                data_raw = self.r.recognize_google(audio, language="de")
                data_lower = data_raw.lower()
                print(O + "You said: " + B + data_raw + W)
                understood = True
                data_list = data_lower.split()
                for w in data_list:
                    if w in zahlen:
                        print(w)
                        data_list[data_list.index(w)] = zahlen.index(w)
                print(data_list)
                return " ".join(str(e) for e in data_list)
            except sr.UnknownValueError:
                print(R + "Google Speech Recognition could not understand audio" + W)
            except sr.RequestError as e:
                print(R + f"Could not request results from Google Speech Recognition service; {e}" + W)

    def change_voice(self):
        if self.voice == 0:
            self.voice = 1
            self.vlc_speak.set_rate(1)
            self.speak("Stimme gewechselt zu IBM")

        elif self.voice == 1:
            self.voice = 0
            self.vlc_file.set_rate(1.3)
            self.speak("Stimme gewechselt zu Google")