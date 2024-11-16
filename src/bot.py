# IMPORTS
import logging, asyncio, chat_exporter, discord, json, os
from discord.ext.commands import Bot
from dpyConsole import Console
from discord import app_commands
from static import embeds
from global_variables import global_variables
from discord.ui import View
from discord.ext import commands
from dotenv import load_dotenv
from discord.ui import Button, View

# LOGGING
logging.basicConfig(level=logging.INFO, filename="ovr-bot.log", format="%(asctime)s - %(levelname)s - %(message)s")
logging.info("\n\nNEW SESSION --------------------------------------------------------------------------------------------")

# VARIABLES
load_dotenv()
global ordb,crdb,ctdb,madb,scdb,gdb,mdb,hidb
ordb = crdb = ctdb = madb = scdb = gdb = mdb = hidb = False
error_str="---------------An error occured, please check ovr-bot.log---------------"
description = '''Oceanpoint Vacation Rentals bot commands, prefix "!"'''
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = Bot(command_prefix='!', description=description, intents=intents, help_command=None)
my_console = Console(bot)
my_id = 787065576995553301
rentalsPath = "global_variables/openedRentals.json"
ticketsPath = "global_variables/openedTickets.json"

# - ID TEST SERVER VARIABLES
test_guild_id = 1291429430895575080

# - ID MAIN SERVER VARIABLES
main_guild_id = 1274894955663593492
main_employee_role_id=1287519565915619360
main_rentals_cat_id=1291088217113624616
main_tickets_cat_id=1291208418282962944
main_roles = {
    "employee": 1287519565915619360,
    "member": 1274907158982688820,
    "unverified": 1274910503151472641,
    "hr": 1274921886886789131,
    "master_contractor": 1287521769422323784
}

# FUNCTIONS
async def transcript(ctx: discord.Interaction, type: str):
    transcript = await chat_exporter.export(ctx.channel)
    times=1
    for folder_name, subfolders, filenames in os.walk('static/transcripts'):
        for subfolder in subfolders:
            if type=="gen":  
                if f"gen-{ctx.user.name[:4]}" in subfolder:
                    times+=1
            elif type=="mana":
                if f"mana-{ctx.user.name[:4]}" in subfolder:
                    times+=1
            else:
                if f"rental-{ctx.user.name[:4]}" in subfolder:
                    times+=1

    transcript_dir=f"static/transcripts/{ctx.channel.name}-{times}"
    file_dir=f"{transcript_dir}/{ctx.channel.name}-{times}.html"
    os.makedirs(transcript_dir)
    with open(file_dir, "w", encoding="utf-8") as file:
            file.write(transcript)

    transcript=discord.File(file_dir)
    transcript_channel = bot.get_channel(1306608318160044144) # MAIN SERVER TRANSCRIPTS CHANNEL
    transcript_msg = await transcript_channel.send(file=transcript)
    logging.info(f"""Transcript successfully made at "/{file_dir}" ({transcript_msg.attachments[0].url})""")

def check_tickets(interaction):
    with open("global_variables/openedTickets.json", "r") as file:
        openedTickets = json.load(file)
    tickets=0
    for i in openedTickets:
        if openedTickets[i]["creator_id"]==interaction.user.id: tickets+=1
    return tickets

# BUTTONS

def rental_channel(guild_id: int, channel_id: int):
    channel_button = Button(label='Go to rental channel', url=f'https://discord.com/channels/{guild_id}/{channel_id}')
    view=View()
    view.add_item(channel_button)
    return view

def rental_close():
    
    close_button=Button(style=discord.ButtonStyle.danger, label='Close', custom_id='rental_close_button', emoji='🔒')
    
    async def callback(interaction):
        await interaction.response.send_message("Closing channel, please wait...")
        await transcript(interaction, "r")
        await interaction.channel.delete(reason=f"User {interaction.user.name} (ID: {interaction.user.id}) clicked the 'Close' button")
        global_variables.delete_key("global_variables/openedRentals.json", interaction.channel_id)

    close_button.callback=callback

    view=View(timeout=None)
    view.add_item(close_button)
    return view

