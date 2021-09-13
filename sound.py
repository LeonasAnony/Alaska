import speech_recognition as sr
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from gtts import gTTS
import vlc
import config as cfg

authenticator = IAMAuthenticator(cfg.ibm_cfg["api_key"])
text_to_speech = TextToSpeechV1(authenticator=authenticator)
text_to_speech.set_service_url(cfg.ibm_cfg["service_url"])


class SoundHandler:
    def __init__(self):
        self.vlc_speak = vlc.MediaPlayer()
        self.vlc_speak.set_rate(1.3)

        self.vlc_file = vlc.MediaPlayer()
        self.vlc_file.set_rate(1)

        self.voice = 0

        self.r = sr.Recognizer()

    def speak(self, tts_string):
        print(tts_string)
        if self.voice == 0:
            tts = gTTS(text=tts_string, lang='de', )
            tts.save("speak.mp3")

        elif self.voice == 1:
            with open('speak.mp3', 'wb') as audio_file:
                audio_file.write(text_to_speech.synthesize(tts_string, voice='de-DE_DieterV3Voice', accept='audio/mp3')
                                 .get_result().content)

        speak_file = vlc.Media("speak.mp3")
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
            with sr.Microphone(device_index=8) as source:
                print("Say something!")
                self.r.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.r.listen(source)

            try:
                data_raw = self.r.recognize_google(audio, language="de")
                data_lower = data_raw.lower()
                print("You said: " + data_raw)
                understood = True
                return data_lower.replace(" eins ", " 1 ").replace(" zwei ", " 2 ").replace(" drei ", " 3 ")\
                    .replace("vier ", " 4 ").replace(" fünf ", " 5 ").replace(" sechs ", " 6 ")\
                    .replace(" sieben ", " 7 ").replace(" acht ", " 8 ").replace(" neun ", " 9 ")\
                    .replace(" zehn ", " 10 ")
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")

    def change_voice(self):
        if self.voice == 0:
            self.voice = 1
            self.vlc_speak.set_rate(1)
            self.speak("Stimme gewechselt zu IBM")

        elif self.voice == 1:
            self.voice = 0
            self.vlc_file.set_rate(1.3)
            self.speak("Stimme gewechselt zu Google")
