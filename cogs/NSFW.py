import discord, json, requests
from discord.ext import commands, tasks
from KaitoUWU.Asacoco.kaichu import Kaichu

class Yabai(commands.Cog):
    def __init__(self, client):
        self.client = client

    def buildEMB(self, Dict):
        emb = discord.Embed(title=Dict["title"], description="Score:{}".format(Dict["scores"]))
        emb.set_image(url=Dict["url"])
        emb.add_field(name="link", value=Dict["url"])
        return emb

    async def dm(user, item):
        pass

    @commands.command()
    async def culture(self, ctx, Type, index="random", *Options):
        if len(Options) == 0:
            Options = ("top", 10)
        if str(Type).startswith("r/"):
            try:
                if index == "random":
                    index = "lewds"
                subreddit = Kaichu(f"{Type[2:]}")
                #await subreddit.fetch(f"{Options[0]}", f"{index}")
                await subreddit.fetch2(f"{Options[0]}")
                items = await subreddit.GetDict()
                for i in items:
                    await ctx.send(embed=self.buildEMB(items[i]))
                await ctx.send(str(items))
            except Exception as e:
                await ctx.send(f"Error {e}"

    @commands.command()
    async def openL(self, ctx, link):
        try:
            req = requests.get(link)
            #temp = json.loads(req.json())
            await ctx.send(req.text)
            await ctx.send(req.json)
        except Exception as e:
            await ctx.send(f"Error {e}")

    @commands.command()
    async def ncode(self, ctx, code, mode="view"):
        pass
        


def setup(client):
    client.add_cog(Yabai(client))
