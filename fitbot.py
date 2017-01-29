import json
import logging
from random import randrange
from urllib.request import Request, urlopen

from discord.ext import commands

description = '''A Bot that searches o.smium.org for fittings and outputs them to a discord channel'''

# Setup Logs

discord_logger = logging.getLogger('discord')
discord_logger.setLevel(logging.WARNING)
log = logging.getLogger()
log.setLevel(logging.INFO)
handler = logging.FileHandler(filename='fitbot.log', encoding='utf-8', mode='w')
log.addHandler(handler)


bot = commands.Bot(command_prefix='?', description='FitBot')


def is_fitting_channel():
    def predicate(ctx):
        return ctx.message.channel.name == 'fitting'
    return commands.check(predicate)


@bot.event
async def on_ready():
    print('Logged in as:')
    print('Username: ' + bot.user.name)
    print('ID: ' + bot.user.id)
    print('------')


@bot.command()
@is_fitting_channel()
async def random():
    """Grabs a random Osmium fitting and outputs it in EFT format"""

    offset = randrange(1,1000)

    url = Request("https://o.smium.org/api/json/loadout/query/@dps >=0?limit=1&sortby=creationdate&offset=" + str(offset))
    url.add_header("User-Agent","FitBot Discord Bot - Contact EvilGrin#0659")
    response = urlopen(url)



    data = json.loads(response.read().decode('utf8'))

    fitid = data[0]['uri'].split("/")[4]
    efturl = "https://o.smium.org/api/convert/" + fitid + "/eft/"
    eftresponse = urlopen(efturl)

    await bot.say("```\n" + eftresponse.read().decode("utf-8") + "```")


@bot.command()
@is_fitting_channel()
async def search(query : str):
    """Searches Osmium fittings and outputs it in EFT format
    More complex queries need to be enclosed in double quotes

    If you are unsure of the syntax please read the instructions
    on the Osmium website:

    https://o.smium.org/help/search

    Complex searches should look like:

    ?search "@ship drake @tags pve @dps > 400"
    """

    url = Request("https://o.smium.org/api/json/loadout/query/" + query + "?minify=0&limit=1&offset=1")
    url.add_header('User-Agent','FitBot Discord Bot - Contact EvilGrin#0659')
    response = urlopen(url)

    data = json.loads(response.read().decode('utf8'))

    if data:
        fitid = data[0]['uri'].split("/")[4]
        efturl = "https://o.smium.org/api/convert/" + fitid + "/eft/"
        eftresponse = urlopen(efturl)
        await bot.say("```\n" + eftresponse.read().decode("utf-8") + "```")
    else:
        await bot.say("No results. Check your search syntax is correct or try something else.")


bot.run('Mjc0NTcwNTg3NjIyNjA0ODAw.C20BTg.RKRrlcYs36wEq42A_NUYY6zE3Gc')
