import configparser

class ICONS():
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("urls.ini")
        self.image = config["Icons"]
