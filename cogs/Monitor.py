import discord
from discord.ext import commands, tasks
import json, time, configparser, random
from KaitoUWU import mcsrvstat as MCsrv
from KaitoUWU import KaiBase
from KaitoUWU import BotUtils

#endpoints
linkIco = "https://api.mcsrvstat.us/icon/<address>"

config = configparser.ConfigParser()
config.read("Properties.ini")

class MonitorError(Exception):
    pass

class Tracking():
    def __init__(self):
        pass
            
class MCServersMonitor(commands.Cog):
    def __init__(self, client):
        self.client = client
        #self.Monitor.start()
        #self.ico_data = Klink.ICONS()
        #self.ico = self.ico_data.image
        self.emb_err = BotUtils.EMBEDS(Type="error", title="Error!")
        self.emb_scc = BotUtils.EMBEDS(Type="success", title="Success!", color=0x00FF00)
        self.emb_fail = BotUtils.EMBEDS(Type="fail", title="Failed!", color=0xFFA500)
        self.spams = []
        self.zoe = BotUtils.SENDER(client)
        self.Annoy.start()

    async def Report(self, ID, content):
        report = self.client.get_channel(ID)
        try:
            send = await report.send(content)
            return send
        except:
            pass
        
    async def ReportEmb(self, ID, EMB):
        report = self.client.get_channel(ID)
        try:
            send = await report.send(embed=EMB)
            return send
        except:
            pass

    async def EditEMB(self, msg, new):
        try:
            send = await msg.edit(embed=new)
            return send
        except:
            pass

    async def ReportFile(self, ID, path):
        report = self.client.get_channel(ID)
        try:
            send = await report.send(file=discord.File(f"{path}"))
            return send
        except:
            pass

    async def GetReport(self, ID):
        CH = self.client.get_channel(ID)
        messages = await CH.history(limit=200).flatten()
        contents = []
        msg_id = []
        for msg in messages:
            contents.append(str(msg.content))
            msg_id.append(msg.id)
        return contents, msg_id

    async def BuildDict(self, DataList):
        dick = {}
        if len(DataList) >= 1:
            for data in DataList:
                #print(data)
                try:
                    dictdata = json.loads(data)
                    #print(data)
                    for i in dictdata:
                        dick[f"{i}"] = dictdata[f"{i}"]
                except:
                    pass
        return dick

    async def DictSearch(self, keyword, DataList, DataID):
        #print("ds")
        for data in DataList:
            cursor = DataList.index(data)
            items = json.loads(data)
            #print(data, DataID[cursor])
            if str(keyword) in items:
                return data, DataID[cursor]

    def fetchsrv(self, ip, platform):
        serv = MCsrv.Mcsrv(platform)
        try:
            serv.ping(f"{ip}")
            if serv.result["online"] == True:
                return serv.result
            else:
                raise MonitorError("Server not found.")
        except Exception as e:
            raise MonitorError(e)

    @tasks.loop(seconds=5)
    async def Annoy(self):
        #print("called")
        zoe = BotUtils
        for i in self.spams:
            #print(i[0])
            await self.zoe.Report(i[0], i[1])
            time.sleep(1)

    @commands.command()
    async def spam(self, ctx, *msg):
        mss = ""
        for i in msg:
            mss += f"{i} "
        self.spams.append((ctx.channel.id, mss))
    
    """
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

                await self.ReportFile(int(config["Notifs"]["Logs"]), "mcsrvMonitor.json")"""
                

    @commands.command()
    async def monitor(self, ctx, option, *args):
        add_EMB = BotUtils.EMBEDS(Type="loading", title="Processing", description="Brain loading, please wait...", color=0xFF0000)
        MEMB = await ctx.send(embed=add_EMB.get())

        async def add_srv2(RID, mEMB, ip, platform,):
            Data = KaiBase.Database()
            def build_con(List):
                Dict = {}
                for i in List:
                    Dict[f"{i[0]}":f"{i[1]}"]
                return Dict
            def append_server(ip, platform):
                try:
                    Data.execute(f"insert into server_track(ip, platform) values ('{ip}', '{platform}')")
                    Data.commit()
                    return 0
                except Exception as e:
                    print(e)
                    return 1
            def append_channel(RID, ip):
                try:
                    Data.execute(f"insert into chanel_reports(id, serv_ip) values ('{RID}', '{ip}')")
                    Data.commit()
                    return 0
                except:
                    return 1
            try:
                result = self.fetchsrv(ip, platform)
            except:
                await self.EditEMB(mEMB, self.emb_fail.get(Des="Unknown server"))
                return 1
            items = result
            f_ip = items["ip"]
            f_port = items["port"]
            b_ip = f"{f_ip}:{f_port}"
            add_srv = append_server(b_ip, platform)
            add_ch = append_channel(RID, b_ip)
            if add_srv == 0 and add_ch==0:
                emb = DiscordUtils.EMBEDS(Type="success", title="Saved!!", description="the server has been saved successfully!")
                await self.EditEMB(mEMB, emb)
            else:
                await self.EditEMB(mEMB, self.emb_fail.get(Des="Server is already added."))

            """
            Data = KaiBase.Database()
            Data.execute("select * from server_track")
            contents = Data.cursor.fetchall()
            tracking_list = build_con(contents)"""

        async def list_srv(RID, CH):
            pass

        async def unknown_args(MEMB):
            res_add_EMB = BotUtils.EMBEDS(title="Unknown Arguement", description="my brain cant process this command.", color=0x964B00)
            res_add_EMB.set_img("Others/mumei_think1")
            await self.EditEMB(MEMB, res_add_EMB.get())

        try:  ######START#######
            arg = args
            if len(arg) <= 0:
                arg = ("channel", "idk")

            if str(option) == "add":
                if str(args[0]).lower() == "server":
                    print("shit")
                    ip = str(args[1])
                    try:
                        platform = str(args[2])
                    except:
                        platform = "java"
                    await add_srv2(ctx.channel.id, MEMB, ip, platform)
                else:
                    await unknown_args(MEMB)            


            #print(args)
            elif str(option) == "list":
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
                    await MEMB.edit(embed=emb)
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
                    await MEMB.edit(embed=emb)
            else:
                res_add_EMB = self.emb_fail.get(Title="Not found", Des="cant find this command.", color=0x964B00)
                await self.EditEMB(MEMB, res_add_EMB)
        except Exception as e:
            send_err = self.emb_err.get(Des="error while executing command.")
            send_err.add_field(name=str(type(e)), value=e)
            await self.EditEMB(MEMB, send_err)

def setup(client):
    client.add_cog(MCServersMonitor(client))
