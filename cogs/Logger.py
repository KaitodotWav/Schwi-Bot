import discord
from discord.ext import commands, tasks
import time, configparser

config = configparser.ConfigParse()
config.read("Properties.ini")

class BotLogger(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.endline = 0
        self.Scan.start()

    @tasks.loop(seconds=10)
    async def Scan(self):
        cache = [line.strip('') for line in open("Data\\logs.txt")]
        if len(cache) != self.endline:
            send = cache[self.endline-1:]
            for i in send:
                await self.Sender(i)
            self.endline = len(cache)

    async def Sender(self, msg):
        logCH = await self.client.get_channel(int(config["Notifs"]["Logs"]))
        await logCH.send(str(msg))

def setup(client):
    client.add_cog(BotLogger(client))
