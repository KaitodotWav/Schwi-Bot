import configparser, discord, json
from discord.ext import commands

class NewHelp(commands.HelpCommand):
    def __init__(self):
        super().__init__()
        with open("Data/cmdlinks.json") as c:
            links = json.loads(c.read())
        self.cogl = links["cogs"]
        self.cmdl = links["commands"]

    async def SS(self, con):
        if type(con) == discord.Embed:
            await self.get_destination().send(embed=con)
        else:
            await self.get_destination().send(con)

    async def send_bot_help(self, mapping):
        emb = discord.Embed(title="Help", description=f"use {self.clean_prefix}help [command] to show command usage")
        cmdlinked = False
        c = 0
        for cog in mapping:
            name = [command.name for command in mapping[cog]]
            des = [command.help for command in mapping[cog]]
            if len(name) > 0:
                cname = "None"
                try:
                    cname = f"{cog.qualified_name}"
                except: pass
                val = ""
                for i in range(len(name)):
                    val += "- "
                    nn = f"**{name[i]}**"
                    if name[i] in self.cmdl:
                        val += f"[{nn}]({self.cmdl[name[i]]})"
                        cmdlinked = True
                    else: val += nn
                    if des[i] != None: val += f" {des[i]}"
                    val += '\n'
                if cname in self.cogl: val += f"- [more info]({self.cogl[cname]})\n"
                emb.add_field(name=cname, value=val, inline=False)
        if cmdlinked: emb.set_footer(text="tip: click on blue commands to see more info")
        await self.SS(emb)
        
    async def send_cog_help(self, cog):
        name = [cmd.name for cmd in cog.get_commands()]
        des = [cmd.help for cmd in cog.get_commands()]
        cname = "None"
        try: cname = f"{cog.qualified_name}"
        except: pass
        emb = discord.Embed(title=f"Help for cog \"{cname}\"", description=f"use {self.clean_prefix}help [command] to show command usage")
        if len(name) > 0:
            val = ""
            for i in range(len(name)):
                val += f"- **{name[i]}**"
                if des[i] != None: val += f" {des[i]}"
                val += '\n'
            if cname in self.cogl: val += f"[click here]({self.cogl[cname]}) to see more\n"
            emb.add_field(name="commands", value=val, inline=False)
        await self.SS(emb)

    async def send_group_help(self, group):
        name = [cmd.name for en, cmd in enumerate(group.commands)]
        des = [cmd.help for en, cmd in enumerate(group.commands)]
        cname = "None"
        try: cname = f"{group.name}"
        except: pass
        emb = discord.Embed(title=f"Help for group \"{cname}\"", description=f"use {self.clean_prefix}help [command] to show command usage")
        if len(name) > 0:
            val = ""
            for i in range(len(name)):
                val += f"- **{name[i]}**"
                if des[i] != None: val += f" {des[i]}"
                val += '\n'
            if cname in self.cogl: val += f"[click here]({self.cogl[cname]}) to see more\n"
            emb.add_field(name="commands", value=val, inline=False)
        await self.SS(emb)

    async def send_command_help(self, command):
        usage = command.clean_params
        param = ""
        parent = "None"
        val = f"{command.help}\n"
        try:
            if command.cog.qualified_name != None: parent = command.cog.qualified_name
        except: pass
        for p in usage: param += f" {p},"
        emb = discord.Embed(title=f"Help for command \"{command.name}\"", description=f"this command is part of **{parent}**")
        if command.name in self.cmdl: val += f"[click here]({self.cmdl[command.name]}) to see more info\n"
        emb.add_field(name=f"**{command.name}** [{param[1:-1]}]", value=val)
        await self.SS(emb)
        

class Bot():
    def __init__(self, client):
        config = configparser.ConfigParser()
        config.read("Properties.ini")
        self.token = config[client]["Token"]
        self.logs = int(config[client]["Logs"])
        self.report = int(config[client]["Reports"])
        self.prefix = config[client]["Prefix"]
        self.debug = config[client]["Debug"]
        self.help = NewHelp
