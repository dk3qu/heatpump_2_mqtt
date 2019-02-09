#!/usr/bin/python3
#
# -*- coding: utf-8 -*-
# --- ---
import time
import csv

# --- LOGGING ---
import os
import os.path
import json
import logging
import logging.config

# --- ---
from collection import Collection
from mqtt_client import MqttClient


def setup_logging(
        default_path='logging.json',
        default_level=logging.INFO,
        env_key='LOG_CFG'
):
    """
    Setup logging configuration
    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
    logging.debug("Logging eingerichtet")


setup_logging()

# ---------------
# Config
config = {}


def setup_config(
        default_path='config.json',
        env_key='CFG'
):
    global config
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    logging.debug("Config laden: {0}".format(path))
    if os.path.exists(path):
        try:
            with open(path, 'rt') as f:
                config = json.load(f)
            config["STATUS"] = True
            logging.debug("Config geladen")
        except ValueError as err:
            pass
            logging.error("Config konnte nicht geladen werden ! '{0}' -> {1}".format(path, err.args))
    else:
        config = {"STATUS": False}
        logging.error("Config konnte nicht gefunden werden !")


setup_config()


# ---------------

def wait_until(end_at):
    """
    Wartet bis es "end_at" ist ...
    :param end_at:
    :return:
    """
    while time.time() < end_at:
        time.sleep(0.1)
    return time.time()


# -----------------------------------------
# Run the program
# -----------------------------------------
if __name__ == '__main__':
    # logging.debug("--- Start ---")
    logging.info("--- Start --- {0}s warten bis alles da ist ...".format(config["main"]["wait"]))
    time.sleep(config["main"]["wait"])
    #
    # MQTT-Login  #TODO: User/Passwort & ClientID über die Config
    collection = Collection(config)
    mqtt = MqttClient(config)
    mqtt.loop_start()

    while True:
        #
        # jetzt ist es gerade ...
        t0 = time.time()
        t0_str = time.strftime("%d.%m.%Y %H:%M:%S")
        logging.info("--- {0} ----------".format(t0_str))
        #
        # Daten besorgen
        collection.collect_data()
        data = collection.get_all_data()  # TODO: ggf. die einzelnen Werte
        #
        # MQTT senden
        mqtt.pup_data(data)
        #
        # Logging der Werte
        # json #TODO: rotate
        if config["logging"]["json"]["enable"]:
            file = open(config["logging"]["json"]["filename"], "a")
            d = {"time": t0_str, "data": data}
            file.write(json.dumps(d))
            file.write("\n")
            file.close()
            pass
        #
        # csv #TODO: rotate
        if config["logging"]["csv"]["enable"]:
            if not os.path.isfile(config["logging"]["csv"]["filename"]):
                with open(config["logging"]["csv"]["filename"], 'w') as csvfile:
                    csvwriter = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
                    # TODO: hier Werte eintragen
                    csvwriter.writerow([
                        'Zeitstempel',
                        'temperature_outside',
                        'temperature_source_in',
                        'temperature_source_out',
                        'temperature_return_set',
                        'temperature_return',
                        'temperature_flow',
                        'state_heatingpump',
                        'state_compressor1',
                        'state'
                    ])

            with open(config["logging"]["csv"]["filename"], 'a') as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
                # TODO: hier Werte eintragen
                csvwriter.writerow([
                    t0_str,
                    str(data['temperature_outside']["value"]).replace('.', ','),
                    str(data['temperature_source_in']["value"]).replace('.', ','),
                    str(data['temperature_source_out']["value"]).replace('.', ','),
                    str(data['temperature_return_set']["value"]).replace('.', ','),
                    str(data['temperature_return']["value"]).replace('.', ','),
                    str(data['temperature_flow']["value"]).replace('.', ','),
                    data['state_heatingpump']["value"],
                    data['state_compressor1']["value"],
                    data['state']["value"]
                ])
        pass
        #
        # fertig.
        # warten ...
        logging.info("Warten: {0}s".format(config["heatpump"]["abtastung"]))
        #
        wait_until(t0 + config["heatpump"]["abtastung"])
        #
