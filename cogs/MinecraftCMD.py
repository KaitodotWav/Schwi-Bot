import discord
from discord.ext import commands, tasks
import json
from KaitoUWU import mcsrvstat as MCsrv
from KaitoUWU import BotUtils 

#endpoints
linkIco = "https://api.mcsrvstat.us/icon/<address>"
default_ico = "https://cdn.discordapp.com/attachments/889038336453394433/894638342979878972/worldICO.png"

class SyntaxError(Exception):
    pass

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
        self.main_emb = BotUtils.EMBEDS(Type="loading", title="Processing", description="please wait...")
        self.zoe = BotUtils.SENDER(client)
        self.emb_err = BotUtils.EMBEDS(Type="error", title="Error!")
        self.emb_scc = BotUtils.EMBEDS(Type="success", title="Success!", color=0x00FF00)
        self.emb_fail = BotUtils.EMBEDS(Type="fail", title="Failed!", color=0xFFA500)

    @commands.command()
    async def ping(self, ctx, ip=None, platform="java", *options):
        try:
            mainemb = self.main_emb.get()
            main_emb = await self.zoe.ReportEMB(ctx.channel.id, mainemb)
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
                    await self.zoe.EditEMB(main_emb, emb)
                else:
                    emb = discord.Embed(title=ip, description="status: Offline")
                    emb.add_field(name="platform", value=platform)
                    emb.add_field(name="no connection.", value="server is offline or cant be found.", inline=False)
                    await self.zoe.EditEMB(main_emb, emb)
            
            elif options[0] == "dump":
                serv.dump("dumps_{}_{}.json".format(serv.result["ip"], serv.result["port"]))
                await main_emb.delete()
                await ctx.send(file=discord.File("dumps_{}_{}.json".format(serv.result["ip"], serv.result["port"])))

            else:
                raise SyntaxError("unknown command -> {}".format(options[0])

        except Exception as e:
            emb = self.emb_err.get(Des="while executing the command.")
            emb.add_field(name=str(type(e)), value=e)
            await self.zoe.EditEMB(main_emb, emb)
             
def setup(client):
    client.add_cog(Minecraft(client))
