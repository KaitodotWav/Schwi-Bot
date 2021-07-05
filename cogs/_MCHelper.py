#help commands for minecraft
import discord
from dicord.ext import commands
import json

class NotFound(Error):
        pass

def LtoS(List):
    build = ""
    for i in List:
        build += f" {i},"
    return build[1:len(build)-1]

class MCforDummies(commands.Cog):
    def __init__(self, client):
        self.client = client

    def search(self, search, where, All=False):
        with open("enchantments.json", "r") as F:
            cache = json.loads(F.read())
        enchants = cache["enchants"]
        results = []

        try:
            for i in enchants:
                names = str(i[f"{where}"]).lower()
                find = str(search).lower()
                if names == find:
                    if All:
                        results.append(i)
                    else:
                        return i
                if All:
                    return results
        except:
            raise NotFound(f"{search} not found.")

    def buildEmbed(self, items):
        emb = discord.embed(title=items["displayName"], description=)

    @commands.command()
    async def enchant(self, enchantment):


def setup(client):
    client.add_cog(MCforDummies(client))
