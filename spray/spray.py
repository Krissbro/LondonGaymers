from discord.ext import commands
from random import randint
from random import choice as choice
import random
import discord
import aiohttp
import os
import asyncio
from .utils.dataIO import dataIO
from .utils import checks
from __main__ import send_cmd_help
try:
    if not discord.opus.is_loaded():
        discord.opus.load_opus('libopus-0.dll')
except OSError:
    opus = False
except:
    opus = None
else:
    opus = True

spraylist = [
"https://media.giphy.com/media/uSy9uVHKqRNjG/giphy.gif",
"https://media.giphy.com/media/l2R0bByKRZ0Lv4vxm/giphy.gif",
"https://media.giphy.com/media/3oEduY8Kh1AoOWUBnW/giphy.gif",
"https://media.giphy.com/media/nZKPBavKWBMEo/giphy.gif",
"https://media.giphy.com/media/qw0TXAwW8hsk0/giphy.gif"
]
        
class Spray:
    """Lets you Spray someone."""

    def __init__(self, bot):
        self.bot = bot
        self.spraylist = dataIO.load_json("data/spray/sprays.json")
        
    @commands.command(pass_context=True)
    async def spray(self, ctx, *, user: discord.Member=None,):
        """Lets you spray someone."""

        multimsg = 'Have been sprayed!!'
        if user != None:
            if len(message.mentions) == 0:
                await self.bot.say("You haven't told me who to spray, so I guess I'll spray you {}! {}".format (author.mention, choice(self.spraylist)))
            elif user.id == self.bot.user.id:
                user = ctx.message.author
                msg = " I can\'t believe you tried to spray me. I\'m a bot, i\'ll break!!!"
                await self.bot.say(user.mention + msg)
            else:
                await self.bot.say("{} you have just sprayed {}\n{}".format(author.mention, user.mention, choice(self.spraylist)))
        else:
            await self.bot.say(user.mention + multimsg + choice(self.spraylist))

    @commands.command(pass_context=True)
    @checks.admin_or_permissions(administrator=True)
    async def addspray(self, ctx, spraylink_giphypls):
        """Adds a spray to the list."""
        spraylink = spraylink_giphypls
        if spraylink.startswith("http"):
            self.spraylist.append(spraylink)
            dataIO.save_json("data/spray/sprays.json", self.spraylist)
            await self.bot.say("Spray added!")
        else:
            await self.bot.say("spraylink was not a proper link")
        
    @commands.command()
    @checks.mod_or_permissions()
    async def delspray(self, spraylink_and_owner):
        """Deletes a spray.
        
        Example:
        [p]delspray "https://media.giphy.com/media/uSy9uVHKqRNjG/giphy.gif"
        """
        spraylink = spraylink_and_owner
        try:
            self.spraylist.remove(spraylink)
            dataIO.save_json("data/spray/sprays.json", self.spraylist)
            await self.bot.say("Spray removed!")
        except:
            await self.bot.say("Couldn't delete the spray from sprays.json, was the format correct?")

def check_folders():
    if not os.path.exists("data/spray"):
        print("Creating data/spray folder...")
        os.makedirs("data/spray")
        
def check_files():
    if not os.path.exists("data/spray/sprays.json"):
        print("Creating data/spray/sprays.json file...")
        dataIO.save_json("data/spray/sprays.json", spraylist)
        
def setup(bot):
    check_folders()
    check_files()
    n = Spray(bot)
    bot.add_cog(n)