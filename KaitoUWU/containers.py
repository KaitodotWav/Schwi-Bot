import  configparser

class Bot():
    def __init__(self, client):
        config = configparser.ConfigParser()
        config.read("Properties.ini")
        self.token = config[client]["Token"]
        self.logs = int(config[client]["Logs"])
        self.report = int(config[client]["Reports"])
        self.prefix = config[client]["Prefix"]
        self.debug = config[client]["Debug"]
