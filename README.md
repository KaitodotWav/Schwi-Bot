# Schwi-Bot

Bot for discord

-------------------------------------------------------
# Help

## Minecraft

### `ping [server ip] [platform: java or bedrock] [options]`

Sends minecraft server information
Options:
-- open <default> : sends server information
-- dump : sends server data in json format
Note:
player list is only available on java and if server allowed player query

## For Weebs

### `anisauce [link or pictures]`

Anime picture search engine

Sends Anime titles and sources using pictures using tracemoe API

-- link : sends anime title/sources using link to a picture file

ex: `blank`

-- pictures : sends anime title/sources base on uploaded pictures

"sends results depends on how many pictures has been sent"

### `sauce [link or  pictures]`

Anime, Manga, Hentai, Doujin & Fan arts search engine

Send Anime, Manga or Doujin titles and sources using pictures and clips

-- link : search title/sources using link to a picture or clip

ex: `blank`

-- pictures : search title/sources using uploaded picture/clips

"sends results depends on how many pictures/clips has been sent"

-------------------------------------------------------
# Info 

## Python programs:

### `Schwi.py` main program

## Folders:

### /cogs = bot commands and functions

all files that contains `_` as prefix is under rework, trash or restricted so i wont include them

all files that contains `sys` as prefix are by default will be loaded automatically and cant be unloaded

`MCtools.py` contains all Minecraft commands

`AniTools.py` contains all ForWeebs commands

`sysBotHandler.py` contains commands for bot management and for bot admins only

`sysLogger.py` background process for sending bot logs to discord

###  /dumps = dumping folder of servers meta data

dont sweat the details this is just an empty folder

### /KaitoUWU = all packages created for schwii

`mcsrvstat.py` API module for collecting Minecraft server information

`KaiBase.py` module to handle local and postgres Database

`containers.py` module to handle class containers

`BotUtils.py` module contails all classes used for bot operations

`AniSearch.py` API module for collecting data from tracemoe

###  /Data = contains all files needed by the bot


# Data files:

## Properties.ini = Bot Settings

### `Bot_Name` (default:Schwi)

`Token` Bot discord token

`Logs` Channel ID for bot logs

`Reports` Channel ID for bot reports

`Prefix` Bot Prefix

`Debug` Bot debug mode (default:false)

### `reddit` reddit bot credentials

`id` bot id

`secret` bot client secret

`agent` bot agent`

### API

`saucenao` saucenao api auth token

## Emotes.ini

collection of image links for bot response

`fail` for failed operations

`success` for sucessful operations

`error` for error response

`loading` for command loading display

`bonk` for NSWF content warning

`dame` for blocked operations

`ayo` non toxic response to a greeting

`Others` i forgor what is the contents of these links

## logs.txt

bot logs, obviously

## admins.txt

list of users that has higher access on bots

## blocklist

list of users that is not allowed to use to bot

## TwitterAuth.json = Auth for tweepy

`bot name` :

	`bearer`
	
	`token`
	
	`secret`
	
	`con_key`
	
	`con_secret`


-------------------------------------------------------
# Note:

this bot is currently being coded base on the first bot "Poyoyo bot"

still not done but already functional

a faster, less buggy and improved discord bot

-------------------------------------------------------




