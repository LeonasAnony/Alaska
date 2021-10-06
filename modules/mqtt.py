from paho.mqtt import client as mqtt_client
import config as cfg

lights = ["V4", "V13", "V14", "V15", "V16", "V17", "V18", "V19", "V21", "V22"]
topic = cfg.mqtt_cfg["topic"]


class MQTT:
    def __init__(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        self.client = mqtt_client.Client(cfg.mqtt_cfg["client_id"])
        self.client.username_pw_set(cfg.mqtt_cfg["username"], cfg.mqtt_cfg["password"])
        self.client.on_connect = on_connect
        self.client.connect(cfg.mqtt_cfg["broker"], cfg.mqtt_cfg["port"])
        self.client.loop_start()

    def light(self, lt="light/all", pl="off", l_n=None):
        if lt == "light/n":
            if pl == 0:
                self.client.publish(topic + lights[int(l_n) - 1], "off")
            if pl == 1:
                self.client.publish(topic + lights[int(l_n) - 1], "on")
        if lt == "light/all":
            if pl == 0:
                self.client.publish(topic + "all", "off")
            if pl == 1:
                self.client.publish(topic + "all", "on")

    def publish(self, topic=None, message=None, qos=0):
        self.client.publish(topic=topic, payload=message, qos=qos)

    """
    def subscribe(client: mqtt_client):
        def on_message(client, userdata, msg):
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

        client.subscribe(topic)
        client.on_message = on_message
    """
