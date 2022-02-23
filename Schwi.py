#Schwi bot created by Kaito

#imports
import discord, time, sys, configparser, requests, json, os

with open("Data\\logs.txt", "a") as log:
    print("bot logger is connected", file=log)

from KaitoUWU import BotUtils

stime = BotUtils.Timer()
stime.start()

from discord.ext import commands
from KaitoUWU import CMD

config = configparser.ConfigParser()
config.read("Properties.ini")
errors = []

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
        import socket
        host = socket.gethostname()
        zoe = BotUtils.SENDER(client)
        await zoe.Report(int(config['Notifs']['Reports']), "test brodcast", True)
    except Exception as e:
        print(e)
        errors.append((type(e), e))
        host = "unknown"
    finally:
        on_emb = discord.Embed(title=f"{client.user} is now online", description=f"Host:{host}", color=0x00FF00)
        for i in errors:
            print(i)
            emb = BotUtils.EMBEDS(Type="error", title="Error!", description="while starting the bot.")
            sendE = emb.get()
            sendE.add_field(name=str(i[0]), value=str(i[1]))
            await report.send(embed=sendE)
        btime = stime.end()
        on_emb.add_field(name="elapse bot start", value="{} sec/s".format(round(btime,2)))
        print(f"{client.user} is now online on host:{host}")
        await report.send(embed=on_emb)

#run
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        if filename.startswith("_"):
            pass
        else:
            try:
                client.load_extension(f"cogs.{filename[:-3]}")
            except Exception as e:
                errors.append((type(e), e))
                print(f"Error!: {e}")
try:
    client.run(Token)
except Exception as e:
    if str(e) == "Cannot connect to host discord.com:443 ssl:default [getaddrinfo failed]":
        print("Error! no internet.")
    else:
        print(e)
