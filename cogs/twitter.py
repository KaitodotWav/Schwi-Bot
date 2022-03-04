from KaitoUWU import BotUtils
import discord, tweepy, json
from discord.ext import commands, tasks
from mega import Mega

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
#cloudclient
mega = Mega()
cloudClient = mega.login(
    "tiaramolinos@gmail.com",
    "kaito12.2004"
)

class Twitter(commands.Cog):
    def __init__(self, client, birb1, birb2, cloud):
        self.client = client
        self.zoe = BotUtils.SENDER(self.client)
        self.birb1 = birb1
        self.birb2 = birb2
        self.watashi = self.birb2.get_me()
        self.cloud = cloud

    @commands.command()
    async def gettweets(self, ctx, user):
        try:
            que = self.birb1.user_timeline(screen_name=str(user))
            item = que[0]
            ttt = item.entities
            if "media" in ttt:
                for media in ttt["media"]:
                    await ctx.send(media["media_url"])
            
        except Exception as e:
            await ctx.send(f"Error! {e}")

    @commands.command()
    async def test(self, ctx, args):
        #folder = self.cloud.find(f"{args}")
        try:
            mk=self.cloud.create_folder(f"{args}")
            await self.debug(ctx, mk)
            await ctx.send("folder created")
        except Exception as e:
            await ctx.send("Error! {e}")

    async def debug(self, ctx, item):
        try:
            await ctx.send("t! "+str(type(item)))
        except Exception as e:
            await ctx.send(f"Error! {e}")
        try:
            await ctx.send("c! "+str(len(item)))
        except Exception as e:
            await ctx.send(f"Error! {e}")
        try:
            await ctx.send("d! "+str(dir(item)))
        except Exception as e:
            await ctx.send(f"Error! {e}")
        try:
            await ctx.send("! "+str(item))
        except Exception as e:
            await ctx.send(f"Error! {e}")

def setup(client):
    client.add_cog(Twitter(client, tclient1, tclient2, cloudClient))



