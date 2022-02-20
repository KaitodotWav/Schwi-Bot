import configparser, discord, random, time

def ini_get(ini):
    config = configparser.ConfigParser()
    config.read(ini)
    return config

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
        
    async def Report(self, ID, content):
        report = self.client.get_channel(ID)
        try:
            send = await report.send(content)
            return send
        except Exception as e:
            raise ERROR.Send_Error(e)
        
    async def ReportEMB(self, ID, EMB):
        report = self.client.get_channel(ID)
        try:
            send = await report.send(embed=EMB)
            return send
        except Exception as e:
            raise ERROR.Send_Error(e)

    async def EditEMB(self, msg, new):
        try:
            send = await msg.edit(embed=new)
            return send
        except Exception as e:
            raise ERROR.Send_Error(e)

    async def ReportFile(self, ID, path):
        report = self.client.get_channel(ID)
        try:
            send = await report.send(file=discord.File(f"{path}"))
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
