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
    """Useful stuffz"""

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
        """Sends a suggestion to the team."""
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

    @commands.command()
    async def emoteurl(self, *, emote:discord.Emoji):
        """Gets the url for a CUSTOM emote (meaning no emotes like :eyes: and :ok_hand:)"""
        await self.bot.say(emote.url)
        
    @commands.command(pass_context=True)
    async def shorten(self, ctx, url):
        """Shorten a link."""
        await self.bot.say("{}, here you go <{}>.".format(ctx.message.author.mention, self.short(url)))

    @commands.command()
    async def ctof(self, celsius:float):
        """Convert celsius to fahrenheit."""
        await self.bot.say("{}°C = {}°F ({}°K)".format(celsius, celsius * float(1.8) + 32, celsius + 273.15))
        
    @commands.command()
    async def ftoc(self, fahrenheit:float):
        """Convert fahrenheit to celsius."""
        await self.bot.say("{}°F = {}°C ({}°K)".format(fahrenheit, (fahrenheit - 32) / float(1.8), ((fahrenheit - 32) / float(1.8)) + 273.15))
        
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