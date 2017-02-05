# Developed by Tarrnobi for connectivity with RedBot for
# LondonGaymers.  Requires grequests to work.
# use "pip install grequests" to accomplish this.

from   discord.ext import commands
import aiohttp
import math
try: #check if grequests is installed
    import grequests
    grequestsAvailable = True
except ImportError:
    grequestsAvailable = False


class Overwatch:

    # Initialise the bot's settings
    def __init__(self, bot):
        self.bot = bot
        self.base_api_location = "https://api.lootbox.eu"
        self.profile_endpoint  = "{0}/{1}/{2}/{3}/profile"
        self.heroes_endpoint   = "{0}/{1}/{2}/{3}/{4}/heroes"
    # Set up the command information:
    # Grab the battle tag that we're searching for
    # Let's pretend everyone's in the EU realm
    @commands.command(name="owpc")
    async def owpc(self, battle_tag):
        await self.overwatch_info(battle_tag.replace("#","-").capitalize(), "eu", "pc")
    @commands.command(name="owps4")
    async def owpsn(self,battle_tag):
        await self.overwatch_info(battle_tag.replace("#","-").capitalize(), "eu", "psn")
    @commands.command(name="owxbx")
    async def owxbl(self,battle_tag):
        await self.overwatch_info(battle_tag.replace("#","-").capitalize(), "eu", "xbl")

    async def overwatch_info(self, battle_tag, game_region, game_platform):
        await self.bot.say("I am looking up {0}. Please give me a moment".format(battle_tag))
        urls = [
            self.profile_endpoint.format(self.base_api_location, game_platform, game_region, battle_tag),
            self.heroes_endpoint.format(self.base_api_location , game_platform, game_region, battle_tag,"competitive"),
            self.heroes_endpoint.format(self.base_api_location , game_platform, game_region, battle_tag,"quickplay"),
        ]
        requests  = (grequests.get(u, timeout=30) for u in urls)
        responses = grequests.map(requests)

        if None in responses:
            await self.bot.say("Things were running slow and I couldn't get the data in time. Sorry :(")
            return
        if responses[0].status_code == 200 and responses[1].status_code == 200 and responses[2].status_code == 200:
            user_data     = responses[0].json()
            comp_heroes   = responses[1].json()
            quick_heroes  = responses[2].json()

            # Build our hero break downs for competitive and quick play.
            # We'll take the top five heroes and work out their percentage playtime
            # of the total.
            cp_hero_breakdown = {}
            cp_tot_hero_playtime = float(0)
            for item in comp_heroes:
                hero_name = item.get("name").replace("&#xFA;","u")
                if "minutes" in item.get("playtime"):
                    playtime = float(item.get("playtime").replace("minutes",""))/60
                elif "hours" in item.get("playtime"):
                    playtime = float(item.get("playtime").replace("hours",""))

                cp_tot_hero_playtime += playtime

                cp_hero_breakdown[hero_name] = playtime
                if len(cp_hero_breakdown.keys()) >= 5:
                    break
            qp_hero_breakdown = {}
            qp_tot_hero_playtime = float(0)
            # Repeat the above process for quick play.
            for item in quick_heroes:
                hero_name = item.get("name").replace("&#xFA;","u")
                if "minutes" in item.get("playtime"):
                    playtime = float(item.get("playtime").replace("minutes",""))/60
                elif "hours" in item.get("playtime"):
                    playtime = float(item.get("playtime").replace("hours",""))

                qp_tot_hero_playtime += playtime

                qp_hero_breakdown[hero_name] = playtime
                if len(qp_hero_breakdown.keys()) >= 5:
                    break
            #Now we can build our message to have the bot say.
            msg  = "```\n"
            msg += "--------------\n"
            msg += "User : {0}\n".format(user_data["data"]["username"])
            msg += "Level: {0}\n".format(user_data["data"]["level"])
            msg += "--------------\n"
            msg += "             Played|Wins  |losses|Time\n"
            msg += "Quick Play : {0}|{1}|{2}|{3}\n".format( str(user_data.get("data").get("games").get("quick").get("played","0")).ljust(6),
                                                            str(user_data.get("data").get("games").get("quick").get("wins","0")).ljust(6),
                                                            str(user_data.get("data").get("games").get("quick").get("lost","0")).ljust(6),
                                                            str(user_data.get("data").get("playtime").get("quick","0")))
            msg += "Competitive: {0}|{1}|{2}|{3}\n".format( str(user_data.get("data").get("games").get("competitive").get("played","0")).ljust(6),
                                                            str(user_data.get("data").get("games").get("competitive").get("wins","0")).ljust(6),
                                                            str(user_data.get("data").get("games").get("competitive").get("lost","0")).ljust(6),
                                                            str(user_data.get("data").get("playtime").get("competitive","0")))

            msg += "------------------------------\n"
            msg += "Competitive Hero Breakdown\n"
            msg += "------------------------------\n"
            for name, playtime in cp_hero_breakdown.items():
                if cp_tot_hero_playtime > 0:
                    percentage = round((playtime / cp_tot_hero_playtime * 100),0)
                else:
                    percentage = 0
                msg += "{0} [{1}]\n".format(name.ljust(12), ("|" * int(math.ceil(percentage/10))).ljust(10))
            msg += "------------------------------\n"
            msg += "QuickPlay Hero Breakdown\n"
            msg += "------------------------------\n"
            for name, playtime in qp_hero_breakdown.items():
                if qp_tot_hero_playtime > 0:
                    percentage = round((playtime / qp_tot_hero_playtime * 100),0)
                else:
                    percentage = 0
                msg += "{0} [{1}]\n".format(name.ljust(12), ("|" * int(math.ceil(percentage/10))).ljust(10))
            msg += "```"

            # Now instruct the bot to say the message.
            await self.bot.say(msg)
        else:
            await self.bot.say("Sorry, I could not find the battle-tag {0}".format(battle_tag))

def setup(bot):
    if not grequestsAvailable:
        raise RuntimeError("You need to run \'pip install grequests\' in command prompt.")
    bot.add_cog(Overwatch(bot))
