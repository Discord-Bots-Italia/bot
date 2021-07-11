"""
ඞඞඞඞඞඞඞ⢿⠟⠛⠿⠻⠿⠿⠟⠿ඞඞඞඞඞඞඞඞඞඞඞඞඞඞ
ඞඞඞ⡿⠛⢙⣨⣥⣶⣶ඞ⢿ඞඞ⣷⣦⣅⠛⢿ඞඞඞඞඞඞඞඞඞඞඞ
ඞඞ⠟⢀⡴⠟⠋⢉⣀⣠⣤⣤⣤⣀⠉⠻ඞ⣧⡈⢿ඞඞඞඞඞඞඞඞඞඞ
ඞඞ⠀⠁⣠⣴⣾ඞඞඞඞඞඞඞ⣷⠀⢻ඞ⣇⠝ඞඞඞඞඞඞඞඞඞඞ
ඞඞ⠀⣼ඞඞඞඞඞඞඞඞඞඞ⡿⡀⣼⡿⠟⠀⠙⣛⣬⠱ඞඞඞඞඞඞ
ඞඞ⠀⠹ඞඞඞඞඞඞඞඞ⠿⠋⢀⠄⠁⣠⣶⣾ඞඞඞ⡆⣼ඞඞඞඞඞ
ඞඞ⠀⣀⠙⣛⣛⣻⠛⠋⣉⣢⣤⣾⠃⣰⡄⠸ඞඞඞඞඞ⣷⠘ඞඞඞඞඞ
ඞඞ⣤⢹⣷⣶⣶⣶⣾ඞඞඞඞඞ⡄⠸⣷⠀⢻ඞඞ⡿⠟⠛⠡ඞඞඞඞඞ    DABABY SUSSY AMOUS WHEN THE IMPOSTOR IS SUS XXXXDDDDDDD YOUTUBE KIDS
ඞඞඞ⠄⢻ඞඞඞඞඞඞඞඞඞ⣷⠄⠻⠇⢈⠁⠀⠀⠲⠠⠞⠿ඞඞඞඞ
ඞඞඞ⣷⠈⢿ඞඞඞඞඞඞඞඞ⣷⣶⣶⢤⠀⠀⢲ඞඞඞ⣷⣤⡉⣻ඞඞ
ඞඞඞඞ⣧⠈⢿ඞඞඞඞඞඞඞඞඞඞඞඞ⣳⡀⢻ඞඞඞඞ⣷⠐ඞඞ
ඞඞඞඞඞ⣯⡈⢻ඞඞඞඞඞඞඞඞඞඞඞ⣾⡇⡆ඞඞඞඞ⡟⣀ඞඞ
ඞඞඞඞඞඞ⣷⡀⢻ඞඞඞඞඞඞඞඞඞඞඞ⠃⢃⡿⠿⠛⡋⣀⣾ඞඞ
ඞඞඞඞඞඞඞ⣷⣀⠹ඞඞඞඞඞඞඞ⠿⠋⢁⣠ඞ⡦⠐⠀⢈⡙⢿ඞඞ
ඞඞඞඞඞඞඞඞ⠋⢀ඞඞඞඞ⠟⢃⣤⣤⡀⠻ඞ⣇⣠⣴⡿⠄⠹⣧⡸ඞ
ඞඞඞඞඞඞ⡿⠃⢠⣾ඞඞ⡿⢋⣤ඞඞඞඞ⣄⠈⢿⡿⠋⣠⣤⣀⠈⣡ඞ
ඞඞඞ⠅⣀⣈⠁⣰ඞඞ⡿⠋⣤⣾ඞඞඞඞඞඞ⣷⣵⣂⣽ඞඞඞඞඞඞ
ඞඞඞ⣄⠘⢿ඞඞ⠟⠋⣠⣾ඞඞඞඞඞඞඞඞඞඞඞඞඞඞඞඞඞඞ
ඞඞඞඞ⣷⣤⣬⣅⣶ඞඞඞඞඞඞඞඞඞඞඞඞඞඞඞඞඞඞඞඞඞ
"""

import discord, os, config
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option

os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_HIDE"] = "True"

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=commands.when_mentioned_or(">"), intents=intents)
slash = SlashCommand(bot, sync_commands=True, override_type=True)
bot.remove_command("help")
bot.load_extension("jishaku")

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Streaming(name="torturando miky", url="https://www.twitch.tv/mikyottantotto"))
    print("ready as", bot.user)

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(config.token)
