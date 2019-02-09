import logging
from connection import Connection


class Collection:
    """

    """



    def __init__(self, config):
        """
        Erstellt die Connection und übergibt die benätigten Keys für die Wärmepumpe.
        """
        logging.debug("Collection - init")
        #
        self.__config = config
        self.__data = {}
        #
        self.__con = Connection(self.__config["heatpump"]["ip"],
                                self.__config["heatpump"]["user"],
                                self.__config["heatpump"]["pwd"])
        #
        self.__con.set_keys(["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A10", "A11", "A12", "A14", "A15", "I51"],
                            0)
        self.__con.set_keys(["A61"], 1)
        self.__con.set_keys([], 2)
        self.__con.set_keys([], 3)
        self.__con.set_keys([], 4)
        #
        self.__lauf = [1, 1, 1, 1, 1]
        self.__max_lauf = [1, 5, 10, 20, 120]
        # con.get_status()
        pass



    def collect_data(self):
        """
        Startet das Auslesen der Daten.
        """
        logging.debug("Collection - collect_data [{0},{1},{2},{3},{4}]".format(
            self.__lauf[0] - 1,
            self.__lauf[1] - 1,
            self.__lauf[2] - 1,
            self.__lauf[3] - 1,
            self.__lauf[4] - 1
        ))
        for i in range(0, 5):
            self.__lauf[i] -= 1
            if self.__lauf[i] < 1:
                logging.debug("Collection - collect_data KeySet:{0}".format(i))
                self.__lauf[i] = self.__max_lauf[i]
                _erg = self.__con.get_values(i)
                # print("Status: " + str(self.__con.get_status()))
                self.prepare(_erg)
        pass



    def get_all_data(self):
        """
        Gibt alle Daten zurück.
        """
        return self.__data



    def get_data(self, key):
        """
        Gibt die einzelnen Values der Keys mit richtigem Typ zurück.
        """
        logging.debug("Collection - get_data")
        pass



    def prepare(self, data):
        """
        Fügt die erhaltenen Daten in die passenden Keys ein.
        siehe: https://github.com/openhab/openhab1-addons/blob/master/bundles/binding/org.openhab.binding.ecotouch/src/main/java/org/openhab/binding/ecotouch/EcoTouchTags.java
        """
        logging.debug("Collection - prepare")

        #
        # "A1" : "temperature_outside"
        #
        try:
            val = data["A1"]
            key = "temperature_outside"
            if val["status"]:
                self.__data[key] = {
                    "key": key,
                    "value": int(val["value"]) / 10.0,
                    "name": "Außentemperatur",
                    "unit": "°C",
                    "time": val["time"],
                    "status": True
                }
                logging.debug(
                    "{0} = {1} {2}".format(self.__data[key]["key"], self.__data[key]["value"],
                                           self.__data[key]["unit"]))
            else:
                self.__data[key]["status"] = False
        except KeyError:
            pass

        #
        # "A2" : "temperature_outside_1h"
        #
        try:
            val = data["A2"]
            key = "temperature_outside_1h"
            if val["status"]:
                self.__data[key] = {
                    "key": key,
                    "value": int(val["value"]) / 10.0,
                    "name": "Außentemperatur 1h",
                    "unit": "°C",
                    "time": val["time"],
                    "status": True
                }
                logging.debug(
                    "{0} = {1} {2}".format(self.__data[key]["key"], self.__data[key]["value"],
                                           self.__data[key]["unit"]))
            else:
                self.__data[key]["status"] = False
        except KeyError:
            pass

        #
        # "A3" : "temperature_outside_24h"
        #
        try:
            val = data["A3"]
            key = "temperature_outside_24h"
            if val["status"]:
                self.__data[key] = {
                    "key": key,
                    "value": int(val["value"]) / 10.0,
                    "name": "Außentemperatur 24h",
                    "unit": "°C",
                    "time": val["time"],
                    "status": True
                }
                logging.debug(
                    "{0} = {1} {2}".format(self.__data[key]["key"], self.__data[key]["value"],
                                           self.__data[key]["unit"]))
            else:
                self.__data[key]["status"] = False
        except KeyError:
            pass

        #
        # "A4" : "temperature_source_in" : "Quelleneintrittstemperatur
        #
        try:
            val = data["A4"]
            key = "temperature_source_in"
            if val["status"]:
                self.__data[key] = {
                    "key": key,
                    "value": int(val["value"]) / 10.0,
                    "name": "Quelleneintrittstemperatur",
                    "unit": "°C",
                    "time": val["time"],
                    "status": True
                }
                logging.debug(
                    "{0} = {1} {2}".format(self.__data[key]["key"], self.__data[key]["value"],
                                           self.__data[key]["unit"]))
            else:
                self.__data[key]["status"] = False
        except KeyError:
            pass

        #
        # "A5" : "temperature_source_out"
        #
        try:
            val = data["A5"]
            key = "temperature_source_out"
            if val["status"]:
                self.__data[key] = {
                    "key": key,
                    "value": int(val["value"]) / 10.0,
                    "name": "Quellenaustrittstemperatur",
                    "unit": "°C",
                    "time": val["time"],
                    "status": True
                }
                logging.debug(
                    "{0} = {1} {2}".format(self.__data[key]["key"], self.__data[key]["value"],
                                           self.__data[key]["unit"]))
            else:
                self.__data[key]["status"] = False
        except KeyError:
            pass

        #
        # "A6" : "temperature_evaporation" : Verdampfungstemperatur
        #
        try:
            val = data["A6"]
            key = "temperature_evaporation"
            if val["status"]:
                self.__data[key] = {
                    "key": key,
                    "value": int(val["value"]) / 10.0,
                    "name": "Verdampfungstemperatur",
                    "unit": "°C",
                    "time": val["time"],
                    "status": True
                }
                logging.debug(
                    "{0} = {1} {2}".format(self.__data[key]["key"], self.__data[key]["value"],
                                           self.__data[key]["unit"]))
            else:
                self.__data[key]["status"] = False
        except KeyError:
            pass

        #
        # "A7" : "temperature_suction"
        #
        try:
            val = data["A7"]
            key = "temperature_suction"
            if val["status"]:
                self.__data[key] = {
                    "key": key,
                    "value": int(val["value"]) / 10.0,
                    "name": "Sauggastemperatur",
                    "unit": "°C",
                    "time": val["time"],
                    "status": True
                }
                logging.debug(
                    "{0} = {1} {2}".format(self.__data[key]["key"], self.__data[key]["value"],
                                           self.__data[key]["unit"]))
            else:
                self.__data[key]["status"] = False
        except KeyError:
            pass

        #
        # "A8" : "pressure_evaporation" : Verdampfungsdruck
        #
        try:
            val = data["A8"]
            key = "pressure_evaporation"
            if val["status"]:
                self.__data[key] = {
                    "key": key,
                    "value": int(val["value"]) / 10.0,
                    "name": "Verdampfungsdruck",
                    "unit": "bar",
                    "time": val["time"],
                    "status": True
                }
                logging.debug(
                    "{0} = {1} {2}".format(self.__data[key]["key"], self.__data[key]["value"],
                                           self.__data[key]["unit"]))
            else:
                self.__data[key]["status"] = False
        except KeyError:
            pass

        #
        # "A10" : "temperature_return_set" : "Temperatur Rücklauf Soll"
        #
        try:
            val = data["A10"]
            key = "temperature_return_set"
            if val["status"]:
                self.__data[key] = {
                    "key": key,
                    "value": int(val["value"]) / 10.0,
                    "name": "Temperatur Rücklauf Soll",
                    "unit": "°C",
                    "time": val["time"],
                    "status": True
                }
                logging.debug(
                    "{0} = {1} {2}".format(self.__data[key]["key"], self.__data[key]["value"],
                                           self.__data[key]["unit"]))
            else:
                self.__data[key]["status"] = False
        except KeyError:
            pass

        #
        # "A11" : "temperature_return" : "Temperatur Rücklauf"
        #
        try:
            val = data["A11"]
            key = "temperature_return"
            if val["status"]:
                self.__data[key] = {
                    "key": key,
                    "value": int(val["value"]) / 10.0,
                    "name": "Temperatur Rücklauf",
                    "unit": "°C",
                    "time": val["time"],
                    "status": True
                }
                logging.debug(
                    "{0} = {1} {2}".format(self.__data[key]["key"], self.__data[key]["value"],
                                           self.__data[key]["unit"]))
            else:
                self.__data[key]["status"] = False
        except KeyError:
            pass

        #
        # "A12" : "temperature_outside_1h" : "Temperatur Vorlauf"
        #
        try:
            val = data["A12"]
            key = "temperature_flow"
            if val["status"]:
                self.__data[key] = {
                    "key": key,
                    "value": int(val["value"]) / 10.0,
                    "name": "Temperatur Vorlauf",
                    "unit": "°C",
                    "time": val["time"],
                    "status": True
                }
                logging.debug(
                    "{0} = {1} {2}".format(self.__data[key]["key"], self.__data[key]["value"],
                                           self.__data[key]["unit"]))
            else:
                self.__data[key]["status"] = False
        except KeyError:
            pass

        #
        # "A14" : "temperature_condensation" : "Kondensationstemperatur"
        #
        try:
            val = data["A14"]
            key = "temperature_condensation"
            if val["status"]:
                self.__data[key] = {
                    "key": key,
                    "value": int(val["value"]) / 10.0,
                    "name": "Kondensationstemperatur",
                    "unit": "°C",
                    "time": val["time"],
                    "status": True
                }
                logging.debug(
                    "{0} = {1} {2}".format(self.__data[key]["key"], self.__data[key]["value"],
                                           self.__data[key]["unit"]))
            else:
                self.__data[key]["status"] = False
        except KeyError:
            pass

        #
        # "A15" : "pressure_condensation" : "Kondensationsdruck"
        #
        try:
            val = data["A15"]
            key = "pressure_condensation"
            if val["status"]:
                self.__data[key] = {
                    "key": key,
                    "value": int(val["value"]) / 10.0,
                    "name": "Kondensationsdruck",
                    "unit": "bar",
                    "time": val["time"],
                    "status": True
                }
                logging.debug(
                    "{0} = {1} {2}".format(self.__data[key]["key"], self.__data[key]["value"],
                                           self.__data[key]["unit"]))
            else:
                self.__data[key]["status"] = False
        except KeyError:
            pass

        #
        # "I51" : "state" : "Status der Wärmepumpenkomponenten"
        #
        try:
            val = data["I51"]
            key = "state"
            if val["status"]:
                self.__data[key] = {
                    "key": key,
                    "value": val["value"],
                    "name": "Status der Wärmepumpenkomponenten",
                    "unit": "",
                    "time": val["time"],
                    "status": True
                }
                logging.debug(
                    "{0} = {1} {2}".format(self.__data[key]["key"], self.__data[key]["value"],
                                           self.__data[key]["unit"]))
            else:
                self.__data[key]["status"] = False
        except KeyError:
            pass

        #
        # "I51.0" : "state_sourcepump" : "Status der Wärmepumpenkomponenten: Quellenpumpe"
        #
        try:
            val = data["I51"]
            key = "state_sourcepump"
            if val["status"]:
                self.__data[key] = {
                    "key": key,
                    "value": (("{:08b}".format(int(val["value"])))[::-1] + '00000000000')[0] == '1',
                    "name": "Status der Wärmepumpenkomponenten: Quellenpumpe",
                    "unit": "",
                    "time": val["time"],
                    "status": True
                }
                logging.debug(
                    "{0} = {1} {2}".format(self.__data[key]["key"], self.__data[key]["value"],
                                           self.__data[key]["unit"]))
            else:
                self.__data[key]["status"] = False
        except KeyError:
            pass

        #
        # "I51.1" : "state_heatingpump" : "Status der Wärmepumpenkomponenten: Heizungsumwälzpumpe"
        #
        try:
            val = data["I51"]
            key = "state_heatingpump"
            if val["status"]:
                self.__data[key] = {
                    "key": key,
                    "value": (("{:08b}".format(int(val["value"])))[::-1] + '00000000000')[1] == '1',
                    "name": "Status der Wärmepumpenkomponenten: Heizungsumwälzpumpe",
                    "unit": "",
                    "time": val["time"],
                    "status": True
                }
                logging.debug(
                    "{0} = {1} {2}".format(self.__data[key]["key"], self.__data[key]["value"],
                                           self.__data[key]["unit"]))
            else:
                self.__data[key]["status"] = False
        except KeyError:
            pass

        #
        # "I51.2" : "state_evd" : "Status der Wärmepumpenkomponenten: Freigabe Regelung EVD"
        #
        try:
            val = data["I51"]
            key = "state_evd"
            if val["status"]:
                self.__data[key] = {
                    "key": key,
                    "value": (("{:08b}".format(int(val["value"])))[::-1] + '00000000000')[2] == '1',
                    "name": "Status der Wärmepumpenkomponenten: Freigabe Regelung EVD",
                    "unit": "",
                    "time": val["time"],
                    "status": True
                }
                logging.debug(
                    "{0} = {1} {2}".format(self.__data[key]["key"], self.__data[key]["value"],
                                           self.__data[key]["unit"]))
            else:
                self.__data[key]["status"] = False
        except KeyError:
            pass

        #
        # "I51.3" : "state_compressor1" : "Status der Wärmepumpenkomponenten: Verdichter 1"
        #
        try:
            val = data["I51"]
            key = "state_compressor1"
            if val["status"]:
                self.__data[key] = {
                    "key": key,
                    "value": (("{:08b}".format(int(val["value"])))[::-1] + '00000000000')[3] == '1',
                    "name": "Status der Wärmepumpenkomponenten: Verdichter 1",
                    "unit": "",
                    "time": val["time"],
                    "status": True
                }
                logging.debug(
                    "{0} = {1} {2}".format(self.__data[key]["key"], self.__data[key]["value"],
                                           self.__data[key]["unit"]))
            else:
                self.__data[key]["status"] = False
        except KeyError:
            pass

        #
        # "I51.4" : "state_compressor2" : "Status der Wärmepumpenkomponenten: Verdichter 2"
        #
        try:
            val = data["I51"]
            key = "state_compressor2"
            if val["status"]:
                self.__data[key] = {
                    "key": key,
                    "value": (("{:08b}".format(int(val["value"])))[::-1] + '00000000000')[4] == '1',
                    "name": "Status der Wärmepumpenkomponenten: Verdichter 2",
                    "unit": "",
                    "time": val["time"],
                    "status": True
                }
                logging.debug(
                    "{0} = {1} {2}".format(self.__data[key]["key"], self.__data[key]["value"],
                                           self.__data[key]["unit"]))
            else:
                self.__data[key]["status"] = False
        except KeyError:
            pass

        #
        # "I51.5" : "state_extheater" : "Status der Wärmepumpenkomponenten: externer Wärmeerzeuger"
        #
        try:
            val = data["I51"]
            key = "state_extheater"
            if val["status"]:
                self.__data[key] = {
                    "key": key,
                    "value": (("{:08b}".format(int(val["value"])))[::-1] + '00000000000')[5] == '1',
                    "name": "Status der Wärmepumpenkomponenten: externer Wärmeerzeuger",
                    "unit": "",
                    "time": val["time"],
                    "status": True
                }
                logging.debug(
                    "{0} = {1} {2}".format(self.__data[key]["key"], self.__data[key]["value"],
                                           self.__data[key]["unit"]))
            else:
                self.__data[key]["status"] = False
        except KeyError:
            pass

        #
        # "I51.6" : "state_alarm" : "Status der Wärmepumpenkomponenten: Alarmausgang"
        #
        try:
            val = data["I51"]
            key = "state_alarm"
            if val["status"]:
                self.__data[key] = {
                    "key": key,
                    "value": (("{:08b}".format(int(val["value"])))[::-1] + '00000000000')[6] == '1',
                    "name": "Status der Wärmepumpenkomponenten: Alarmausgang",
                    "unit": "",
                    "time": val["time"],
                    "status": True
                }
                logging.debug(
                    "{0} = {1} {2}".format(self.__data[key]["key"], self.__data[key]["value"],
                                           self.__data[key]["unit"]))
            else:
                self.__data[key]["status"] = False
        except KeyError:
            pass

        #
        # "I51.7" : "state_cooling" : "Status der Wärmepumpenkomponenten: Motorventil Kühlbetrieb"
        #
        try:
            val = data["I51"]
            key = "state_cooling"
            if val["status"]:
                self.__data[key] = {
                    "key": key,
                    "value": (("{:08b}".format(int(val["value"])))[::-1] + '00000000000')[7] == '1',
                    "name": "Status der Wärmepumpenkomponenten: Motorventil Kühlbetrieb",
                    "unit": "",
                    "time": val["time"],
                    "status": True
                }
                logging.debug(
                    "{0} = {1} {2}".format(self.__data[key]["key"], self.__data[key]["value"],
                                           self.__data[key]["unit"]))
            else:
                self.__data[key]["status"] = False
        except KeyError:
            pass

        #
        # "I51.8" : "state_water" : "Status der Wärmepumpenkomponenten: Motorventil Warmwasser"
        #
        try:
            val = data["I51"]
            key = "state_water"
            if val["status"]:
                self.__data[key] = {
                    "key": key,
                    "value": (("{:08b}".format(int(val["value"])))[::-1] + '00000000000')[8] == '1',
                    "name": "Status der Wärmepumpenkomponenten: Motorventil Warmwasser",
                    "unit": "",
                    "time": val["time"],
                    "status": True
                }
                logging.debug(
                    "{0} = {1} {2}".format(self.__data[key]["key"], self.__data[key]["value"],
                                           self.__data[key]["unit"]))
            else:
                self.__data[key]["status"] = False
        except KeyError:
            pass

        #
        # "I51.9" : "state_pool" : "Status der Wärmepumpenkomponenten: Motorventil Pool"
        #
        try:
            val = data["I51"]
            key = "state_pool"
            if val["status"]:
                self.__data[key] = {
                    "key": key,
                    "value": (("{:08b}".format(int(val["value"])))[::-1] + '00000000000')[9] == '1',
                    "name": "Status der Wärmepumpenkomponenten: Motorventil Pool",
                    "unit": "",
                    "time": val["time"],
                    "status": True
                }
                logging.debug(
                    "{0} = {1} {2}".format(self.__data[key]["key"], self.__data[key]["value"],
                                           self.__data[key]["unit"]))
            else:
                self.__data[key]["status"] = False
        except KeyError:
            pass

        #
        # "I51.10" : "state_solar" : "Status der Wärmepumpenkomponenten: Solarbetrieb"
        #
        try:
            val = data["I51"]
            key = "state_solar"
            if val["status"]:
                self.__data[key] = {
                    "key": key,
                    "value": (("{:08b}".format(int(val["value"])))[::-1] + '00000000000')[10] == '1',
                    "name": "Status der Wärmepumpenkomponenten: Solarbetrieb",
                    "unit": "",
                    "time": val["time"],
                    "status": True
                }
                logging.debug(
                    "{0} = {1} {2}".format(self.__data[key]["key"], self.__data[key]["value"],
                                           self.__data[key]["unit"]))
            else:
                self.__data[key]["status"] = False
        except KeyError:
            pass

        #
        # "I51.11" : "state_cooling4way" : "Status der Wärmepumpenkomponenten: 4-Wegeventil im Kältekreis"
        #
        try:
            val = data["I51"]
            key = "state_cooling4way"
            if val["status"]:
                self.__data[key] = {
                    "key": key,
                    "value": (("{:08b}".format(int(val["value"])))[::-1] + '00000000000')[11] == '1',
                    "name": "Status der Wärmepumpenkomponenten: 4-Wegeventil im Kältekreis",
                    "unit": "",
                    "time": val["time"],
                    "status": True
                }
                logging.debug(
                    "{0} = {1} {2}".format(self.__data[key]["key"], self.__data[key]["value"],
                                           self.__data[key]["unit"]))
            else:
                self.__data[key]["status"] = False
        except KeyError:
            pass

        #
        # "A61" : "hysteresis_heating" : "Hysterese Heizung"
        #
        try:
            val = data["A61"]
            key = "hysteresis_heating"
            if val["status"]:
                self.__data[key] = {
                    "key": key,
                    "value": int(val["value"]) / 10.0,
                    "name": "Hysterese Heizung",
                    "unit": "°C",
                    "time": val["time"],
                    "status": True
                }
                logging.debug(
                    "{0} = {1} {2}".format(self.__data[key]["key"], self.__data[key]["value"],
                                           self.__data[key]["unit"]))
            else:
                self.__data[key]["status"] = False
        except KeyError:
            pass




        #
        #print()
        pass
