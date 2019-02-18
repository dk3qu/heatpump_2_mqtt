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
        self.pup_value(data, root, "temp_outside", "temp_outside")
        self.pup_value(data, root, "temp_outside_1h", "temp_outside_1h")
        self.pup_value(data, root, "temp_outside_24h", "temp_outside_24h")
        self.pup_value(data, root, "temp_source_in", "temp_source_in")
        self.pup_value(data, root, "temp_source_out", "temp_source_out")
        self.pup_value(data, root, "temp_evaporation", "temp_evaporation")
        self.pup_value(data, root, "temp_suction", "temp_suction")
        self.pup_value(data, root, "press_evaporation", "press_evaporation")
        self.pup_value(data, root, "temp_return_set", "temp_return_set")
        self.pup_value(data, root, "temp_return", "temp_return")
        self.pup_value(data, root, "temp_flow", "temp_flow")
        self.pup_value(data, root, "temp_condensation2", "temp_condensation2")
        self.pup_value(data, root, "temp_condensation", "temp_condensation")
        self.pup_value(data, root, "press_condensation", "press_condensation")
        self.pup_value(data, root, "temp_water", "temp_water")
        self.pup_value(data, root, "power_compressor", "power_compressor")
        self.pup_value(data, root, "power_heating", "power_heating")
        self.pup_value(data, root, "power_cooling", "power_cooling")
        self.pup_value(data, root, "cop_heating", "cop_heating")
        self.pup_value(data, root, "cop_cooling", "cop_cooling")
        self.pup_value(data, root, "temp_heating", "temp_heating")
        self.pup_value(data, root, "temp_heating_set", "temp_heating_set")
        self.pup_value(data, root, "temp_cooling_return", "temp_cooling_return")
        self.pup_value(data, root, "temp_cooling_set", "temp_cooling_set")
        self.pup_value(data, root, "temp_water_set", "temp_water_set")
        self.pup_value(data, root, "temp_water_set2", "temp_water_set2")
        self.pup_value(data, root, "hysteresis_heating", "hysteresis_heating")
        self.pup_value(data, root, "temp_out_1h_heating", "temp_out_1h_heating")
        self.pup_value(data, root, "temp_nvi_outside_x1", "temp_nvi_outside_x1")
        self.pup_value(data, root, "temp_nvi_heating_y1", "temp_nvi_heating_y1")
        self.pup_value(data, root, "temp_nvi_outside_x2", "temp_nvi_outside_x2")
        self.pup_value(data, root, "temp_nvi_heating_y2", "temp_nvi_heating_y2")
        self.pup_value(data, root, "nvi_temp_max", "nvi_temp_max")
        self.pup_value(data, root, "temp_nvi_heating_set", "temp_nvi_heating_set")
        self.pup_value(data, root, "temp_set_0deg", "temp_set_0deg")
        self.pup_value(data, root, "hysteresis_cooling", "hysteresis_cooling")
        self.pup_value(data, root, "temp_cooling_enable", "temp_cooling_enable")
        self.pup_value(data, root, "temp_cooling", "temp_cooling")
        self.pup_value(data, root, "hysteresis_water", "hysteresis_water")
        self.pup_value(data, root, "temp_dt", "temp_dt")
        self.pup_value(data, root, "temp_source_dt", "temp_source_dt")
        self.pup_value(data, root, "expansion_valve", "expansion_valve")
        self.pup_value(data, root, "date_day", "date_day")
        self.pup_value(data, root, "date_month", "date_month")
        self.pup_value(data, root, "date_year", "date_year")
        self.pup_value(data, root, "time_hour", "time_hour")
        self.pup_value(data, root, "time_minute", "time_minute")
        self.pup_value(data, root, "operating_hours_compressor1", "operating_hours_compressor1")
        self.pup_value(data, root, "operating_hours_compressor2", "operating_hours_compressor2")
        self.pup_value(data, root, "operating_hours_circulation_pump", "operating_hours_circulation_pump")
        self.pup_value(data, root, "operating_hours_source_pump", "operating_hours_source_pump")
        self.pup_value(data, root, "operating_hours_solar", "operating_hours_solar")
        self.pup_value(data, root, "enable_heating", "enable_heating")
        self.pup_value(data, root, "enable_cooling", "enable_cooling")
        self.pup_value(data, root, "enable_warmwater", "enable_warmwater")
        self.pup_value(data, root, "enable_pool", "enable_pool")
        self.pup_value(data, root, "enable_pv", "enable_pv")
        self.pup_value(data, root, "alarm", "alarm")
        self.pup_value(data, root, "interruptions", "interruptions")
        self.pup_value(data, root, "state_service", "state_service")
        self.pup_value(data, root, "adapt_heating", "adapt_heating")
        self.pup_value(data, root, "manual_heatingpump", "manual_heatingpump")
        self.pup_value(data, root, "manual_sourcepump", "manual_sourcepump")
        self.pup_value(data, root, "manual_solarpump1", "manual_solarpump1")
        self.pup_value(data, root, "manual_solarpump2", "manual_solarpump2")
        self.pup_value(data, root, "manual_tankpump", "manual_tankpump")
        self.pup_value(data, root, "manual_valve", "manual_valve")
        self.pup_value(data, root, "manual_poolvalve", "manual_poolvalve")
        self.pup_value(data, root, "manual_coolvalve", "manual_coolvalve")
        self.pup_value(data, root, "manual_4wayvalve", "manual_4wayvalve")
        self.pup_value(data, root, "manual_multiext", "manual_multiext")
        self.pup_value(data, root, "temp_surrounding", "temp_surrounding")
        self.pup_value(data, root, "temp_suction_air", "temp_suction_air")
        self.pup_value(data, root, "temp_sump", "temp_sump")

        self.pup_value(data, root, "state", "state")
        self.pup_value(data, root, "state_sourcepump", "state_sourcepump")
        self.pup_value(data, root, "state_heatingpump", "state_heatingpump")
        self.pup_value(data, root, "state_evd", "state_evd")
        self.pup_value(data, root, "state_compressor1", "state_compressor1")
        self.pup_value(data, root, "state_extheater", "state_extheater")
        self.pup_value(data, root, "state_alarm", "state_alarm")
        self.pup_value(data, root, "state_cooling", "state_cooling")
        self.pup_value(data, root, "state_water", "state_water")
        self.pup_value(data, root, "state_pool", "state_pool")
        self.pup_value(data, root, "state_solar", "state_solar")
        self.pup_value(data, root, "state_cooling4way", "state_cooling4way")

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
