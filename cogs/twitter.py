from KaitoUWU import BotUtils
import discord, tweepy
from discord.ext import commands, tasks

properties = BotUtils.ini_get('Properties.ini')
tweetC = properties['twitter']
notify = properties['Notifs']

client2 = tweepy.Client(
    consumer_key=str(tweetC['con_key']),
    consumer_secret=str(tweetC['con_secret']),
    access_token=str(tweetC['token']),
    access_token_secret=str(tweetC['secret'])
)

class Twitter(commands.Cog):
    def __init__(self, client, birb):
        self.client = client
        self.zoe = BotUtils.SENDER(self.client)

        self.birb = birb
        self.me = self.birb.get_me()

    @commands.command()
    async def debug(self, ctx):
        try:
            item = self.me.data
            await ctx.send(str(item))
            await ctx send(str(type(item)))
            
        except Exception as e:
            await ctx.send(f"Error! {e})

def setup(client):
    client.add_cog(Twitter(client, client2))



