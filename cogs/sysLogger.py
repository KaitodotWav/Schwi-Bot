import discord
from discord.ext import commands, tasks
import time, configparser
from KaitoUWU import BotUtils

config = configparser.ConfigParser()
config.read("Properties.ini")

class BotLogger(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.report = int(config['Notifs']['Reports'])
        self.logCH = int(config['Notifs']['Logs'])
        self.emb = BotUtils.EMBEDS()
        self.send = BotUtils.SENDER(self.client)
        self.endline = 0
        self.firstrun = True
        #self.Scan.start()

    async def Sender(self, msg):
        await self.send.Report(self.logCH, str(msg))

    @commands.Cog.listener()
    async def on_ready(self):
        self.Scan.start()
        print("Logger scan has been started")

    @tasks.loop(seconds=3)
    async def Scan(self):
        try:
            cache = [line.strip('') for line in open("Data\\logs.txt")]
            #print(len(cache), self.endline)
            if len(cache) != self.endline:
                send = cache[self.endline:]
                for i in send:
                    await self.Sender(i)
                self.endline = len(cache)
        except Exception as e:
            emb_err = self.emb.get(Type='error', Title=str(type(e)), Des=str(e))
            await self.send.ReportEMB(self.report, emb_err)

def setup(client: commands.Bot):
    client.add_cog(BotLogger(client))