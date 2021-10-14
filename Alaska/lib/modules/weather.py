from pyowm.owm import OWM
from pyowm.utils.config import get_default_config
from Alaska import config as cfg


config_dict = get_default_config()
config_dict['language'] = 'de'

owm = OWM(cfg.owm_cfg["api_key"], config_dict)


def direction(degree):
    if 337 < degree < 361 or 0 <= degree < 23:
        return "Nord"
    elif 22 < degree < 68:
        return "Nordost"
    elif 67 < degree < 113:
        return "Ost"
    elif 112 < degree < 158:
        return "Südost"
    elif 157 < degree < 203:
        return "Süd"
    elif 202 < degree < 248:
        return "Südwest"
    elif 247 < degree < 293:
        return "West"
    elif 292 < degree < 338:
        return "Nordwest"


class Weather:
    def __init__(self, data):
        data_split = data.split(" ")
        if "in" in data:
            city = data_split.index("in")
            self.location = data_split[city + 1]
        elif "für" in data:
            city = data_split.index("für")
            self.location = data_split[city + 1]
        else:
            print("No city specified. Standard is " + cfg.owm_cfg["std_city"] + ", " + cfg.owm_cfg["std_country"] + ".")
            self.location = cfg.owm_cfg["std_city"]
        mgr = owm.weather_manager()
        observation = mgr.weather_at_place(self.location + "," + cfg.owm_cfg["std_country"])
        self.weather = observation.weather

    def status(self):
        return self.location, self.weather.detailed_status

    def wind(self):
        return self.location, self.weather.wind()["speed"], self.weather.wind()["deg"], direction(self.weather.wind(["deg"]))

    def sunrise(self):
        return self.location, self.weather.sunrise_time(timeformat='date')

    def sunset(self):
        return self.location, self.weather.sunset_time(timeformat='date')
