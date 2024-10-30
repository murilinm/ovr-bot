# IMPORTS
from discord.ext.commands import Bot
import discord
from dpyConsole import Console
import json
from discord import app_commands
from static import buttons, embeds
from global_variables import global_variables
from discord.ui import View

# VARIABLES
description = '''Oceanpoint Vacation Rentals bot commands, prefix "!"'''
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = Bot(command_prefix='!', description=description, intents=intents)
my_console = Console(bot)
my_id = 787065576995553301
rentalsPath = "global_variables/openedRentals.json"
ticketsPath = "global_variables/openedTickets.json"
with open(ticketsPath, "r") as file:
    openedTickets = json.load(file)

# - ID TEST SERVER VARIABLES
test_guild_id = 1291429430895575080
test_tickets_cat_id = 1292466525998940244
test_rentals_cat_id = 1291534971043057724
test_support_channel_id = 1291890339342450841
test_employee_role_id = 1291826425430806669

# - ID MAIN SERVER VARIABLES
main_guild_id = 1274894955663593492

# FUNCTIONS
def get_guild(guild_id):
    return bot.fetch_guild(guild_id)

# EVENTS
@bot.event
async def on_ready():
    v=View(timeout=None)
    v.add_item(buttons.ticket_general())
    bot.add_view(buttons.ticket_close_())
    bot.add_view(v)
    bot.add_view(buttons.rental_close())
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

# SERVER COMMANDS
# - SLASH COMMANDS
@bot.tree.command(name='openrental', description='Open a rental channel')
@app_commands.describe(contact_info="Include your Roblox username and your roleplay name (Example: pizzaiolo7, Izzay).", people_in_house="How many people will be living in the house (numbers only).", renting_time="For how many time you will keep the house.", house_type="The house type.", preferred_location="Preffered location of the house (ex. Housing Suburbs) (optional).", pets_in_house="If there will be pets in the house or not.")
@app_commands.choices(preferred_location=[app_commands.Choice(name="Housing Suburbs", value=1), app_commands.Choice(name="Farms", value=2), app_commands.Choice(name="Sheriff's Office", value=3), app_commands.Choice(name="Springfield", value=4), app_commands.Choice(name="High Rock Park", value=5)], house_type=[app_commands.Choice(name="Small house", value=1), app_commands.Choice(name="Medium house", value=2), app_commands.Choice(name="Large house", value=3), app_commands.Choice(name="Single trailer", value=4), app_commands.Choice(name="Double trailer", value=5), app_commands.Choice(name="Log cabin", value=6)], pets_in_house=[app_commands.Choice(name="Yes", value=1), app_commands.Choice(name="No", value=2), app_commands.Choice(name="Not sure", value=3)])
async def openrental(ctx: discord.Interaction, contact_info: str, people_in_house: int, renting_time: str, house_type: app_commands.Choice[int], preferred_location: app_commands.Choice[int], pets_in_house: app_commands.Choice[int]):
    with open(rentalsPath, "r") as file:
        openedRentals = json.load(file)
    
    times = 0
    for i in openedRentals:
        if openedRentals[i]["renter_id"] == ctx.user.id:
            times += 1

    if times >= 3:
        return await ctx.response.send_message("You've reached the limit of rentals opened, please close a rental in order to open another one.", ephemeral=True)

    
    guild = await bot.fetch_guild(test_guild_id)
    name = ctx.user.name
    user = ctx.user
    category = await guild.fetch_channel(test_rentals_cat_id)
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        user: discord.PermissionOverwrite(read_messages=True),
        guild.get_role(test_employee_role_id): discord.PermissionOverwrite(read_messages=True)
    }

    channel = await category.create_text_channel(f'rental-{name[:4]}-{times+1}', overwrites=overwrites)
    
    await ctx.response.send_message(view=buttons.rental_channel(ctx.guild_id, channel.id), ephemeral=True)
    global_variables.update_json_file(rentalsPath, {channel.id: {"renter_id": user.id, "is_active": None, "employee_id": None}})
    await channel.send(content='@here', embed=embeds.rental_channel(ctx.user, contact_info, people_in_house, renting_time, house_type.name, pets_in_house.name), view=buttons.rental_close())

@bot.tree.command(name="markas", description="Mark the rental as active/inactive")
@app_commands.choices(status=[app_commands.Choice(name="Active", value=1), app_commands.Choice(name="Inactive", value=2)])
async def markas(ctx: discord.Interaction, status: app_commands.Choice[int]):
    with open(rentalsPath, "r") as file:
        data = json.load(file)
    if status.name == data[f"{ctx.channel_id}"]["is_active"]: return await ctx.response.send_message(content=f"Rental is already marked as {status.name.lower()}.", ephemeral=True)
    global_variables.update_specific_data(rentalsPath, status.name, str(ctx.channel_id), "is_active")
    await ctx.response.send_message(content=f'Marked the rental as {status.name}', ephemeral=True)

@bot.tree.command(name="claimrental", description="Claim this rental (meaning you will handle the rental).")
async def claimrental(ctx):
    with open(rentalsPath, "r") as file:
        data = json.load(file)
    if ctx.user.id == data[f"{ctx.channel_id}"]["employee_id"]: return await ctx.response.send_message(content=f"Rental is already claimed by {ctx.user.name}.", ephemeral=True)
    global_variables.update_specific_data(rentalsPath, str(ctx.user.id), str(ctx.channel_id), "employee_id")
    await ctx.response.send_message(content=f"{ctx.user.name} is now handling this rental.")

# - PREFIX COMMANDS
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
        print("Successfully synced bot tree")

@bot.command()
async def ticketembed(ctx):
    if ctx.message.author.id == my_id:
        embed = discord.Embed(description="<:line_tan:1296460282201374782><:line_tan:1296460282201374782><:line_tan:1296460282201374782><:line_tan:1296460282201374782><:line_tan:1296460282201374782><:line_tan:1296460282201374782><:line_tan:1296460282201374782><:line_tan:1296460282201374782><:line_tan:1296460282201374782><:line_tan:1296460282201374782>")
        embed.set_footer(text="Oceanpoint Vacation Rentals")
        v=View()
        v.add_item(buttons.ticket_general())
        v.add_item(buttons.ticket_management())
        await ctx.send(embeds=[embed], view=v)
        await ctx.message.delete()

# CONSOLE COMMANDS
@my_console.command()
async def hey(user: discord.User):
    print(f'hey {user.name}')

@my_console.command()
async def prinn(arg):
    if arg == "openedRentals":
        with open(rentalsPath, "r") as file:
            openedRentals = json.load(file)
        print(openedRentals)
    if arg == "openedTickets":
        print(openedTickets)

# STARTS BOT
my_console.start()
bot.run('MTI5MTQyODg5NzY5ODc0MjMyMw.GZD3Y5.Z-X9A6puKGPLV3gej1y1YwOtHhCqGRpZFw1wDY', reconnect=True)