import discord
from discord.ext import commands, tasks
import json, time, configparser
import mcsrvstat as MCsrv

#endpoints
linkIco = "https://api.mcsrvstat.us/icon/<address>"

config = configparser.ConfigParser()
config.read("Properties.ini")

class MCServersMonitor(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.monitor.start()

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
    async def monitor(self):
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
                serv.ping(f"{i}")
                result = serv.result
                confirmed = False
                showIcon =  str(linkIco.replace("<address>", f"{i}"))
                
                #online check
                if result["online"] != lserv["online"]:
                    checkres = []
                    for r in range(3):
                        check = MCsrv.Mcsrv(platform)
                        check.ping(f"{i}")
                        checked = check.result
                        if checked["online"] == result["online"]:
                            checkres.append(True)
                        else:
                            checkres.append(False)
                            #print("ping")
                        #time.sleep(1)
                    #print(checked)
                    if checkres.count(True) == 3:
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
                
                #Player check
                try:
                    rplist = result["players"]["list"]
                    if rplist != lserv["players"]:
                        #print("detected")
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
                except KeyError as e:
                    if confirmed:
                        print(e)
                        lserv["players"] = []
            if refresh == True:
                cache[f"{i}"] = lserv
                with open("mcsrvMonitor.json", "w", encoding="utf8") as F:
                    json.dump(cache, F, ensure_ascii=False, indent=4)

                await self.ReportFile(int(config["Notifs"]["Logs"]), "mcsrvMonitor.json")
                

    @commands.command()
    async def Monitor(self, ctx, option, *args):
        if str(option) == "list":
            if args[0] == "all":
                emb = discord.Embed(title="Monitoring Servers list", description="list of Minecraft servers being monitored")
                with open("mcsrvMonitor.json", "r", encoding = "utf8") as F:
                    cache = json.loads(F.read())
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

def setup(client):
    client.add_cog(MCServersMonitor(client))
