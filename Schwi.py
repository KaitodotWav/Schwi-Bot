#Schwi2.0 bot created by Kaito

#imports
import discord, time, sys, configparser, requests, json, os, socket
from KaitoUWU import BotUtils, containers
from discord.ext import commands

if len(sys.argv) >= 2: bot = (str(sys.argv[1]))
else:
    if __name__ == "__main__":
        bot = "Schwi"

stime = BotUtils.Timer(2)
stime.start()
logger = BotUtils.Logger("Data\\logs.txt", f"{bot} loaded! starting up.", True)
BOT = containers.Bot(bot)
errors = []

#Auth
intents = discord.Intents(messages=True, guilds=True)
client = commands.Bot(command_prefix = BOT.prefix, help_command=BOT.help(),intents=intents)

@client.event
async def on_ready():
    zoe = BotUtils.SENDER(client)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,
    name=f"{BOT.prefix} commands"))
    try: host = socket.gethostname()
    except Exception as e:
        print(e)
        errors.append((type(e), e))
        host = "unknown"
    finally:
        on_emb = discord.Embed(title=f"{client.user} is now online", description=f"Host:{host}", color=0x00FF00)
        for i in errors:
            logger.log(f"{i[0]} {i[1]}")
            emb = BotUtils.EMBEDS(Type="error", title="Error!", description="while starting the bot.")
            sendE = emb.get()
            sendE.add_field(name=str(i[0]), value=str(i[1]))
            await zoe.ReportEMB(BOT.report, sendE)
        startup = stime.end()
        inf = ""

        if type(startup) == float or type(startup) == int: inf += f"**startup:** {startup}sec/s\n"
        else: inf += f"**startup:** {startup}\n"
        inf += f"**prefix:** {BOT.prefix}\n"
        on_emb.add_field(name="Info", value=f"{inf}")
        logger.log(f"[bot] {client.user} is now online on host:{host}\nprefix: {BOT.prefix}, startup: {startup}sec/s")
        await zoe.ReportEMB(BOT.report, on_emb, True)

#run
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        if filename.startswith("_"): pass
        else:
            try:
                client.load_extension(f"cogs.{filename[:-3]}")
                logger.log(f"[cogs] {filename[:-3]} has been loaded")
            except Exception as e:
                errors.append((type(e), e))
                logger.log(f"Error!: {e}")

try: client.run(BOT.token)
except Exception as e:
    if str(e) == "Cannot connect to host discord.com:443 ssl:default [getaddrinfo failed]":
        logger.log("[system] Error! no internet.")
    else: logger.log(e)



