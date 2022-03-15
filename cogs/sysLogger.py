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
        self.endline = -1
        self.firstrun = True
        self.Scan.start()

    async def Sender(self, msg):
        await self.send.Report(self.logCH, str(msg))

    @tasks.loop(seconds=10)
    async def Scan(self):
        try:
            if self.firstrun:
                self.firstrun = False
                pass
            else:
                cache = [line.strip('') for line in open("Data\\logs.txt")]
                if len(cache) != self.endline:
                    send = cache[self.endline-1:]
                    for i in send:
                        await self.Sender(i)
                    self.endline = len(cache)
        except Exception as e:
            emb_err = self.emb.get(Type='error', Title=str(type(e)), Des=str(e))
            await self.send.ReportEMB(self.report, emb_err)

def setup(client):
    client.add_cog(BotLogger(client))
