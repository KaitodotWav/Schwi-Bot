from KaitoUWU import BotUtils
import discord, tweepy
from discord.ext import commands, tasks

properties = BotUtils.ini_get('Properties.ini')
#tweetC = properties['twitter']
notify = properties['Notifs']

AuthCon = BotUtils.FileHandler.JSON("Data/TwitterAuth.json")
cache = AuthCon.Load()
tweetC = cache["kai2ymd"]

akey = str(tweetC['token'])
asecret = str(tweetC['secret'])
ckey = str(tweetC['con_key'])
csecret = str(tweetC['con_secret'])
bearer = str(tweetC['bearer'])
"""
auth = tweepy.OAuthHandler(ckey, csecret)
auth.set_access_token(akey, asecret)
client2 = tweepy.API(auth)
"""
client2 = tweepy.Client(
    bearer_token=bearer,
    consumer_key=ckey,
    consumer_secret=csecret,
    access_token=akey,
    access_token_secret=asecret
)

class Twitter(commands.Cog):
    def __init__(self, client, birb):
        self.client = client
        self.zoe = BotUtils.SENDER(self.client)
        self.birb = birb
        self.watashi = self.birb.get_me()


    @commands.command()
    async def debug(self, ctx, args):
        try:
            #user = self.birb.get_user(screen_name=str(args))
            user = self.birb.get_user(username=str(args))
            item = user
            await ctx.send(str(type(item)))
            await ctx.send(str(item))

            
        except Exception as e:
            await ctx.send(f"Error! {e}")

def setup(client):
    client.add_cog(Twitter(client, client2))



