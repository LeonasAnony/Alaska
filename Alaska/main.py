# Alaska - Voice Assistant

# TODO:
#   Rebuild Command detection (Jellyfish/ NeuralIntents)
#   Splitting main.py into modules
#   Rebuild Wake word detection
#       Multi-Threading (multiple short detection threads)
#   Error Handling
#   Englisch translation
#   Rebuilding/ Optimizing modules
#   Documenting the code
#   Optimizing performance

import threading
import time

from Alaska import config as cfg
from Alaska.lib.Neural.neuralintents import GenericAssistant
from Alaska.lib.modules.sound import Sound



class AlaskaThreads(threading.Thread):
    def __init__(self, fredid, name):
        threading.Thread.__init__(self)
        self.iD = fredid
        self.name = name



class Alaska():
    def __init__(self, mapping, input_mode):
        self.sh = Sound()
        self.assistant = GenericAssistant('Alaska/lib/Neural/Alaska_German-1.0.0.json', intent_methods=mapping.get_mappings(), model_name="German-1.0.0")
        self.assistant.load_model()
        self.said = 0
        self.threads_start(input_mode)
    

    def wake_word(self, record):
        if self.said == 0:
            if "alaska" in record:
                self.sh.file_play("Alaska/data/audio/recognition.mp3")
                time.sleep(0.2)
                self.said = 1

            else:
                print("Alaska wasn´t called")
                self.said = 0

        elif self.said == 1:
            self.assistant.request(record)
            self.said = 0


    def wakeword_loop(self):
        while True:
            self.wake_word(self.sh.record_audio())
            
    
    def terminal_loop(self):
        while True:
            command = input("Input Command: ")
            self.assistant.request(command)
            
    
    def threads_start(self, terminal):
        if terminal:
            self.tl = threading.Thread(target=self.terminal_loop)

            self.tl.start()
        else:
            self.sh.file_play("Alaska/data/audio/welcome.mp3")
            time.sleep(2)

            self.wl = threading.Thread(target=self.wakeword_loop)

            self.wl.start()
