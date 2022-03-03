from KaitoUWU import BotUtils
import discord, tweepy
from discord.ext import commands, tasks

properties = BotUtils.ini_get('Properties.ini')
notify = properties['Notifs']

#OAuth
AuthCon = BotUtils.FileHandler.JSON("Data/TwitterAuth.json")
cache = AuthCon.Load()
tweetC = cache["kai2ymd"]
#TweepyAuth
akey = str(tweetC['token'])
asecret = str(tweetC['secret'])
ckey = str(tweetC['con_key'])
csecret = str(tweetC['con_secret'])
bearer = str(tweetC['bearer'])
#AuthV1
auth = tweepy.OAuth1UserHandler(
   ckey, csecret,
   akey, asecret
)
tclient1 = tweepy.API(auth)
#AuthV2
tclient2 = tweepy.Client(
    bearer_token=bearer,
    consumer_key=ckey,
    consumer_secret=csecret,
    access_token=akey,
    access_token_secret=asecret
)

class Twitter(commands.Cog):
    def __init__(self, client, birb1, birb2):
        self.client = client
        self.zoe = BotUtils.SENDER(self.client)
        self.birb1 = birb1
        self.birb2 = birb2
        self.watashi = self.birb2.get_me()

    @commands.command()
    async def gettweets(self, ctx, user):
        try:
            que = self.birb1.user_timeline(screen_name=str(user))
            await ctx.send(str(len(que))+" items")
            for i in que:
                await ctx.send(str(type(i)))
                #await ctx.send("! "+str(i))
        except Exception as e:
            await ctx.send(f"Error! {e}")

    @commands.command()
    async def debug(self, ctx, args):
        try:
            user = self.birb2.get_user(username=str(args))
            item = self.birb2.get_list_tweets(user.data.id, max_results=3)
            await ctx.send(str(type(item)))
            await ctx.send(str(item))

            
        except Exception as e:
            await ctx.send(f"Error! {e}")

def setup(client):
    client.add_cog(Twitter(client, tclient1, tclient2))



