import paho.mqtt.client as mqtt
import logging
import time


class MqttClient:

    def __init__(self, config):
        """

        """
        self.__config = config
        self.__connected = False
        #

        self.__client = mqtt.Client()
        self.__client.on_connect = self.on_connect
        self.__client.on_disconnect = self.on_disconnect
        self.__client.on_message = self.on_message

        self.__client.connect(self.__config["mqtt"]["ip"], self.__config["mqtt"]["port"])
        logging.debug("MqttClient - init")

        pass



    def loop_start(self):
        logging.debug("MqttClient - loop_start")
        self.__client.loop_start()



    def loop_stop(self):
        logging.debug("MqttClient - loop_stop")
        self.__client.loop_stop()



    def on_connect(self):
        logging.debug("MqttClient - on_connect")
        self.__connected = True



    def on_disconnect(self):
        logging.debug("MqttClient - on_disconnect")
        self.__connected = False



    def on_message(self, client, userdata, message):
        logging.debug("MqttClient - on_message")
        print(message.payload.decode())
        print(message.topic)



    def sub_data(self):
        """
        Besorgt zusätzliche Daten von anderen Geräten.
        z.B.: Termometer im Raum oder Draussen.
        """
        logging.debug("MqttClient - sub_data")

        pass



    def pup_data(self, data):
        """
        Sendet ausgewählte Daten in den MQTT-Server

        wp
            time
            temperature_outside
            temperature_source_in
            temperature_source_out
            temperature_return_set
            temperature_return
            temperature_flow
            state_heatingpump
            state_compressor1
            state

        """
        logging.debug("MqttClient - pup_data")

        root = self.__config["mqtt"]["topics"]["root"]
        #
        self.pup_value(data, root, "temperature_outside", "temperature_outside")
        self.pup_value(data, root, "temperature_source_in", "temperature_source_in")
        self.pup_value(data, root, "temperature_source_out", "temperature_source_out")
        self.pup_value(data, root, "temperature_return_set", "temperature_return_set")
        self.pup_value(data, root, "temperature_return", "temperature_return")
        self.pup_value(data, root, "temperature_flow", "temperature_flow")
        self.pup_value(data, root, "state_heatingpump", "state_heatingpump")
        self.pup_value(data, root, "state_compressor1", "state_compressor1")
        self.pup_value(data, root, "state", "state")
        #

        pass



    def pup_value(self, data, root, key, key_data):
        self.__client.publish(topic="/{0}/{1}/key".format(root, key), payload=str(data[key_data]["key"]))
        self.__client.publish(topic="/{0}/{1}/value".format(root, key), payload=str(data[key_data]["value"]))
        self.__client.publish(topic="/{0}/{1}/name".format(root, key), payload=str(data[key_data]["name"]))
        self.__client.publish(topic="/{0}/{1}/unit".format(root, key), payload=str(data[key_data]["unit"]))
        self.__client.publish(topic="/{0}/{1}/time".format(root, key), payload=str(data[key_data]["time"]))
        self.__client.publish(topic="/{0}/{1}/status".format(root, key), payload=str(data[key_data]["status"]))
        self.__client.publish(topic="/{0}/{1}/str".format(root, key),
                              payload="{0} {1}".format(data[key]["value"], data[key_data]["unit"]))
