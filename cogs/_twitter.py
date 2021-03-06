from KaitoUWU import BotUtils
import discord, tweepy, json, time, requests, os
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

async def saveCloud(ctx, link, folder):
    try:
        file = requests.get(link)
        slicelink = str(link).split("/")
        filename = slicelink[-1]
        if "?" in filename:
            slice2 = filename.split("?")
            for i in slice2:
                if "." in i:
                    filename = i
        with open(f"Data/{filename}", "wb") as F:
            F.write(file.content)
        #await ctx.send("saved")
        fold = cloudClient.find(f"TweetArchive/{folder}")
        #await ctx.send(str(fold))
        if fold == None:
            cloudClient.create_folder(f"TweetArchive/{folder}")
            fold = cloudClient.find(f"TweetArchive/{folder}")
        cloudClient.upload(f'Data/{filename}', fold[0])
        os.remove(f"Data/{filename}")
        #await ctx.send("Saved to cloud!")
    except Exception as e:
        #await ctx.send(f"Error! {e}")
        pass


async def filterLink(ctx, tweets, user, cloud):
    def selvid(vidlist):
        bitrate = -1
        lvid = None
        for V in vidlist["variants"]:
            try:
                if int(V["bitrate"]) > bitrate:
                    lvid = V["url"]
                    bitrate = int(V["bitrate"])
            except:
                pass
        return bitrate, lvid
    try:
        for t in tweets:
            try:
                tx = t.extended_entities
                med = tx["media"]
                urls = []
                for m in med:
                    m_type = str(m["type"])
                    if m_type == "photo":
                        urls.append(str(m["media_url"]))
                        await ctx.send(str(m["media_url"]))
                    elif m_type == "video":
                        vinf = m["video_info"]
                        bitrate, lvid = selvid(vinf)
                        urls.append(lvid)
                        await ctx.send(f"VID! bitrate: {bitrate}\n{lvid}")
                    elif m_type == "animated_gif":
                        vinf = m["video_info"]
                        bitrate, lvid = selvid(vinf)
                        urls.append(lvid)
                        await ctx.send(f"GIF! bitrate: {bitrate}\n{lvid}")
                    else:
                        for k in m:
                            await ctx.send(">>{}:\n{}".format(k, m[f"{k}"]))
                for l in urls:
                    if cloud:
                        await saveCloud(ctx, l, user)
            except:
                #tx = t.entities
                #await self.debug(ctx, tx)
                pass
    except Exception as e:
        await ctx.send(f"Error! {e}")

class TweetCollector():
    def __init__(self, client, user, birb, cloud):
        self.client = client
        self.birb1 = birb
        self.loop = True
        self.last_id = None
        self.user = user
        self.cloud = cloud

    async def loophandle(self, last_id=None):
        ctx = self.client
        cc = 50
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
                await filterLink(ctx, tweets, user, self.cloud)
                self.last_id = tweets[-1].id
            #except tweepy.RateLimitError:
                #time.sleep(15*60)
            except Exception as e:
                if str(e) == "list index out of range":
                    await ctx.send(f"Error! {e}\nloop will now stop...")
                    break
                else:
                    await ctx.send(f"Error! {e}\nloop will stop for 15mins")
                    time.sleep(15*60)
            time.sleep(2)
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
    async def getmedia(self, ctx, user, option=None):
        try:
            async def makeinstance(option):
                save = False
                if str(option) == "save":
                    save = True
                Tobj = TweetCollector(ctx, user, self.birb1, save)
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
                    await makeinstance(option)
            else:
                await makeinstance(option)
            
        except Exception as e:
            await ctx.send(f"Error! {e}")

    @commands.command()
    async def test(self, ctx, args):
        try:
            tweets = self.birb1.user_timeline(screen_name=str(args), count=2)
        except Exception as e:
            await ctx.send(f"Error! {e}")
        else:
            await filterLink(ctx, tweets, args, False)

    

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



