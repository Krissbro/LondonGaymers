import discord
from __main__ import send_cmd_help
from discord.ext import commands
import datetime

class Serverinfo:
    """Adds [p]server and all subcommands!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="server", pass_context=True)
    async def _server(self, ctx):
        """Server info commands."""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @_server.command(pass_context=True, no_pm=True)
    async def owner(self, ctx):
        """Tells you who's the boss on this server"""
        await self.bot.send_message(ctx.message.channel, embed=discord.Embed(title="Server owner", description="{}, the server owner is {}.".format(ctx.message.author.mention, ctx.message.server.owner.mention), colour=0X008CFF))
        
    @_server.command(pass_context=True, no_pm=True)
    async def name(self, ctx):
        """Shows you the server name."""
        await self.bot.send_message(ctx.message.channel, embed=discord.Embed(title="Server name", description="{}, the server name is {}.".format(ctx.message.author.mention, ctx.message.server), colour=0X008CFF))
		
    @_server.command(pass_context=True, no_pm=True)
    async def sid(self, ctx):
        """Shows you the server ID."""
        await self.bot.send_message(ctx.message.channel, embed=discord.Embed(title="Server ID", description="{}, the Server ID is {}.".format(ctx.message.author.mention, ctx.message.server.id), colour=0X008CFF))
        
    @_server.command(pass_context=True, no_pm=True)
    async def channelname(self, ctx):
        """Shows you the channel name."""
        await self.bot.send_message(ctx.message.channel, embed=discord.Embed(title="Channel name", description="{}, the channelname is #{}.".format(ctx.message.author.mention, ctx.message.channel.name), colour=0X008CFF))
		
    @_server.command(pass_context=True, no_pm=True)
    async def cid(self, ctx):
        """Shows you the channel ID."""
        await self.bot.send_message(ctx.message.channel, embed=discord.Embed(title="Channel ID", description="{}, the Channel ID is {}.".format(ctx.message.author.mention, ctx.message.channel.id), colour=0X008CFF))
        
    @_server.command(pass_context=True, no_pm=True)
    async def time(self, ctx):
        """Shows you the server time."""
        await self.bot.send_message(ctx.message.channel, embed=discord.Embed(title="Server time", description="{}, the server time is {}.".format(ctx.message.author.mention, datetime.datetime.now()), colour=0X008CFF))
        
    @_server.command(pass_context=True, no_pm=True)
    async def roles(self, ctx):
        """Lists all Roles"""
        comma = ", "
        roles = [r.name for r in ctx.message.server.role_hierarchy]
        await self.bot.send_message(ctx.message.channel, embed=discord.Embed(title="Roles", description="{}, the current roles are \n{}.".format(ctx.message.author.mention, comma.join(roles)), colour=0X008CFF))

    @_server.command(pass_context=True, no_pm=True)
    async def emojis(self, ctx):
        """Lists all emojis"""
        comma = ", "
        emojis = [e.name for e in ctx.message.server.emojis]
        await self.bot.send_message(ctx.message.channel, embed=discord.Embed(title="Emojis", description="{}, the current emojis are \n{}.".format(ctx.message.author.mention, comma.join(emojis)), colour=0X008CFF))
            
    @_server.command(pass_context=True, no_pm=True)
    async def users(self, ctx):
        """Lists all users"""
        comma = "**, **"
        members = [m.name for m in ctx.message.server.members]
        if len(ctx.message.server.members) < 32:
            await self.bot.send_message(ctx.message.channel, embed=discord.Embed(title="Users", description="{}, the current users are \n**{}**.".format(ctx.message.author.mention, comma.join(members)), colour=0X008CFF))
        else:
            await self.bot.send_message(ctx.message.author, embed=discord.Embed(title="Users", description="The current users in **{}** are \n**{}**.".format(ctx.message.server.name, comma.join(members)), colour=0X008CFF))
            
    @_server.command(pass_context=True, no_pm=True)
    async def channels(self, ctx):
        """Lists all channels"""
        comma = "**, **"
        voicechans = [x.name for x in ctx.message.server.channels if x.type == discord.ChannelType.voice]
        textchans = [x.name for x in ctx.message.server.channels if x.type == discord.ChannelType.text]
        await self.bot.send_message(ctx.message.channel, embed=discord.Embed(title="Channels", description="{}, the current voice channels are \n**{}**.\nThe current text channels are\n**{}**.".format(ctx.message.author.mention, comma.join(voicechans), comma.join(textchans)), colour=0X008CFF))
			
    @_server.command(pass_context=True, no_pm=True)
    async def compareids(self, ctx):
        """Compares the id of the server and the channel to see if the channel is the default one."""
        if ctx.message.server.id == ctx.message.channel.id:
            await self.bot.send_message(ctx.message.channel, embed=discord.Embed(title="Channel is default", description=
            "{}, the ids of the channel and the server are the same, so this is the default channel.\n(SID=`{}`, CID=`{}`)".format(ctx.message.author.mention, ctx.message.server.id, ctx.message.channel.id), colour=0X008CFF))
        else:
            await self.bot.send_message(ctx.message.channel, embed=discord.Embed(title="Channel isn't default", description=
            "{}, The ids of the channel and the server are not the same, this is not the default channel. If there is a #general try it in that channel first.\n(SID=`{}`, CID=`{}`)".format(ctx.message.author.mention, ctx.message.server.id, ctx.message.channel.id), colour=0X008CFF))
            
    @_server.command(pass_context=True, no_pm=True)
    async def icon(self, ctx):
        """Shows the server icon."""
        await self.bot.send_message(ctx.message.channel, embed=discord.Embed(title="Server icon", description="{}, the server icon is {}.".format(ctx.message.author.mention, ctx.message.server.icon_url), colour=0X008CFF))
        
    @_server.command(pass_context=True, no_pm=True)
    async def info(self, ctx):
        """Show server info."""
        members = set(ctx.message.server.members)
        offline = filter(lambda m: m.status is discord.Status.offline, members)
        offline = set(offline)
        bots = filter(lambda m: m.bot, members)
        bots = set(bots)
        users = members - bots
        servericon = ctx.message.server.icon_url
        channel_passed = (ctx.message.timestamp - ctx.message.channel.created_at).days 
        server_passed = (ctx.message.timestamp - ctx.message.server.created_at).days
        channel_created_at = ("Created on {} ({} days ago!)".format(ctx.message.channel.created_at.strftime("%d %b %Y %H:%M"), channel_passed))
        server_created_at = ("Created on {} ({} days ago!)".format(ctx.message.server.created_at.strftime("%d %b %Y %H:%M"), server_passed))
        try:
            em = discord.Embed(description="{}, here you go:".format(ctx.message.author.mention), color=0X008CFF, title="Server Info")
            em.set_thumbnail(url=servericon)
            em.add_field(name="Server Name", value=str(ctx.message.server.name))
            em.add_field(name="Server ID", value=str(ctx.message.server.id))
            em.add_field(name="Server Region", value=str(ctx.message.server.region))
            em.add_field(name="Server Verification", value=str(ctx.message.server.verification_level))
            em.add_field(name="Server Roles", value=str(len(ctx.message.server.roles) -1))
            em.add_field(name="Server Owner", value=str(ctx.message.server.owner.name))
            em.add_field(name="Server Created At", value=str(server_created_at))
            em.add_field(name="Owner ID", value=str(ctx.message.server.owner.id))
            em.add_field(name="Owner Nick", value=str(ctx.message.server.owner.nick))
            em.add_field(name="Owner Status", value=str(ctx.message.server.owner.status))
            em.add_field(name="Total Bots", value=str(len(bots)))
            em.add_field(name="Bots Online", value=str(len(bots - offline)))
            em.add_field(name="Bots Offline", value=str(len(bots & offline)))
            em.add_field(name="Total Users", value=str(len(users)))
            em.add_field(name="Online Users", value=str(len(users - offline)))
            em.add_field(name="Offline Users", value=str(len(users & offline)))
            em.add_field(name="Channel Name", value=str(ctx.message.channel.name))
            em.add_field(name="Channel ID", value=str(ctx.message.channel.id))
            em.add_field(name="Channel Default", value=str(ctx.message.channel.is_default))
            em.add_field(name="Channel Position", value=str(ctx.message.channel.position + 1))
            em.add_field(name="Channel Created At", value=str(channel_created_at))
            if ctx.message.channel.topic != None:
                em.add_field(name="Channel Topic", value=(ctx.message.channel.topic))
            else:
                pass
            await self.bot.say(embed=em)
        except discord.HTTPException:
            await self.bot.say("An unknown error occured while sending the embedded message, maybe try giving me the `embed links` permission?")

    @_server.command(pass_context=True, no_pm=True)
    async def channelinfo(self, ctx, channel : discord.Channel = None):
        if channel == None:
            channel = ctx.message.channel
        passed = (ctx.message.timestamp - channel.created_at).days
        try:
            channel_created_at = ("Created on {} ({} days ago!)".format(channel.created_at.strftime("%d %b %Y %H:%M"), passed))
            em = discord.Embed(description="{}, here you go:".format(ctx.message.author.mention), title="Channel Info", color=0X008CFF)
            em.add_field(name="Channel Name", value=str(channel.name))
            em.add_field(name="Channel ID", value=str(channel.id))
            em.add_field(name="Channel Default", value=str(channel.is_default))
            em.add_field(name="Channel Position", value=str(channel.position + 1))
            em.add_field(name="Channel Topic", value=(channel.topic))
            em.set_footer(text=channel_created_at)
            await self.bot.say(embed=em)
        except discord.HTTPException:
            channel_created_at = ("Created on {} ({} days ago!)".format(channel.created_at.strftime("%d %b %Y %H:%M"), passed))            
            em = discord.Embed(description="{}, here you go:".format(ctx.message.author.mention), title="Channel Info", color=0X008CFF)
            em.add_field(name="Channel Name", value=str(channel.name))
            em.add_field(name="Channel ID", value=str(channel.id))
            em.add_field(name="Channel Default", value=str(channel.is_default))
            em.add_field(name="Channel Position", value=str(channel.position + 1))
            em.add_field(name="Channel Topic", value="None")
            em.set_footer(text=channel_created_at)
            await self.bot.say(embed=em)
        
    @_server.command(pass_context=True, no_pm=True)
    async def membercount(self, ctx):
        """Counts the users"""
        members = set(ctx.message.server.members)
        bots = filter(lambda m: m.bot, members)
        bots = set(bots)
        users = members - bots
        await self.bot.send_message(ctx.message.channel, embed=discord.Embed(title="Server Membercount", description="{}, there are currently **{}** users and **{}** bots with a total of **{}** members in this server.".format(ctx.message.author.mention, len(users), len(bots), len(ctx.message.server.members)), colour=0X008CFF))
        
    @_server.command(pass_context=True, no_pm=True)
    async def channelcount(self, ctx):
        """Counts the users"""
        chans = ctx.message.server.channels
        textchans = [x for x in ctx.message.server.channels if x.type == discord.ChannelType.text]
        voicechans = [x for x in ctx.message.server.channels if x.type == discord.ChannelType.voice]
        await self.bot.send_message(ctx.message.channel, embed=discord.Embed(title="Server Channelcount", description="{}, there are currently **{}** text channels and **{}** voice channels with a total of **{}** channels in this server.".format(ctx.message.author.mention, len(textchans), len(voicechans), len(chans)), colour=0X008CFF))
            
    @_server.command(pass_context=True, no_pm=True)
    async def rolecount(self, ctx):
        """Counts the roles"""
        await self.bot.send_message(ctx.message.channel, embed=discord.Embed(title="Server Rolecount", description="{}, there are currently **{}** roles in this server.".format(ctx.message.author.mention, len(ctx.message.server.role_hierarchy)), colour=0X008CFF))
        
    @_server.command(pass_context=True, no_pm=True)
    async def emojicount(self, ctx):
        """Counts the emojis"""
        await self.bot.send_message(ctx.message.channel, embed=discord.Embed(title="Server Emojicount", description="{}, there are currently **{}** emojis in this server.".format(ctx.message.author.mention, len(ctx.message.server.emojis)), colour=0X008CFF))
        
    @_server.command(pass_context=True)
    async def userinfo(self, ctx, user: discord.Member=None):
        """Shows you the info for the given user, or yours if you didn't give a user."""
        if user == None:
            user = ctx.message.author
        comma = ", "
        roles = [r.name for r in user.roles if r.name != "@everyone"]
        if roles:
            roles = sorted(roles, key=[x.name for x in ctx.message.server.role_hierarchy if x.name != "@everyone"].index)
            roles = comma.join(roles)
        else:
            roles = "None"

        em = discord.Embed(description="{} here you go:".format(
            ctx.message.author.mention), title="User Info", color=0X008CFF)
        if user.avatar_url:
            em.set_thumbnail(url=user.avatar_url)
        else:
            em.set_thumbnail(url=user.default_avatar_url)
        em.add_field(name="Name", value=user.name)
        em.add_field(name="Discriminator", value=user.discriminator)
        if user.nick:
            em.add_field(name="Nickname", value=user.nick)
        else:
            em.add_field(name="Nickname", value="None")
        em.add_field(name="ID", value=user.id)
        em.add_field(name="Status", value=user.status)
        if user.game:
            em.add_field(name="Playing", value=user.game)
        else:
            em.add_field(name="Playing", value="Nothing")
        em.add_field(name="Is AFK", value=user.is_afk)
        em.add_field(name="Is bot", value=user.bot)
        em.add_field(name="Highest role color", value=user.color)
        em.add_field(name="Serverwide muted", value=user.mute)
        em.add_field(name="Serverwide deafened", value=user.deaf)
        em.add_field(name="Joined discord at",
                     value=user.created_at.strftime("%d %b %Y %H:%M"))
        em.add_field(name="Joined server at",
                     value=user.joined_at.strftime("%d %b %Y %H:%M"))
        em.add_field(name="Roles", value=roles)

        await self.bot.say(embed=em)
        
    @_server.command(pass_context=True)
    async def roleinfo(self, ctx, *, role):
        roleObj = discord.utils.get(ctx.message.server.roles, name=role)
        if roleObj is None:
            await self.bot.say("`{}` is not a valid role".format(role))
            return
        count = len([member for member in ctx.message.server.members if discord.utils.get(member.roles, name=roleObj.name)])
        perms = roleObj.permissions
        em = discord.Embed(description="{} here you go,".format(ctx.message.author.mention), title="Server Role Info", color=0X008CFF)
        em.add_field(name="Name", value=roleObj.name)
        em.add_field(name="Color", value=roleObj.color)
        em.add_field(name="Position", value=str(roleObj.position))
        em.add_field(name="User count", value=count)
        em.add_field(name="Mentionable", value=roleObj.mentionable)
        em.add_field(name="Display separately", value=roleObj.hoist)
        em.add_field(name="Administrator", value=perms.administrator)
        em.add_field(name="Can ban members", value=perms.ban_members)
        em.add_field(name="Can kick members", value=perms.kick_members)
        em.add_field(name="Can change nickname", value=perms.change_nickname)
        em.add_field(name="Can connect to voice channels", value=perms.connect)
        em.add_field(name="Can create instant invites", value=perms.create_instant_invite)
        em.add_field(name="Can deafen members", value=perms.deafen_members)
        em.add_field(name="Can embed links", value=perms.embed_links)
        em.add_field(name="Can use external emojis", value=perms.external_emojis)
        em.add_field(name="Can manage channel", value=perms.manage_channels)
        em.add_field(name="Can manage emojis", value=perms.manage_emojis)
        em.add_field(name="Can manage messages", value=perms.manage_messages)
        em.add_field(name="Can manage nicknames", value=perms.manage_nicknames)
        em.add_field(name="Can manage roles", value=perms.manage_roles)
        em.add_field(name="Can manage server", value=perms.manage_server)
        em.add_field(name="Can mention everyone", value=perms.mention_everyone)
        em.add_field(name="Can move members", value=perms.move_members)
        em.add_field(name="Can mute members", value=perms.mute_members)
        em.add_field(name="Can read message history", value=perms.read_message_history)
        em.add_field(name="Can send messages", value=perms.send_messages)
        em.add_field(name="Can speak", value=perms.speak)
        em.add_field(name="Can use voice activity", value=perms.use_voice_activation)
        em.add_field(name="Can manage webhooks", value=perms.manage_webhooks)
        em.add_field(name="Can add reactions", value=perms.add_reactions)
        await self.bot.say(embed=em)
        
def setup(bot):
    bot.add_cog(Serverinfo(bot))