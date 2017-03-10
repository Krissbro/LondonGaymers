import discord
from discord.ext import commands
from .utils.chat_formatting import *
import random
from random import randint
from random import choice as randchoice
import datetime
from __main__ import send_cmd_help
import re
import urllib
import time
import aiohttp
import asyncio
from cogs.utils.dataIO import dataIO
import io, os
import logging
from __main__ import send_cmd_help, user_allowed
from cogs.utils import checks
from cogs.utils.dataIO import dataIO
from cogs.utils.chat_formatting import box, pagify, escape_mass_mentions
from random import choice
from copy import deepcopy
from cogs.utils.settings import Settings

log = logging.getLogger("red.admin")

class Utility:
    """Utility commands."""

    def __init__(self, bot):
        self.bot = bot

    def _role_from_string(self, server, rolename, roles=None):
        if roles is None:
            roles = server.roles
        role = discord.utils.find(lambda r: r.name.lower() == rolename.lower(),
                                  roles)
        try:
            log.debug("Role {} found from rolename {}".format(
                role.name, rolename))
        except:
            log.debug("Role not found for rolename {}".format(rolename))
        return role

    @commands.command(pass_context=True)
    async def whoplays(self, ctx, *, rolename):
        """See who plays games across this server"""
        server = ctx.message.server
        message = ctx.message
        channel = ctx.message.channel
        await self.bot.send_typing(ctx.message.channel)
        therole = discord.utils.find(lambda r: r.name.lower() == rolename.lower(), ctx.message.server.roles)
        if therole is not None and len([m for m in server.members if therole in m.roles]) < 100:
            lolies = await self.bot.say(" :raised_hand: Wait up Getting Names :bookmark: ")
            await asyncio.sleep(1) #taking time to retrieve the names
            server = ctx.message.server
            member = " :video_game:  ***{1}*** people play ***{0}*** in this server!, :video_game: \n".format(rolename, len([m for m in server.members if therole in m.roles]))
            member += "```diff\n+"
            member += " \n+".join(m.display_name for m in server.members if therole in m.roles)
            member += "```"
            await self.bot.edit_message(lolies, member)
        elif len([m for m in server.members if therole in m.roles]) > 100:
            awaiter = await self.bot.say("Getting Member Names")
            await asyncio.sleep(1)
            await self.bot.edit_message(awaiter, " :raised_hand: Woah way too many people in **{0}** Role, **{1}** Members found\n".format(rolename,  len([m for m in server.members if therole in m.roles])))
        else:
            await self.bot.say("`` Couldn't Find that role (╯°□°）╯︵ ┻━┻``")

    @commands.command(pass_context=True)
    async def emotes(self, ctx):
        """ServerEmote List"""
        server = ctx.message.server
        
        list = [e for e in server.emojis if not e.managed]
        emoji = ''
        for emote in list:
            emoji += "<:{0.name}:{0.id}> ".format(emote)
        try:
            await self.bot.say(emoji)
        except:
            await self.bot.say("**This server has no facking emotes what is this a ghost town ???**")
    @commands.command(pass_context=True)
    @checks.serverowner_or_permissions(administrator=True)
    async def roles(self, ctx):
        """States roles from highest to lowest"""

        list = "\n".join([x.name for x in ctx.message.server.role_hierarchy if x.name != "@everyone"])
        for page in pagify(list, ["\n"], shorten_by=7, page_length=2000):
            await self.bot.say(box(page))

def setup(bot):
    n = Utility(bot)
    bot.add_cog(n)