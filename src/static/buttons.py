import discord
from discord.ui import Button, View
from global_variables import global_variables
from static import embeds
import json

# VARIABLES (MAIN SERVER)
guild_id=1274894955663593492
tickets_cat_id=1291208418282962944

def check_tickets(interaction):
    with open("global_variables/openedTickets.json", "r") as file:
        openedTickets = json.load(file)
    tickets=0
    for i in openedTickets:
        if openedTickets[i]["creator_id"]==interaction.user.id: tickets+=1
    return tickets

def rental_channel(guild_id: int, channel_id: int):
    channel_button = Button(label='Go to rental channel', url=f'https://discord.com/channels/{guild_id}/{channel_id}')
    view=View()
    view.add_item(channel_button)
    return view

def rental_close():
    close_button=Button(style=discord.ButtonStyle.danger, label='Close', custom_id='rental_close_button', emoji='🔒')
    
    async def callback(interaction):
        await interaction.response.send_message("Closing channel, please wait...")
        await interaction.channel.delete(reason=f"User {interaction.user.name} (ID: {interaction.user.id}) clicked the 'Close' button")
        global_variables.delete_key("global_variables/openedRentals.json", interaction.channel_id)

    close_button.callback=callback

    view=View(timeout=None)
    view.add_item(close_button)
    return view

def ticket_close_():
    button=Button(style=discord.ButtonStyle.danger, label='Close', custom_id='ticket_close_button', emoji='🔒')

    async def callback(interaction):
        await interaction.response.send_message("Closing channel, please wait...")
        await interaction.channel.delete(reason=f"User {interaction.user.name} (ID: {interaction.user.id}) clicked the 'Close' button")
        global_variables.delete_key("global_variables/openedTickets.json", interaction.channel_id)

    button.callback=callback

    v=View(timeout=None)
    v.add_item(button)
    return v


def ticket_general():
    button = Button(style=discord.ButtonStyle.secondary, label="General", custom_id="ticket_general_button", emoji='📑')
    async def callback(interaction):
        if check_tickets(interaction)>=1: return await interaction.response.send_message(content="You already have a ticket opened, please close it before opening another one", ephemeral=True)
        # VARIABLES
        category = discord.utils.get(interaction.guild.categories, id=tickets_cat_id)
        employee_role=interaction.guild.get_role(1287519565915619360)
        overwrites = {
        interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        interaction.user: discord.PermissionOverwrite(read_messages=True),
        interaction.guild.get_role(1287519565915619360): discord.PermissionOverwrite(read_messages=False), # EMPLOYEE
        interaction.guild.get_role(1274907158982688820): discord.PermissionOverwrite(read_messages=False), # MEMBER
        interaction.guild.get_role(1287521769422323784): discord.PermissionOverwrite(read_messages=True), # MASTER CONTRACTOR
        interaction.guild.get_role(1274921886886789131): discord.PermissionOverwrite(read_messages=True), # HIGH RANK
        interaction.guild.get_role(1274910503151472641): discord.PermissionOverwrite(read_messages=False), # UNVERIFIED
        }

        # CODE
        channel = await category.create_text_channel(f'gen-{interaction.user.name[:4]}', overwrites=overwrites)
        channel_button = Button(style=discord.ButtonStyle.link, label="Go to ticket", url=f'https://discord.com/channels/{guild_id}/{channel.id}')
        v=View()
        v.add_item(channel_button)
        await interaction.response.send_message(view=v, ephemeral=True)
        await channel.send(content='@here', embed=embeds.general_ticket_channel(interaction.user.name), view=ticket_close_())
        global_variables.update_json_file("global_variables/openedTickets.json", {str(channel.id): {"creator_id": interaction.user.id, "employee_id": None, "type": "gen"}})

    button.callback=callback

    return button

def ticket_management():
    button=Button(style=discord.ButtonStyle.secondary, label="Management", custom_id="ticket_management_button", emoji='⛔')
    async def callback(interaction):
        if check_tickets(interaction)>=1: return await interaction.response.send_message(content="You already have a ticket opened, please close it before opening another one.", ephemeral=True)
        # VARIABLES
        category = discord.utils.get(interaction.guild.categories, id=tickets_cat_id)
        overwrites = {
        interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        interaction.user: discord.PermissionOverwrite(read_messages=True),
        interaction.guild.get_role(1287519565915619360): discord.PermissionOverwrite(read_messages=False), # EMPLOYEE
        interaction.guild.get_role(1274907158982688820): discord.PermissionOverwrite(read_messages=False), # MEMBER
        interaction.guild.get_role(1274921886886789131): discord.PermissionOverwrite(read_messages=True), # HIGH RANK
        interaction.guild.get_role(1274910503151472641): discord.PermissionOverwrite(read_messages=False), # UNVERIFIED
        }

        # CODE
        channel = await category.create_text_channel(f'mana-{interaction.user.name[:4]}', overwrites=overwrites)
        channel_button = Button(style=discord.ButtonStyle.link, label="Go to ticket", url=f'https://discord.com/channels/{guild_id}/{channel.id}')
        v=View()
        v.add_item(channel_button)
        await interaction.response.send_message(view=v, ephemeral=True)
        await channel.send(content='@here', embed=embeds.management_ticket_channel(interaction.user.name), view=ticket_close_())
        global_variables.update_json_file("global_variables/openedTickets.json", {str(channel.id): {"creator_id": interaction.user.id, "employee_id": None, "type": "mana"}})

    button.callback=callback

    return button

