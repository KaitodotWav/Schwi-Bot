import psycopg2, configparser, os

class Database():
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("Database.ini")
        self.Linfo = self.config["Schwii"]
        self.HOST = str(self.Linfo["Host"])
        self.DB = str(self.Linfo["Database"])
        self.USER = str(self.Linfo["User"])
        self.PORT = str(self.Linfo["Port"])
        self.PASS = str(self.Linfo["Password"])
        
        self.server = psycopg2.connect(host=self.HOST, database=self.DB, user=self.USER, password=self.PASS, port=self.PORT)
        self.cursor = self.server.cursor()
        
    def execute(self, Input):
        self.cursor.execute(str(Input))

    def close_all(self):
        self.cursor.close()
        self.server.close()

    def commit(self):
        self.server.commit()

if __name__ == "__main__":
    os.chdir("C:\\Users\\user\\Desktop\\Codes\\DiscordBots\\Schwi-Heroku\\beta2\\Schwi-Bot")
    Data = Database()
    a = Data.execute("select * from server_track")
    print(Data.cursor.fetchall())
    Data.close_all()