def ticket_close():
    button=Button(style=discord.ButtonStyle.danger, label='Close', custom_id='ticket_close_button', emoji='🔒')

    async def callback(interaction):
        await interaction.response.send_message("Closing channel, please wait...")
        await transcript(interaction, "gen" if "gen" in interaction.channel.name else "mana")
        await interaction.channel.delete(reason=f"User {interaction.user.name} (ID: {interaction.user.id}) clicked the 'Close' button")
        global_variables.delete_key("global_variables/openedTickets.json", interaction.channel_id)

    button.callback=callback

    v=View(timeout=None)
    v.add_item(button)
    return v


def ticket_general():
    button = Button(style=discord.ButtonStyle.secondary, label="General", custom_id="ticket_general_button", emoji='📑')
    async def callback(interaction):
        global gdb
        if gdb: return await interaction.response.send_message(content="Cooldown, please try again in 10 seconds.", ephemeral=True)
        gdb=True
        if check_tickets(interaction)>=1: return await interaction.response.send_message(content="You already have a ticket opened, please close it before opening another one", ephemeral=True)
        # VARIABLES
        category = discord.utils.get(interaction.guild.categories, id=main_tickets_cat_id)
        overwrites=category.overwrites
        overwrites[interaction.user]=discord.PermissionOverwrite(read_messages=True)
        # CODE
        channel = await category.create_text_channel(f'gen-{interaction.user.name[:4]}', overwrites=overwrites)
        channel_button = Button(style=discord.ButtonStyle.link, label="Go to ticket", url=f'https://discord.com/channels/{interaction.guild_id}/{channel.id}')
        v=View()
        v.add_item(channel_button)
        await interaction.response.send_message(view=v, ephemeral=True)
        await channel.send(content='@here', embed=embeds.general_ticket_channel(interaction.user.name), view=ticket_close())
        global_variables.update_json_file("global_variables/openedTickets.json", {str(channel.id): {"creator_id": interaction.user.id, "employee_id": None, "type": "gen"}})
        await asyncio.sleep(5)
        gdb=False

    button.callback=callback

    return button

def ticket_management():
    button=Button(style=discord.ButtonStyle.secondary, label="Management", custom_id="ticket_management_button", emoji='⛔')
    async def callback(interaction):
        global mdb
        if mdb: await interaction.response.send_message(content="Cooldown, please try again in 10 seconds.", ephemeral=True)
        if check_tickets(interaction)>=1: return await interaction.response.send_message(content="You already have a ticket opened, please close it before opening another one.", ephemeral=True)
        # VARIABLES
        mdb=True
        category = discord.utils.get(interaction.guild.categories, id=main_tickets_cat_id)
        overwrites=category.overwrites
        overwrites[interaction.user]=discord.PermissionOverwrite(read_messages=True)
        # CODE
        channel = await category.create_text_channel(f'mana-{interaction.user.name[:4]}', overwrites=overwrites)
        channel_button = Button(style=discord.ButtonStyle.link, label="Go to ticket", url=f'https://discord.com/channels/{interaction.guild_id}/{channel.id}')
        v=View()
        v.add_item(channel_button)
        await interaction.response.send_message(view=v, ephemeral=True)
        await channel.send(content='@here', embed=embeds.management_ticket_channel(interaction.user.name), view=ticket_close())
        global_variables.update_json_file("global_variables/openedTickets.json", {str(channel.id): {"creator_id": interaction.user.id, "employee_id": None, "type": "mana"}})
        await asyncio.sleep(5)
        mdb=False

    button.callback=callback

    return button

# EVENTS
@bot.event
async def on_ready():
    v=View(timeout=None)
    v.add_item(ticket_general())
    v.add_item(ticket_management())
    bot.add_view(v)
    bot.add_view(ticket_close())
    bot.add_view(rental_close())
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    logging.info("Bot ready.")

@bot.event
async def on_message(msg):
    global hidb
    if msg.author.id == bot.user.id:
        return

    if "hi" in msg.content and any(bot.user.id == mention.id for mention in msg.mentions):
        if hidb:
            return
        hidb = True

        await msg.reply("hi")
        await asyncio.sleep(3)
        hidb = False

    await bot.process_commands(msg)

