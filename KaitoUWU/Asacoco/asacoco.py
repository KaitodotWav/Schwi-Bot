import praw, random, requests, configparser
from datetime import datetime

class OAUTHError(Exception):
    pass

cache = configparser.ConfigParser()
cache.read("Properties.ini")
lib = cache["reddit"]

try:
    reddit = praw.Reddit(client_id = lib["id"], 
                         client_secret = lib["secret"], 
                         user_agent = lib["agent"]
                         )
except Exception as e:
    raise OAUTHError(e)

def getContents(posts):
    image_urls = []
    image_titles = []
    image_timestamps = []
    for post in posts:
        image_urls.append(post.url.encode('utf-8'))
        image_titles.append(post.title.encode('utf-8'))
        #image_scores.append(post.score)
        image_timestamps.append(datetime.fromtimestamp(post.created))
        #print(datetime.fromtimestamp(subreddit.created))
        #image_ids.append(post.id)
    return image_urls, image_titles, image_timestamps

def getAll(posts):
    image_urls = []
    image_titles = []
    image_timestamps = []
    image_scores = []
    image_ids = []
    for post in posts:
        image_urls.append(post.url.encode('utf-8'))
        image_titles.append(post.title.encode('utf-8'))
        image_scores.append(post.score)
        image_timestamps.append(datetime.fromtimestamp(post.created))
        image_ids.append(post.id)
    return image_urls, image_titles, image_timestamps, image_scores, image_ids
    

def getMemes(post_range=10):
    image_urls = []
    image_titles = []
    image_timestamps = []
    for subreddit in reddit.subreddit('Hololive').search("memes", syntax="meme", sort="top", time_filter="year"):
        image_urls.append(subreddit.url.encode('utf-8'))
        image_titles.append(subreddit.title.encode('utf-8'))
        #image_scores.append(post.score)
        image_timestamps.append(datetime.fromtimestamp(subreddit.created))
        #print(datetime.fromtimestamp(subreddit.created))
        #image_ids.append(post.id)
    return image_urls, image_titles, image_timestamps

def getLewds(Type="hot"):
    subreddit = reddit.subreddit('Hololewd')
    hot_post = subreddit.hot()
    new_post = subreddit.new()
    if Type == "hot":
        a, b, c = getContents(hot_post)
    elif Type == "new":
        a, b, c = getContents(new_post)
    else:
        a, b, c = getContents(subreddit)
    return a, b ,c

class Asacoco():
    def __init__(self, Subreddit, Sort="top", Time_Filter="week"):
        self.subreddit = Subreddit
        self.sort = Sort
        self.time_filter = Time_Filter
        self.search = None
        self.url = []
        self.title = []
        self.timestamps = []
        self.scores = []
        self.id = []
        self.filter_image = []
        self.cache = ""
        self.old = []
        self.new = []

    def fetch(self, Type="top"):
        if Type == "hot":
            for subreddit in reddit.subreddit(self.subreddit).hot():
                self.url.append(subreddit.url)
                self.title.append(subreddit.title)
                self.scores.append(subreddit.score)
                self.timestamps.append(datetime.fromtimestamp(subreddit.created))
                self.id.append(subreddit.id)
        elif Type == "top":
            for subreddit in reddit.subreddit(self.subreddit).top():
                self.url.append(subreddit.url)
                self.title.append(subreddit.title)
                self.scores.append(subreddit.score)
                self.timestamps.append(datetime.fromtimestamp(subreddit.created))
                self.id.append(subreddit.id)

    def Search(self, syntax, Sort="top"):
        for subreddit in reddit.subreddit('Hololive').search(syntax, sort=Sort, time_filter=self.time_filter):
            self.url.append(subreddit.url)
            self.title.append(subreddit.title)
            self.scores.append(subreddit.score)
            self.timestamps.append(datetime.fromtimestamp(subreddit.created))
            self.id.append(subreddit.id)
            print(subreddit.title)

    def Search2(self, POST, SORT="hot"):
        fetched = []
        for subreddit in reddit.subreddit(self.subreddit).flair():
            print(subreddit)
        
    def ImageLink(self):
        images = []
        img_format = [".jpg", ".png"]
        for u in self.url:
            for i in img_format:
                if i in u:
                    images.append(u)
        self.filter_image = images
        return images

    def SetCache(self, directory):
        self.cache = directory
        try:
            open(self.cache)
        except:
            with open(str(self.cache), "w") as F:
                F.write("")
        else:
            self.old = [line.strip() for line in open(self.cache)]

    def SetTimeFilter(self, time_filter):
        self.time_filter = time_filter

    def GetNew(self, List):
        new = []
        old = [line.strip() for line in open(self.cache)]
        self.old = old
        for u in List:
            if u in self.old:
                pass
            else:
                new.append(u)
        self.new = new
        return new

    def WriteCache(self, target):
        try:
            open(self.cache)
        except:
            WF = open(self.cache, "w")
            WF.write(target)
            WF.close()
        else:
            AF = open(self.cache, "a")
            print(target, file=AF)
            AF.close()
    
    def Debug(self):
        print(self.filter_image)
    
if __name__ == "__main__":
    Holo = Asacoco("Hololewd")
    Holo.Search("Ayame")
    
