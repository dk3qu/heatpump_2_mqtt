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
        self.__con.set_keys([
            "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A10", "A11", "A12", "A13", "A14", "A15", "A19", "A25",
            "A26", "A27", "A28", "A29", "A30", "A31", "A33", "A34", "A37", "A38", "A61", "A90", "A91", "A92", "A93",
            "A94", "A95", "A96", "A97", "A107", "A108", "A109", "A139", "A1014", "A1035", "A1469", "I8", "I9", "I30",
            "I31", "I32", "I51", "I52", "I53"],
            0)
        self.__con.set_keys([], 1)
        self.__con.set_keys([], 2)
        self.__con.set_keys(
            ["I5", "I6", "I7", "I10", "I14", "I18", "I20", "I22", "I33", "I41", "I135", "I263", "I1270", "I1281",
             "I1287", "I1289", "I1291", "I1293", "I1295", "I1297", "I1299", "I1319", "I2020", "I2021", "I2023"],
            3)
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



    def into_data_int(self, data, keyname, command, german, unitname):
        try:
            val = data[keyname]
            if val["status"]:
                self.__data[command] = {
                    "key": command,
                    "value": int(val["value"]),
                    "name": german,
                    "unit": unitname,
                    "time": val["time"],
                    "status": True
                }
                logging.debug(
                    "{0} = {1} {2}".format(self.__data[command]["key"], self.__data[command]["value"],
                                           self.__data[command]["unit"]))
            else:
                self.__data[command]["status"] = False
        except KeyError:
            pass



    def into_data_float(self, data, keyname, command, german, unitname):
        try:
            val = data[keyname]
            if val["status"]:
                self.__data[command] = {
                    "key": command,
                    "value": int(val["value"]) / 10.0,
                    "name": german,
                    "unit": unitname,
                    "time": val["time"],
                    "status": True
                }
                logging.debug(
                    "{0} = {1} {2}".format(self.__data[command]["key"], self.__data[command]["value"],
                                           self.__data[command]["unit"]))
            else:
                self.__data[command]["status"] = False
        except KeyError:
            pass



    def prepare(self, data):
        """
        Fügt die erhaltenen Daten in die passenden Keys ein.
        siehe: https://github.com/openhab/openhab1-addons/blob/master/bundles/binding/org.openhab.binding.ecotouch/src/main/java/org/openhab/binding/ecotouch/EcoTouchTags.java
        """
        logging.debug("Collection - prepare")

        #
        #
        #

        self.into_data_float(data, "A1", "temp_outside", "Außentemperatur", "°C")
        self.into_data_float(data, "A2", "temp_outside_1h", "Außentemperatur gemittelt über 1h", "°C")
        self.into_data_float(data, "A3", "temp_outside_24h", "Außentemperatur gemittelt über 24h", "°C")
        self.into_data_float(data, "A4", "temp_source_in", "Quelle Eintritt Temp.", "°C")
        self.into_data_float(data, "A5", "temp_source_out", "Quelle Austritt Temp.", "°C")
        self.into_data_float(data, "A6", "temp_evaporation", "Verdampfungs Temp.", "°C")
        self.into_data_float(data, "A7", "temp_suction", "Sauggastemperatur", "°C")
        self.into_data_float(data, "A8", "press_evaporation", "Verdampfungsdruck", "bar")
        self.into_data_float(data, "A10", "temp_return_set", "Temperatur Rücklauf Soll", "°C")
        self.into_data_float(data, "A11", "temp_return", "Temperatur Rücklauf", "°C")
        self.into_data_float(data, "A12", "temp_flow", "Temperatur Vorlauf", "°C")
        self.into_data_float(data, "A13", "temp_condensation2", "Kondensationstemperatur 2", "°C")
        self.into_data_float(data, "A14", "temp_condensation", "Kondensationstemperatur", "°C")
        self.into_data_float(data, "A15", "press_condensation", "Kondensationsdruck", "bar")
        self.into_data_float(data, "A19", "temp_water", "Warmwasser-Temp. Aktuell", "°C")
        self.into_data_float(data, "A25", "power_compressor", "elektrische Leistung Verdichter", "kW")
        self.into_data_float(data, "A26", "power_heating", "abgegebene thermische Heizleistung der Wärmepumpe", "kW")
        self.into_data_float(data, "A27", "power_cooling", "abgegebene thermische KälteLeistung der Wärmepumpe", "kW")
        self.into_data_float(data, "A28", "cop_heating", "COP Heizleistung", "")
        self.into_data_float(data, "A29", "cop_cooling", "COP Kälteleistungleistung", "")
        self.into_data_float(data, "A30", "temp_heating", "Heizen-Temp. Akt. Rücklauf", "°C")
        self.into_data_float(data, "A31", "temp_heating_set", "Heizen-Temp. Soll", "°C")
        self.into_data_float(data, "A33", "temp_cooling_return", "Aktuelle Kühlkreistemperatur", "°C")
        self.into_data_float(data, "A34", "temp_cooling_set", "Geforderte Temperatur im Kühlbetrieb", "°C")
        self.into_data_float(data, "A37", "temp_water_set", "Warmwasser-Temp. Soll", "°C")
        self.into_data_float(data, "A38", "temp_water_set2", "Warmwasser-Temp. Sollwert", "°C")
        self.into_data_float(data, "A61", "hysteresis_heating", "Schaltdifferenz Heizen", "°C")
        self.into_data_float(data, "A90", "temp_out_1h_heating", "Heizkurve - Außentemperatur 1h", "°C")
        self.into_data_float(data, "A91", "temp_nvi_outside_x1", "Heizkurve - T-Norm-Aussen (x1)", "°C")
        self.into_data_float(data, "A92", "temp_nvi_heating_y1", "Heizkurve - T-Heizkreis-Norm (y1)", "°C")
        self.into_data_float(data, "A93", "temp_nvi_outside_x2", "Heizkurve - T-Heizgrenze (x2)", "°C")
        self.into_data_float(data, "A94", "temp_nvi_heating_y2", "Heizkurve - T-Heizgrenze-Soll (y2)", "°C")
        self.into_data_float(data, "A95", "nvi_temp_max", "Heizkurve max. VL-Temp", "°C")
        self.into_data_float(data, "A96", "temp_nvi_heating_set", "Heiztemperatur Soll", "°C")
        self.into_data_float(data, "A97", "temp_set_0deg", "Heizkreis Soll-Temp bei 0° Aussen", "°C")
        self.into_data_float(data, "A107", "hysteresis_cooling", "Schaltdifferenz Kühlen", "°C")
        self.into_data_float(data, "A108", "temp_cooling_enable", "Kühlen Einschalt-Temp. Aussentemp", "°C")
        self.into_data_float(data, "A109", "temp_cooling", "Heizkurve - nviSollKuehlen", "°C")
        self.into_data_float(data, "A139", "hysteresis_water", "Schaltdifferenz Warmwasser", "°C")
        self.into_data_float(data, "A1014", "temp_dt", "Temperatur dT", "°C")
        self.into_data_float(data, "A1035", "temp_source_dt", "Quelle dT", "°C")
        self.into_data_float(data, "A1469", "expansion_valve", "% Ventilöffnung elektrisches Expansionsventil", "%")
        self.into_data_int(data, "I5", "date_day", "Datum: Tag", "")
        self.into_data_int(data, "I6", "date_month", "Datum: Monat", "")
        self.into_data_int(data, "I7", "date_year", "Datum: Jahr", "")
        self.into_data_int(data, "I8", "time_hour", "Uhrzeit: Stunde", "")
        self.into_data_int(data, "I9", "time_minute", "Uhrzeit: Minute", "")
        self.into_data_int(data, "I10", "operating_hours_compressor1", "Betriebsstunden Verdichter 1", "h")
        self.into_data_int(data, "I14", "operating_hours_compressor2", "Betriebsstunden Verdichter 2", "h")
        self.into_data_int(data, "I18", "operating_hours_circulation_pump", "Betriebsstunden Heizungsumwälzpumpe",
                             "h")
        self.into_data_int(data, "I20", "operating_hours_source_pump", "Betriebsstunden Quellenpumpe", "h")
        self.into_data_int(data, "I22", "operating_hours_solar", "Betriebsstunden Solarkreis", "h")
        self.into_data_int(data, "I30", "enable_heating", "Handabschaltung Heizbetrieb", "")
        self.into_data_int(data, "I31", "enable_cooling", "Handabschaltung Kühlbetrieb", "")
        self.into_data_int(data, "I32", "enable_warmwater", "Handabschaltung Warmwasserbetrieb", "")
        self.into_data_int(data, "I33", "enable_pool", "Handabschaltung Pool_Heizbetrieb", "")
        self.into_data_int(data, "I41", "enable_pv", "Betriebsmodus PV 0=Aus, 1=Auto, 2=Ein", "")
        self.into_data_int(data, "I52", "alarm", "Meldungen von Ausfällen F0xx die zum Wärmepumpenausfall führen", "")
        self.into_data_int(data, "I53", "interruptions", "Unterbrechungen", "")
        self.into_data_int(data, "I135", "state_service", "Serviceebene (0: normal, 1: service)", "")
        self.into_data_float(data, "I263", "adapt_heating", "Temperaturanpassung für die Heizung", "°C")
        self.into_data_int(data, "I1270", "manual_heatingpump", "Handschaltung Heizungspumpe (H-0-A)", "")
        self.into_data_int(data, "I1281", "manual_sourcepump", "Handschaltung Quellenpumpe (H-0-A)", "")
        self.into_data_int(data, "I1287", "manual_solarpump1", "Handschaltung Solarpumpe 1 (H-0-A)", "")
        self.into_data_int(data, "I1289", "manual_solarpump2", "Handschaltung Solarpumpe 2 (H-0-A)", "")
        self.into_data_int(data, "I1291", "manual_tankpump", "Handschaltung Speicherladepumpe (H-0-A)", "")
        self.into_data_int(data, "I1293", "manual_valve", "Handschaltung Brauchwasserventil (H-0-A)", "")
        self.into_data_int(data, "I1295", "manual_poolvalve", "Handschaltung Poolventil (H-0-A)", "")
        self.into_data_int(data, "I1297", "manual_coolvalve", "Handschaltung Kühlventil (H-0-A)", "")
        self.into_data_int(data, "I1299", "manual_4wayvalve", "Handschaltung Vierwegeventil (H-0-A)", "")
        self.into_data_int(data, "I1319", "manual_multiext", "Handschaltung Multiausgang Ext. (H-0-A)", "")
        self.into_data_float(data, "I2020", "temp_surrounding", "Umgebung", "°C")
        self.into_data_float(data, "I2021", "temp_suction_air", "Sauggas", "°C")
        self.into_data_float(data, "I2023", "temp_sump", "Ölsumpf", "°C")

        #
        # "I51" : "state" : "Status der Wärmepumpenkomponenten"
        #
        self.into_data_int(data, "I51", "state", "Status der Wärmepumpenkomponenten", "")

        #
        # "I51.0" : "state_sourcepump" : "Status der Wärmepumpenkomponenten: Quellenpumpe"
        #
        try:
            val = data["I51"]
            key = "state_sourcepump"
            if val["status"]:
                self.__data[key] = {
                    "key": key,
                    "value": (("{:08b}".format(int(val["value"])))[::-1] + '00000000000')[0],
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
                    "value": (("{:08b}".format(int(val["value"])))[::-1] + '00000000000')[1],
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
                    "value": (("{:08b}".format(int(val["value"])))[::-1] + '00000000000')[2],
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
                    "value": (("{:08b}".format(int(val["value"])))[::-1] + '00000000000')[3],
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
                    "value": (("{:08b}".format(int(val["value"])))[::-1] + '00000000000')[4],
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
                    "value": (("{:08b}".format(int(val["value"])))[::-1] + '00000000000')[5],
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
                    "value": (("{:08b}".format(int(val["value"])))[::-1] + '00000000000')[6],
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
                    "value": (("{:08b}".format(int(val["value"])))[::-1] + '00000000000')[7],
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
                    "value": (("{:08b}".format(int(val["value"])))[::-1] + '00000000000')[8],
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
                    "value": (("{:08b}".format(int(val["value"])))[::-1] + '00000000000')[9],
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
                    "value": (("{:08b}".format(int(val["value"])))[::-1] + '00000000000')[10],
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
                    "value": (("{:08b}".format(int(val["value"])))[::-1] + '00000000000')[11],
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
        # print()
        pass
