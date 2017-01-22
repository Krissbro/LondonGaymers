from discord.ext import commands
from .utils import checks
from __main__ import settings
import os
import discord
import glob
from .utils.chat_formatting import pagify, box
import re
import os
import aiohttp
import asyncio
import random
from cogs.utils.dataIO import dataIO
import requests
import json
from random import choice
from subprocess import check_output
try:
    import ffmpy
    ffmpyinstalled = True
except:
    print("You don't have ffmpy installed, installing it now...")
    try:
        check_output("pip3 install ffmpy", shell=True)
        print("FFMpy installed succesfully!")
        import ffmpy
        ffmpyinstalled = True
    except:
        print("FFMpy didn't install succesfully.")
        ffmpyinstalled = False
try:
    from pyshorteners import Shortener
    pyshortenersinstalled = True
except:
    print("You don't have pyshorteners installed, installing it now...")
    try:
        check_output("pip3 install pyshorteners", shell=True)
        print("Pyshorteners installed succesfully!")
        import pyshorteners
        pyshortenersinstalled = True
    except:
        print("Pyshorteners didn't install succesfully.")
        pyshortenersinstalled = False

class Useful:
    """Useful stuffz!"""

    def __init__(self, bot):
        self.bot = bot
        self.settings = dataIO.load_json("data/useful/settings.json")

    @commands.command(pass_context=True, name="calc", aliases=["calculate"])
    async def _calc(self, ctx, evaluation):
        """Solves a math problem so you don't have to!
        + = add, - = subtract, * = multiply, and / = divide

        Example:
        [p]calc 1+1+3*4"""
        prob = re.sub("[^0-9+-/* ]", "", ctx.message.content[len(ctx.prefix + "calc "):].strip())
        try:
            answer = str(eval(prob))
            await self.bot.say("`{}` = `{}`".format(prob, answer))
        except:
            await self.bot.say("I couldn't solve that problem, it's too hard")

    @commands.command(pass_context=True)
    async def suggest(self, ctx, *, suggestion : str):
        """Sends a suggestion to the owner."""
        if settings.owner == "id_here":
            await self.bot.say("I have no owner set, cannot suggest.")
            return
        owner = discord.utils.get(self.bot.get_all_members(), id=settings.owner)
        author = ctx.message.author
        if ctx.message.channel.is_private is False:
            server = ctx.message.server
            source = "server **{}** ({})".format(server.name, server.id)
        else:
            source = "direct message"
        sender = "**{}** ({}) sent you a suggestion from {}:\n\n".format(author, author.id, source)
        message = sender + suggestion
        try:
            await self.bot.send_message(owner, message)
        except discord.errors.InvalidArgument:
            await self.bot.say("I cannot send your message, I'm unable to find"
                               " my owner... *sigh*")
        except discord.errors.HTTPException:
            await self.bot.say("Your message is too long.")
        except:
            await self.bot.say("I'm unable to deliver your message. Sorry.")
        else:
            await self.bot.say("Your message has been sent.")

    @commands.command(pass_context=True)
    @checks.is_owner()
    async def uploadcog(self, ctx, cogname):
        """If you're a lazy fuck and don't want to go to the folder where your bot is located. Smh"""
        if os.path.exists("cogs/{}.py".format(cogname)):
            await self.bot.send_file(ctx.message.channel, content="Here you go:", fp="cogs/{}.py".format(cogname), filename="{}.py".format(cogname))
        else:
            await self.bot.say("That cog does not exist.")

    @commands.command(pass_context=True)
    async def shorten(self, ctx, url):
        """Shorten a link."""
        await self.bot.say("{}, here you go <{}>.".format(ctx.message.author.mention, self.short(url)))
        
    @commands.command(pass_context=True)
    async def qrcode(self, ctx, url):
        """Creates a qrcode from a link."""
        shorten = Shortener('Bitly', bitly_token='dd800abec74d5b12906b754c630cdf1451aea9e0')
        short_link = shorten.short(url)
        async with aiohttp.get(shorten.qrcode(width=128, height=128)) as r:
            file = await r.content.read()
        number = random.randint(1000, 9999)
        fileloc = "data/useful/qrcode{}.png".format(number)
        with open(fileloc, 'wb') as f:
            f.write(file)
            file = None
            f = None
        await self.bot.send_file(ctx.message.channel, fp="data/useful/qrcode{}.png".format(number), filename="qrcode{}.png".format(number))
        os.remove("data/useful/qrcode{}.png".format(number))

    @commands.command()
    async def ctof(self, celsius:float):
        """Convert celsius to fahrenheit."""
        await self.bot.say("{}°C = {}°F ({}°K)".format(celsius, celsius * float(1.8) + 32, celsius + 273.15))
        
    @commands.command()
    async def ftoc(self, fahrenheit:float):
        """Convert fahrenheit to celsius."""
        await self.bot.say("{}°F = {}°C ({}°K)".format(fahrenheit, (fahrenheit - 32) / float(1.8), ((fahrenheit - 32) / float(1.8)) + 273.15))
        
    @commands.command(pass_context=True)
    async def gist(self, ctx, *, snippet):
        """Create a snippet on gist."""
        data = {"description": "A github gist made with the {} Discord bot.".format(self.bot.user.name),
                "public": True,
                "files": {
                    "gist.txt": {
                        "content": snippet
                        }
                    }
                }
        post = requests.post("https://api.github.com/gists", data=json.dumps(data))
        await self.bot.say("{} here you go: <{}>.".format(ctx.message.author.mention, self.short(json.loads(post.content.decode("utf-8"))['files']['gist.txt']['raw_url'])))
        
    def short(self, url):
        shorten = Shortener('Bitly', bitly_token='dd800abec74d5b12906b754c630cdf1451aea9e0')
        return shorten.short(url)
        
    def _list_cogs(self):
        cogs = [os.path.basename(f) for f in glob.glob("cogs/*.py")]
        return ["cogs." + os.path.splitext(f)[0] for f in cogs]
        
    async def on_server_join(self, server):
        if not self.settings['auth_key'] == "key_here":
            data = {'server_count': int(len(self.bot.servers))}
            post = requests.post("https://bots.discord.pw/api/bots/" + self.settings['client_id'] + "/stats", headers={'Authorization': self.settings['auth_key'], 'Content-Type' : 'application/json'}, data=json.dumps(data))
            print("Joined a server, updated stats on bots.discord.pw. " + post.content.decode("utf-8"))
        if not self.settings['auth_key_dl'] == "dl_key_here":
            data = {"token": self.settings['auth_key_dl'], "servers": len(bot.servers)}
            post = requests.post("https://bots.discordlist.net/api.php", data=json.dumps(data))
            print("Left a server, updated stats on bots.discordlist.net. " + post.content.decode("utf-8"))
        
    async def on_server_remove(self, server):
        if not self.settings['auth_key'] == "key_here":
            data = {'server_count': int(len(self.bot.servers))}
            post = requests.post("https://bots.discord.pw/api/bots/" + self.settings['client_id'] + "/stats", headers={'Authorization': self.settings['auth_key'], 'Content-Type' : 'application/json'}, data=json.dumps(data))
            print("Left a server, updated stats on bots.discord.pw. " + post.content.decode("utf-8"))
        if not self.settings['auth_key_dl'] == "dl_key_here":
            data = {"token": self.settings['auth_key_dl'], "servers": len(bot.servers)}
            post = await requests.post("https://bots.discordlist.net/api.php", data=json.dumps(data))
            print("Left a server, updated stats on bots.discordlist.net. " + post.content.decode("utf-8"))
        
def check_folders():
    if not os.path.exists("data/useful"):
        print("Creating data/useful folder...")
        os.makedirs("data/useful")
        
def check_files():
    if not os.path.exists("data/useful/settings.json"):
        print("Creating data/useful/settings.json file...")
        dataIO.save_json("data/useful/settings.json", {'auth_key': 'key_here', 'client_id': 'client_id_here'})
        
class ModuleNotFound(Exception):
    pass
        
def setup(bot):
    if not ffmpyinstalled:
        raise ModuleNotFound("FFmpy is not installed, install it with pip3 install ffmpy.")
    if not pyshortenersinstalled:
        raise ModuleNotFound("Pyshorteners is not installed, install it with pip3 install pyshorteners.")
    check_folders()
    check_files()
    bot.add_cog(Useful(bot))