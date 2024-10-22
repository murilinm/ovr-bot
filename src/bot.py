# IMPORTS
from discord.ext.commands import Bot
import discord
from dpyConsole import Console

# VARIABLES
description = '''Oceanpoint Vacation Rentals bot commands, prefix "!"'''
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = Bot(command_prefix='!', description=description, intents=intents)
my_console = Console(discord.Client(intents=intents))
my_id = 787065576995553301
openedRentals = {}
openedTickets = {}

# - ID TEST SERVER VARIABLES
test_guild_id = 1291429430895575080
test_tickets_cat_id = 1292466525998940244
test_rentals_cat = 1291534971043057724
test_support_channel_id = 1291890339342450841
test_employee_role_id = 1291826425430806669

# - ID MAIN SERVER VARIABLES
main_guild_id = 1274894955663593492

# EVENTS
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

# SERVER COMMANDS
@bot.tree.command(name='openrental', description='Open a rental channel')
async def openrental(ctx: discord.Interaction, contact_info: str, people_in_house: int, renting_time: str, house_type: str, pets_in_house: bool):
    times = 0
    for i in range(1, len(openedRentals)):
        if openedRentals[i] == ctx.user.id:
            times += 1

    if times >= 3:
        return await ctx.response.send_message("You've reached the limit of rentals opened, please close a rental in order to open another one.")
    
    name = ctx.user.name
    user = ctx.user
    guild = bot.get_guild(test_guild_id)
    category = guild.get_channel(1291534971043057724)
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        user: discord.PermissionOverwrite(read_messages=True),
        guild.get_role(test_employee_role_id): discord.PermissionOverwrite(read_messages=True)
    }
    
    channel = await category.create_text_channel(f'rental-{name[:4]}', overwrites=overwrites)
    await ctx.response.send_message(f'Click [here](https://discord.com/channels/{guild.id}/{channel.id}) to go to your rental channel', ephemeral=True)
    openedRentals[ctx.channel_id] = user.id

@bot.group()
async def cool(ctx):
    """Says if a user is cool."""
    if ctx.invoked_subcommand is None and ctx.message.author.id == my_id:
        await ctx.send(f'No, {ctx.subcommand_passed} is not cool')

@cool.command(name='bot')
async def _bot(ctx):
    """Is the bot cool?"""
    if ctx.message.author.id == my_id:
        await ctx.send('Yes, the bot is cool.')

@cool.command(name='murilo2.0')
async def _bot(ctx):
    if ctx.message.author.id == my_id:
        await ctx.send('Yes, the creator is cool :sunglasses:')

@bot.command()
async def sync(ctx):
    if ctx.message.author.id == my_id:
        bot.tree.copy_global_to(guild=discord.Object(id=test_guild_id))
        await bot.tree.sync(guild=discord.Object(id=test_guild_id))
        await ctx.send(':white_check_mark:')

@bot.command()
async def print(ctx, arg):
    if ctx.message.author.id == my_id:
        if arg == "openedRentals":
            await ctx.send(openedRentals)

@my_console.command()
async def hey(user: discord.User):
    pass

# STARTS BOT
my_console.start()
bot.run('MTI5MTQyODg5NzY5ODc0MjMyMw.GZD3Y5.Z-X9A6puKGPLV3gej1y1YwOtHhCqGRpZFw1wDY', reconnect=True)