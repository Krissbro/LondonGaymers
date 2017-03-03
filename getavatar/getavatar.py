import discord
from discord.ext import commands


class Avatar:
    """Get user's avatar"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def getavatar(self, ctx, *, user: discord.Member=None):
        """Gives your avatar. Tag someone to get theirs"""
        author = ctx.message.author

        if not user:
            user = author
            avatar = user.avatar_url .strip("webp?size=1024")
        if "gif" not in user.avatar.url:
            await self.bot.say(":eyes: {} | {}'s Avatar is : {}jpg".format(author.mention, user.mention, avatar))
        else:
            await self.bot.say(":eyes: {} | {}'s Avatar is : {}".format(author.mention, user.mention, avatar))

def setup(bot):
    bot.add_cog(Avatar(bot))