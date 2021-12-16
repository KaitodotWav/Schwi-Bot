import discord
from discord.ext import commands, tasks
from KaitoUWU.Asacoco.kaichu import Kaichu

class Yabai(commands.Cog):
    def __init__(self, client):
        self.client = client

    def buildEMB(sef, Dict):
        emb = discord.Embed(title=Dict["title"], description="Score:{}".format(Dict["scores"]))
        emb.set_image(url=Dict["url"])
        return emb

    @commands.command()
    async def culture(self, ctx, Type, index="random", *Options):
        if len(Options) == 0:
            Options = ("hot", "lol")
        if str(Type).startswith("r/"):
            if index == "random":
                index = "lewds"
            subreddit = Kaichu(f"{Type[2:]}")
            #await subreddit.fetch(f"{Options[0]}", f"{index}")
            await subreddit.fetch2(f"{Options[0]}")
            items = await subreddit.GetDict()
            for i in items:
                await ctx.send(embed=self.buildEMB(items[i]))
            
        


def setup(client):
    client.add_cog(Yabai(client))
