#Schwi bot created by Kaito

#imports
import discord, time, sys, configparser, requests, json, os
from discord.ext import commands
import mcsrvstat as MCsrv
import CMD

config = configparser.ConfigParser()
config.read("Properties.ini")

#Auth
Token = str(config["Schwi"]["Token"])

client = commands.Bot(command_prefix = str(config["Schwi"]["Prefix"]))

#Commands
CMD.Process(client)

@client.command()
async def reload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")
    await ctx.send(f"{extension} has been reloaded")

@client.command()
async def load(ctx, extension):
    try:
        client.load_extension(f"cogs.{extension}")
        await ctx.send(f"{extension} has been loaded")
    except discord.ext.commands.errors.ExtensionNotLoaded as e:
        await ctx.send(f"{e}")
    except discord.ext.commands.errors.CommandInvokeError:
        await ctx.send(f"Error: CommandInvokeError\n{extention} could not be loaded.")
@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    await ctx.send(f"{extension} has been unloaded")
    
@client.event
async def on_ready():
    print("{0.user} is online".format(client))
    report = client.get_channel(int(config["Notifs"]["Reports"]))
    await report.send("Report: {0.user} is online.".format(client))

#run
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        try:
            client.load_extension(f"cogs.{filename[:-3]}")
        except discord.ext.commands.errors.ExtensionFailed as e:
            print("Error: ", e)
    
client.run(Token)