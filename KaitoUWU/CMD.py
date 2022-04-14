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
    

    #on message event
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        #logger.log(f"[{message.author}] {message.content}")
        await client.process_commands(message)
