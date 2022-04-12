import discord
from discord.ext import commands, tasks
import json, time
from KaitoUWU import mcsrvstat as MCsrv
from KaitoUWU import BotUtils, AniSearch
from discord_components import DiscordComponents, ComponentsBot, Button

logger = BotUtils.Logger("Data\\logs.txt", "AniTools logger is now connected")

class Embeds():
    def tracermoe(result) -> discord.Embed:
        def othertl(tlk, tlv):
            final = ""
            for t in range(len(tlk)):
                final += f"**{tlk[t]}:** {tlv[t]}\n"
            return final
        meta = result["anilist"]
        tllist = {}
        for t in meta["title"]:
            if meta["title"][t] != None:
                tllist[t] = meta["title"][t]
        Tk = list(tllist.keys())
        Tv = list(tllist.values())
        emb = discord.Embed(title=tllist[Tk[0]], description=f"**episode:** {result['episode']}")
        if len(tllist) > 1: emb.add_field(name="Other Titles", value=othertl(Tk[1:], Tv[1:]), inline=False)
        emb.set_image(url=result["image"])
        inf = ""
        inf += f"**Similarity:** {int(result['similarity']*100)}%\n"
        if meta["isAdult"]: inf += "**NSFW**\n"
        emb.add_field(name="Info", value=inf, inline=True)
        F = result["from"]
        T = result["to"]
        emb.add_field(name="Frames", value=f"**from: **{F}\n**to:** {T}")
        return emb
            
class Main(commands.Cog, name="For Weebs"):
    def __init__(self, client):
        self.client = client
        self.pager = BotUtils.Pages(client)
        self.embs = BotUtils.Response()
        self.zoe = BotUtils.SENDER(client)
        
    async def startup(self, ctx):
        mainemb = self.embs.load.get()
        main_emb = await self.zoe.ReportEMB(ctx.channel.id, mainemb)
        return main_emb

    async def Error(self, main_emb, msg):
        send_err = self.embs.err.get(Des="error while executing command.")
        send_err.add_field(name=str(type(msg)), value=msg)
        await self.zoe.EditEMB(main_emb, send_err)

    @commands.Cog.listener()
    async def on_ready(self):
        self.ButEvents.start()
        logger.log("[AniTools] Buttons scan has been started")

    @tasks.loop(seconds=1)
    async def ButEvents(self):
        try:
            async def callback(event, emb):
                #print("called")
                await event.message.edit(embed=emb)
            #print("started")
            await self.pager.Button_Events(callback)
            #print("done")
        except Exception as e:
            print(e)

    async def tracemoe(self, ctx, attc):
        mainemb = await self.startup(ctx)
        try:
            url = attc.url
            engine = AniSearch.TraceMoe.Asyncro()
            find = await engine.search(url)
            result = find["result"]
            engine.DUMP("rrr.json")
            #print(f"building embeds for {len(result)} results")
            embs = []
            for r in result:
                c = result.index(r) + 1
                t = len(result)
                emb = Embeds.tracermoe(r)
                emb.set_footer(text=f"showing {c} out of {t} results from trace.moe API")
                embs.append(emb)
            preview, buttons = self.pager.Book(embs)
            await self.zoe.EditEMB(mainemb, preview, buttons)
        except Exception as e:
            await self.Error(mainemb, e)

    @commands.command()
    async def anisauce(self, ctx):
        """
        searching tool mainly for Anime"""
        def checker(m):
            if m.author.id == ctx.message.author.id and m.channel.id == ctx.channel.id:
                print("match")
                print(m.attachments)
                return m
        contents = ctx.message.attachments
        if len(contents) > 0:
            for att in contents:
                await self.tracemoe(ctx, att)
        else:
            event = await self.client.wait_for("message", check=checker)
            for att in event.attachments:
                await self.tracemoe(ctx, att)

def setup(client: commands.Bot):
    client.add_cog(Main(client))
