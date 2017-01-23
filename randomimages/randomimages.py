"""
Random images cog by Phantium
https://github.com/phantium/phantium-cogs
"""

import discord
import aiohttp
try:
    import lxml.html
except ImportError:
    exit("ImportError, please install lxml: pip install lxml")
from discord.ext import commands


class RandomImages:
    """RandomImages"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def cat(self):
        """Returns a cat picture from random.cat"""

        cat_api = "http://random.cat/meow"

        try:
            with aiohttp.ClientSession() as session:
                async with session.get(cat_api) as api:
                    cat = await api.json()
                    message = ":cat: {}".format(cat["file"])
        except:
            message = "Error: unable to get random :cat: image."

        await self.bot.say(message)

    @commands.command(pass_context=True)
    async def dog(self):
        """Returns a dog picture from random.dog"""

        dog_api = "http://random.dog"

        try:
            with aiohttp.ClientSession() as session:
                async with session.get(dog_api) as response:
                    response = await response.read()
                    html = lxml.html.fromstring(response.decode())
                    message = ":dog: {}/{}".format(dog_api, str(html.xpath("//img/@src")[0]))
        except:
            message = "Error: unable to get random :dog: image."

        await self.bot.say(message)


def setup(bot):
    bot.add_cog(RandomImages(bot))
