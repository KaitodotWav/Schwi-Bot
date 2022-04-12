import configparser, discord, random, time, json
from discord_components import DiscordComponents, ComponentsBot, Button

def ini_get(ini):
    config = configparser.ConfigParser()
    config.read(ini)
    return config

class Logger():
    def __init__(self, path, startup="", reset=False):
        self.path = path
        self.startup = startup
        self.contents = None
        try:
            open(self.path)
        except:
            with open(self.path, "w", encoding="utf8") as f:
                f.write(self.startup)
        else:
            if reset:
                with open(self.path, "w", encoding="utf8") as f: f.write("")
            if len(self.startup) > 0:
                with open(self.path, "a", encoding="utf8") as a: print(self.startup, file=a)
            with open(self.path, "r", encoding="utf8") as r: self.contents = r.read()

    def log(self, content, echo="all"):
        with open(self.path, "a", encoding="utf8") as f:
            if echo == "all" or echo == "file":
                print(content, file=f)
            if echo == "all" or echo == "console":
                print("Log: " + content)

class FileHandler():
    class ParseError(Exception):
        pass
    class SaveError(Exception):
        pass

    class TEXT():
        def __init__(self, path, encoding="utf8"):
            self.path = str(path)
            self.enc = str(encoding)

        def Load(self):
            try:
                with open(self.path, "r", encoding=self.enc) as f:
                    cache = f.read()
                return cache
            except Exception as e:
                raise FileHandler.ParseError(e)

        def Write(self, text):
            try:
                with open(self.path, "w", encoding=self.enc) as f:
                    f.write(str(text))
            except Exception as e:
                raise FileHandler.SaveError(e)

        def Add(self, text):
            try:
                with open(self.path, "a", encoding=self.enc) as f:
                    print(f"{text}", file=f)
            except Exception as e:
                raise FileHandler.SaveError(e)

    class JSON():
        def __init__(self, path, encoding='utf8'):
            self.path = str(path)
            self.enc = str(encoding)

        def Load(self):
            try:
                with open(self.path, 'r', encoding=self.enc) as f:
                    cache = json.loads(f.read())
                return cache
            except Exception as e:
                raise FileHandler.ParseError(e)

        def Save(self, items, Indent=4):
            try:
                with open(self.path, 'w', encoding=self.enc) as f:
                    json.dump(items, f, ensure_ascii=False, indent=Indent)
            except Exception as e:
                raise FileHandler.SaveError(e)

        def Add(self, items, keys=None, indent=4):
            cache = self.Load()
            coords = []
            if type(keys) == list:
                select = cache
                create = items
                _wait = []
                for k in keys:
                    if k in select and len(_wait) == 0:
                        sel = str(select[f"{k}"])
                        coords.append(sel)
                    else:
                        _wait.append(k)
                for _ in range(len(_wait)):
                    k = _wait.pop()
                    temp = {}
                    temp[f"{k}"] = create
                    create = temp
                
                for c in range(len(coords)):
                    pass

class Timer():
    def __init__(self):
        self.startT = 1
        self.endT = 2
    
    def start(self):
        self.startT = time.time()

    def end(self):
        self.endT = time.time()
        ET = self.elapse()
        self.reset()
        return ET

    def elapse(self):
        elp = self.endT - self.startT
        return elp
    
    def reset(self):
        self.startT = self.endT = None

class ERROR():
    class Embed_Error(Exception):
        pass
    class Send_Error(Exception):
        pass
    
    class AccessDenied(Exception):
        pass

    class SyntaxError(Exception):
        pass

class EMBEDS():
    def __init__(self, ico_ini_path="Data/Emotes.ini", Type=None, title=None, description=None, color=None):
        self.ico_path = ico_ini_path
        self.ico = ini_get(self.ico_path)
        self.title = title
        self.des = description
        self.type = Type
        self.color = color
        self.setimg = []

    def get(self, Type=None, Title=None, Des=None, color=None):
        check = Type
        self.update_ico()
        if Title == None:
            Title = self.title
        if Des == None:
            Des = self.des
        if Type == None:
            Type = self.type
        if color == None:
            color = self.color
        try:
            if len(self.setimg) == 0:
                image_raw = self.ico[str(Type)]
                image_list = self.build(image_raw)
            else:
                image_list = self.setimg
            emb = self.template(image_list, Title, Des, color)
            return emb
            
        except Exception as e:
            raise ERROR.Embed_Error(type(e))

    def set_img(self, path):
        target = path.split("/")
        current = self.ico
        for i in target:
            current = current[i]
        self.setimg.append(current)

    def build(self, lib):
        contents = []
        for i in lib:
            contents.append(lib[i])
        return contents

    def template(self, ico, Title=None, des=None, Color=None):
        if len(ico) > 1:
            icon = random.choice(ico)
        else:
            icon = ico[0]
        if Title==None and des==None:
            raise ERROR.Embed_Error("No Parammiter has given.")
        
        if Color == None:
            if des != None:
                emb = discord.Embed(title=Title, description=des)
            else:
                emb = discord.Embed(title=Title)
        else:
            if des != None:
                emb = discord.Embed(title=Title, description=des, color=Color)
            else:
                emb = discord.Embed(title=Title, color=Color)
        emb.set_thumbnail(url=icon)
        return emb

    def update_ico(self):
        self.ico = ini_get(self.ico_path)

