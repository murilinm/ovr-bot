# IMPORTS
import discord
from discord.ext import commands
from dpyConsole import Console
import string

# VARIABLES
description = '''Oceanpoint Vacation Rentals bot commands, prefix "!"'''
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', description=description, intents=intents)
my_console = Console(discord.Client(intents=intents))

# - ID TEST SERVER VARIABLES
test_guild_id = 1291429430895575080
test_tickets_cat_id = 1292466525998940244
test_rentals_cat = 1291534971043057724
test_support_channel_id = 1291890339342450841

# - ID MAIN SERVER VARIABLES
main_guild_id = 1274894955663593492

# EVENTS
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

# SERVER COMMANDS
@bot.command()
async def openRental(ctx, contact: str, people_in_house: int, renting_time: str, house_type: str, pets_in_house: str):
    name = ctx.author.name
    guild = bot.get_guild(test_guild_id)
    category = guild.get_channel(1291534971043057724)
    overwrites = {
        #"https://discordpy.readthedocs.io/en/stable/api.html?highlight=channel#discord.Guild.create_text_channel"
    }
    channel = await category.create_text_channel(f'rental-{name[0]}{name[1]}{name[2]}{name[3]}', overwrites=overwrites)

@bot.group()
async def cool(ctx):
    """Says if a user is cool.

    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None and ctx.message.author.id == 787065576995553301:
        await ctx.send(f'No, {ctx.subcommand_passed} is not cool')

@cool.command(name='bot')
async def _bot(ctx):
    """Is the bot cool?"""
    if ctx.message.author.id == 787065576995553301:
        await ctx.send('Yes, the bot is cool.')

# CONSOLE COMMANDS
"""
@my_console.command()
async def hey():
    pass
"""

# STARTS CONSOLE AND BOT
my_console.start()
bot.run('MTI5MTQyODg5NzY5ODc0MjMyMw.GZD3Y5.Z-X9A6puKGPLV3gej1y1YwOtHhCqGRpZFw1wDY')