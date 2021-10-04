import discord
from discord.ext import commands, tasks
import json
from KaitoUWU import mcsrvstat as MCsrv

#endpoints
linkIco = "https://api.mcsrvstat.us/icon/<address>"
default_ico = "https://cdn.discordapp.com/attachments/889038336453394433/894638342979878972/worldICO.png"

#other functions
def LtoS(List):
    build = ""
    for i in List:
        build += f" {i},"
    return build[1:len(build)-1]

class Minecraft(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.lastcall = {}

    @commands.command()
    async def mcserver(self, ctx, ip=None, platform="java", *options):
        serv = MCsrv.Mcsrv(platform)
        self.lastcall[f"{ctx.channel.id}"] = serv
        serv.ping(f"{ip}")
        if len(options) == 0:
            options = ("open", "idk")
        if options[0] == "open":
            print("called")
            if serv.result["online"] == True:
                try:
                    emb = discord.Embed(title=serv.result["hostname"], description="status: Online")
                except:
                    emb = discord.Embed(title=serv.result["ip"], description="status: Online")
                emb.add_field(name="ip",value=serv.result["ip"])
                emb.add_field(name="port",value=serv.result["port"])
                emb.add_field(name="version",value=serv.result["version"], inline=False)
                emb.add_field(name="players",value="online: {}, max: {}".format(serv.result["players"]["online"], serv.result["players"]["max"]), inline=False)
                try:
                    emb.add_field(name="list", value=LtoS(serv.result["players"]["list"]), inline=False)
                except:
                    pass
                try:
                    emb.set_thumbnail(url=linkIco.replace("<address>", serv.result["ip"]))
                except:
                    emb.set_thumbnail(url=default_ico)
                await ctx.send(embed=emb)
            else:
                emb = discord.Embed(title=ip, description="status: Offline")
                emb.add_field(name="platform", value=platform)
                emb.add_field(name="no connection.", value="server is offline or cant be found.", inline=False)
                await ctx.send(embed=emb)
        elif options[0] == "monitor":
            with open("mcsrvMonitor.json", "r", encoding="utf8") as F:
                build = json.loads(F.read())
                reports = []
                try:
                    for i in build[serv.result["hostname"]]["report"]:
                        #print(i)
                        reports.append(i)
                except:
                    pass
                
            if options[1] == None:
                if ctx.channel.id not in reports:
                    reports.append(ctx.channel.id)
                    try:
                        build[serv.result["hostname"]] ={"platform":platform, "online":serv.result["online"], "players":serv.result["players"]["list"], "report":reports}
                    except:
                        build[serv.result["hostname"]] ={"platform":platform, "online":serv.result["online"], "report":reports}

                    with open("mcsrvMonitor.json", "w", encoding="utf8") as F:
                        json.dump(build, F, ensure_ascii=False, indent=4)
                    await ctx.send("{} is now being monitored.".format(serv.result["hostname"]))
                else:
                    await ctx.send("{} is already being monitored".format(serv.result["hostname"]))
                
            elif options[1] == "remove":
                if len(reports) <= 1:
                    try:
                        build.pop(str(serv.result["hostname"]))
                    except:
                        pass
                else:
                    List = build[serv.result["hostname"]]["report"]
                    List.remove(ctx.channel.id)
                    build[serv.result["hostname"]]["report"] = List
                with open("mcsrvMonitor.json", "w", encoding="utf8") as F:
                    json.dump(build, F, ensure_ascii=False, indent=4)
                await ctx.send("{} is now removed in monitoring list.".format(serv.result["hostname"]))
        elif options[0] == "dump":
            serv.dump("dumps\\{}.json".format(serv.result["hostname"]))
            await ctx.send(file=discord.File("dumps\\{}.json".format(serv.result["hostname"])))
             
def setup(client):
    client.add_cog(Minecraft(client))
