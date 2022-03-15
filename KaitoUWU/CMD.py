#imports
import discord, json
from KaitoUWU import BotUtils

#other functions
def LtoS(List):
    build = ""
    for i in List:
        build += f" {i},"
    return build[1:len(build)-1]

#main commands
def Process(client):
    #commands
    
    @client.command()
    async def status(ctx, *option):
        try:
            BotUtils.Permission.Block(ctx)
            stat = BotUtils.FileHandler.JSON(r"Data\botstatus.json")
            opt = list(option)
            if len(opt) <= 0:
                opt = ["show"]
            
            if option[0] == "show":
                items = stat.Load()
                current = items["current"]
                ctx.send(items["response"][current])

            elif option[0] == "set":
                BotUtils.Permission.Admin(ctx)
                try:
                    items = stat.Load()
                    rep = str(option[1])
                    selection = key(items["response"])

                except:
                    pass

            
        except Exception as e:
            erremb = discord.Embed(title="Error!", description=f"{e}", color=0xFF0000)
            await ctx.send(embed=erremb)

    #on message event
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        print(message.content)
        await client.process_commands(message)
