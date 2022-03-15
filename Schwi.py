#Schwi bot created by Kaito

#imports
import discord, time, sys, configparser, requests, json, os
from KaitoUWU import BotUtils

stime = BotUtils.Timer()
stime.start()
logger = BotUtils.Logger("Data\\logs.txt", "Bot logger is now connected\n", True)

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

    
@client.event
async def on_ready():
    report = int(config["Notifs"]["Reports"])
    zoe = BotUtils.SENDER(client)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,
    name="{} commands".format(config["Schwi"]["Prefix"])))
    try:
        import socket
        host = socket.gethostname()
    except Exception as e:
        print(e)
        errors.append((type(e), e))
        host = "unknown"
    finally:
        on_emb = discord.Embed(title=f"{client.user} is now online", description=f"Host:{host}", color=0x00FF00)
        for i in errors:
            logger.log("{} {}".format(i[0], i[1]))
            emb = BotUtils.EMBEDS(Type="error", title="Error!", description="while starting the bot.")
            sendE = emb.get()
            sendE.add_field(name=str(i[0]), value=str(i[1]))
            await zoe.ReportEMB(report, sendE)
        btime = stime.end()
        on_emb.add_field(name="elapse bot start", value="{} sec/s".format(round(btime,2)))
        logger.log(f"{client.user} is now online on host:{host}")
        await zoe.ReportEMB(report, on_emb, True)

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
                logger.log(f"Error!: {e}")
try:
    client.run(Token)
except Exception as e:
    if str(e) == "Cannot connect to host discord.com:443 ssl:default [getaddrinfo failed]":
        logger.log("Error! no internet.")
    else:
        logger.log(e)
