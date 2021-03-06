import discord
from discord.ext import commands, tasks
import json, time
from KaitoUWU import mcsrvstat as MCsrv
from KaitoUWU import BotUtils, AniSearch
from discord_components import DiscordComponents, ComponentsBot, Button
from saucenao_api import SauceNao, errors, BasicSauce, BookSauce, VideoSauce
import configparser

logger = BotUtils.Logger("Data\\logs.txt", "AniTools logger is now connected")
config = configparser.ConfigParser()
config.read("Properties.ini")
APIs = config["API"]

class RateLimitError(Exception):
    pass

class Embeds():
    def tracermoe(result, color=None) -> discord.Embed:
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
        if color != None:
            emb = discord.Embed(title=tllist[Tk[0]], description=f"**episode:** {result['episode']}", color=color)
        else: emb = discord.Embed(title=tllist[Tk[0]], description=f"**episode:** {result['episode']}")
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

    def SNAO(result, color=None) -> discord.Embed:
        #[r.author, r.index_id, r.index_name, r.similarity, r.thumbnail, r.title, r.raw]
        author = result.author
        s_index_name = result.index_name.split("-")
        f_index_name = s_index_name[0]
        if author is None: author = "Unknown"
        if color != None:
            emb = discord.Embed(title=result.title, description=f_index_name, color=color)
        else: emb = discord.Embed(title=result.title, description=f_index_name)
        emb.set_thumbnail(url=result.thumbnail)
        exl = ""
        for l in range(len(result.urls)): exl += f" [link{l+1}]({result.urls[l]}) |"
        inf = ""
        inf += f'**similarity:** {result.similarity}%\n'
        if result.author != None: inf += f"**Author:** {author}"
        if isinstance(result, VideoSauce):
            inf += f"**episode:** {result.part}\n"
            inf += f"**year:** {result.year}\n"
            inf += f"**frame:** {result.est_time}\n"
        elif isinstance(result, BookSauce):
            inf += f"**Chapter:** {result.part}\n"
        if len(result.urls) > 0: emb.add_field(name="external links", value=exl[1:-1], inline=False)
        emb.add_field(name="info:", value=inf)
        return emb
            
class Main(commands.Cog, name="For Weebs"):
    def __init__(self, client):
        self.client = client
        self.pager = BotUtils.Pages(client)
        self.embs = BotUtils.Response()
        self.zoe = BotUtils.SENDER(client)
        self.snao = SauceNao(APIs["saucenao"])
        self.nao_l = None
        
    async def startup(self, ctx):
        mainemb = self.embs.load.get(color=ctx.author.color)
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
            async def callback(event, emb): await event.message.edit(embed=emb)
            await self.pager.Button_Events(callback)
        except Exception as e: print(e)

    async def tracemoe(self, ctx, attc):
        mainemb = await self.startup(ctx)
        try:
            if type(attc) == str: url = attc
            else: url = attc.url
            engine = AniSearch.TraceMoe.Asyncro()
            find = await engine.search(url)
            result = find["result"]
            engine.DUMP("rrr.json")
            #print(f"building embeds for {len(result)} results")
            embs = []
            for r in result:
                c = result.index(r) + 1
                t = len(result)
                emb = Embeds.tracermoe(r, color=ctx.author.color)
                emb.set_footer(text=f"showing {c} out of {t} results from trace.moe API")
                embs.append(emb)
            preview, buttons = self.pager.Book(embs)
            await self.zoe.EditEMB(mainemb, preview, buttons)
        except Exception as e:
            await self.Error(mainemb, e)

    async def SauceSy(self, ctx, attc=None):
        mainemb = await self.startup(ctx)
        try:
            if type(attc) == str: url = attc
            else: url = attc.url
            embs= []
            IDX = 1
            try: results = self.snao.from_url(url)
            except Exception as e:
                if type(e) == errors.ShortLimitReachedError: raise RateLimitError("Chill bro i can only do 6 request per 30 secs")
            for r in results:
                c = IDX
                t = len(results)
                emb = Embeds.SNAO(r, color=ctx.author.color)
                emb.set_footer(text=f"showing {c} out of {t} results from saucenao API")
                embs.append(emb)
                IDX += 1
            preview, buttons = self.pager.Book(embs)
            await self.zoe.EditEMB(mainemb, preview, buttons)
                
        except Exception as e:
            await self.Error(mainemb, e)
        
    @commands.command()
    async def anisauce(self, ctx, link=None):
        """
        searching tool mainly for Anime"""
        if link != None: await self.tracemoe(ctx, link)
        def checker(m):
            if m.author.id == ctx.message.author.id and m.channel.id == ctx.channel.id:
                return m
        contents = ctx.message.attachments
        if len(contents) > 0:
            for att in contents: await self.tracemoe(ctx, att)
        else:
            event = await self.client.wait_for("message", check=checker)
            for att in event.attachments: await self.tracemoe(ctx, att)

    @commands.command()
    async def sauce(self, ctx, link=None):
        """Anime, Manga & fanarts search engine"""
        if link != None: await self.SauceSy(ctx, link)
        def checker(m):
            if m.author.id == ctx.message.author.id and m.channel.id == ctx.channel.id:
                return m
        contents = ctx.message.attachments
        if len(contents) > 0:
            for att in contents: await self.SauceSy(ctx, att)
        else:
            event = await self.client.wait_for("message", check=checker)
            for att in event.attachments: await self.SauceSy(ctx, att)
                
def setup(client: commands.Bot):
    client.add_cog(Main(client))