class SENDER():
    def __init__(self, client):
        self.client = client
        
    async def Report(self, ID, content, publish=False):
        report = self.client.get_channel(ID)
        try:
            send = await report.send(content)
            if publish:
                await send.publish()
            return send
        except Exception as e:
            raise ERROR.Send_Error(e)
        
    async def ReportEMB(self, ID, EMB, publish=False):
        report = self.client.get_channel(ID)
        try:
            send = await report.send(embed=EMB)
            if publish:
                await send.publish()
            return send
        except Exception as e:
            raise ERROR.Send_Error(e)

    async def EditEMB(self, msg, new, Comp=None):
        try:
            if Comp != None:
                send = await msg.edit(embed=new, components=Comp)
            else:
                send = await msg.edit(embed=new)
            return send
        except Exception as e:
            raise ERROR.Send_Error(e)

    async def ReportFile(self, ID, path, publish=False):
        report = self.client.get_channel(ID)
        try:
            send = await report.send(file=discord.File(f"{path}"))
            if publish:
                send.publish()
            return send
        except Exception as e:
            raise ERROR.Send_Error(e)

    async def DEL(self, ctx):
        try:
            await ctx.message.delete()
        except Exception as e:
            raise ERROR.Send_Error(e)

class Permission():
    def Admin(ctx):
        admins = [line.strip() for line in open("Data/admin.txt")]
        if str(ctx.author.id) in admins:
            pass
        else:
            raise ERROR.AccessDenied("this command is for bot admins only.")

    def Block(ctx):
        blocked = [line.strip() for line in open("Data/blocklist.txt")]
        if str(ctx.author.id) in blocked:
            raise ERROR.AccessDenied(f"<@{ctx.author.id}> is blocklisted from using the bot.")
        else:
            pass

    def NSFW(ctx):
        if ctx.channel.is_nsfw():
            pass
        else:
            raise ERROR.AccessDenied("this command is for NSFW channel only.")

class Response():
    load = EMBEDS(Type="loading", title="Processing", description="please wait...")
    scc = EMBEDS(Type="success", title="Success!", color=0x00FF00)
    err = EMBEDS(Type="error", title="Error!")
    FF = EMBEDS(Type="fail", title="Operation Failed!", color=0xFFA500)

class Pages():
    def __init__(self, client):
        self.pages = {}
        self.client = client
        DiscordComponents(client)

    def build_pages(self, embs):
        build = {"current":0}
        pages = {}
        for n, emb in enumerate(embs):
            pages[f"{n}"] = emb
        build["pages"] = pages
        ID = time.time()
        #print(ID)
        return build, ID

    def Book(self, embs):
        pages, ID = self.build_pages(embs)
        self.pages[f"{ID}"] = pages
        Butt = [[
            Button(label="Prev", custom_id=f"P{ID}"),
            Button(label="Next", custom_id=f"N{ID}")
            ]]
        return pages["pages"]["0"], Butt

    def Handler(self, ID, OP):
        get = self.pages[ID]
        Max = len(get["pages"])
        if OP == "N":
            if get["current"] != Max -1:
                get["current"] += 1
        elif OP == "P":
            if get["current"] != 0:
                get["current"] -= 1
        return get["pages"][str(get["current"])]

    async def Button_Events(self, callback):
        bullshit = "this message is not needed but discord is being such a bullshit throwing errors if i dont made this useless message so yeah fuck you."
        def checker(m):
            if m.custom_id[1:] in self.pages: return m
            else: pass
        event = await self.client.wait_for("button_click", check = checker)
        ID = event.custom_id[1:]
        Action = event.custom_id[0]
        get = self.Handler(ID, Action)
        await callback(event, get)
        await event.respond(content=f"done, {bullshit}")

    
if __name__ == "__main__":
    test = []
    for t in range(8):
        test.append(f"test{t}")
    fk = Pages()
    fk.Book(test)
    while True:
        ID = input("ID: ")
        print(fk.Handler(ID, "N"))
