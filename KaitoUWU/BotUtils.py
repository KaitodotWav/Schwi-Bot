import configparser, discord, random, time, json
#import discord_components

def ini_get(ini):
    config = configparser.ConfigParser()
    config.read(ini)
    return config

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
                raise ParseError(e)

        def Write(self, text):
            try:
                with open(self.path, "w", encoding=self.enc) as f:
                    f.write(str(text))
            except Exception as e:
                raise ParseError(e)

        def Add(self, text):
            try:
                with open(self.path, "a", encoding=self.enc) as f:
                    print(f"{text}", file=f)
            except Exception as e:
                raise ParseError(e)

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
                raise ParseError(e)

        def Save(self, items, Indent=4):
            try:
                with open(self.path, 'w', encoding=self.enc) as f:
                    json.dump(items, f, ensure_ascii=False, indent=Indent)
            except Exception as e:
                raise SaveError(e)

        def Add(self, items, keys=None, indent=4):
            cache = Load()
            coords = []
            if type(keys) == list:
                select = cache
                create = items
                _wait = []
                for k in keys:
                    if k in select and len(_wait) == 0:
                        select = select[f"{k}"]
                        coords.append[select]
                    else:
                        _wait.append(k)
                for _ in _wait:
                    k = _wait.pop()
                    temp = {}
                    temp[f"{k}"] = create
                    create = temp
class Timer():
    def __init__(self):
        self.startT = None
        self.endT = None
    
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

class EMBEDS():
    def __init__(self, ico_ini_path="Emotes.ini", Type=None, title=None, description=None, color=None):
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

    async def EditEMB(self, msg, new):
        try:
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

if __name__ == "__main__":
    a = EMBEDS()
    a.set_img("Others/mumei_think1")
