import discord
from discord.ext import commands, tasks
import json, time
from KaitoUWU import mcsrvstat as MCsrv
from KaitoUWU import BotUtils
from discord_components import DiscordComponents, ComponentsBot, Button

#endpoints
linkIco = "https://api.mcsrvstat.us/icon/<address>"
default_ico = "https://cdn.discordapp.com/attachments/889038336453394433/894638342979878972/worldICO.png"

class SyntaxError(Exception):
    pass
class ServerError(Exception):
    pass
class EventError(Exception):
    pass

#other functions
def LtoS(List):
    build = ""
    for i in List:
        build += f" {i},"
    return build[1:len(build)-1]

def PtoS(List):
    table = []
    row = []
    for L in List:
        if len(table) < 3:
            if len(row) < 10:
                row.append(L)
            else:
                table.append(row)
                row = [L]
    if len(row)>0 and len(table)<4:
        table.append(row)
    print(table)
                
class mcserver():
    def __init__(self):
        default = "unknown"
        self.ip = default
        self.port = default
        self.ver = default
        self.players = default
    
    def set(self, ip=None, port=None, version=None, players=None):
        self.ip = self.check(ip)
        self.port = self.check(port)
        self.ver = self.check(version)
        self.players = self.check(players)

    def check(self, text):
        if len(str(text)) >= 1 and text != None:
            return text
        else:
            return "unknown"

class ServerPing():
    def __init__(self, ip, platform="all"):
        self.ip = ip
        self.plat = platform
        self.res = []
        self.raw = []

    def ping(self):
        platforms = ["java", "bedrock"]
        if self.plat == "all":
            for p in platforms:
                serv = MCsrv.Mcsrv(p)
                serv.ping(self.ip)
                serv.result["platform"] = p
                if serv.result["online"]:
                    self.res.append(serv)
                self.raw.append(serv)
        elif self.plat in platforms:
            serv = MCsrv.Mcsrv(self.plat)
            serv.ping(self.ip)
            if serv.result["online"]:
                self.res.append(serv)
            self.raw.append(serv)
        else:
            raise ServerError(f"unsupported platform -> {self.plat}.")

    def json_raw(self):
        rip = []
        for raw in self.raw:
            rip.append(raw.result)
        return rip

    def json_dump(self):
        print("dump")
        dumped = []
        if len(self.raw) > 0:
            for r in self.raw:
                plat = r.result["platform"]
                ip = r.result["ip"]
                port = r.result["port"]
                path = f"dumps/{plat}_{ip}_{port}.json"
                r.dump(path)
                dumped.append(path)
        else: raise ServerError("ping has not been called.")
        return dumped

    def get_embed(self):
        Embeds = []
        if len(self.res) > 0:
            for r in self.res:
                server = mcserver()
                server.set(
                    r.result["ip"],
                    r.result["port"],
                    r.result["version"],
                    "online: {}, max: {}".format(r.result["players"]["online"], r.result["players"]["max"])
                )
                try:
                    emb = discord.Embed(title=r.result["hostname"], description="platform: {}".format(r.result["platform"]))
                except:
                    emb = discord.Embed(title=r.result["ip"], description="platform: {}".format(r.result["platform"]))
                emb.add_field(name="ip",value=server.ip)
                emb.add_field(name="port",value=server.port, inline=True)
                emb.add_field(name="version",value=server.ver, inline=False)
                emb.add_field(name="players",value=server.players, inline=True)
                try:
                    emb.add_field(name="list", value=LtoS(r.result["players"]["list"]), inline=False)
                except:
                    pass
                try:
                    emb.set_thumbnail(url=linkIco.replace("<address>", r.result["ip"]))
                except:
                    emb.set_thumbnail(url=default_ico)
                Embeds.append(emb)
        else:
            if len(self.raw) > 0:
                emb = discord.Embed(title=self.ip, description="status: Offline")
                emb.add_field(name="Plarform", value=f"{self.plat}".replace("all", "Unknown"))
                emb.add_field(name="no connection.", value="server is offline or cant be found.", inline=False)
                Embeds.append(emb)
            else: raise ServerError("ping has not been called.")
        return Embeds        

class Minecraft(commands.Cog, name="Minecraft Server"):
    def __init__(self, client):
        self.client = client
        DiscordComponents(client)
        self.lastcall = {}
        self.butevents = {}
        self.embs = BotUtils.Response()
        self.zoe = BotUtils.SENDER(client)
        self.Button_Events.start()

    async def startup(self, ctx):
        mainemb = self.embs.load.get()
        main_emb = await self.zoe.ReportEMB(ctx.channel.id, mainemb)
        return main_emb

    async def Error(self, main_emb, msg):
        send_err = self.embs.err.get(Des="error while executing command.")
        send_err.add_field(name=str(type(msg)), value=msg)
        await self.zoe.EditEMB(main_emb, send_err)

    """
    @commands.command()
    async def ping2(self, ctx, ip=None, platform="java", *options):
        try:
            serv = MCsrv.AMCstat()
            res = await serv.Jping(ip)
            await ctx.send(str(res))
        except Exception as e:
            await ctx.send(f"Error {e}")"""

    @tasks.loop(seconds=5)
    async def Button_Events(self):
        bullshit = "this message is not needed but discord is being such a bullshit throwing errors if i dont made this useless message so yeah fuck you."
        def checker(m):
            if m.custom_id in self.butevents:
                return m
            else: pass
        event = await self.client.wait_for("button_click", check = checker)
        await event.message.edit(embed=self.butevents[event.custom_id])
        await event.respond(content=f"done, {bullshit}")
        
    @commands.command()
    async def ping(self, ctx, ip=None, platform="all", *options):
        mainemb = await self.startup(ctx)
        try:
            BotUtils.Permission.Block(ctx)
            options = list(options)
            server = ServerPing(ip, platform)
            server.ping()

            if len(options) <= 0: options = ["open"]
                
            if options[0] == "open":
                tid = time.time()
                emb = server.get_embed()
                if len(emb) == 1: await self.zoe.EditEMB(mainemb, emb[0])
                elif len(emb) == 2:
                    ids = [f"jav{tid}", f"bangbros{tid}"]
                    compo = [[
                        Button(label="Java", custom_id=ids[0]),
                        Button(label="Bedrock", custom_id=ids[1])
                        ]]
                    for i in range(len(ids)):
                        self.butevents[ids[i]] = emb[i]
                    await self.zoe.EditEMB(mainemb, emb[0], compo)

            elif options[0] == "dump":
                paths = server.json_dump()
                await mainemb.delete()
                for p in paths:
                    await ctx.send(file=discord.File(f"{p}"))

            else:
                raise SyntaxError("unknown command -> {}".format(options[0]))

        except Exception as e:
            await self.Error(mainemb, e)
             
def setup(client: commands.Bot):
    client.add_cog(Minecraft(client))