# - ERROR LOGGER
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        if "purge" in ctx.message.content: return
        await ctx.send("**Command not found, use !help to see the list of available commands.**")
    elif isinstance(error, commands.CommandInvokeError):
        await ctx.send("**An error occurred, please try again in some moments. If this message keeps showing, please open a general ticket in <@1274925768090320987>.**")
        logging.error(error)
        return print(error_str)
    elif isinstance(error, commands.CommandOnCooldown):
        return await ctx.send(f"**Cooldown, please try again in {error.retry_after} seconds.**")
    elif isinstance(error, commands.NotOwner):
        msg = await ctx.message.reply("You do not own this bot.")
        await ctx.message.delete(delay=2)
        await msg.delete(delay=2)
    else:
        await ctx.send("**An unknown error occurred, please try again in some moments. If this message keeps showing, please open a general ticket in <#1274925768090320987>.**")
        logging.error(error)
        return print(error_str, error)

@bot.event
async def on_app_command_error(interaction: discord.Interaction, error):
    if isinstance(error, commands.CommandInvokeError):
        await interaction.response.send_message("**An error occurred, please try again in some moments. If this message keeps showing, please open a general ticket in <#1274925768090320987>.**", ephemeral=True)
        logging.error(error)
        return print(error_str)
    else:
        await interaction.response.send_message("**An unknown error occurred, please try again in some moments. If this message keeps showing, please open a general ticket at <#1274925768090320987>.**", ephemeral=True)
        logging.error(error)
        return print(error_str)

# SERVER COMMANDS
# - SLASH COMMANDS
@bot.tree.command(name='openrental', description='Open a rental channel')
@app_commands.describe(contact_info="Include your Roblox username and your roleplay name (Example: pizzaiolo7, Izzay).", people_in_house="How many people will be living in the house (numbers only).", renting_time="For how many time you will keep the house.", house_type="The house type.", preferred_location="Preffered location of the house (ex. Housing Suburbs) (optional).", pets_in_house="If there will be pets in the house or not.")
@app_commands.choices(preferred_location=[app_commands.Choice(name="Housing Suburbs", value=1), app_commands.Choice(name="Farms", value=2), app_commands.Choice(name="Sheriff's Office", value=3), app_commands.Choice(name="Springfield", value=4), app_commands.Choice(name="High Rock Park", value=5)], house_type=[app_commands.Choice(name="Small house", value=1), app_commands.Choice(name="Medium house", value=2), app_commands.Choice(name="Large house", value=3), app_commands.Choice(name="Single trailer", value=4), app_commands.Choice(name="Double trailer", value=5), app_commands.Choice(name="Log cabin", value=6)], pets_in_house=[app_commands.Choice(name="Yes", value=1), app_commands.Choice(name="No", value=2), app_commands.Choice(name="Not sure", value=3)])
async def openrental(ctx: discord.Interaction, contact_info: str, people_in_house: int, renting_time: str, house_type: app_commands.Choice[int], preferred_location: app_commands.Choice[int], pets_in_house: app_commands.Choice[int]):
    global ordb
    if ordb: return await ctx.response.send_message(f"Cooldown, please try again in 10 seconds", ephemeral=True)
    ordb=True
    with open(rentalsPath, "r") as file:
        openedRentals = json.load(file)
    
    times = 1
    for i in openedRentals:
        if openedRentals[i]["renter_id"] == ctx.user.id:
            times += 1

    if times >= 3:
        return await ctx.response.send_message("You've reached the limit of rentals opened, please close a rental in order to open another one.", ephemeral=True)

    
    guild = await bot.fetch_guild(main_guild_id)
    name = ctx.user.name
    user = ctx.user
    category = await guild.fetch_channel(main_rentals_cat_id)
    overwrites = category.overwrites
    overwrites[user]=discord.PermissionOverwrite(read_messages=True)

    channel = await category.create_text_channel(f'rental-{name[:4]}-{times}', overwrites=overwrites)
    
    await ctx.response.send_message(view=rental_channel(ctx.guild_id, channel.id), ephemeral=True)
    global_variables.update_json_file(rentalsPath, {channel.id: {"renter_id": user.id, "is_active": None, "employee_id": None, "guild_id": ctx.guild_id}},)
    await channel.send(content='@here', embed=embeds.rental_channel(ctx.user, contact_info, people_in_house, renting_time, house_type.name, pets_in_house.name), view=rental_close())
    await asyncio.sleep(5)
    ordb=False

