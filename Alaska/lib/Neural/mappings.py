from Alaska.lib import Commands



class Mappings:
    def __init__(self, disablemqtt):
        self.disablemqtt = disablemqtt
        self.commands = Commands(self.disablemqtt)
        
        
    def get_mappings(self, training=False):
        if training or not self.disablemqtt:
            return {
                "greeting":     self.commands.greeting,
                "howlate":      self.commands.howlate,
                "weather":      self.commands.weather,
                "wind":         self.commands.wind,
                "sunrise":      self.commands.sunrise,
                "sunset":       self.commands.sunset,
                "voicechange":  self.commands.voicechange,
                "joke":         self.commands.joke,
                "definition":   self.commands.definition,
                "capital":      self.commands.capitalof,
                "calc":         self.commands.calc,
                "lighton":      self.commands.lighton,
                "lightoff":     self.commands.lightoff,
                "lampon":       self.commands.lampon,
                "lampoff":      self.commands.lampoff,
                "multilamppn":  self.commands.multilampon,
                "multilampoff": self.commands.multilampoff,
                "playlistplay": self.commands.playlistplay,
                "play":         self.commands.play,
                "pause":        self.commands.pause,
                "randomon":     self.commands.randomon,
                "randomoff":    self.commands.randomoff,
                "random":       self.commands.random,
                "setvolume":    self.commands.setvolume,
                "volumeup":     self.commands.volumeup,
                "volumedown":   self.commands.volumedown,
                "songlike":     self.commands.songlike,
                "songdislike":  self.commands.songdislike,
                "showplay":     self.commands.showplay,
                "trackskip":    self.commands.trackskip,
                "trackback":    self.commands.trackback
            }
        else:
            return {
                "greeting":     self.commands.greeting,
                "howlate":      self.commands.howlate,
                "weather":      self.commands.weather,
                "wind":         self.commands.wind,
                "sunrise":      self.commands.sunrise,
                "sunset":       self.commands.sunset,
                "voicechange":  self.commands.voicechange,
                "joke":         self.commands.joke,
                "definition":   self.commands.definition,
                "capital":      self.commands.capitalof,
                "calc":         self.commands.calc,
                "playlistplay": self.commands.playlistplay,
                "play":         self.commands.play,
                "pause":        self.commands.pause,
                "randomon":     self.commands.randomon,
                "randomoff":    self.commands.randomoff,
                "random":       self.commands.random,
                "setvolume":    self.commands.setvolume,
                "volumeup":     self.commands.volumeup,
                "volumedown":   self.commands.volumedown,
                "songlike":     self.commands.songlike,
                "songdislike":  self.commands.songdislike,
                "showplay":     self.commands.showplay,
                "trackskip":    self.commands.trackskip,
                "trackback":    self.commands.trackback
            }
