import discord, configparser
from discord.ext import commands, tasks
from KaitoUWU import BotUtils

config = configparser.ConfigParser()
config.read("Properties.ini")

class SystemError(Exception):
    pass

class BotTools(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.main_emb = BotUtils.EMBEDS(Type="loading", title="Processing", description="please wait...")
        self.emb_scc = BotUtils.EMBEDS(Type="success", title="Success!", color=0x00FF00)
        self.emb_err = BotUtils.EMBEDS(Type="error", title="Error!")
        self.zoe = BotUtils.SENDER(client)

    async def startup(self, ctx):
        mainemb = self.main_emb.get()
        main_emb = await self.zoe.ReportEMB(ctx.channel.id, mainemb)
        return main_emb

    async def security(self, ctx):
        BotUtils.Permission.Admin(ctx)
        BotUtils.Permission.Block(ctx)

    async def Error(self, main_emb, msg):
        send_err = self.emb_err.get(Des="error while executing command.")
        send_err.add_field(name=str(type(msg)), value=msg)
        await self.zoe.EditEMB(main_emb, send_err)

    async def Done(self, main_emb, msg):
        DD = self.emb_scc.get(Des=msg)
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



def setup(client):
    client.add_cog(BotTools(client))
