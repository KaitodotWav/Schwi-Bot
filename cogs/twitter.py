from KaitoUWU import BotUtils
import discord, tweepy, json, time
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

class TweetCollector():
    def __init__(self, client, user, cloud, birb):
        self.client = client
        self.cloud = cloud
        self.birb1 = birb
        self.loop = True
        self.last_id = None
        self.user = user

    async def loophandle(self, last_id=None):
        ctx = self.client
        cc = 2
        if last_id != None:
            self.last_id = last_id
        user = self.user
        while True:
            if self.loop == False:
                break
            try:
                if self.last_id == None:
                    tweets = self.birb1.user_timeline(screen_name=str(user), count=cc)
                else:
                    tweets = self.birb1.user_timeline(screen_name=str(user), count=cc, max_id=self.last_id-1)
                for t in tweets:
                    if "media" in t.entities:
                        for med in t["media"]:
                            await ctx.send(str(med["media_url"]))

                self.last_id = tweets[-1].id
            #except tweepy.RateLimitError:
                #time.sleep(15*60)
            except Exception as e:
                await ctx.send(f"Error! {e}")
            time.sleep(5)
        await ctx.send("loop stopped")

    async def start(self, last_id=None):
        self.loop = True
        await self.loophandle(last_id)

    async def stop(self):
        self.loop = False


class Twitter(commands.Cog):
    def __init__(self, client, birb1, birb2, cloud):
        self.client = client
        self.zoe = BotUtils.SENDER(self.client)
        self.birb1 = birb1
        self.birb2 = birb2
        self.watashi = self.birb2.get_me()
        self.cloud = cloud
        self.running = {}

    @commands.command()
    async def gettweets(self, ctx, user, option=None):
        try:
            async def makeinstance():
                Tobj = TweetCollector(ctx, user, self.cloud, self.birb1)
                self.running[str(ctx.channel.id)] = Tobj
                run = self.running[str(ctx.channel.id)]
                await run.start()

            if str(ctx.channel.id) in self.running:
                Tobj = self.running[f"{ctx.channel.id}"]
                if Tobj.user == user:
                    if str(option) == "stop":
                        await Tobj.stop()
                    elif str(option) == "continue":
                        await Tobj.start()
                    else:
                        await ctx.send("fetching tweets in background...")
                else:
                    await makeinstance()
            else:
                await makeinstance()
                
            #if "media" in ttt:
            #    for media in ttt["media"]:
            #        await ctx.send(media["media_url"])
            
        except Exception as e:
            await ctx.send(f"Error! {e}")

    @commands.command()
    async def test(self, ctx, args):
        try:
            tweets = self.birb1.user_timeline(screen_name=str(args), count=2)
            for t in tweets:
                try:
                    tx = t.extended_entities
                    med = tx["media"]
                    for m in med:
                        await ctx.send(str(m["media_url"]))
                        await self.debug(ctx, m)
                except:
                    tx = t.entities
                    await self.debug(ctx, tx)
        except Exception as e:
            await ctx.send(f"Error! {e}")

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
        if type(item) == dict:
            try:
                jd = json.dumps(item, ensure_ascii=False, indent=4)
                await ctx.send("json! "+str(jd))
            except Exception as e:
                await ctx.send(f"Error! {e}")
        else:
            pass
        try:
            await ctx.send("! "+str(item))
        except Exception as e:
            await ctx.send(f"Error! {e}")



def setup(client):
    client.add_cog(Twitter(client, tclient1, tclient2, cloudClient))



