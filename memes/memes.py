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

memelist = [
"http://i.imgur.com/yeF0kg4.jpg",
"http://i.imgur.com/OyNz2uG.png",
"http://i.imgur.com/E0NtqiR.gif",
"http://i.imgur.com/oUdWheT.gif",
"http://i.imgur.com/lTTGPTl.gif", 
"http://i.imgur.com/4SUPkgB.gif",
"http://i.imgur.com/oiBCuSk.gif",
"http://i.imgur.com/dKTMitf.png", 
"http://i.imgur.com/eVXxdPX.gif",
"http://i.imgur.com/FTgbH6V.gif",
"http://i.imgur.com/mKDz3CB.gif",
"http://i.imgur.com/ZkDEFVc.jpg",
"http://i.imgur.com/a2t7ilg.gif",
"http://i.imgur.com/1InP4XV.gif",
"http://i.imgur.com/9O9HPNh.gif",
"http://i.imgur.com/XIX8kag.gif",
"http://i.imgur.com/rkNFKdW.gif",
"http://i.imgur.com/LkAIhqW.png",
"http://i.imgur.com/2PjPLsK.gif",
"http://i.imgur.com/ISuTCuL.gifv",
"http://i.imgur.com/rq4LLyx.png",
"http://i.imgur.com/zxHK2YJ.png",
"http://i.imgur.com/GQRxbPR.png", 
"http://i.imgur.com/ynJWUjf.png",
"http://i.imgur.com/scnHxiW.png",
"http://i.imgur.com/VP4qJVp.png",
"http://i.imgur.com/H2QY5H8.gif",
"http://i.imgur.com/TFy8o7J.gif",
"http://i.imgur.com/a7oc0h4.gif",
"http://i.imgur.com/7AgiFiQ.gif",
"http://i.imgur.com/cIyXtKP.jpg",
"http://i.imgur.com/nrecDTy.jpg",
"http://i.imgur.com/w8vQAnI.jpg",
"http://i.imgur.com/JqCqC96.jpg",
"http://i.imgur.com/OrTu9dY.jpg",
"http://i.imgur.com/bbCjewo.jpg",
"http://i.imgur.com/aWsJTdC.gif",
"http://i.imgur.com/QOmWLWW.jpg",
"http://i.imgur.com/bV0FoPt.jpg",
"http://i.imgur.com/BkuCizz.jpg",
"http://i.imgur.com/EiYJueo.jpg",
"http://i.imgur.com/ge3lODN.jpg",
"http://i.imgur.com/jtOMMmu.jpg",
"http://i.imgur.com/pG2MNpN.png",
"http://i.imgur.com/1BP4XXS.png",
"http://i.imgur.com/L67XuUz.jpg",
"http://i.imgur.com/6Brq0mL.jpg",
"http://i.imgur.com/nlJiz4F.png",
"http://i.imgur.com/RCIZVlk.jpg",
"http://i.imgur.com/ZR3jJtN.png"
]
        
