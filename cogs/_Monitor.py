import discord
from discord.ext import commands, tasks
import json, time, configparser
from KaitoUWU import mcsrvstat as MCsrv

#endpoints
linkIco = "https://api.mcsrvstat.us/icon/<address>"

config = configparser.ConfigParser()
config.read("Properties.ini")

class MCServersMonitor(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.Monitor.start()

    async def Report(self, ID, content):
        report = self.client.get_channel(ID)
        try:
            await report.send(content)
        except:
            pass
        
    async def ReportEmb(self, ID, EMB):
        report = self.client.get_channel(ID)
        try:
            await report.send(embed=EMB)
        except:
            pass

    async def ReportFile(self, ID, path):
        report = self.client.get_channel(ID)
        try:
            await report.send(file=discord.File(f"{path}"))
        except:
            pass

    @tasks.loop(seconds=30)
    async def Monitor(self):
        with open("mcsrvMonitor.json", "r", encoding="utf8") as F:
            cache = json.loads(F.read())
        for i in cache:
            refresh = False
            if str(i) == "ignore":
                pass
            else:
                lserv = cache[f"{i}"]
                platform = lserv["platform"]
                
                serv = MCsrv.Mcsrv(platform)
                try:
                    serv.ping(f"{i}")
                except Exception as e:
                    Eremb = discord.Embed(title="Error!", description=e)
                    Eremb.set_footer(text="Monitor")
                    fetchChannel = config["Notifs"]["Reports"]
                    await self.ReportEmb(fetchChannel, Eremb)
                    time.sleep(60)
                result = serv.result
                confirmed = False
                showIcon =  str(linkIco.replace("<address>", f"{i}"))
                
                #online check
                try:
                    if result["online"] != lserv["online"]:
                        checkres = []
                        for r in range(3):
                            check = MCsrv.Mcsrv(platform)
                            check.ping(f"{i}")
                            checked = check.result
                            if checked["online"] == result["online"]:
                                checkres.append("1")
                            else:
                                checkres.append("0")
                            time.sleep(1)
                                
                        if checkres.count("1") == 3:
                            confirmed = True
                        
                        if confirmed:        
                            if result["online"] == True:
                                for s in lserv["report"]:
                                    Nemb = discord.Embed(title="Server is now online.", icon_url=showIcon, color=0x00FF00)
                                    Nemb.set_footer(text=str(result["hostname"]))
                                    await self.ReportEmb(s, Nemb)
                            else:
                                for s in lserv["report"]:
                                    Nemb = discord.Embed(title="Server is now offline.", color=0xFF0000)
                                    Nemb.set_footer(text=str(result["hostname"]), icon_url=showIcon)
                                    await self.ReportEmb(s, Nemb)
                            refresh = True
                            lserv["online"] = result["online"]
                except Exception as e:
                    print(f"Error in Monitor! {e}")
                #Player check
                rplist = []
                try:
                    rplist = result["players"]["list"]
                except KeyError as e:
                    if confirmed:
                        print(f"Error! {e}")
                if rplist != lserv["players"]:
                    #print("detected", i)
                    for p in rplist:
                        if p not in lserv["players"]:
                            for s in lserv["report"]:
                                Nemb = discord.Embed(title=f"{p} joined the server", color=0xFFFF00)
                                Nemb.set_footer(text=f"{i}", icon_url=showIcon)
                                await self.ReportEmb(s, Nemb)
                    for p in lserv["players"]:
                        if p not in rplist:
                            for s in lserv["report"]:
                                Nemb = discord.Embed(title=f"{p} left the server", color=0xFFFF00)
                                Nemb.set_footer(text=f"{i}", icon_url=showIcon)
                                await self.ReportEmb(s, Nemb)
                    refresh = True
                    lserv["players"] = rplist
                
            if refresh == True:
                cache[f"{i}"] = lserv
                with open("mcsrvMonitor.json", "w", encoding="utf8") as F:
                    json.dump(cache, F, ensure_ascii=False, indent=4)

                await self.ReportFile(int(config["Notifs"]["Logs"]), "mcsrvMonitor.json")
                

    @commands.command()
    async def monitor(self, ctx, option, *args):
        arg = args
        if len(arg) <= 0:
            arg = ("channel", "idk")
        #print(args)
        if str(option) == "list":
            with open("mcsrvMonitor.json", "r", encoding = "utf8") as F:
                cache = json.loads(F.read())
            if arg[0] == "all":
                emb = discord.Embed(title="Monitoring Servers list", description="list of all Minecraft servers being monitored")
                for i in cache:
                    if i == "ignore":
                        pass
                    else:
                        serv = cache[i]
                        status = None
                        if serv["online"] == True:
                            status = "Online"
                        else:
                            status = "Offline"
                        emb.add_field(name=i, value=f"status: {status}", inline=False)
                await ctx.send(embed=emb)
            if arg[0] == "channel":
                emb = discord.Embed(title="Monitoring Servers list", description="list of Minecraft servers being monitored in this channel")
                for i in cache:
                    if i == "ignore":
                        pass
                    else:
                        serv = cache[i]
                        rebuild = []
                        for r in serv["report"]:
                            rebuild.append(int(r))
                        if int(ctx.channel.id) in rebuild:
                            if serv["online"] == True:
                                status = "Online"
                            else:
                                status = "Offline"
                            emb.add_field(name=i, value=f"status: {status}", inline=False)
                await ctx.send(embed=emb)

def setup(client):
    client.add_cog(MCServersMonitor(client))
