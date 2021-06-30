import discord
from discord.ext import commands, tasks
import json
import mcsrvstat as MCsrv

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
    async def mcserver(self, ctx, ip=None, platform="java", options=None, options2=None):
        serv = MCsrv.Mcsrv(platform)
        self.lastcall[f"{ctx.channel.id}"] = serv
        serv.ping(f"{ip}")
        if options == None:
            if serv.result["online"] == True:
                emb = discord.Embed(title=serv.result["hostname"], description="status: Online")
                #emb.set_thumbnail(url=str(serv.result["icon"]))
                emb.add_field(name="ip",value=serv.result["ip"])
                emb.add_field(name="port",value=serv.result["port"])
                emb.add_field(name="version",value=serv.result["version"], inline=False)
                emb.add_field(name="players",value="online: {}, max: {}".format(serv.result["players"]["online"], serv.result["players"]["max"]), inline=False)
                try:
                    emb.add_field(name="list", value=LtoS(serv.result["players"]["list"]), inline=False)
                except:
                    pass
                await ctx.send(embed=emb)
            else:
                emb = discord.Embed(title=ip, description="status: Offline")
                emb.add_field(name="platform", value=platform)
                emb.add_field(name="no connection.", value="server is offline or cant be found.", inline=False)
                await ctx.send(embed=emb)
        elif options == "monitor":
            with open("mcsrvMonitor.json", "r", encoding="utf8") as F:
                build = json.loads(F.read())
                reports = []
                try:
                    for i in build[serv.result["hostname"]]["report"]:
                        #print(i)
                        reports.append(i)
                except:
                    pass
                
            if options2 == None:
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
                
            elif options2 == "remove":
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
        elif options == "dump":
            serv.dump("dumps\\{}.json".format(serv.result["hostname"]))
            await ctx.send(file=discord.file("dumps\\{}.json".format(serv.result["hostname"])))
             
def setup(client):
    client.add_cog(Minecraft(client))
