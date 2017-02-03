import math
# Developed by Tarrnobi for LondonGaymers.
# Requires grequests to work.
# use pip install grequests .

try: #check if grequests is installed
    import grequests
    grequestsAvailable = True
except ImportError:
    grequestsAvailable = False

battle_tag      = "Tarr-1489"
game_platform   = "pc"
game_region     = "eu"
base_api_location = "https://api.lootbox.eu"
profile_endpoint  = "{0}/{1}/{2}/{3}/profile"
heroes_endpoint   = "{0}/{1}/{2}/{3}}/{4}}/heroes"
urls = [
    #profile
    "{0}/{1}/{2}/{3}/profile".format(base_api_location, game_platform, game_region, battle_tag),
    #competetive heroes
    "{0}/{1}/{2}/{3}/{4}/heroes".format(base_api_location, game_platform, game_region, battle_tag,"competitive"),
    #quickplay heroes
    "{0}/{1}/{2}/{3}/{4}/heroes".format(base_api_location, game_platform, game_region, battle_tag,"quickplay"),
]

print (urls)

print ("getting response")
requests = (grequests.get(u) for u in urls)
responses = grequests.map(requests)
print ("got response")
#Build Our Response:
#'''
#User : data[username]
#Level: data[level]
#----Stats----
#               Played|Wins|Losses|Time
#QuickPlay      data[games][quick][played]|data[games][quick][wins]|data[games][quick][lost]| data[playtime][quick]
#Competitive    data[games][quick][played]|data[games][quick][wins]|data[games][quick][lost]| data[playtime][quick]
#
#'''
if responses[0].status_code == 200 and responses[1].status_code == 200 and responses[2].status_code == 200:
    user_data     = responses[0].json()
    comp_heroes   = responses[1].json()
    quick_heroes  = responses[2].json()


    print (user_data)
    print (comp_heroes)
    print (quick_heroes)

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

print(msg)
#
#
# class Overwatch:
#
#     # Initialise the bot's settings
#     def __init(self, bot):
#         self.bot = bot
#         self.base_api_location = "https://api.lootbox.eu"
#         self.profile_endpoint  = "{0}/{1}/{2}/{3}/profile".format(base_api_location, game_platform, game_region, battle_tag)
#         self.heroes_endpoint   = "{0}/{1}/{2}/{3}/{4}/heroes"
#     # Set up the command information:
#     # Grab the battle tag that we're searching for
#     # Let's pretend everyone's in the EU realm
#     @commands.command(name="owpc")
#     async def owpc(self, battle_tag):
#         self.overwatch_info(self, battle_tag, "eu", "pc")
#     @commands.command(name="owps4")
#     async def owpsn(self,battle_tag):
#         self.overwatch_info(self, battle_tag, "eu", "psn")
#     @commands.command(name="owxbx")
#     async def owxbl(self,battle_tag):
#         self.overwatch_info(self, battle_tag, "eu", "xbl")
#
#     def overwatch_info(self, battle_tag, game_region, game_platform):
#         urls = [
#             self.profile_endpoint.format(self.base_api_location, game_platform, game_region, battle_tag),
#             self.heroes_endpoint.format(self.base_api_location , game_platform, game_region, battle_tag,"competitive"),
#             self.heroes_endpoint.format(self.base_api_location , game_platform, game_region, battle_tag,"quickplay"),
#         ]
#
#         requests = (grequests.get(u) for u in urls)
#         response = grequests.map(requests)
#
#         #Build Our Response:
#         #'''
#         #User : data[username]
#         #Level: data[level]
#         #----Stats----
#         #               Played|Wins|Losses|Time
#         #QuickPlay      data[games][quick][played]|data[games][quick][wins]|data[games][quick][lost]| data[playtime][quick]
#         #Competitive    data[games][quick][played]|data[games][quick][wins]|data[games][quick][lost]| data[playtime][quick]
#         #
#         #'''
#
# def setup(bot):
#     if not grequestsAvailable:
#         raise RuntimeError("You need to run \'pip install grequests\' in command prompt.")
#     bot.add_cog(Overwatch(bot))
