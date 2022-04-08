from unicodedata import name
import discord, configparser
from discord.ext import commands, tasks
from KaitoUWU import BotUtils

config = configparser.ConfigParser()
config.read("Properties.ini")

class SystemError(Exception):
    pass

class CommandError(Exception):
    pass

def filte(item):
    remove = "<@!>"
    for r in remove:
        try:
            item = item.replace(r, "")
        except: pass
    return item

class BotTools(commands.Cog, name="Bot Management"):
    def __init__(self, client):
        self.client = client
        self.embs = BotUtils.Response()
        self.zoe = BotUtils.SENDER(client)

    async def startup(self, ctx):
        mainemb = self.embs.load.get()
        main_emb = await self.zoe.ReportEMB(ctx.channel.id, mainemb)
        return main_emb

    async def security(self, ctx):
        BotUtils.Permission.Admin(ctx)
        BotUtils.Permission.Block(ctx)

    async def Error(self, main_emb, msg):
        send_err = self.embs.err.get(Des="error while executing command.")
        send_err.add_field(name=str(type(msg)), value=msg)
        await self.zoe.EditEMB(main_emb, send_err)

    async def Done(self, main_emb, msg):
        DD = self.embs.scc.get(Des=msg)
        await self.zoe.EditEMB(main_emb, DD)

    @commands.command()
    async def reload(self, ctx, extension):
        Main = await self.startup(ctx)
        try:
            await self.security(ctx)
            if extension.startswith("sys"):
                raise SystemError("cogs that's starts with \"sys\" cant be unloaded")
            self.client.unload_extension(f"cogs.{extension}")
            self.client.load_extension(f"cogs.{extension}")
            await self.Done(Main, f"{extension} has been reloaded")
        except Exception as e:
            await self.Error(Main, e)

    @commands.command()
    async def load(self, ctx, extension):
        Main = await self.startup(ctx)
        try:
            await self.security(ctx)
            self.client.load_extension(f"cogs.{extension}")
            await self.Done(Main, f"{extension} has been loaded")
        except Exception as e:
            await self.Error(Main, e)
            
    @commands.command()
    async def unload(self, ctx, extension):
        Main = await self.startup(ctx)
        try:
            await self.security(ctx)
            if extension.startswith("sys"):
                raise SystemError("cogs that's starts with \"sys\" cant be unloaded")
            self.client.unload_extension(f"cogs.{extension}")
            await self.Done(Main, f"{extension} has been unloaded")
        except Exception as e:
            await self.Error(Main, e)

    @commands.command()
    async def add_user(self, ctx, user_id, operation):
        def checker(ID):
            adm = [line.strip() for line in open("Data\\admin.txt", "r")]
            bll = [line.strip() for line in open("Data\\blocklist.txt", "r")]
            if ID in adm: return "block an admin"
            elif ID in bll: return "turn a blocked person into admin"
            else: return None
        Main = await self.startup(ctx)
        try:
            await self.security(ctx)
            allowed = ["admin.txt", "blocklist.txt"]
            if f"{operation}.txt" in allowed:
                if checker(filte(user_id)) == None:
                    with open(f"Data\\{operation}.txt", "a") as F:
                        print(filte(user_id), file=F)
                    await self.Done(Main, f"{user_id} has been added to {operation}")
                else:
                    raise CommandError(f"you cant {checker(filte(user_id))}")
            else: raise CommandError("unknown syntax -> {operation}")
        except Exception as e:
            await self.Error(Main, e)

    @commands.command()
    async def remove_user(self, ctx, user_id, operation):
        Main = await self.startup(ctx)
        try:
            await self.security(ctx)
            allowed = ["admin.txt", "blocklist.txt"]
            if f"{operation}.txt" in allowed:
                cache = [line.strip() for line in open(f"Data\\{operation}.txt")]
                if filte(user_id) in cache:
                    rem = cache.index(filte(user_id))
                    if rem == 0: raise CommandError("Fuck you! youre not allowed to do that!")
                    else:
                        cache.pop(rem)
                        with open(f"Data\\{operation}.txt", "w") as F:
                            F.write("")
                        with open(f"Data\\{operation}.txt", "a") as A:
                            for c in cache:
                                print(c, file=A)
                        await self.Done(Main, f"{user_id} has been removed to {operation}")
                else: raise CommandError(f"{user_id} is not in {operation}")
            else: raise CommandError("unknown syntax -> {operation}")
        except Exception as e:
            await self.Error(Main, e) 

    @commands.command()
    async def status(self, ctx, *option):
        try:
            BotUtils.Permission.Block(ctx)
            stat = BotUtils.FileHandler.JSON(r"Data\botstatus.json")
            if len(option) <= 0:
                opt = ["show"]
            else:
                opt = list(option)
        
            if opt[0] == "show":
                items = stat.Load()
                current = items["current"]
                await ctx.send(items["response"][current])

            elif opt[0] == "set":
                await self.security(ctx)
                try:
                    items = stat.Load()
                    rep = str(opt[1])
                    key = ["normal", "debug", "maintenance"]
                    if rep in key:
                        items["current"] = rep
                        stat.Save(items)
                        await ctx.send(f"status has been set to {rep}")
                    else: await ctx.send(f"unknown mode \"{rep}\"")
                except:
                    pass

            else:
                ctx.send(f"unknown command \"{opt[0]}\"")

            
        except Exception as e:
            erremb = discord.Embed(title="Error!", color=0xFF0000)
            erremb.add_field(name=str(type(e)), value=e)
            await ctx.send(embed=erremb)


def setup(client):
    client.add_cog(BotTools(client))
