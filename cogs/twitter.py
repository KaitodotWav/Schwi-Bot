from KaitoUWU import BotUtils
import discord, tweepy
from discord.ext import commands, tasks

properties = BotUtils.ini_get('Properties.ini')
tweetC = properties['twitter']
notify = properties['Notifs']

akey = str(tweetC['token'])
asecret = str(tweetC['secret'])
ckey = str(tweetC['con_key'])
csecret = str(tweetC['con_secret'])
bearer = str(tweetC['bearer'])

auth = tweepy.OAuthHandler(ckey, csecret)
auth.set_access_token(akey, asecret)

"""
clientA = tweepy.Client(
    #bearer_token=
    consumer_key=,
    consumer_secret=,
    access_token=,
    access_token_secret=
)
"""

client2 = tweepy.API(auth)

class Twitter(commands.Cog):
    def __init__(self, client, birb):
        self.client = client
        self.zoe = BotUtils.SENDER(self.client)

        self.birb = birb


    @commands.command()
    async def debug(self, ctx, args):
        try:
            user = self.birb.get_user(screen_name=str(args))

            item = user
            await ctx.send(str(item))
            await ctx.send(str(type(item)))
            
        except Exception as e:
            await ctx.send(f"Error! {e}")

def setup(client):
    client.add_cog(Twitter(client, client2))