@bot.tree.command(name="markas", description="Mark the rental as active/inactive")
@app_commands.choices(status=[app_commands.Choice(name="Active", value=1), app_commands.Choice(name="Inactive", value=2)])
async def markas(ctx: discord.Interaction, status: app_commands.Choice[int]):
    global madb
    if madb: return await ctx.response.send_message("Cooldown, please try again in 10 seconds.", ephemeral=True)
    madb=True
    with open(rentalsPath, "r") as file:
        data = json.load(file)
        if not ctx.channel.id in data: return await ctx.response.send_message(content="**Error: not a rental/ticket channel.** If you think this is an error, please open a general ticket.", ephemeral=True)
    if status.name == data[f"{ctx.channel_id}"]["is_active"]: return await ctx.response.send_message(content=f"Rental is already marked as {status.name.lower()}.", ephemeral=True)
    global_variables.update_specific_data(rentalsPath, status.name, str(ctx.channel_id), "is_active")
    await ctx.response.send_message(content=f'Marked the rental as {status.name}', ephemeral=True)
    await asyncio.sleep(5)
    madb=False

@bot.tree.command(name="claimrental", description="Claim this rental (meaning you will handle the rental).")
async def claimrental(ctx):
    global crdb
    if crdb: return await ctx.response.send_message("Cooldown, please try again in 10 seconds.", ephemeral=True)
    crdb=True
    with open(rentalsPath, "r") as file:
        data = json.load(file)
        if not ctx.channel_id in data: return await ctx.response.send_message(content="**Error: not a rental channel.** If you think this is an error, please open a general ticket.", ephemeral=True)
    if ctx.user.id == data[f"{ctx.channel_id}"]["employee_id"]: return await ctx.response.send_message(content=f"Rental is already claimed by you.", ephemeral=True)
    global_variables.update_specific_data(rentalsPath, str(ctx.user.id), str(ctx.channel_id), "employee_id")
    await ctx.response.send_message(content=f"{ctx.user.name} is now handling this rental.")
    await asyncio.sleep(5)
    crdb=False

@bot.tree.command(name="claimticket", description="Claim this ticket (meaning you will handle this ticket).")
async def claimticket(ctx):
    global ctdb
    if ctdb: return await ctx.response.send_message("Cooldown, please try again in 10 seconds.", ephemeral=True)
    ctdb=True
    with open(ticketsPath, "r") as file:
        data = json.load(file)
        if not str(ctx.channel_id) in data: return await ctx.response.send_message(content="**Error: not a ticket channel.** If you think this is an error, please open a general ticket.", ephemeral=True)
    if ctx.user.id == data[f"{ctx.channel_id}"]["employee_id"]: return await ctx.response.send_message(content="Rental is already claimed by you.", ephemeral=True)
    global_variables.update_specific_data(ticketsPath, str(ctx.user.id), str(ctx.channel_id), "employee_id")
    await ctx.response.send_message(content=f"{ctx.user.name} is now handling this ticket.")
    await asyncio.sleep(5)
    ctdb=False

@bot.tree.command(name='scheduleclosing', description='Schedule a time for this rental/ticket to close.')
@app_commands.choices(time=[app_commands.Choice(name='1 minute', value=60), app_commands.Choice(name='5 minutes', value=300), app_commands.Choice(name='10 minutes', value=600), app_commands.Choice(name='15 minutes', value=900), app_commands.Choice(name='30 minutes', value=1800)])
async def scheduleclosing(ctx: discord.Interaction, time: app_commands.Choice[int]):
    global scdb
    if scdb: return await ctx.response.send_message("Cooldown, please try again in 10 seconds.", ephemeral=True)
    scdb=True

    with open(ticketsPath, "r") as f:
        ticketsData = json.load(f)
    with open(rentalsPath, "r") as ff:
        rentalsData = json.load(ff)

    if str(ctx.channel_id) not in rentalsData and str(ctx.channel_id) not in ticketsData: return await ctx.response.send_message(content="**Error: not a ticket/rental channel.** If you think this is an error, please open a general ticket.", ephemeral=True)

    await ctx.response.send_message(content=f'Channel closing in {time.name}.')
    logging.info(f'{ctx.channel_id} closing in {time.name}.')
    await asyncio.sleep(time.value)
    await ctx.channel.send(content='Closing channel, please wait...')
    type=""
    if "gen" in ctx.channel.name:
        type="gen"
    elif "mana" in ctx.channel.name:
        type="mana"
    print(f"type: {type}, channel name: {ctx.channel.name}")
    await transcript(ctx=ctx, type=type)
    await ctx.channel.delete()
    fp=ticketsPath if str(ctx.channel_id) in ticketsData else rentalsPath
    global_variables.delete_key(file_path=fp, key_to_remove=ctx.channel_id)
    
    await asyncio.sleep(5)
    scdb=False