class Memes:
    """Dank memes."""

    def __init__(self, bot):
        self.bot = bot
        self.memelist = dataIO.load_json("data/memes/memes.json")
        self.airhorn = [
        "data/memes/airhorns/airhorn1.mp3",
        "data/memes/airhorns/airhorn2.mp3",
        "data/memes/airhorns/airhorn3.mp3"
        ]
		
    @commands.command()
    async def yesno(self):
        """Says yes or no."""
        self.yesno = ["yes. https://media.giphy.com/media/l46CabMtEkqUtrzkA/giphy.gif", "yes. https://media.giphy.com/media/l3vRhtXnCLgypqh7a/giphy.gif", "yes. https://media.giphy.com/media/l3vR3ACyHLgbOIjZe/source.gif", "no. https://media.giphy.com/media/3oz8xM4Qy4IVCelqZq/source.gif", "no. https://media.giphy.com/media/KaXENSCPjqnK0/giphy.gif", "no. https://media.giphy.com/media/T5QOxf0IRjzYQ/giphy.gif"]
        await self.bot.say("I say " + choice(self.yesno))
        
    @commands.command(pass_context=True)
    async def datboi(self, ctx):
        """Here come dat boi,
        
        Oh shit waddup"""
        await self.bot.say("Here come dat boi.")
        ohshit = await self.bot.say("Oh shit")
        W = "\U0001f1fc"
        A = "\U0001f1e6"
        D = "\U0001f1e9"
        U = "\U0001f1fa"
        P = "\U0001f1f5"
        await self.bot.add_reaction(ohshit, W)
        await self.bot.add_reaction(ohshit, A)
        await self.bot.add_reaction(ohshit, D)
        await self.bot.add_reaction(ohshit, U)
        await self.bot.add_reaction(ohshit, P)
        self.datboiLoaded = os.path.exists('data/memes/datboi.png')
        if not self.datboiLoaded:
            try:
                async with aiohttp.get("http://i.imgur.com/KEb9OJv.jpg") as r:
                    image = await r.content.read()
                with open('data/memes/datboi.png', 'wb') as f:
                    f.write(image)
            except Exception as e:
                print(e)
                print("Memes error D: I couldn't download the file, so we're gonna use the url instead.")
            await self.bot.send_file(ctx.message.channel, fp="data/memes/datboi.png", filename="datboi.png")
        else:
            await self.bot.send_file(ctx.message.channel, fp="data/memes/datboi.png", filename="datboi.png")
            
    async def memes(self, message):
        if message.server != None:
            if not "bots" in message.server.name.lower():
                if "ayy" in message.content.lower():
                    self.lmaoLoaded = os.path.exists('data/memes/maolmao.png')
                    if not self.lmaoLoaded:
                        try:
                            async with aiohttp.get("http://i.imgur.com/yfkKXGQ.png") as r:
                                image = await r.content.read()
                            with open('data/memes/maolmao.png','wb') as f:
                                f.write(image)
                            L = "\U0001f1f1"
                            M = "\U0001f1f2"
                            A = "\U0001f1e6"
                            O = "\U0001f1f4"
                            await self.bot.send_file(message.channel, fp="data/memes/maolmao.png", filename="maolmao.png")
                            await self.bot.add_reaction(message, L)
                            await self.bot.add_reaction(message, M)
                            await self.bot.add_reaction(message, A)
                            await self.bot.add_reaction(message, O)
                            
                        except Exception as e:
                            print(e)
                            print("Memes error D: I couldn't download the file, so we're gonna use the url instead.")
                            L = "\U0001f1f1"
                            M = "\U0001f1f2"
                            A = "\U0001f1e6"
                            O = "\U0001f1f4"
                            await self.bot.send_message(message.channel, "http://i.imgur.com/yfkKXGQ.png")
                            await self.bot.add_reaction(message, L)
                            await self.bot.add_reaction(message, M)
                            await self.bot.add_reaction(message, A)
                            await self.bot.add_reaction(message, O)
                    else:
                        L = "\U0001f1f1"
                        M = "\U0001f1f2"
                        A = "\U0001f1e6"
                        O = "\U0001f1f4"
                        await self.bot.send_file(message.channel, fp="data/memes/maolmao.png", filename="maolmao.png")
                        await self.bot.add_reaction(message, L)
                        await self.bot.add_reaction(message, M)
                        await self.bot.add_reaction(message, A)
                        await self.bot.add_reaction(message, O)       
                    
                if message.content.lower() == "oh shit":
                    W = "\U0001f1fc"
                    A = "\U0001f1e6"
                    D = "\U0001f1e9"
                    U = "\U0001f1fa"
                    P = "\U0001f1f5"
                    await self.bot.add_reaction(message, W)
                    await self.bot.add_reaction(message, A)
                    await self.bot.add_reaction(message, D)
                    await self.bot.add_reaction(message, U)
                    await self.bot.add_reaction(message, P)
                    
                if message.content.lower() == "o shit":
                    W = "\U0001f1fc"
                    A = "\U0001f1e6"
                    D = "\U0001f1e9"
                    U = "\U0001f1fa"
                    P = "\U0001f1f5"
                    await self.bot.add_reaction(message, W)
                    await self.bot.add_reaction(message, A)
                    await self.bot.add_reaction(message, D)
                    await self.bot.add_reaction(message, U)
                    await self.bot.add_reaction(message, P)
                    
                if (message.content.lower() == "feels bad man") or (message.content.lower() == "feelsbadman"):
                    self.fbmLoaded = os.path.exists('data/memes/feelsbadman.png')
                    if not self.fbmLoaded:
                        try:
                            async with aiohttp.get("http://i.imgur.com/U26pQQo.png") as r:
                                image = await r.content.read()
                            with open('data/memes/feelsbadman.png','wb') as f:
                                f.write(image)
                            await self.bot.send_file(message.channel, fp="data/memes/feelsbadman.png", filename="feelsbadman.png")
                        except Exception as e:
                            print(e)
                            print("Memes error D: I couldn't download the file, so we're gonna use the url instead.")
                            await self.bot.send_message(message.channel, "http://i.imgur.com/U26pQQo.png")
                    else:
                        await self.bot.send_file(message.channel, fp="data/memes/feelsbadman.png", filename="feelsbadman.png")
            
def check_folders():
    if not os.path.exists("data/memes"):
        print("Creating data/memes folder...")
        os.makedirs("data/memes")
    if not os.path.exists("data/memes/airhorns"):
        print("Creating data/memes/airhorns folder...")
        os.makedirs("data/memes/airhorns")
    if not os.path.exists("data/memes/airhornsongs"):
        print("Creating data/memes/airhornsongs folder...")
        os.makedirs("data/memes/airhornsongs")
        
def check_files():
    if not os.path.exists("data/memes/memes.json"):
        print("Creating data/memes/memes.json file...")
        dataIO.save_json("data/memes/memes.json", memelist)
        
def setup(bot):
    check_folders()
    check_files()
    n = Memes(bot)
    bot.add_listener(n.memes, "on_message")
    bot.add_cog(n)