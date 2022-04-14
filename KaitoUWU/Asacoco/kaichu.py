import asyncpraw as AP
import asyncio
import random, configparser

class AgeException(Exception):
    pass

class OAUTHError(Exception):
    pass

cache = configparser.ConfigParser()
cache.read("Properties.ini")
lib = cache["reddit"]

try:
    reddit = AP.Reddit(
        client_id=lib["id"],
        client_secret=lib["secret"],
        user_agent=lib["agent"]
        )

except Exception as e:
    raise OAUTHError(e)

class Kaichu():
    def __init__(self, Subreddit=None):
        self.Subreddit = Subreddit
        self.fetched = []

    async def parseGal(self, id):
        post = await reddit.submission(str(id))
        gallery = []
        ids = [i['media_id'] for i in post.gallery_data['items']]
        for id in ids:
            url = post.media_metadata[id]['p'][0]['u']
            url = url.split("?")[0].replace("preview", "i")
            gallery.append(url)
        return gallery

    async def Build(self, post):
        nsfw = False
        Type = "post"
        if post.over_18:
            nsfw = True
        if "gallery" in str(post.url).lower():
            Type = "gallery"
        template = {"type":Type, "url":post.url, "title":post.title, "scores":post.score, "timestamp":post.created, "nsfw":nsfw}
        if Type == "gallery":
            link = str(post.url).split("/")
            id = link[-1]
            imgs = await self.parseGal(id)
            template["img_url"] = imgs
        return template

    async def search(self, Syntax=None, Sort="hot", Time="month", o18=False):
        subreddit = await reddit.subreddit(self.Subreddit)
        result = []
        async for submition in subreddit.search(Syntax, sort=Sort, time_filter=Time):
            result.append(submition)
        return result

    async def fetch(self, Type="hot", search="all"):
        subreddit = await reddit.subreddit(self.Subreddit)
        post = []
        if Type == "hot":
            Filt = subreddit.hot()
            for i in Filt:
                post.append(i)
        elif Type == "new":
            Filt = subreddit.new()
            for i in Filt:
                post.append(i)
        elif Type == "top":
            Filt = subreddit.top()
            for i in Filt:
                post.append(i)

    async def fetch2(self, Type="hot", Range=10):
        subreddit = await reddit.subreddit(self.Subreddit)
        async for submission in subreddit.hot(limit=Range):
            self.fetched.append(submission)

    async def GetDict(self, Mode="random"):
        List = self.fetched
        temp = {}
        if Mode == "random":
            get = random.choice(List)
            content = await self.Build(get)
            temp = {f"{get}":content}
            return temp
        
        elif Mode == "all":
            temp = {"temp", "temps"}
            for item in List:
                content = await self.Build(item)
                temp[item] = content
            temp.pop("temp")
            return temp
            


