import requests
import calendar
import time
import logging
import sys


class Connection:

    def __init__(self, ip, user, pwd):
        self.__ip = ip
        self.__user = user
        self.__pwd = pwd
        self.__cookies = None
        self.__keys = {0: ["A1"]}
        self.__status = "999"
        logging.debug("Connection - init")



    def login(self):
        """
        Login zur Wärmepumpe.
        Der Cookie wird in "self.__cookies" gespeichert
        und muß für alle weiteren Abfragen verwendet werden.
        :return Status-Code (200=ok)
        """
        #
        login_data = {'username': self.__user, 'password': self.__pwd}
        #
        url_login = "http://{0}/cgi/login".format(self.__ip)
        #
        logging.debug("Connection - login  [{0}]   User: {1}".format(url_login, self.__user))
        #
        try:
            login = requests.get(url=url_login, params=login_data, timeout=3.0)
            self.__cookies = login.cookies
            self.__status = login.status_code
            if self.__status == 200:
                if str(login.content).split("\\n")[1] == "#S_OK":
                    # b'1\n#S_OK\nIDALToken=57c7f20fe1fb5e91e1211cb1ccd7a60c'
                    logging.debug("Connection - Login - OK")
                    return self.__status
                else:
                    # b'-45\n#E_PASS_DONT_MATCH'
                    logging.error("Connection - Login - Fehler : {0}".format(str(login.content).split("\\n")[1]))
                    self.__status = 998
                    return self.__status
            else:
                logging.error("Connection - Login - Status: {0}".format(self.__status))
                raise RuntimeError('Login-Error (Code:{0})'.format(self.__status))
        except requests.exceptions.ConnectTimeout as err:
            logging.error("Connection - Login - ConnectTimeout")
            pass
        except:
            logging.error("Connection - Login - ???")
            print("Unexpected error:", sys.exc_info()[0])
        pass



    def get_values_from_pump(self, keys):
        """
        Hier findet die eigentliche Kommunikation zur Pumpe ab.
        """
        #print()
        #print()
        logging.debug("Connection - get_values_from_pump  -> {0}".format(keys))
        if len(keys) ==0:
            logging.debug("Connection - get_values_from_pump  - keine Keys")
            return None, 200
        if len(keys) > 75:
            logging.error("Connection - get_values_from_pump  -> Anzahl der Keys zu hoch ({0})".format(len(keys)))
            raise RuntimeError('Anzahl der Keys zu hoch ({0})'.format(len(keys)))
        #
        url_request = "http://{0}/cgi/readTags".format(self.__ip)
        #
        mytime = calendar.timegm(time.gmtime())
        data_request = {'n': str(len(keys)), '_': str(mytime)}
        #
        n = 0
        for k in keys:
            n += 1
            data_request['t{0}'.format(n)] = k
        #
        erg = requests.get(url=url_request, params=data_request, cookies=self.__cookies)
        #
        logging.debug("Connection - get_values_from_pump  -> {0}".format(erg.status_code))
        logging.debug("Connection - get_values_from_pump  -> {0}".format(erg.content))
        _ret = []
        self.__status = erg.status_code
        if self.__status == 200:
            # b'#A1\tS_OK\n192\t42\n#A2\tS_OK\n192\t40\n#A3\tS_OK\n192\t23\n'
            # b'#X1\tE_UNKNOWNTAG\n#A2\tS_OK\n192\t40\n#A3\tS_OK\n192\t23\n'
            c2 = str(erg.content).split("'")[1].split("#")
            for i in range(1, len(c2)):
                c3 = c2[i].split("\\n")
                z0 = c3[0].split("\\t")
                z1 = c3[1].split("\\t")
                if z0[1] == "S_OK":
                    _ret.append({"key": z0[0], "value": z1[1], "time": mytime, "status": True})
                else:
                    _ret.append({"key": z0[0], "value": None, "time": mytime, "status": False})
            return _ret, self.__status
        else:
            return None, self.__status



    def get_values(self, group=0):
        """
        Organisiert das Holen der einzelnen Werte von der Heizung...
        """
        keys = self.__keys[group]
        logging.debug("Connection - get_values  [{0}]={1}".format(group, keys))

        t0 = 5
        t = t0  # Anzahl der Versuche ...
        while not self.__status == 200:
            t -= 1
            logging.debug("Connection - get_values  {0}".format(t))
            if t < 0:
                logging.error("Connection - get_values - Anzahl der Login-Versuche überschritten !")
                return {"__STATUS__": self.__status, "__TIME__": calendar.timegm(time.gmtime())}
            #
            self.login()
            #
            # hat nicht geklappt -> etwas warten z.B. 3 Sekunden
            if not self.__status == 200:
                logging.info("Connection - get_values  etwas warten ? aktueller Status:{0}".format(self.__status))
                time.sleep(3)
        #
        # Keys vorbereiten ...
        #
        _keys = []
        _k = []
        n = 0
        for k in keys:
            n += 1
            if n > 75:
                n = 1
                _keys.append(_k)
                _k = []
            _k.append(k)
        if len(_k) > 0:
            _keys.append(_k)
        #
        # Durchläufe
        #
        _ret = {}
        status = None
        time = None
        for _k in _keys:
            (ret, status) = self.get_values_from_pump(_k)
            for r in ret:
                _ret[r["key"]] = r
                if time == None:
                    time = r["time"]

        #
        _ret["__TIME__"] = time
        _ret["__STATUS__"] = status
        return _ret



    def get_cookies(self):
        """
        Gibt die Cookies zurück.
        """
        return self.__cookies



    def set_cookies(self, cookies):
        """
        Setzt die Cookies für die nächste Abfrage.
        """
        self.__cookies = cookies



    def get_status(self):
        """
        aktuellen HTML-Status-Code abfragen.
        """
        return self.__status



    def set_keys(self, keys, group=0):
        """
        Hinterlegt die abzufragenden Keys.
        Die Keys können in Gruppen angeordnet werden,
        damit z.B. bestimmte Keys öfters abgerufen werden als andere.

        Z.B.: Die Seriennummer wird sich kaum ändern ...

        """
        logging.debug("Connection - set_keys [{0}]={1}".format(group, keys))
        self.__keys[group] = keys
        #print(self.__keys)