# - PREFIX COMMANDS
@bot.group()
@commands.is_owner()
async def cool(ctx):
    """Says if a user is cool."""
    if ctx.invoked_subcommand is None:
        await ctx.send(f'No, {ctx.subcommand_passed} is not cool')

@cool.command(name='bot')
@commands.is_owner()
async def _bot(ctx):
    """Is the bot cool?"""
    await ctx.send('Yes, the bot is cool.')

@cool.command(name='murilo2.0')
@commands.is_owner()
async def _bot(ctx):
    """Is the creator cool?"""
    await ctx.send('Yes, the creator is cool :sunglasses:')

@bot.command()
@commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
@commands.is_owner()
async def sync(ctx):
    bot.tree.copy_global_to(guild=discord.Object(id=test_guild_id))
    bot.tree.copy_global_to(guild=discord.Object(id=main_guild_id))
    await bot.tree.sync(guild=discord.Object(id=test_guild_id))
    await bot.tree.sync(guild=discord.Object(id=main_guild_id))
    await ctx.send(':white_check_mark:')
    print("Successfully synced bot tree")

@bot.command()
@commands.is_owner()
async def ticketembed(ctx):
    embed = discord.Embed(description="<:line_tan:1296460282201374782><:line_tan:1296460282201374782><:line_tan:1296460282201374782><:line_tan:1296460282201374782><:line_tan:1296460282201374782><:line_tan:1296460282201374782><:line_tan:1296460282201374782><:line_tan:1296460282201374782><:line_tan:1296460282201374782><:line_tan:1296460282201374782><:line_tan:1296460282201374782><:line_tan:1296460282201374782><:line_tan:1296460282201374782><:line_tan:1296460282201374782><:line_tan:1296460282201374782><:line_tan:1296460282201374782><:line_tan:1296460282201374782><:line_tan:1296460282201374782><:line_tan:1296460282201374782><:line_tan:1296460282201374782>")
    v=View()
    v.add_item(ticket_general())
    v.add_item(ticket_management())
    await ctx.send(embeds=[embed], view=v)
    await ctx.message.delete()   

@bot.command()
@commands.is_owner()
async def ping(ctx):
    if ctx.message.author.id==my_id:
        await ctx.send(f'Pong! {round(bot.latency * 1000)}ms.')

@bot.command(name='help', description='Oceanpoint Vacation Rentals help command.')
@commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
async def _help(ctx):
    await ctx.send(content="""```Oceanpoint Vacation Rentals bot commands, prefix "!"\n\n​Prefix commands ("!"):\n\thelp\t\t\tShows this message.\n\nSlash commands:\n\t/openrental\n\t\tOpens a rental channel (all fields required).\n\nOther bot functionalities:\n\t#📡┃support\n\t\tUse the buttons below the embed to open a general ticket or a management ticket.\n\nIf you need more help on a command, or found an error, don't exitate to open a general ticket on the #📡┃support channel.```""")

# CONSOLE COMMANDS
@my_console.command()
async def hey(user: discord.User):
    print(f'hey {user.name}')

@my_console.command()
async def ors():
    with open(rentalsPath, "r") as file:
        print(json.load(file))

@my_console.command()
async def ots():
    with open(ticketsPath, "r") as file:
        print(json.load(file))

@my_console.command()
async def clearlog():
    with open("ovr-bot.log", "w") as f:
        f.writelines([])
        print("bot.py: Restart required.")

@my_console.command()
async def ping():
    print(f'Pong! {round(bot.latency * 1000)}ms')

@sync.error
async def sync_erro(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("cooldown blud")
    else:
        print(error_str)
        logging.error(error)

# STARTS BOT
my_console.start()
bot.run(os.getenv("TOKEN"), reconnect=True)