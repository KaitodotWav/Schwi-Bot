#Schwi bot created by Kaito

#imports
import discord, time, sys, configparser, requests, json, os, socket
from discord.ext import commands
from KaitoUWU import CMD

config = configparser.ConfigParser()
config.read("Properties.ini")

#Auth
Token = str(config["Schwi"]["Token"])

client = commands.Bot(command_prefix = str(config["Schwi"]["Prefix"]))

"""
#Instance
def ShowWarning(TITLE, MESSAGE):
    root = Tk()
    root.withdraw()
    TKmsg.showwarning(title=TITLE, message=MESSAGE)
from tendo import singleton

try:
    me = singleton.SingleInstance()
except:
    warnThread = Thread(target=ShowWarning, args=("Error: Multiple Instance", "Main program is already running."))
    warnThread.start()
    WriteF("Error: Reject launch\nMain program is already running", "MainReport.txt")
    print("done")
    sys.exit(-1)
else:
    pass
"""

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
    except Exception as e:
        erremb = discord.Embed(title="Error!", description=f"{e}", color=0xFF0000)
        await ctx.send(embed=erremb)
        
@client.command()
async def unload(ctx, extension):
    try:
        client.unload_extension(f"cogs.{extension}")
        await ctx.send(f"{extension} has been unloaded")
    except Exception as e:
        erremb = discord.Embed(title="Error!", description=f"{e}", color=0xFF0000)
        await ctx.send(embed=erremb)
    
@client.event
async def on_ready():
    report = client.get_channel(int(config["Notifs"]["Reports"]))
    try:
        host = socket.gethostname()
        #report = client.get_channel(int(config["Notifs"]["Reports"]))
        print(f"{client.user} is online in {host}")
        await report.send(f"Report: {client.user} is online in {host}.")
    except Exception as e:
        print(e)
        
        print("{0.user} is online".format(client))
        await report.send("Report: {0.user} is online.".format(client))

#run
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        if filename.startswith("_"):
            pass
        else:
            try:
                client.load_extension(f"cogs.{filename[:-3]}")
            except Exception as e:
                print(f"Error!: {e}")
try:
    client.run(Token)
except Exception as e:
    if str(e) == "Cannot connect to host discord.com:443 ssl:default [getaddrinfo failed]":
        print("Error! no internet.")
    else:
        print(e)
