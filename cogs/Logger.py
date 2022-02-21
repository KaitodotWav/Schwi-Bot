import discord
from discord.ext import commands, tasks
import time, configparser
from KaitoUWU import BotUtils

config = configparser.ConfigParser()
config.read("Properties.ini")

class BotLogger(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.endline = 0
        self.send = BotUtils.SENDER(self.client)
        self.Scan.start()

    @tasks.loop(seconds=10)
    async def Scan(self):
        cache = [line.strip('') for line in open("Data\\logs.txt")]
        await self.Seder(cache)
        if len(cache) != self.endline:
            send = cache[self.endline-1:]
            for i in send:
                await self.Sender(i)
            self.endline = len(cache)

    async def Sender(self, msg):
        logCH = config['Notifs']['Logs']
        await self.send.Report(int(logCH), msg)

def setup(client):
    client.add_cog(BotLogger(client))
